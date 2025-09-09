import os
from dotenv import load_dotenv
import gradio as gr

from deep_reservoir.researcher.openai import (
    OpenAIChatCompletionsResearcher,
    OpenAIChatCompletionsResearchModel,
    OpenAIResponsesResearchModel,
)
from deep_reservoir.researcher.perplexity import SonarResearchModel
from deep_reservoir.summariser.openai import OpenAISummariser, OpenAISummariserModel


def research(researcher, summariser, countries, policies):
    researcher = OpenAIChatCompletionsResearcher(
        OpenAIChatCompletionsResearchModel.GPT_4O_MINI_SEARCH_PREVIEW
    )

    summariser = OpenAISummariser(OpenAISummariserModel.GPT_5_MINI)

    countries = countries.strip().split("\n")[1:]
    policies = policies.strip().split("\n")[1:]

    results = ["policy,country,status,explanation,source"]
    for country in countries:
        for i, policy in enumerate(policies, 1):
            research_result = researcher.research(country, policy)
            summary = summariser.summarise(research_result)
            sources = ",".join(summary.sources)
            result = ",".join(
                [policy, country, summary.status, summary.explanation, sources]
            )
            results.append(result)

            os.makedirs("./results/dumps", exist_ok=True)
            with open(f"./results/dumps/{country}-{i}.txt", "w") as f:
                f.write(summary.dump)

    return "\n".join(results)


COUNTRIES_PLACEHOLDER = "country\nNew Zealand\nVietnam\nAustralia"
POLICIES_PLACEHOLDER = "policy\nBagels can be eaten for dinner\nChicken salt is allowed on fries\nKangaroos are not to be ridden"


def main():
    load_dotenv()

    demo = gr.Interface(
        fn=research,
        inputs=[
            gr.Dropdown(
                [
                    *[model.value for model in OpenAIChatCompletionsResearchModel],
                    *[model.value for model in OpenAIResponsesResearchModel],
                    *[model.value for model in SonarResearchModel],
                ],
                label="Researcher Agent",
            ),
            gr.Dropdown(
                [model.value for model in OpenAISummariserModel],
                label="Summariser Agent",
            ),
            gr.Textbox(
                label="countries.csv",
                lines=5,
                placeholder=COUNTRIES_PLACEHOLDER,
                max_lines=10,
            ),
            gr.TextArea(
                label="policies.csv",
                lines=5,
                placeholder=POLICIES_PLACEHOLDER,
                max_lines=10,
            ),
        ],
        outputs=gr.Textbox(label="output.csv", lines=40),
    )

    password = os.getenv("GRADIO_PASSWORD")

    if not password:
        raise Exception("You forgot to set a gradio password")

    demo.launch(auth=("agf", password))


if __name__ == "__main__":
    main()
