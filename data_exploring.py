import numpy as np

def get_labels(df, col_name, Nvals):

    bar_labels = df.sort_values(by=[col_name], ascending=False)['name'].head(Nvals).tolist()

    labels = []
    for i, name in enumerate(bar_labels,start=1):
        labels.append(f"{i}: {name}")

    return labels

def get_most_recent_record(df, cnpj):
    return df[df['cnpj']==cnpj].to_dict('records')[0]


def get_subset_for_last_records_of_the_year(df,year):

    df_subset = df[(df['date'].dt.year > year-1) & (df['date'].dt.year < year+1)]
    unique_cnpj_list = df_subset['cnpj'].unique().tolist()

    for cnpj in unique_cnpj_list:
        date = get_most_recent_record(df_subset,cnpj)['date']
        df_subset = df_subset[~((df_subset['date']!=date) & (df_subset['cnpj']==cnpj))]

    return df_subset


def get_label_colors(bar_labels):

    bar_colors = []

    for label in bar_labels:
        if 'INPASA' in label:
            bar_colors.append('tab:red')
        elif 'FS ' in label:
            bar_colors.append('tab:blue')
        elif 'RAIZEN' in label:
            bar_colors.append('tab:orange')
        elif 'SAO MARTINHO' in label:
            bar_colors.append('tab:olive')
        elif 'TROPICAL' in label:
            bar_colors.append('tab:purple')
        elif 'ATVOS' in label:
            bar_colors.append('tab:green')
        else:
            bar_colors.append('tab:gray')

    return bar_colors


def subplot_bar_chart_capacities(ax,col_name,df,Nvals):

    xvals = np.arange(1,Nvals+1,1)
    yvals = df.sort_values(by=[col_name], ascending=False)[col_name].head(Nvals)

    bar_labels = get_labels(df,col_name,Nvals)
    bar_colors = get_label_colors(bar_labels)

    bar_chart = ax.bar(xvals , yvals, label = bar_labels, color = bar_colors)
    ax.bar_label(bar_chart, label_type='center')
    ax.legend(title='Key',fontsize=8)
    ax.set_title(col_name.replace('_',' '),fontsize=10)
    ax.set_xticks(xvals)
    ax.set_xlabel('Rank', fontsize=14)
    ax.set_ylabel('Production capacity (m³/day)', fontsize=14)


