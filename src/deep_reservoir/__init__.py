# from typing import List
# from dotenv import load_dotenv
# from itertools import product
# import csv
# import time
# import os

# from deep_reservoir.researcher.openai import OpenAIModel, OpenAIResearcher
# from deep_reservoir.researcher.perplexity import SonarModel, SonarResearcher
# from deep_reservoir.result import Result


# def main() -> None:
#     load_dotenv()
#     countries = read_countries()
#     policies = read_policies()

#     # researcher = SonarResearcher(SonarModel.PRO)
#     researcher = OpenAIResearcher(OpenAIModel.GPT_4O_MINI)

#     total_calls = len(countries) * len(policies)
#     print(f"Starting research for {total_calls} combinations")
#     print(f"Countries: {len(countries)}")
#     print(f"Policies: {len(policies)}")
#     print()
#     start_time = time.time()

#     results = []
#     for i, (country, policy) in enumerate(product(countries, policies), 1):
#         print(f"Researching ({i}/{total_calls}):\n{country}: {policy}\n")
#         research_result = researcher.go(country, policy)
#         results.append(research_result)
#         dump_result(i, country, policy, researcher.model.value, research_result)

#     # End timing and calculate results
#     end_time = time.time()
#     total_duration = end_time - start_time
#     avg_time_per_call = total_duration / total_calls

#     print("\n=== Research Timing Results ===")
#     print(f"Total research calls: {total_calls}")
#     print(
#         f"Total time: {total_duration:.2f} seconds ({total_duration / 60:.2f} minutes)"
#     )
#     print(f"Average time per call: {avg_time_per_call:.2f} seconds")
#     print("=== End Timing Results ===\n")

#     write_results(results)


# def dump_result(
#     index: int, country: str, policy: str, model: str, result: Result
# ) -> None:
#     os.makedirs("./results/dumps", exist_ok=True)
#     unique_timestamp = int(time.time())
#     with open(f"./results/dumps/{country}-{index}-{unique_timestamp}", "w") as f:
#         f.write(f"{model}\n{policy}\n{result.dump}")


# def read_countries() -> List[str]:
#     countries = []
#     with open("inputs/countries.csv", "r", encoding="utf-8-sig") as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             countries.append(row["country"])
#     return countries


# def read_policies() -> List[str]:
#     policies = []
#     with open("inputs/policies.csv", "r", encoding="utf-8-sig") as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             policies.append(row["policy"])
#     return policies


# def write_results(results: List[Result]) -> None:
#     with open("results/output.csv", "w", newline="", encoding="utf-8") as file:
#         writer = csv.writer(file)
#         writer.writerow(["policy", "country", "status", "explanation", "source"])

#         for result in results:
#             sources = ",".join(result.sources)
#             writer.writerow(
#                 [
#                     result.policy,
#                     result.country,
#                     result.status.value,
#                     result.explanation,
#                     sources,
#                 ]
#             )

