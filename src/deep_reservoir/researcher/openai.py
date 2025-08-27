import json
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
    GPT_4O_MINI = "gpt-4o-mini"


class OpenAIResearcher(Researcher):
    def __init__(self, model: OpenAIModel):
        self.model = model

    def go(self, country: str, policy: str) -> Result:
        prompt = f"Determine whether {country} {policy}"

        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
        )

        # First pass: Web search mode - gather comprehensive information
        first_pass_response = client.chat.completions.create(
            model="gpt-4o-mini-search-preview",
            messages=[
                {
                    "role": "developer",
                    "content": "Act as a helpful research assistant who can search the web thoroughly. "
                    + "Search for comprehensive information about the query. Gather as much relevant data as possible "
                    + "including policy details, implementation status, dates, and sources. Do not provide structured output yet.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        # Second pass: Structured output based on first pass results
        first_pass_content = first_pass_response.choices[0].message.content
        full_first_pass_dump = first_pass_response.model_dump_json(indent=2)

        second_pass_response = client.responses.parse(
            model=self.model.value,
            input=[
                {
                    "role": "developer",
                    "content": "Based on the comprehensive research provided below, analyze the information and provide "
                    + "a structured response about the policy status. You must only use the URLs and results provided "
                    + "in the research. Do not invent or modify sources.",
                },
                {
                    "role": "user",
                    "content": f"Original query: {prompt}\n\nResearch results:\n{first_pass_content}\n\n"
                    + f"Full research data (including tool calls, annotations, URLs):\n{full_first_pass_dump}\n\n"
                    + "Based on this research, determine the policy status and provide structured output.",
                },
            ],
            text_format=QueryResponse,
        )

        content = second_pass_response.output_parsed

        if not content:
            raise ValueError(
                "Failed to parse openai output", second_pass_response.model_dump_json()
            )

        # Combine both passes in the dump for full traceability
        combined_dump = {
            "first_pass": first_pass_response.model_dump(),
            "second_pass": second_pass_response.model_dump(),
        }

        return Result(
            policy=policy,
            country=country,
            status=content.status,
            explanation=content.explanation,
            sources=content.sources,
            dump=json.dumps(combined_dump, indent=2),
        )
