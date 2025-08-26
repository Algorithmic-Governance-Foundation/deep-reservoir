import os
from enum import Enum
from typing import List
from openai import OpenAI
from pydantic import BaseModel, Field
from deep_reservoir.researcher import Researcher
from deep_reservoir.result import Status, Result


class QueryResponse(BaseModel):
    status: Status = Field(description="Status of the policy for the given country")
    explanation: str = Field(
        description="1 sentence explanation of the status with citations"
    )
    sources: List[str] = Field(description="A list of URLs cited in the explanation")


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

        response = client.responses.parse(
            model=self.model.value,
            tools=[{"type": "web_search_preview"}],
            input=[
                {
                    "role": "developer",
                    "content": "Act as a helpful research assistant who can search the web and answer questions clearly and concisely"
                    + "You must only use the URLs and results provided by the search results. Do not invent or modify sources.",
                },
                {"role": "user", "content": prompt},
            ],
            text_format=QueryResponse,
        )

        content = response.output_parsed

        if not content:
            raise ValueError(
                "Failed to parse openai output", response.model_dump_json()
            )

        return Result(
            policy=policy,
            country=country,
            status=content.status,
            explanation=content.explanation,
            sources=content.sources,
            dump=response.model_dump_json(indent=2),
        )
