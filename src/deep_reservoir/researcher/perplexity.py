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


class SonarModel(Enum):
    PRO = "sonar-pro"

    # Reasoning models don't produce a valid schema
    # so both reasoning-pro and deep-research need alternative or 2 step approaches
    # REASONING_PRO = "sonar-reasoning-pro"
    # DEEP_RESEARCH = "sonar-deep-research"


class SonarResearcher(Researcher):
    def __init__(self, model: SonarModel):
        self.model = model

    def go(self, country: str, policy: str) -> Result:
        prompt = f"Determine whether {country} {policy}"

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
                    "schema": QueryResponse.model_json_schema(),
                },
            },
        )

        content = response.choices[0].message.content

        if content:
            try:
                parsed_content = QueryResponse.model_validate_json(content)
                status = parsed_content.status
                explanation = parsed_content.explanation
                sources: List[str] | None = response.model_dump()["citations"]
                if not sources:
                    sources = []
            except Exception:
                raise ValueError("Unable to parse Perplexity Result", content)
        else:
            raise ValueError("Unable to parse Perplexity Result", content)

        return Result(
            policy=policy,
            country=country,
            status=status,
            explanation=explanation,
            sources=sources,
            dump=response.model_dump_json(indent=2),
        )
