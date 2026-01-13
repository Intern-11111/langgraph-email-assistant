import pandas as pd
from sklearn.model_selection import train_test_split
from src.utils.text_cleaning import clean_text

def load_and_prepare_dataset(path):
    df = pd.read_csv(path)

    df["text"] = df["subject"] + " " + df["body"]
    df["text"] = df["text"].apply(clean_text)

    X = df["text"]
    y = df["label"]

    return train_test_split(X, y, test_size=0.2, random_state=42)
