import os
from dotenv import load_dotenv
import gradio as gr
import pandas as pd

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

    countries = countries.strip().split(",")
    countries = [country.strip() for country in countries]

    policies = policies.strip().split("\n")
    policies = [policy.strip() for policy in policies]

    results = []
    for country in countries:
        for i, policy in enumerate(policies, 1):
            research_result = researcher.research(country, policy)
            summary = summariser.summarise(research_result)
            sources = ",".join(summary.sources)
            results.append(
                {
                    "policy": policy,
                    "country": country,
                    "status": summary.status,
                    "explanation": summary.explanation,
                    "source": sources,
                }
            )

            os.makedirs("./results/dumps", exist_ok=True)
            with open(f"./results/dumps/{country}-{i}.txt", "w") as f:
                f.write(summary.dump)

    df = pd.DataFrame(results)
    return df


def run_research_and_enable_download(researcher, summariser, countries, policies):
    df = research(researcher, summariser, countries, policies)

    # Save to CSV file
    os.makedirs("./results", exist_ok=True)
    csv_path = "./results/research_results.csv"
    df.to_csv(csv_path, index=False, quoting=0)

    return df, gr.DownloadButton("Download CSV", value=csv_path, visible=True)


def main():
    load_dotenv()

    with gr.Blocks() as demo:
        gr.Markdown("# Deep Reservoir Research Interface")

        with gr.Row():
            with gr.Column():
                researcher_dropdown = gr.Dropdown(
                    [
                        *[model.value for model in OpenAIChatCompletionsResearchModel],
                        *[model.value for model in OpenAIResponsesResearchModel],
                        *[model.value for model in SonarResearchModel],
                    ],
                    label="Researcher Agent",
                    value=OpenAISummariserModel.GPT_4_1.value,
                )
                summariser_dropdown = gr.Dropdown(
                    [model.value for model in OpenAISummariserModel],
                    label="Summariser Agent",
                    value=OpenAISummariserModel.GPT_4_1.value,
                )
                countries_input = gr.Textbox(
                    lines=3,
                    label="Countries",
                    info="A list of comma separated values",
                    placeholder="Australia, Canada, UK",
                )
            with gr.Column():
                policies_input = gr.TextArea(
                    lines=10,
                    label="Policies",
                    info="Each policy should be on a new line\nFor best results, policies should start with a **verb** and be clearly defined",
                    placeholder="Enjoys bagels\nConsiders baked beans a breakfast\nHas warm weather",
                )

                run_btn = gr.Button("Run Research")

        with gr.Row():
            with gr.Column():
                output_df = gr.DataFrame(
                    label="Research Results",
                    headers=["policy", "country", "status", "explanation", "source"],
                    column_widths=["10%", "10%", "10%", "20%", "50%"],
                    show_fullscreen_button=True,
                    show_row_numbers=True,
                    show_copy_button=True,
                    show_search="filter",
                    wrap=True,
                )
                download_btn = gr.DownloadButton("Download CSV", visible=False)

        run_btn.click(
            fn=run_research_and_enable_download,
            inputs=[
                researcher_dropdown,
                summariser_dropdown,
                countries_input,
                policies_input,
            ],
            outputs=[output_df, download_btn],
        )

    password = os.environ.get("GRADIO_PASSWORD")

    if not password:
        raise Exception(f"You forgot to set a gradio password\n{os.environ}")

    # demo.launch(auth=("agf", password))
    demo.launch()


if __name__ == "__main__":
    print("Starting gradio-reservoir...")
    main()
