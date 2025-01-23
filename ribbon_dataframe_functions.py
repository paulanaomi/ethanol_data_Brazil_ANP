import numpy as np
import pandas as pd

import data_exploring as de

def create_df_with_yearly_data(year_start, year_end,df,col_name,Nvals):

    # merge data from over the years into a single dataframe
    for year in range(year_start,year_end+1):

        # Filters data for specified year
        df_year = de.get_subset_for_last_records_of_the_year(df, year)
        N = df_year.index.size

        df_temp = df_year[['name','cnpj',col_name]].sort_values(by=[col_name], ascending=False)
        #df_temp.drop(['date','state','capacity_anhydrous'], axis=1, inplace=True)
        df_temp.rename(columns={col_name:str(year)}, inplace=True)
        df_temp  = df_temp.set_index(np.arange(N)).head(Nvals)

        if 'final_df' in locals():
            final_df = pd.merge(final_df, df_temp[['cnpj',str(year)]], how='outer', on='cnpj')
        else:
            final_df = df_temp

    # fills in NaN values
    for pos in range(len(final_df)):
        empty_field = final_df.iloc[pos].isnull()

        for field in final_df.columns:
            if empty_field[field]:
                if field=='name':
                    if empty_field['name']:
                        df_year = de.get_subset_for_last_records_of_the_year(df, year_end)
                        cnpj = final_df.iloc[pos]['cnpj']
                        name = df_year.iloc[df_year[df_year['cnpj']==cnpj].index.tolist()[0]]['name']
                        final_df.at[pos,'name'] = name
                else:
                    df_year = de.get_subset_for_last_records_of_the_year(df, int(field))
                    if df_year[ df_year['cnpj'] == final_df.iloc[pos]['cnpj'] ].size == 0:
                        final_df.at[pos,field] = 0
                    else:
                        record = df_year[ df_year['cnpj'] == final_df.iloc[pos]['cnpj'] ]
                        final_df.at[pos,field] = record.loc[record[col_name].index.tolist()[0]][col_name]

    return final_df


def create_ribbon_chart_df (df):
    ribbon_chart_df = df[['name', 'cnpj']]

    years = df.columns.tolist()[2:]

    for i, col in enumerate(years):

        ch1 = df.loc[:,['cnpj',col]]
        ch1.sort_values(str(col), inplace=True)
        ch1[f'y{i}_upper'] = ch1[col].cumsum()
        ch1[f'y{i}_lower'] = ch1[f'y{i}_upper'].shift(1)
        ch1 = ch1.fillna(0)
        ch1[f'y{i}'] = ch1.apply(lambda x: (x[f'y{i}_upper'] + x[f'y{i}_lower'])/2, axis=1)
        ribbon_chart_df = ribbon_chart_df.merge(ch1.iloc[:, [0, 2, 3, 4]], on='cnpj')

    return ribbon_chart_df
