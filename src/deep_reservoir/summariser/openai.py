from enum import Enum
import os
from typing import List
from openai import OpenAI
from pydantic import BaseModel, Field
from deep_reservoir.result import Research, Status, Summary, remove_utm_source
from deep_reservoir.summariser import Summariser


class QueryResponse(BaseModel):
    status: Status = Field(description="Status of the policy for the given country")
    explanation: str = Field(description="1 sentence explanation of the status")
    sources: List[str] = Field(description="A list of URLs cited in the explanation")


class OpenAISummariserModel(Enum):
    """OpenAI Models to summarise Research results"""

    GPT_4_1 = "gpt-4.1"
    GPT_5 = "gpt-5"
    GPT_5_MINI = "gpt-5-mini"
    GPT_5_NANO = "gpt-5-nano"


class OpenAISummariser(Summariser):
    def __init__(self, model: OpenAISummariserModel):
        self.model = model

    def summarise(self, research: Research) -> Summary:
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
        )

        prompt = f"Determine whether {research.country} {research.policy}"

        # Structured output based on research results
        instructions = """
        You are a policy analysis assistant. Based on the comprehensive research provided below, analyze the information 
        and provide a structured response about the policy status for the specified country.
        
        Rules for determining policy status:
        - YES: The policy is fully implemented in the country with legally binding national legislation. 
          - Explanation must include: 
            - The responsible national authority (e.g., ministry, agency, parliament).
            - The binding document (title, citation, or URL).
            - A short quoted excerpt (1–2 sentences) showing the relevant wording.
        - PARTIAL: The policy is partially implemented in the country with only non-binding commitments or international agreements. 
          - Explanation must include: 
            - The responsible national or international authority.
            - The non-binding document (title, citation, or URL).
            - A short excerpt or wording from the commitment/agreement.
        - NO: The policy is absent in both national legislation and non-binding commitments. 
          - Explanation must specify:
            - Which policy elements are missing.
            - Which relevant binding document(s) lack these provisions.
        - UNKNOWN: The research does not provide enough information to decide. 
          - Explanation must specify:
            - What information is missing or ambiguous.
            - Why this prevents determining the policy status.
        
        Important:
        - You must only use the URLs and results provided in the research.
        - Do not invent or modify sources.
        - Assess the policy status strictly at the national (country) level.
        - Only determine policy status according to the criteria above.
        """
        response = client.responses.parse(
            model=self.model.value,
            input=[
                {"role": "developer", "content": instructions},
                {
                    "role": "user",
                    "content": f"Original query: {prompt}\n\nResearch results:\n{research.data}",
                },
            ],
            text_format=QueryResponse,
        )

        content = response.output_parsed

        if not content:
            raise ValueError(
                "Failed to parse openai output", response.model_dump_json()
            )

        dump = f"{research.prompt}\n\nResearch results:\n{research.data}\n\nSummary response:\n{response.model_dump_json(indent=2)}"

        # Removing ?utm_source=openai from URLs for cleaner output
        cleaned_sources = [remove_utm_source(source) for source in content.sources]

        return Summary(
            status=content.status,
            explanation=content.explanation,
            sources=cleaned_sources,
            dump=dump,
        )
