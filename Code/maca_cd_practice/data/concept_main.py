''' HFUT SPY @2025
MACA-CD concept augmentation, adapted for FoundationalASSIST from MACA-CD/SLP/data/concept_main.py.
Run from this directory, one stage at a time:
    python concept_main.py --stage preprocess   # cleaned_data.csv, used_concepts.txt, graph/concept_data.json
    python concept_main.py --stage metadata     # concept descriptions (2 agents + judge debate)
    python concept_main.py --stage init         # root nodes of the concept DAG
    python concept_main.py --stage extend       # breadth-first DAG extension (resumable)
    python concept_main.py --stage embed        # embeddings of the descriptions
    python concept_main.py --stage practice_embed   # practice version: embeddings of the six practice definitions
'''
import os,sys
import json,random
import argparse
import re
from tqdm import tqdm
from utils import print_with_color
import numpy as np
import pandas as pd
from collections import defaultdict
from task_prompt_templates import *
import networkx as nx
import Levenshtein

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(DATA_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from llm_provider import create_assistant, embed_text

MAX_DEBATE_ROUNDS = 50
RAW_DATA_DIR = os.path.abspath(os.path.join(DATA_DIR, "..", "..", "..", "Data"))  # FoundationalASSIST/Data
CONCEPT_DATA_FILE = "./graph/concept_data.json"

############################ Load Information or important tools ####################################
### define the agent information.
with open(os.path.join(PROJECT_ROOT, 'parameter.json'), 'r') as f:
    parameter = json.load(f)

llm_cfg = {
    'provider': parameter.get("Agent_provider", "qwen"),
    'model': parameter["Agent_model"],
    'model_server': parameter.get("model_server", "dashscope"),
    'API_key': parameter.get("API_key", ""),
    'Agent_API_key': parameter.get("Agent_API_key", ""),
    'Agent_API_key_env': parameter.get("Agent_API_key_env", ""),
    'top_p': parameter.get("model_topk", 0.8),
    'temperature': parameter.get("Agent_temperature", 0.5),
    'Embedding_provider': parameter.get("Embedding_provider", parameter.get("Agent_provider", "qwen")),
    'Embedding_API_key': parameter.get("Embedding_API_key", ""),
    'Embedding_API_key_env': parameter.get("Embedding_API_key_env", ""),
    'Embedding_model': parameter.get("Embedding_model", ""),
    'Embedding_model_server': parameter.get("Embedding_model_server", ""),
    'Embedding_dimension': parameter.get("Embedding_dimension", 256),
}


def filter_and_rename(df, column_name, min_count=30):
    counts = df[column_name].value_counts()
    valid_values = counts[counts >= min_count].index
    df_filtered = df[df[column_name].isin(valid_values)].copy()
    value_mapping = {old: new for new, old in enumerate(valid_values)}
    df_filtered[column_name] = df_filtered[column_name].map(value_mapping)
    return df_filtered

def pre_process(min_count=30):
    # Skills: several skill_ids share one node_code and node_name, so a concept is a node_code
    skills = pd.read_csv(os.path.join(RAW_DATA_DIR, "Skills.csv"), dtype=str)
    skills = skills.dropna(subset=["problem_id", "node_code", "node_name"])
    skills["node_name"] = skills["node_name"].str.strip()
    skills = skills.drop_duplicates(["problem_id", "node_code"])
    code2name = skills.drop_duplicates("node_code").set_index("node_code")["node_name"].to_dict()
    lower_names = [name.lower() for name in code2name.values()]
    assert len(set(lower_names)) == len(lower_names), "Two skill codes share a name"
    problem_codes = skills.groupby("problem_id")["node_code"].apply(lambda codes: "|".join(sorted(set(codes))))

    # Interactions: each interaction once, first attempt per student and problem
    interactions = pd.read_csv(os.path.join(RAW_DATA_DIR, "Interactions.csv"),
                               usecols=["id", "problem_id", "user_id", "discrete_score", "end_time"],
                               dtype={"problem_id": str, "user_id": str, "end_time": str})
    print("interactions loaded: " + str(len(interactions)))
    interactions = interactions.drop_duplicates("id").dropna(subset=["discrete_score", "user_id", "problem_id"])
    interactions["score"] = pd.to_numeric(interactions["discrete_score"], errors="coerce").round()
    interactions = interactions[interactions["score"].isin([0, 1])]
    interactions = interactions[interactions["problem_id"].isin(problem_codes.index)]
    interactions = interactions.sort_values(["end_time", "id"], na_position="last", kind="stable")
    interactions = interactions.drop_duplicates(["user_id", "problem_id"], keep="first")

    df = pd.DataFrame({
        "student_id": interactions["user_id"].values,
        "question_id": interactions["problem_id"].values,
        "problem_id": interactions["problem_id"].values,
        "score": interactions["score"].astype(int).values,
        "full_score": 1,
        "concept_codes": interactions["problem_id"].map(problem_codes).values,
        "end_time": interactions["end_time"].values,
    })
    columns_to_process = ['student_id', "question_id"]
    for col in columns_to_process:
        df = filter_and_rename(df, col, min_count=min_count)

    # save data
    df.to_csv('cleaned_data.csv', index=False)

    used_codes = sorted({code for codes in df["concept_codes"] for code in codes.split("|")})
    used_concepts = [code2name[code] for code in used_codes]
    with open('./used_concepts.txt', 'w') as file:
        for item in used_concepts:
            file.write(f"{item}\n")

    print("responses: " + str(len(df)))
    print("student number is: " + str(df["student_id"].nunique()))
    print("exercise number is: " + str(df["question_id"].nunique()))
    print("concept number is: " + str(len(used_concepts)))
    write_concept_data(used_codes, used_concepts)
    return used_concepts


def find_json(text):
    json_match = re.search(r'```json\s*\n(.*?)\n\s*```', text, re.DOTALL)
    if json_match:
        find_str = json_match.group(1)
    elif "{" in text and "}" in text:
        find_str = text[text.index("{"): text.rindex("}") + 1]
    else:
        raise ValueError("No Valid Json")
    find_str = find_str.replace('\\leq', '≤').replace('\\geq', '≥')
    return find_str

def find_definition(description):
    """The concept definition MACA-CD shows in the graph prompts:
    analyses -> definition_and_scope -> definition, or the first "definition" key found."""
    try:
        data = json.loads(find_json(description))
    except (ValueError, json.JSONDecodeError):
        print_with_color("Description is not valid JSON, using its start instead", "red")
        return " ".join(description.split())[:300]
    try:
        return data["analyses"]["definition_and_scope"]["definition"]
    except (KeyError, TypeError):
        pass

    def search(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if "definition" in str(key).lower() and isinstance(value, str):
                    return value
            for value in node.values():
                found = search(value)
                if found:
                    return found
        elif isinstance(node, list):
            for value in node:
                found = search(value)
                if found:
                    return found
        return None

    found = search(data)
    return found if found else " ".join(description.split())[:300]

def find_answer(text):
    json_match = re.search(r'<Answer>(.*?)</Answer>', text, re.DOTALL)
    if not json_match:
        raise ValueError("No Valid Json")
    return json_match.group(1)

def parse_answer_names(answer):
    """Concept names from an <Answer> such as "add","multiply". Names are quoted because some
    FoundationalASSIST skill names contain commas; unquoted answers are split on commas."""
    names = re.findall(r'"([^"]+)"', answer)
    if not names:
        names = answer.split(",")
    names = [name.replace("\n", " ").strip().strip("'").strip() for name in names]
    return [name for name in names if name]

def parse_judge_decision(text):
    decision = text.strip().strip(".!'\"").strip().lower()
    if decision in {"yes", "no"}:
        return decision
    return None

def construct_message_base(agent_responses):
    prefix_string_template = "Here are some outputs by the other agent:{other_response}\nHere are your previous output:{your_response}\nUsing these as additional advice, what is your updated analysis?"
    prefix_string0 = prefix_string_template.format(other_response=agent_responses[1],your_response=agent_responses[0])
    prefix_string1 = prefix_string_template.format(other_response=agent_responses[0],your_response=agent_responses[1])
    return [prefix_string0, prefix_string1]

def text_embeddings(text):
    return embed_text(text, llm_cfg)

def load_meta_data():
    """Concept descriptions; the graph stages need one for every concept."""
    with open("./concept_preknowledge/concept_meta_data.json", "r", encoding="utf-8") as f:
        meta_data = json.load(f)
    _, used_concepts = read_concept_names()
    missing = [concept for concept in used_concepts if concept not in meta_data]
    if missing:
        raise RuntimeError("{} concepts have no description yet; run --stage metadata first: {}".format(len(missing), missing[:5]))
    return meta_data
############################################## End Load #############################################

'''
Stage 1 obtain meta data (concept descriptions) only based on concept names:
'''
def meta_data_obtain(used_concepts, save_metadata=True, save_emb=False, limit=None):
    concept_dir = "./concept_preknowledge"
    if not os.path.exists(concept_dir):
        os.makedirs(concept_dir)
        print("Successfully create concept pre-knowledge dir")
    else:
        print("Dir exists")

    meta_data = dict()
    meta_emb = dict()
    # resume: keep the descriptions of an earlier, interrupted run
    if os.path.exists("./concept_preknowledge/concept_meta_data.json"):
        with open("./concept_preknowledge/concept_meta_data.json", "r", encoding="utf-8") as f:
            meta_data = json.load(f)
        print("Resuming: {} concepts already described".format(len(meta_data)))

    meta_data_agent0 = create_assistant(llm_cfg, sys_prompt)
    meta_data_agent1 = create_assistant(llm_cfg, sys_prompt)
    judge_agent = create_assistant(llm_cfg, sys_prompt)
    todo = [concept for concept in used_concepts if concept not in meta_data]
    if limit is not None:
        todo = todo[:limit]
    for c_idx, concept in enumerate(todo):
        messages0, messages1 = [], []
        print("\n\ncurrent concept number id is {} \n\n".format(str(c_idx)))
        agents_responses = []
        exec_id = 0
        while True:
            if exec_id >= MAX_DEBATE_ROUNDS:
                raise RuntimeError(
                    f"Concept description debate did not converge after {MAX_DEBATE_ROUNDS} rounds: {concept}"
                )
            if exec_id == 0:
                prefix = "Please begin analysis for **{}:**".format(concept)
                query = analyze_agent_template.format(concept=concept, prefix=prefix)
                queries = [query, query]
            else:
                prefix_strings = construct_message_base(agents_responses)
                agents_responses = [] # reset
                # query 1 should use output from agent 0
                query0 = analyze_agent_template.format(concept=concept, prefix=prefix_strings[0])
                query1 = analyze_agent_template.format(concept=concept, prefix=prefix_strings[1])
                queries = [query0, query1]

            messages0.append({'role': 'user', 'content': queries[0]})
            messages1.append({'role': 'user', 'content': queries[1]})
            last_response0,last_response1 = None, None
            print_with_color('\nbot 0 response:',"cyan")
            for response in meta_data_agent0.run(messages=messages0):
                last_response0 = response
            last_response0 = last_response0[0]["content"]
            print_with_color(last_response0,"cyan")
            agents_responses.append(last_response0)

            print_with_color('\nbot 1 response:', "yellow")
            for response in meta_data_agent1.run(messages=messages1):
                last_response1 = response
            last_response1 = last_response1[0]["content"]
            print_with_color(last_response1, "yellow")
            agents_responses.append(last_response1)

            print_with_color('\njudge bot response:', "blue")
            judge_prompts = judge_agent_template.format(R1=last_response0,R2=last_response1)
            messages = [{'role': 'user', 'content': judge_prompts}]
            for response in judge_agent.run(messages=messages):
                last_response = response
            last_response = last_response[0]["content"]
            print_with_color(last_response, "blue")

            if parse_judge_decision(last_response) == "yes":
                break
            exec_id += 1

        meta_data[concept] = last_response1 # result from any one is ok
        if save_metadata:
            with open("./concept_preknowledge/concept_meta_data.json", "w") as f:
                json.dump(meta_data, f, indent=4)
        if save_emb:
            embedding = text_embeddings(last_response1)
            meta_emb[concept] = embedding
            print_with_color("\"{}\" has been encoded!\n".format(concept), "green")
            with open("./concept_preknowledge/concept_meta_emb.json", "w") as f:
                json.dump(meta_emb, f, indent=4)

    missing = [concept for concept in used_concepts if concept not in meta_data]
    print("{} of {} concepts described, {} left".format(len(used_concepts) - len(missing), len(used_concepts), len(missing)))


def meta_data_embed():
    """Embeddings of the saved descriptions (as Eedi's concept_main.py regenerates them)."""
    meta_data = load_meta_data()
    _, used_concepts = read_concept_names()

    meta_emb = dict()
    for concept in tqdm(used_concepts):
        embedding = text_embeddings(meta_data[concept])
        meta_emb[concept] = embedding
    print_with_color("{} concepts encoded, dimension {}".format(len(meta_emb), len(embedding)), "green")
    with open("./concept_preknowledge/concept_meta_emb.json", "w") as f:
        json.dump(meta_emb, f, indent=4)


def practice_texts():
    """The six practice sections (name, definition, descriptors) of the zero-shot labeler
    Code/augment_mathematical_practice.py, in the order of its PRACTICE_NAMES (the order of the
    mathematical_practice scores), without the "(JSON key: ...)" text and "===" lines."""
    code_dir = os.path.abspath(os.path.join(PROJECT_ROOT, ".."))  # Code/
    if code_dir not in sys.path:
        sys.path.append(code_dir)
    import augment_mathematical_practice as labeler  # imports vllm: run in the vLLM environment

    sections = [
        labeler.PROMPT_REPRESENTING,
        labeler.PROMPT_ABSTRACTING,
        labeler.PROMPT_JUSTIFYING,
        labeler.PROMPT_MODELING,
        labeler.PROMPT_COLLABORATIVE,
        labeler.PROMPT_PROCEDURAL,
    ]
    texts = dict()
    for name, section in zip(labeler.PRACTICE_NAMES, sections):
        assert name in section, "practice sections are not in PRACTICE_NAMES order: " + name
        text = re.sub(r'\s*\(JSON key: "[^"]*"\)', "", section)
        text = "\n".join(line for line in text.splitlines() if line.strip() != "===")
        texts[name] = text.strip()
    return texts


def practice_meta_embed():
    """z_p input: an embedding of each practice's definition and descriptors."""
    concept_dir = "./concept_preknowledge"
    os.makedirs(concept_dir, exist_ok=True)
    practice_emb = dict()
    for name, text in practice_texts().items():
        practice_emb[name] = text_embeddings(text)
        print_with_color("\"{}\" has been encoded!".format(name), "green")
    print_with_color("{} practices encoded, dimension {}".format(len(practice_emb), len(practice_emb[name])), "green")
    with open("./concept_preknowledge/practice_meta_emb.json", "w") as f:
        json.dump(practice_emb, f, indent=4)

"""
stage 2 Graph Initialization (Beginning nodes)
"""
def graph_initialization():
    graph_dir = "./graph"
    if not os.path.exists(graph_dir):
        os.makedirs(graph_dir)
        print("Successfully create graph dir")
    else:
        print("Graph dir exists")

    meta_data = load_meta_data()
    # Names are quoted in the answer because some skill names contain commas
    task_prompt_template = """You are a helpful assistant to an educational expert. The following factors are key variables related to knowledge concepts which have various causal effects on each other. Our goal is to construct a causal graph between these variables.
    {concept_and_des}
    Now you are going to use the data to construct a causal graph. You will start with identifying the variable(s) that are unaffected by any other variables.
    {prefix} Think step by step. Then, provide your final answer (variable names only, each in double quotes) within the tags <Answer>...</Answer>. For Example, <Answer>\"add\",\"multiply\"</Answer>."""
    concept_and_des = ""
    for concept, description in meta_data.items():
        important = find_definition(description)
        print_with_color(important + "\n", "yellow")
        concept_and_des += "<"+concept + ">: " + important + ";\n"

    exec_id = 0
    Init_agent0 = create_assistant(llm_cfg, sys_prompt)
    Init_agent1 = create_assistant(llm_cfg, sys_prompt)
    judge_agent = create_assistant(llm_cfg, sys_prompt)
    agents_responses = []
    while True:
        if exec_id >= MAX_DEBATE_ROUNDS:
            raise RuntimeError(
                f"Graph initialization debate did not converge after {MAX_DEBATE_ROUNDS} rounds"
            )
        if exec_id == 0:
            task_prompt = task_prompt_template.format(concept_and_des=concept_and_des,prefix="")
            queries = [task_prompt, task_prompt]
        else:
            prefix_strings = construct_message_base(agents_responses)
            agents_responses = []  # reset
            query0 = task_prompt_template.format(concept_and_des=concept_and_des,
                                                 prefix=prefix_strings[0])
            query1 = task_prompt_template.format(concept_and_des=concept_and_des,
                                                 prefix=prefix_strings[1])
            queries = [query0, query1]

        print_with_color(queries[0], "cyan")
        messages = [{'role': 'user', 'content': queries[0]}]
        print_with_color('\nbot 0 response:', "cyan")
        for response in Init_agent0.run(messages=messages):
            last_response0 = response
        last_response0 = last_response0[0]["content"]
        answer0 = find_answer(last_response0)
        print_with_color(answer0, "cyan")
        agents_responses.append(last_response0)

        print_with_color('\nbot 1 response:', "yellow")
        messages = [{'role': 'user', 'content': queries[1]}]
        for response in Init_agent1.run(messages=messages):
            last_response1 = response
        last_response1 = last_response1[0]["content"]
        answer1 = find_answer(last_response1)
        print_with_color(answer1, "yellow")
        agents_responses.append(last_response1)

        print_with_color('\njudge bot response:', "blue")
        judge_prompts = judge_agent_template.format(R1=answer0, R2=answer1)
        messages = [{'role': 'user', 'content': judge_prompts}]
        for response in judge_agent.run(messages=messages):
            last_response = response
        last_response = last_response[0]["content"]
        print_with_color(last_response, "blue")

        if parse_judge_decision(last_response) == "yes":
            break
        exec_id += 1

    graph_data = {"initial_nodes":answer1}
    with open("./graph/initial_nodes.json", "w") as f:
        json.dump(graph_data, f, indent=4)
    print_with_color("Initial nodes: {}".format(parse_answer_names(answer1)), "green")


"""
stage 3&4 Extension&Insertion
"""

def keep_only_english(text):
    return re.sub(r'[^a-zA-Z]', '', text)

def find_most_similar_key(target_str, search_dict, threshold=90):
    max_similarity = 0
    best_key = None

    for key in search_dict:
        similarity = Levenshtein.ratio(target_str, key) * 100
        if similarity > max_similarity:
            max_similarity = similarity
            best_key = key

    if max_similarity >= threshold:
        print("Successful")
        return search_dict[best_key]
    else:
        print("No find Similarity")
        return None


def search_concept_name(node, concept_dict, concept_e_dict):
    node_id = None
    try:
        node_id = concept_dict[node]
    except:
        print("No node is directly selected! ")
    try:
        node_e = keep_only_english(node)
        node_id = concept_e_dict[node_e]
    except:
        print("No node is selected by only english! ")

    try:
        best_key = find_most_similar_key(node, concept_e_dict, 90)
        node_id = concept_e_dict[best_key]
    except:
        print("No node is selected by Similarity")
    return node_id


def write_concept_data(used_codes, used_concepts):
    """Concept ids 1..N (in node_code order), fixed before any LLM stage. Keeps an existing
    file with the same concepts, so rerunning preprocessing does not change the ids."""
    concept_dict = {}
    concept_e_dict = {}
    concept_set = set()
    code2id = {}
    for idx, (code, concept) in enumerate(zip(used_codes, used_concepts)):
        concept_lower = concept.lower()
        concept_dict[concept_lower] = idx + 1
        concept_e_dict[keep_only_english(concept_lower)] = idx + 1
        concept_set.add(concept_lower)
        code2id[code] = idx + 1

    if os.path.exists(CONCEPT_DATA_FILE):
        with open(CONCEPT_DATA_FILE, "r", encoding="utf-8") as f:
            existing = json.load(f)
        if existing.get("code2id") == code2id:
            print("Concept ids unchanged: " + CONCEPT_DATA_FILE)
            return
        raise RuntimeError(
            "The concepts differ from the existing {}. Delete it, ./concept_preknowledge/ and the other "
            "files in ./graph/ (they use the old ids) and run --stage preprocess again.".format(CONCEPT_DATA_FILE)
        )

    data_to_save = {
        "concept_dict": concept_dict,
        "concept_e_dict": concept_e_dict,
        "concept_set": list(concept_set),
        "code2id": code2id,
        "concept_names": used_concepts,
    }
    os.makedirs(os.path.dirname(CONCEPT_DATA_FILE), exist_ok=True)
    with open(CONCEPT_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, indent=4, ensure_ascii=False)
    print("Concept ids written: " + CONCEPT_DATA_FILE)


def load_or_create_concept_data():
    if not os.path.exists(CONCEPT_DATA_FILE):
        raise FileNotFoundError(CONCEPT_DATA_FILE + " is missing; run --stage preprocess first")
    with open(CONCEPT_DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        concept_dict = data["concept_dict"]
        concept_e_dict = data["concept_e_dict"]
        concept_set = set(data["concept_set"])
        return concept_dict, concept_e_dict, concept_set


def read_concept_names():
    """Concept names in id order (id = position + 1)."""
    with open(CONCEPT_DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["concept_dict"], data["concept_names"]


def graph_extension():
    meta_data = load_meta_data()

    concept_dict, concept_e_dict, concept_set = load_or_create_concept_data()
    id2name = {concept_id: name for name, concept_id in concept_dict.items()}

    def extension(current_visit, Causal_relationships, Remaining):
        concept_and_des = ""
        Remaining_variables = ""
        for concept, description in meta_data.items():
            concept = concept.lower()
            if concept in Remaining:
                important = find_definition(description)
                concept_and_des += "<" + concept + ">: " + important + ";\n"
                Remaining_variables += ("\""+concept+"\""+ ", ")
        Remaining_variables = Remaining_variables[:-2]
        if not Remaining_variables:
            return ""
#         task_prompt_template = """Here are description of remaining concepts: {concept_and_des} \n\n\nGiven ({Independent_concepts}) is(are) not affected by other concepts and the following causal relations: \n{Causal_relationships}\nSelect the concept from ({Remaining_variables}) that are caused by {Current_concept}. \n{prefix}
# Think step by step. Then, provide your final answer (variable names only) within the tags <Answer>...</Answer>."""
        task_prompt_template = """Here are descriptions of the remaining concepts:
{concept_and_des}

Given ({Independent_concepts}) is(are) not affected by other concepts and the following causal relations:
{Causal_relationships}
Select the concepts from ({Remaining_variables}) that are caused by {Current_concept}.
{prefix}
        Think step by step. Then, provide your final answer (variable names only) within the tags <Answer>...</Answer>. For Example, <Answer>\"add\",\"multiply\"</Answer>. Please output:"""
        exec_id = 0
        Exten_agent0 = create_assistant(llm_cfg, sys_prompt)
        Exten_agent1 = create_assistant(llm_cfg, sys_prompt)
        judge_agent = create_assistant(llm_cfg, sys_prompt)
        agents_responses = []
        while True:
            if exec_id >= MAX_DEBATE_ROUNDS:
                raise RuntimeError(
                    f"Graph extension debate did not converge after {MAX_DEBATE_ROUNDS} rounds: {current_visit}"
                )
            if exec_id == 0:
                task_prompt = task_prompt_template.format(concept_and_des=concept_and_des,
                                                          prefix="",
                                                          Current_concept=current_visit,
                                                          Remaining_variables=Remaining_variables,
                                                          Independent_concepts=initial_nodes,
                                                          Causal_relationships=Causal_relationships)
                queries = [task_prompt, task_prompt]
            else:
                prefix_strings = construct_message_base(agents_responses)
                agents_responses = []  # reset
                query0 = task_prompt_template.format(concept_and_des=concept_and_des,
                                                     prefix=prefix_strings[0],
                                                     Current_concept=current_visit,
                                                     Remaining_variables=Remaining_variables,
                                                     Independent_concepts=initial_nodes,
                                                     Causal_relationships=Causal_relationships)
                query1 = task_prompt_template.format(concept_and_des=concept_and_des,
                                                     prefix=prefix_strings[1],
                                                     Current_concept=current_visit,
                                                     Remaining_variables=Remaining_variables,
                                                     Independent_concepts=initial_nodes,
                                                     Causal_relationships=Causal_relationships)
                queries = [query0, query1]

            messages0, messages1 = [], []
            print(queries[0])
            messages0.append({'role': 'user', 'content': queries[0]})
            print_with_color('\nbot 0 response:', "cyan")
            for response in Exten_agent0.run(messages=messages0):
                last_response0 = response
            last_response0 = last_response0[0]["content"]
            answer0 = find_answer(last_response0)
            print_with_color(last_response0, "cyan")
            agents_responses.append(answer0)

            print(queries[1])
            print_with_color('\nbot 1 response:', "yellow")
            messages1.append({'role': 'user', 'content': queries[1]})
            for response in Exten_agent1.run(messages=messages1):
                last_response1 = response
            last_response1 = last_response1[0]["content"]
            answer1 = find_answer(last_response1)
            print_with_color(last_response1, "yellow")
            agents_responses.append(answer1)

            print_with_color('\njudge bot response:', "blue")
            if len(answer0) > 0 and len(answer1) > 0:
                judge_prompts = judge_agent_template.format(R1=answer0, R2=answer1)
                messages = [{'role': 'user', 'content': judge_prompts}]
                for response in judge_agent.run(messages=messages):
                    last_response = response
                last_response = last_response[0]["content"]
                print_with_color(last_response, "blue")
                if parse_judge_decision(last_response) == "yes":
                    break
            elif len(answer0) > 0 and len(answer1) == 0:
                print_with_color("no", "blue")
            elif len(answer0) == 0 and len(answer1) > 0:
                print_with_color("no", "blue")
            elif len(answer0) == 0 and len(answer1) == 0:
                print_with_color("yes", "blue")
                break
            else:
                pass
            exec_id += 1

        return answer1



    STATE_FILE = "./graph/execution_state.json"
    frontier, visited, Causal_relationships, DAG, initial_nodes = initialize_or_resume(STATE_FILE)
    if not visited:  # fresh start: the initial nodes by their concept names, unknown names dropped
        canonical = []
        for name in frontier:
            node_id = search_concept_name(name, concept_dict, concept_e_dict)
            if node_id is None:
                print_with_color("Initial node is not a concept, skipped: " + name, "red")
            elif id2name[node_id] not in canonical:
                canonical.append(id2name[node_id])
        frontier = canonical
    while len(frontier)>0:
        current_visit = frontier[0]
        frontier = frontier[1:]
        visited.append(current_visit)
        remaining_concepts = concept_set - set(frontier) - set(visited)
        concept_names = extension(current_visit, Causal_relationships, remaining_concepts)
        if len(concept_names) > 0:
            print("#######################extension results#######################\n{}".format(concept_names))
            nodes = parse_answer_names(concept_names)  # quoted names: some contain commas
            # insertion
            for node in nodes:
                node = node.lower()
                current_visit_id = search_concept_name(current_visit, concept_dict, concept_e_dict)
                node_id = search_concept_name(node, concept_dict, concept_e_dict)
                if node_id is None:
                    print("No node is selected. Pass this node!")
                    continue  # not a concept: do not visit it
                elif current_visit_id is None:
                    print("No node is selected. Pass this node!")
                else:
                    DAG.add_edge(current_visit_id, node_id)
                    if not nx.is_directed_acyclic_graph(DAG):
                        DAG.remove_edge(current_visit_id, node_id)
                    else:
                        Causal_relationships += ("\"" + current_visit + "\"" + " causes " + "\"" + node + "\"" + "\n")
                        print_with_color("Add causal relations: "+"\"" + current_visit + "\"" + " causes " + "\"" + node + "\"" + "\n")
                node = id2name[node_id]  # the concept's own name, as in concept_set
                if (node not in frontier) and (node not in visited):
                    frontier.append(node)

        DAG_dict = {"DAG": list(DAG.edges())}
        with open("./graph/DAG_edges.json", "w") as f:
            json.dump(DAG_dict, f, indent=4)
        save_state(frontier, visited, Causal_relationships, DAG, STATE_FILE)
        print_with_color("visited {}, frontier {}, edges {}".format(len(visited), len(frontier), DAG.number_of_edges()), "green")

    print_with_color("Graph extension finished: {} edges, {} of {} concepts visited".format(
        DAG.number_of_edges(), len(set(visited) & concept_set), len(concept_set)), "green")

def save_state(frontier, visited, Causal_relationships, DAG, STATE_FILE):
    state = {
        "frontier": frontier,
        "visited": visited,
        "Causal_relationships": Causal_relationships,
        "DAG_edges": list(DAG.edges())
    }
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def load_state(STATE_FILE):
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return None


def initialize_or_resume(STATE_FILE):
    state = load_state(STATE_FILE)
    with open("./graph/initial_nodes.json", "r", encoding="utf-8") as f:
        initial_nodes = json.load(f)["initial_nodes"]

    if state:
        print_with_color("Resuming graph extension from " + STATE_FILE, "green")
        DAG = nx.DiGraph()
        DAG.add_edges_from(state["DAG_edges"])
        return state["frontier"], state["visited"], state["Causal_relationships"], DAG, initial_nodes
    else:
        DAG = nx.DiGraph()
        tmp = parse_answer_names(initial_nodes)
        frontier = [w.lower() for w in tmp]
        visited = []
        Causal_relationships = ""
        return frontier, visited, Causal_relationships, DAG, initial_nodes

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description="MACA-CD concept augmentation for FoundationalASSIST")
    arg_parser.add_argument("--stage", required=True, choices=["preprocess", "metadata", "embed", "init", "extend", "practice_embed"])
    arg_parser.add_argument("--limit", type=int, default=None,
                            help="metadata: describe only this many more concepts (smoke test)")
    args = arg_parser.parse_args()
    os.chdir(DATA_DIR)  # every path is relative to this directory

    if args.stage == "preprocess":
        pre_process(min_count=parameter.get("min_interactions", 30))
    elif args.stage == "metadata":
        _, concepts = read_concept_names()
        meta_data_obtain(concepts, save_metadata=True, save_emb=False, limit=args.limit)
    elif args.stage == "embed":
        meta_data_embed()
    elif args.stage == "init":
        graph_initialization()
    elif args.stage == "extend":
        graph_extension()
    elif args.stage == "practice_embed":
        practice_meta_embed()
