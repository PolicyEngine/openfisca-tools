from argparse import ArgumentParser
from typing import List
from openfisca_tools.data.dataset import Dataset
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)


def openfisca_data_cli(datasets: List[Dataset]):
    datasets = {ds.name: ds for ds in datasets}
    parser = ArgumentParser(description="A utility for storing microdata.")
    parser.add_argument("dataset", help="The dataset to select.")
    parser.add_argument("action", help="The action to take.")
    parser.add_argument(
        "args", nargs="*", help="The arguments to pass to the function."
    )
    args = parser.parse_args()
    if args.dataset == "datasets":
        if args.action == "list":
            print(dataset_summary(datasets.values()))
    else:
        try:
            target = getattr(datasets[args.dataset], args.action)
            if callable(target):
                result = target(*args.args)
            else:
                result = target
            if result is not None:
                print(result)
        except Exception as e:
            print("\n\nEncountered an error:")
            raise e


def dataset_summary(datasets: List[Dataset]) -> str:
    years = list(sorted(list(set(sum([ds.years for ds in datasets], [])))))
    df = pd.DataFrame(
        {
            year: ["✓" if year in ds.years else "" for ds in datasets]
            for year in years
        },
        index=[ds.name for ds in datasets],
    )
    df = df.sort_values(by=list(df.columns[::-1]), ascending=False)
    return df.to_markdown(tablefmt="pretty")
