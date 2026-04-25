import matplotlib.pyplot as plt
import seaborn as sns


def plot_distribution(df, column, save_path):
    plt.figure(figsize=(8,5))
    sns.histplot(df[column], bins=30, kde=True)
    plt.title(f'{column} Distribution')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def plot_scatter(df, x_col, y_col, save_path):
    plt.figure(figsize=(8,5))
    sns.scatterplot(x=df[x_col], y=df[y_col])
    plt.title(f'{x_col} vs {y_col}')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def plot_heatmap(corr, save_path):
    plt.figure(figsize=(10,8))
    sns.heatmap(corr, cmap='coolwarm')
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def plot_box(df, column, save_path):
    plt.figure(figsize=(8,5))
    sns.boxplot(x=df[column])
    plt.title(f'{column} Outliers')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()