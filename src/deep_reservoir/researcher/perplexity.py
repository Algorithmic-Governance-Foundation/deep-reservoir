import os
from enum import Enum
from openai import OpenAI
from deep_reservoir.researcher import Researcher
from deep_reservoir.result import Research


class SonarResearchModel(Enum):
    PRO = "sonar-pro"
    REASONING_PRO = "sonar-reasoning-pro"
    DEEP_RESEARCH = "sonar-deep-research"


class SonarResearcher(Researcher):
    def __init__(self, model: SonarResearchModel):
        self.model = model

    def research(self, country: str, policy: str) -> Research:
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
        )

        return Research(
            prompt=prompt,
            policy=policy,
            country=country,
            data=response.model_dump_json(indent=2),
        )
