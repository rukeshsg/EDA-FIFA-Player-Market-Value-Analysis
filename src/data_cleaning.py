def remove_duplicates(df):
    """
    Remove duplicate rows from dataset.
    """
    return df.drop_duplicates()


def handle_missing_values(df):
    """
    Fill missing values based on data type.
    """
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col].fillna('Unknown', inplace=True)
        else:
            df[col].fillna(df[col].median(), inplace=True)
    
    return df