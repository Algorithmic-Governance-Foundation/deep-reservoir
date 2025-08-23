import os
from enum import Enum
from typing import List
from openai import OpenAI
from pydantic import BaseModel, Field
from deep_reservoir.researcher import Researcher
from deep_reservoir.result import Status, Result


class QueryResponse(BaseModel):
    status: Status = Field(description="Status of the policy for the given country")
    explanation: str = Field(description="1 sentence explanation of the status")


class OpenAIModel(Enum):
    GPT_5 = "gpt-5"
    GPT_4_1 = "gpt-4.1"
    GPT_4O_SEARCH_PREVIEW = "gpt-4o-search-preview"


class OpenAIResearcher(Researcher):
    def __init__(self, model: OpenAIModel):
        self.model = model

    def go(self, country: str, policy: str) -> Result:
        prompt = f"Determine whether {country} {policy}"

        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
        )

        response = client.chat.completions.create(
            model=self.model.value,
            messages=[
                {
                    "role": "developer",
                    "content": "Act as a helpful research assistant who can search the web and answer questions clearly and concisely",
                },
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
                            "status": {
                                "type": "string",
                                "description": "Status of the policy for the given country",
                                "enum": ["YES", "NO", "PARTIAL", "UNKNOWN"],
                            },
                            "explanation": {
                                "type": "string",
                                "description": "1 sentence explanation of the status",
                            },
                        },
                        "required": ["status", "explanation"],
                        "additionalProperties": False,
                    },
                },
            },
        )

        with open("cat3.json", "w") as f:
            f.write(response.model_dump_json(indent=2))

        return Result(
            policy=policy,
            country=country,
            status=Status.UNKNOWN,
            explanation="",
            sources=[],
            dump=response.model_dump_json(indent=2),
        )
