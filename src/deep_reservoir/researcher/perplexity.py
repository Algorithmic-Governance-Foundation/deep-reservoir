import os
from enum import Enum
from openai import OpenAI
from deep_reservoir import Researcher
from deep_reservoir.result import Result, Answer
import json


class SonarModel(Enum):
    PRO = "sonar-pro"
    DEEP_RESEARCH = "sonar-deep-research"


class SonarResearcher(Researcher):
    def __init__(self, model: SonarModel):
        self.model = model

    def go(self, prompt: str) -> Result:
        client = OpenAI(
            api_key=os.getenv("PERPLEXITY_API_KEY"),
            base_url="https://api.perplexity.ai",
        )

        response = client.chat.completions.create(
            model=self.model.value,
            messages=[
                {"role": "user", "content": prompt},
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "query_response",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "answer": {
                                "type": "string",
                                "enum": ["YES", "NO", "PARTIAL", "UNKNOWN"],
                            },
                            "note": {"type": "string"},
                        },
                        "required": ["answer", "note"],
                        "additionalProperties": False,
                    },
                },
            },
        )

        content = response.choices[0].message.content

        if content:
            try:
                parsed_content = json.loads(content)
                answer = Answer(parsed_content.get("answer", "UNKNOWN"))
                note = parsed_content.get("note", "")
            except (json.JSONDecodeError, ValueError):
                raise ValueError("Unable to parse Perplexity Result", content)
        else:
            raise ValueError("Unable to parse Perplexity Result", content)

        return Result(
            answer=answer,
            note=note,
            # Suppressing the below because it's an extra field allowed via Perplexity
            # See: https://docs.perplexity.ai/guides/chat-completions-guide#understanding-the-response-structure
            sources=response.search_results,  # type: ignore
            dump=str(response),
        )
