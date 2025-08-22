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


class OpenAIResearcher(Researcher):
    def __init__(self, model: OpenAIModel):
        self.model = model

    def go(self, country: str, policy: str) -> Result:
        prompt = f"Determine whether {country} {policy}"

        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
        )

        response = client.responses.create(
            model=self.model.value,
            tools=[{"type": "web_search_preview"}],
            # reasoning={"effort": "low"},
            # text={"verbosity": "low"},
            input=[
                {
                    "role": "developer",
                    "content": "Act as a helpful research assistant who can search the web and answer questions clearly and concisely",
                },
                {"role": "user", "content": prompt},
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "research_response",
                    "schema": {
                        "type": "object",
                        "strict": True,
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
                }
            },
        )

        content = response

        if content:
            try:
                status = content.status
                explanation = content.explanation
                sources: List[str] = []

                # Extract sources from annotations in the output
                for output_item in response.output:
                    if output_item.type == "message":
                        for content_item in output_item.content:
                            if content_item.type == "output_text":
                                for annotation in content_item.annotations:
                                    if annotation.type == "url_citation":
                                        url = annotation.url
                                        if url:
                                            sources.append(url)
            except Exception:
                raise ValueError("Unable to parse OpenAI Result", content)
        else:
            raise ValueError("Unable to parse OpenAI Result", content)

        return Result(
            policy=policy,
            country=country,
            status=status,
            explanation=explanation,
            sources=sources,
            dump=response.model_dump_json(indent=2),
        )
