from plotly import graph_objs as go, express as px

from ribbon_dataframe_functions import create_ribbon_chart_df


def getupperlower(cnpj, ribbon_chart_df):
    ch1 = ribbon_chart_df.query('cnpj == @cnpj')
    upper_col = [i for i in ch1.columns if 'upper' in i]
    lower_col = [i for i in ch1.columns if 'lower' in i]
    upper_data = ch1[upper_col].values.tolist()[0]
    lower_data = ch1[lower_col].values.tolist()[0]
    annotate_place = ch1['y0'].values.tolist()[0]
    return upper_data, lower_data, annotate_place


def get_name(df_name_cnpj,cnpj):
    return df_name_cnpj[df_name_cnpj['cnpj'] == cnpj]['name'].tolist()[0]


def get_smoothened_points(x,sub=0.1, axis='x'):

    temp = []
    if axis != 'x':
        for i in x:
            temp.append(i)
            temp.append(i)
    else:
        for i in x:
            temp.append(i-sub)
            temp.append(i+sub)

    return temp


def plot_ribbon_chart(df,colors_dict):

    ribbon_chart_df = create_ribbon_chart_df(df)

    years = df.columns.tolist()[2:]

    colors2 =[i for i in colors_dict.values()]

    df_name_cnpj = df[['name','cnpj']]
    x = [int(i) for i in years]
    x = get_smoothened_points(x, sub=.1)
    x_rev = x[::-1]

    fig = go.Figure()

    annotations = []

    # Ribbons
    for i, cnpj in enumerate(df.cnpj):

        upper_col, lower_col, annotate_place = getupperlower(cnpj,ribbon_chart_df)
        y_upper = get_smoothened_points(upper_col,axis='y')
        y_lower = get_smoothened_points(lower_col,axis='y')
        y_lower = y_lower[::-1]
        fig.add_trace(go.Scatter(
            x=x+[x[-1]+1, x[-1]+1]+x_rev,
            y=y_upper+[y_upper[-1], y_lower[0]]+y_lower,
            fill='toself',
            fillcolor=colors2[i],
            opacity=0.5,
            line_color='rgba(0,0,0,0.2)',
            showlegend=False,
            name=get_name(df_name_cnpj,cnpj),
            line_shape='spline',
            mode='lines',
            hovertemplate=' '
        ))
        annotations.append(dict(xref='paper', yref='y',
                                x=-0.005, y=annotate_place,
                                text=get_name(df_name_cnpj,cnpj),align="right",xanchor='right',
                                font=dict(family='Arial', size=14,
                                          color=colors2[i]),
                                showarrow=False))

    # Bars
    for i,year in enumerate(years):

        df_ribbon2 = df[['name','cnpj',year]].sort_values(year, ascending=True)
        df_ribbon2.columns = ['name','cnpj','capacity']
        df_ribbon2['year'] = int(year)

        fig_px = px.bar(df_ribbon2, y="capacity", x="year", color="name",color_discrete_map=colors_dict, hover_name="name", opacity=0.7, text_auto=True)
        fig_px.update_traces(hovertemplate='<b>%{value}</b>')
        fig_px.update_traces(textfont=dict(size=10,color='black'), textposition='auto', cliponaxis=False, texttemplate='%{value}')

        for trace in fig_px['data']:
            fig.add_trace(trace)

    annotation=[]



    fig.update_layout(barmode='stack',  bargap=0.7,showlegend=False)
    #fig.update_layout(plot_bgcolor='#f2f3f4', paper_bgcolor='#f2f3f4', margin=dict(l=100,b=10, r=100))

    fig.update_xaxes(range=[int(years[0])-0.15,int(years[-1])+0.15])
    fig.update_xaxes(nticks=len(years))

    fig.update_yaxes(range=[0,30000],showticklabels=True, showgrid=False, fixedrange=True)
    fig.update_layout(annotations=annotations)
    fig.update_layout(title='Top 5 bioethanol plants in terms of capacity (2020 ~ 2024)')

    fig.show()
