from dotenv import load_dotenv
import gradio as gr

from deep_reservoir.researcher.openai import (
    OpenAIChatCompletionsResearcher,
    OpenAIChatCompletionsResearcherModel,
)
from deep_reservoir.summariser.openai import OpenAISummariser, OpenAISummariserModel


def research(researcher, summariser, countries, policies):
    researcher = OpenAIChatCompletionsResearcher(
        OpenAIChatCompletionsResearcherModel.GPT_4O_MINI_SEARCH_PREVIEW
    )

    summariser = OpenAISummariser(OpenAISummariserModel.GPT_5_MINI)

    countries = countries.strip().split("\n")[1:]
    policies = policies.strip().split("\n")[1:]

    results = ["policy,country,status,explanation,source"]
    for country in countries:
        for policy in policies:
            research_result = researcher.research(country, policy)
            summary = summariser.summarise(research_result)
            sources = ",".join(summary.sources)
            result = ",".join(
                [policy, country, summary.status, summary.explanation, sources]
            )
            results.append(result)

    return "\n".join(results)


COUNTRIES_PLACEHOLDER = "country\nNew Zealand\nVietnam\nAustralia"
POLICIES_PLACEHOLDER = "policy\nBagels can be eaten for dinner\nChicken salt is allowed on fries\nKangaroos are not to be ridden"


def main():
    load_dotenv()

    demo = gr.Interface(
        fn=research,
        inputs=[
            gr.Dropdown(["gpt-4o-mini-search-preview"], label="Researcher Agent"),
            gr.Dropdown(["gpt-5-mini"], label="Summariser Agent"),
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
    demo.launch()


if __name__ == "__main__":
    main()
