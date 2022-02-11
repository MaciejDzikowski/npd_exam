import pandas as pd


def parse_table(file_name: str, types_dict: dict=None, header_list: list=None) -> pd.DataFrame:
    """
    Prepares DataFrame from .xls* files.
    """
    if types_dict:
        if header_list:
            return pd.read_excel(file_name, dtype=types_dict, header=header_list).iloc[3:].reset_index(drop=True)
        return pd.read_excel(file_name, dtype=types_dict).iloc[3:].reset_index(drop=True)
    else:
        if header_list:
            return pd.read_excel(file_name, header=header_list).iloc[3:].reset_index(drop=True)
        return pd.read_excel(file_name).iloc[3:].reset_index(drop=True)


def parse_table_of_content(file_name: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Prepares DataFrames of table of content for 'Ludność. Stan i struktura ludności oraz ruch naturalny
    w przekroju terytorialnym'.
    """
    raw_df = pd.read_excel(file_name)
    df1 = raw_df.iloc[:7].drop(index=0)
    df2 = raw_df.iloc[9:].rename(columns={raw_df.columns[0]: raw_df.iloc[8, 0]}).reset_index(drop=True)
    return df1, df2


def get_id(df: pd.DataFrame, col_names: list) -> pd.Series:
    """
    Prepares data series by aggregating given columns' values to string.
    """
    return pd.Series(df[col_names].astype(str).agg(''.join, axis=1))


def get_needed_columns(df: pd.DataFrame, columns_names: list, new_idx: list=None, drop_lvls: list=None) -> pd.DataFrame:
    """
    Returns reduced dataframe with needed columns and new index.
    """
    if drop_lvls:
        if new_idx:
            return df[columns_names].droplevel(drop_lvls, axis=1).set_index(get_id(df, new_idx))
        return df[columns_names].droplevel(drop_lvls, axis=1)
    else:
        if new_idx:
            return df[columns_names].set_index(get_id(df, new_idx))
        return df[columns_names]
