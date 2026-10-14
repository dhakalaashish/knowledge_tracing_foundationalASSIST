sys_prompt ="You are a helpful assistant."

Taxonomy_Agent_template = """**Role**: Expert Taxonomy Agent specializing in semantic clustering of knowledge concepts in the education domain.

**Objective**:
Organize the input concept set into coherent semantic clusters through hierarchical taxonomy construction.          Each cluster should satisfy:
1.          Intra-cluster concepts share core semantic features
2.          Inter-cluster concepts maintain clear logical boundaries

**Input Format**:
[Concepts]: [concept_1, concept_2, ...         , concept_N]

**Processing Steps**:
1.          Semantic Feature Extraction:
- Analyze concept names and implicit relations
- Identify core semantic dimensions (e.g. functional, structural, procedural)
2.          Cluster Generation:
- Apply spectral clustering with cosine similarity threshold ≥0.7
- Merge overlapping clusters using Jaccard index (threshold=0.4)
3.          Ambiguity Handling:
- Flag polysemous concepts with cross-cluster membership
- Generate disambiguation notes for critical cases

**Output Specification**:
```json
{{
"taxonomy": [
{{
"cluster_id": "C1",
"reasons_for_clustering": "<reasons for this clustering>",
"core_concepts": ["concept_a", "concept_b", ...],
}},
{{
"cluster_id": "C2",
"reasons_for_clustering": "<reasons for this clustering>",
"core_concepts": ["concept_a", "concept_b", ...],
}}
],
}}
**Special Instructions**:
- Prioritize pedagogical relationships over pure lexical similarity
- Handle domain-specific abbreviations through context-aware expansion.

Current input is {all_concepts}, Please output: """

Recruitment_Agent_template = '''# Domain concept expert recruitment requirements
## Qualification requirements
** Required: **
- Deep understanding of all knowledge concepts
- Ability to professionally analyze knowledge concepts based on clustering logic:
- Ability to establish multi-level relationships between concepts (including but not limited to) :
- dependency
- similarity
Now that the knowledge concepts are {all_concepts} and the clustering logic is {logics}, 
output a description of an expert being recruited in the second person. Please output the description directly, do not output irrelevant content.
'''

Reflection_Agent_Template = """## Relation Reflection Agent

### Role Specification
You are a quality control specialist that audits the output of Relation Reasoning Agent.   Your tasks:
1.   Validate the correctness of proposed relations
2.   Identify missing relations between concepts

### Input Data
```json
{{
"input_concepts": {{all concepts}},  
"reasoning_output": {{relations among all concepts}}
}}
```

### Reflection Protocol
| Type               | Condition                          | Recommended Actions |
|--------------------|------------------------------------|---------------------|
| Missing_relations  | Exists unanalyzed concept pairs | Provide potential relations between current concept pair |
| Misclassified_relations      | 1.Wrong relation(e.g.dependency→similarity) 2.Direction error(Only for "dependency" relations) 3.Unnecessary relation (spurious correlation)| Change labels for current concept pair. |

### OUTPUT SPECIFICATION
```json
{{
    "Missing_relations": [
        {{
            "concept_pair": ["concept A", "concept B"],
            "expected_relation_types": ["dependency", "similarity"],
            "confidence_score": 1-5,
        }}
    ],
    "Misclassified_relations": [
        {{
            "original_pair": ["concept A", "concept B"],
            "original_relation_type": "dependency",
            "original_relation_direction": ["concept A" $\\rightarrow$ "concept B"],
            "problem_type": "Wrong relation",
            "suggested_relation_type": "similarity",
            "suggested_relation_direction": ["concept A" $\\leftrightarrow$ "concept B"],
            "reason": "explain why these two concepts are more likely to similarity"
        }},
        {{
            "original_pair": ["concept A", "concept B"],
            "original_relation_type": "dependency",
            "original_relation_direction": ["concept A" $\\rightarrow$ "concept B"],
            "problem_type": "Direction error",
            "suggested_type": "dependency",
            "suggested_relation_direction": ["concept B" $\\rightarrow$ "concept A"],
            "reason": "explain why the dependency direction is wrong."
        }},
        {{
            "original_pair": ["concept A"  "concept B"],
            "original_relation_type": "dependency",
            "original_relation_direction": ["concept A" $\\rightarrow$ "concept B"],
            "type": "Unnecessary relation"
            "suggested_type": "None",
            "suggested_relation_direction": ["concept B" $\\nleftrightarrow$ "concept A"],
            "reason": "explain why the relations between concept A and concept B should be deleted."
        }},
    ]
}}
```

Please do not provide irrelevant content. 
Current input is
```json
{{
"input_concepts": {concepts},  
"reasoning_output": {relations}
}}
```
Please output: 
"""


analyze_agent_template = """### Task Specification
Your task is to analyze the following concept thoroughly and provide structured information based on the guidelines below. Ensure accuracy, completeness, and consistency in your response.

### Input Data
```json
{{
"input_concept": {concept}
}}
```

### Analysis Protocol
Please analyze the concept from the following dimensions:

1. **Definition & Scope**
- Provide a clear, concise, and brief definition from an academic/industry-standard source.
- Clarify boundaries (e.g., how it differs from related concepts).

2. **Key Characteristics**
- List 2 attributes or dimensions.
- Briefly explain each (1 sentence, less than 25 words per attribute).

3. **Applications & Use Cases**
- Describe 1-2 real-world applications or domains where the concept is relevant.
- Include specific examples.

### OUTPUT SPECIFICATION
{{
"concept": the name of analyzed concept,
"analyses": the detailed analyses of the concept
}}

{prefix}
"""

judge_agent_template = """Compare the following two AI agent responses and strictly determine if they convey the same core conclusion (ignore phrasing differences, focus on semantic meaning). Output only 'yes' or 'no':

Agent A's response: {R1}
Agent B's response: {R2}

Return just the single word 'yes' or 'no' with no additional text.
"""