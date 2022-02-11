import click
import glob
import pandas as pd

from package import parsers as pp
from package import functions as pf


@click.command()
@click.argument('t19', type=str)
@click.argument('t20', type=str)
@click.argument('lsis', type=str)
def run(t19, t20, lsis):
    """
    t19: directory name for 'Udziały za 2019 r.' \n
    t20: directory name for 'Udziały za 2020 r.' \n
    lsis: directory name for 'Ludność. Stan i struktura ludności oraz ruch naturalny w przekroju terytorialnym'
    """
    tables19 = glob.glob(t19 + "/*")
    tables20 = glob.glob(t20 + "/*")
    tables_lsis = glob.glob(lsis + "/*")

    gminy2019 = tables19[2]
    powiaty2019 = tables19[3]
    wojewodztwa2019 = tables19[0]
    gminy2020 = tables20[4]
    powiaty2020 = tables20[2]
    wojewodztwa2020 = tables20[3]
    tabII = tables_lsis[19]
    tabIII = tables_lsis[16]
    tabIV = tables_lsis[2]

    columns_names = ['Nazwa JST', 'województwo', 'powiat', 'Dochody wykonane\n(wpłaty minus zwroty)']
    income_row_name = 'Dochody wykonane\n(wpłaty minus zwroty)'
    types_dict = {'WK': str, 'PK': str, 'GK': str, 'GT': str, 'Identyfikator terytorialny\nCode': str}

    df_g19 = pp.get_needed_columns(pp.parse_table(gminy2019, types_dict, [3]), columns_names, ['WK', 'PK', 'GK', 'GT'])
    df_g20 = pp.get_needed_columns(pp.parse_table(gminy2020, types_dict, [3]), columns_names, ['WK', 'PK', 'GK', 'GT'])
    pf.print_income_stats(df_g19, income_row_name)
    pf.print_income_stats(df_g20, income_row_name)
    print("---")

    df_p19 = pp.get_needed_columns(pp.parse_table(powiaty2019, types_dict, [3]), columns_names, ['WK', 'PK'])
    df_p20 = pp.get_needed_columns(pp.parse_table(powiaty2020, types_dict, [3]), columns_names, ['WK', 'PK'])
    pf.print_income_stats(df_p19, income_row_name)
    pf.print_income_stats(df_p20, income_row_name)
    print("---")

    df_w19 = pp.get_needed_columns(pp.parse_table(wojewodztwa2019, types_dict, [3]), columns_names, ['WK'])
    df_w20 = pp.get_needed_columns(pp.parse_table(wojewodztwa2020, types_dict, [3]), columns_names, ['WK'])
    pf.print_income_stats(df_w19, income_row_name)
    pf.print_income_stats(df_w20, income_row_name)
    pf.make_plots(df_w19, df_w20, income_row_name, '2019', '2020')
    print("---")

    # dodanie danych o ludności
    working = 0.6

    df_II = pp.get_needed_columns(
        pp.parse_table(tabII, types_dict, [3]),
            ['Województwa\nVoivodships', 'Ludność\n(stan w dniu 31.12)\nPopulation\n(as of \nDecember 31)']
    ).iloc[1:17].reset_index(drop=True)
    df_II['Województwa\nVoivodships'] = df_II['Województwa\nVoivodships'].apply(lambda x: x.lower())
    df_II.rename(columns={'Województwa\nVoivodships': 'Nazwa JST'}, inplace=True)

    df_III = pp.get_needed_columns(
        pp.parse_table(tabIII, types_dict, [3]),
            ['Województwa \nVoivodships\nPowiaty\nPowiats',
             'Ludność\n(stan w dniu 31.12)\nPopulation\n(as of \nDecember 31)'],
            ['Identyfikator terytorialny\nCode']
        )
    df_III = df_III.drop(df_III[df_III.index == 'nan'].index)

    df_IV = pp.get_needed_columns(
        pp.parse_table(tabIV, types_dict, [3], ),
            ['Województwa\nVoivodships\nGminy\nGminas', 'Ludność\n(stan w dniu 31.12)\nPopulation\n(as of \nDecember 31)'],
            ['Identyfikator terytorialny\nCode']
    )
    df_IV = df_IV.drop(df_IV[df_IV.index == 'nan'].index)

    # średni dochów
    woj20 = pd.merge(df_w20, df_II, on='Nazwa JST')
    pf.get_average_income_per_worker(woj20, 'Dochody wykonane\n(wpłaty minus zwroty)',
                                     'Ludność\n(stan w dniu 31.12)\nPopulation\n(as of \nDecember 31)', working)

    pow20 = pd.merge(df_p20, df_III, left_index=True, right_index=True)
    pf.get_average_income_per_worker(pow20, 'Dochody wykonane\n(wpłaty minus zwroty)',
                                     'Ludność\n(stan w dniu 31.12)\nPopulation\n(as of \nDecember 31)', working)

    gm20 = pd.merge(df_g20, df_IV, left_index=True, right_index=True)
    pf.get_average_income_per_worker(gm20, 'Dochody wykonane\n(wpłaty minus zwroty)',
                                     'Ludność\n(stan w dniu 31.12)\nPopulation\n(as of \nDecember 31)', working)

    # wariancja
    pf.get_variance(woj20, pow20, 'województwo', 'Dochody wykonane\n(wpłaty minus zwroty)')

    gm20['pow_id'] = gm20.index
    gm20['pow_id'] = gm20['pow_id'].apply(lambda x: x[:-3])
    pf.get_variance(pow20, gm20, 'pow_id', 'Dochody wykonane\n(wpłaty minus zwroty)')

    # średnia ważona
    print(pf.get_weighted_average(woj20, pow20, 'województwo', 'Dochody wykonane\n(wpłaty minus zwroty)',
                                  'Ludność\n(stan w dniu 31.12)\nPopulation\n(as of \nDecember 31)', working))
    print(pf.get_weighted_average(pow20, gm20, 'pow_id', 'Dochody wykonane\n(wpłaty minus zwroty)',
                                  'Ludność\n(stan w dniu 31.12)\nPopulation\n(as of \nDecember 31)', working))
    print("---")
    print(woj20)
    print("---")
    print(pow20)
    print("---")
    print(gm20)


if __name__ == "__main__":
    run()