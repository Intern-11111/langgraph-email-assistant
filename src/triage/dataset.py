import pandas as pd


def load_dataset(path):
    """
    Load email dataset from CSV.
    Expected columns: subject, body, label
    """
    return pd.read_csv(path)
