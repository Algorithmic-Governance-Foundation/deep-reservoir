from typing import List
from openai import OpenAI
from dotenv import load_dotenv
import os
import csv
from enum import Enum

from deep_reservoir.researcher import Researcher


def main() -> None:
    load_dotenv()
    countries = read_countries()
    policies = read_policies()

    researcher = Researcher.PERPLEXITY
    for country in countries:
        for policy in policies:
            prompt = f"Determine whether {country} {policy}"
            research_result = research(researcher, prompt)


def read_countries() -> List[str]:
    countries = []
    with open("inputs/countries.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            countries.append(row["country"])
    return countries


def read_policies() -> List[str]:
    policies = []
    with open("inputs/policies.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            policies.append(row["policy"])
    return policies
