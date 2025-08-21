from typing import List
from dotenv import load_dotenv
import csv
import time
import json

from deep_reservoir.researcher import Researcher
from deep_reservoir.researcher.perplexity import SonarModel, SonarResearcher
from deep_reservoir.result import Result


def main() -> None:
    load_dotenv()
    countries = read_countries()
    policies = read_policies()

    researcher = SonarResearcher(SonarModel.PRO)
    for i, country in enumerate(countries):
        for j, policy in enumerate(policies):
            prompt = f"Determine whether {country} {policy}"
            print(prompt)
            research_result = researcher.go(prompt)
            print(research_result)

            unique_timestamp = int(time.time())
            with open(f"./results/dumps/{country}-{j}-{unique_timestamp}", "w") as f:
                f.write(f"{researcher.model}\n{research_result.dump}")

            return


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

def write_results(results: List[Result]) -> None:
    pass
