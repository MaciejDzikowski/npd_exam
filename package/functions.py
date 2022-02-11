import matplotlib.pyplot as plt
import pandas as pd


def get_income_mean(df: pd.DataFrame, income_row_name: str) -> float:
    return df[income_row_name].mean()


def get_income_median(df: pd.DataFrame, income_row_name: str) -> float:
    return df[income_row_name].median()


def get_income_std(df: pd.DataFrame, income_row_name: str) -> float:
    return df[income_row_name].std()


def get_income_min(df: pd.DataFrame, income_row_name: str) -> tuple[float, str]:
    return df[income_row_name].min(), df[income_row_name].idxmin()


def get_income_max(df: pd.DataFrame, income_row_name: str) -> tuple[float, str]:
    return df[income_row_name].max(), df[income_row_name].idxmax()


def print_income_stats(df: pd.DataFrame, income_row_name: str):
    print(f'Mean: {get_income_mean(df, income_row_name)}')
    print(f'Median: {get_income_median(df, income_row_name)}')
    print(f'Standard deviation: {get_income_std(df, income_row_name)}')
    print(f'Min: {get_income_min(df, income_row_name)}')
    print(f'MAx: {get_income_max(df, income_row_name)}')


def make_plots(df1: pd.DataFrame, df2: pd.DataFrame, income_row_name: str, year1: str, year2: str):
    """
    Allows to create bar plot of comparing values for two columns from different dataframes
    by a column without duplicates.
    """
    new_df = df1.copy(deep=True)
    new_df[year2] = df2[income_row_name]
    new_df.rename(columns={income_row_name: year1}, inplace=True)
    fig, ax = plt.subplots(1, 1)
    new_df.plot(kind='bar', ax=ax)
    ax.legend()
    plt.title(income_row_name)
    plt.show()


def get_average_income_per_worker(df: pd.DataFrame, income_name: str, people_name: str, working: float) -> pd.DataFrame:
    df['Average income'] = df[income_name] / (working * df[people_name])
    return df


def get_variance(superior: pd.DataFrame, inferior: pd.DataFrame, group_by: str, income_name: str) -> pd.DataFrame:
    superior['Variance'] = list(inferior.groupby(group_by).var()[income_name])
    return superior


def get_weighted_average(superior: pd.DataFrame, inferior: pd.DataFrame, group_by: str,
                         income_name: str, people_name: str, working: float) -> pd.DataFrame:
    inferior[people_name] = inferior[people_name] * working
    inferior['Weighted average'] = inferior[income_name] * inferior[people_name]
    grouped = inferior.groupby(group_by).sum()
    grouped2 = inferior.groupby(group_by).apply(lambda x: x[people_name].sum() * len(x))
    grouped['Weighted average'] = grouped['Weighted average'] / list(grouped2)
    superior['Weighted average'] = list(grouped['Weighted average'])
    return superior