from typing import List
from dotenv import load_dotenv
from itertools import product
import csv
import time
import os

from deep_reservoir.researcher.openai import (
    OpenAIChatCompletionsResearchModel,
    OpenAIChatCompletionsResearcher,
)
from deep_reservoir.summariser.openai import OpenAISummariserModel, OpenAISummariser
from deep_reservoir.result import Summary


def main() -> None:
    load_dotenv()
    countries = read_countries()
    policies = read_policies()

    # researcher = SonarResearcher(SonarResearchModel.PRO)
    researcher = OpenAIChatCompletionsResearcher(
        OpenAIChatCompletionsResearchModel.GPT_4O_MINI_SEARCH_PREVIEW
    )
    summariser = OpenAISummariser(OpenAISummariserModel.GPT_5_MINI)

    total_calls = len(countries) * len(policies)
    print(f"Starting research for {total_calls} combinations")
    print(f"Countries: {len(countries)}")
    print(f"Policies: {len(policies)}")
    print()
    start_time = time.time()

    results = []
    for i, (country, policy) in enumerate(product(countries, policies), 1):
        print(f"Researching ({i}/{total_calls}):\n{country}: {policy}\n")
        research_result = researcher.research(country, policy)
        summary = summariser.summarise(research_result)
        results.append((country, policy, summary))
        dump_result(i, country, policy, researcher.model.value, summary)

    # End timing and calculate results
    end_time = time.time()
    total_duration = end_time - start_time
    avg_time_per_call = total_duration / total_calls

    print("\n=== Research Timing Results ===")
    print(f"Total research calls: {total_calls}")
    print(
        f"Total time: {total_duration:.2f} seconds ({total_duration / 60:.2f} minutes)"
    )
    print(f"Average time per call: {avg_time_per_call:.2f} seconds")
    print("=== End Timing Results ===\n")

    write_results(results)


def dump_result(
    index: int, country: str, policy: str, model: str, result: Summary
) -> None:
    os.makedirs("results/dumps", exist_ok=True)
    unique_timestamp = int(time.time())
    with open(f"results/dumps/{country}-{index}-{unique_timestamp}.txt", "w") as f:
        f.write(f"{model}\n{policy}\n{result.dump}")


def read_countries() -> List[str]:
    countries = []
    with open("inputs/countries.csv", "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        for row in reader:
            countries.append(row["country"])
    return countries


def read_policies() -> List[str]:
    policies = []
    with open("inputs/policies.csv", "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        for row in reader:
            policies.append(row["policy"])
    return policies


def write_results(results: List[tuple]) -> None:
    with open("results/output.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["policy", "country", "status", "explanation", "source"])

        for country, policy, summary in results:
            sources = ",".join(summary.sources)
            writer.writerow(
                [
                    policy,
                    country,
                    summary.status.value,
                    summary.explanation,
                    sources,
                ]
            )
