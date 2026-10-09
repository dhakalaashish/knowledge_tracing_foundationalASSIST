"""
Quote verification for debate transcripts.

Copied from llm_debate's web/backend/services/parser.py (TranscriptParser.normalize_text and
verify_strict) without its database and web imports. A quote counts as verified when its
normalized text appears in the transcript's story; here the story is the practice framework
plus the item.
"""

import copy
import re
import string

from core.rollouts.utils import TranscriptConfig


class TranscriptParser:
    @classmethod
    def normalize_text(cls, text):
        text = text.replace("”", '"').replace("“", '"')
        text = text.replace("’", "'").replace("‘", "'")
        text = text.translate(str.maketrans("", "", string.punctuation)).lower()
        text = " ".join(text.split())
        return text

    @classmethod
    def verify_strict(cls, transcript: TranscriptConfig) -> (TranscriptConfig, dict):
        transcript = copy.deepcopy(transcript)
        story_normalised = cls.normalize_text(transcript.story)

        def is_quote_present(quote):
            quote_normalised = cls.normalize_text(quote)
            return quote_normalised in story_normalised

        def verify_quotes(s):
            for quote_tag in ["<v_quote>", "<u_quote>"]:
                s = s.replace(quote_tag, "<quote>")
            for quote_tag in ["</v_quote>", "</u_quote>"]:
                s = s.replace(quote_tag, "</quote>")
            verified_quotes = []
            unverified_quotes = []

            def change_tag(match):
                quote = match.group(1)
                if is_quote_present(quote):
                    verified_quotes.append(quote)
                    return f"<v_quote>{quote}</v_quote>"
                else:
                    unverified_quotes.append(quote)
                    return f"<u_quote>{quote}</u_quote>"

            modified_s = re.sub(r"<quote>(.*?)</quote>", change_tag, s)
            return modified_s, verified_quotes, unverified_quotes

        transcript_new = transcript.dict()
        quotes_info = {
            "correct": {"unverified_quotes": [], "verified_quotes": []},
            "incorrect": {"unverified_quotes": [], "verified_quotes": []},
        }
        for round in transcript_new["rounds"]:
            for key in ["correct", "incorrect"]:
                if round[key] is not None:
                    round[key], verified_quotes, unverified_quotes = verify_quotes(
                        round[key]
                    )
                    quotes_info[key]["verified_quotes"].extend(verified_quotes)
                    quotes_info[key]["unverified_quotes"].extend(unverified_quotes)

        for response in transcript_new["responses"]:
            for key in ["correct", "incorrect"]:
                if response[key] is not None:
                    response[key], _, _ = verify_quotes(response[key])

        return TranscriptConfig(**transcript_new), quotes_info
