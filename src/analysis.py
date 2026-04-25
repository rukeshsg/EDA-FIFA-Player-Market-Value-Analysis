def statistical_summary(df):
    """
    Return descriptive statistics.
    """
    return df.describe()


def correlation_matrix(df):
    """
    Return correlation matrix for numerical features.
    """
    return df.corr(numeric_only=True)