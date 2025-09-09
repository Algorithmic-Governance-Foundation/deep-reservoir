import os
from enum import Enum
from typing import List
from openai import OpenAI
from pydantic import BaseModel, Field
from deep_reservoir.researcher import Researcher
from deep_reservoir.result import Status, Research


class OpenAIChatCompletionsResearcherModel(Enum):
    """Available OpenAI models for research tasks using "legacy" Chat Completions API."""

    GPT_4O_SEARCH_PREVIEW = "gpt-4o-search-preview"
    GPT_4O_MINI_SEARCH_PREVIEW = "gpt-4o-mini-search-preview"


class OpenAIChatCompletionsResearcher(Researcher):
    """Researcher implementation using OpenAI's Chat Completions API with web search capabilities."""

    def __init__(self, model: OpenAIChatCompletionsResearcherModel):
        self.model = model

    def research(self, country: str, policy: str) -> Research:
        prompt = f"Determine whether {country} {policy}"

        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
        )

        # Web search mode - gather comprehensive information
        response = client.chat.completions.create(
            model="gpt-4o-mini-search-preview",
            messages=[
                {
                    "role": "developer",
                    "content": "Act as a helpful research assistant who can search the web thoroughly. "
                    + "Search for comprehensive information about the query. Gather as much relevant data as possible "
                    + "including policy details, implementation status, dates, and sources. Provide a detailed summary of findings.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        return Research(
            policy=policy,
            country=country,
            data=response.model_dump_json(indent=2),
        )


class OpenAIResponsesResearcherModel(Enum):
    """Available OpenAI models for research tasks using Response API."""

    GPT_4_1 = "gpt-4.1"
    GPT_5 = "gpt-5"
    GPT_5_MINI = "gpt-5-mini"
    GPT_5_NANO = "gpt-5-nano"
    O3_DEEP_RESEARCH = "o3-deep-research"
    O4_MINI_DEEP_RESEARCH = "o4-mini-deep-research"


class OpenAIResponsesResearcher(Researcher):
    """Researcher implementation using OpenAI's Chat Completions API with web search capabilities."""

    def __init__(self, model: OpenAIResponsesResearcherModel):
        self.model = model

    def research(self, country: str, policy: str) -> Research:
        prompt = f"Determine whether {country} {policy}"

        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
        )

        # Web search mode - gather comprehensive information
        response = client.chat.completions.create(
            model="gpt-4o-mini-search-preview",
            messages=[
                {
                    "role": "developer",
                    "content": "Act as a helpful research assistant who can search the web thoroughly. "
                    + "Search for comprehensive information about the query. Gather as much relevant data as possible "
                    + "including policy details, implementation status, dates, and sources. Provide a detailed summary of findings.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        return Research(
            policy=policy,
            country=country,
            data=response.model_dump_json(indent=2),
        )
