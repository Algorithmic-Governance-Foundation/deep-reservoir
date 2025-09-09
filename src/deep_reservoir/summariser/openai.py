from enum import Enum
import json
import os
from typing import List
from openai import OpenAI
from pydantic import BaseModel, Field
from deep_reservoir.researcher import Researcher
from deep_reservoir.result import Research, Status, Summary
from deep_reservoir.summariser import Summariser


class QueryResponse(BaseModel):
    status: Status = Field(description="Status of the policy for the given country")
    explanation: str = Field(
        description="1 sentence explanation of the status with citations"
    )
    sources: List[str] = Field(description="A list of URLs cited in the explanation")


class OpenAISummariserModel(Enum):
    GPT_5 = "gpt-5"
    GPT_4_1 = "gpt-4.1"
    GPT_4O_MINI = "gpt-4o-mini"


class OpenAISummariser(Summariser):
    def __init__(self, model: OpenAISummariserModel):
        self.model = model

    def summarise(self, research: Research) -> Summary:
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
        )

        # Load research data
        research_data = json.loads(research.data)
        research_content = (
            research_data.get("choices", [{}])[0].get("message", {}).get("content", "")
        )

        prompt = f"Determine whether {research.country} {research.policy}"

        # Structured output based on research results
        response = client.responses.parse(
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
                    "content": f"Original query: {prompt}\n\nResearch results:\n{research_content}\n\n"
                    + f"Full research data (including tool calls, annotations, URLs):\n{research.data}\n\n"
                    + "Based on this research, determine the policy status and provide structured output.",
                },
            ],
            text_format=QueryResponse,
        )

        content = response.output_parsed

        if not content:
            raise ValueError(
                "Failed to parse openai output", response.model_dump_json()
            )

        return Summary(
            status=content.status,
            explanation=content.explanation,
            sources=content.sources,
            dump=response.model_dump_json(indent=2),
        )
