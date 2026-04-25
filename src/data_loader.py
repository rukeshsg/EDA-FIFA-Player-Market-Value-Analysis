import pandas as pd
import os

def load_data(file_path):
    """
    Load dataset from given file path.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at {file_path}")
    
    df = pd.read_csv(file_path)
    
    return df


def preview_data(df):
    """
    Return basic preview of dataset.
    """
    return df.head()


def dataset_info(df):
    """
    Return dataset structure details.
    """
    return {
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "dtypes": df.dtypes
    }