import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import config

def _metricas_noaa(df_noaa_global, stat):
    """
    com o dado de clima do rs, vou filtrar para apenas mostrar os mais semelhantes; a analisar como (colocar uma faixa de +5% a -5%? com correlação de pearson/dtw?)
    """
    
    fig = go.Figure()

    fig = px.line(
        df_noaa_global.loc[df_noaa_global['stat']==stat], 
        x='year', y=config.DICT_Y[stat][0], color='country_code'
        , custom_data=['year', config.DICT_Y[stat][0], 'country_code']
    )

    # hide axes
    fig.update_xaxes(visible=True, title='')
    fig.update_yaxes(visible=True,
                    gridcolor='black',zeroline=True,
                    showticklabels=True, title=''
                    )

    # remove facet/subplot labels
    # fig.update_layout(annotations=[], overwrite=True)

    # Inverte annotation do modelo cor
    # fig.for_each_annotation(lambda a: a.update(
    #     x=0
    #     , textangle=0
    #     , valign='top'
    #     , yref='paper', yanchor='bottom'
    #     , text=a.text.replace("Modelo/Cor=", "")
    # ))

    # Ajustar dado do hover
    fig.update_layout(
        hovermode='x unified',
    )

    # fig.update_traces(
    #     hovertemplate="""
    #     <b>Metr.:</b> %{customdata[1]} 
    #     <b>Med.:</b> %{customdata[2]} 
    #     <b>Mediana:</b> %{customdata[3]} 
    #     <b>Max.:</b> %{customdata[4]} 
    #     """
    # )

    # strip down the rest of the plot
    fig.update_layout(
        showlegend=True,
        plot_bgcolor="black",
        margin=dict(l=10,b=10,r=10)
    )

    fig.update_layout(title={
        'text' : f"""<b>{config.DICT_Y[stat][1]}</b> 
        <br><sup>Comparativo nos anos</sup>"""
    })
    return fig

def _density_noaa(df_noaa_global, stat):
    df_noaa_global = df_noaa_global.loc[df_noaa_global['country_code']!='BR-RS']
    fig = px.violin(
        df_noaa_global.loc[df_noaa_global['stat']==stat], 
        x='country_code', y=config.DICT_Y[stat][0], color='country_code'
        , hover_data=['year']
        , box=True
        , points='all'
    )

    # hide axes
    fig.update_xaxes(visible=True, title='')
    fig.update_yaxes(visible=True, title=''
                    )
    
    fig.update_layout(title={
        'text' : f"""<b>{config.DICT_Y[stat][1]}</b> 
        <br><sup>Distribuição nos anos</sup>"""
    })
    return fig

def _exportacao_vinhos_por_pais(df):
    # Group the data by year and country and calculate the total sales and quantity
    grouped_df = df.groupby(['Year', 'Country']).agg({'Sales (Dollars)': 'sum', 'Quantity (L)': 'sum'}).reset_index()

    # Sort the data by year and total sales in descending order
    sorted_df = grouped_df.sort_values(by=['Year', 'Sales (Dollars)'], ascending=[True, False])

    # Filter the top 10 countries for each year
    filtered_df = sorted_df.groupby('Year').head(10)

    # Create an interactive bar chart
    fig = px.bar(filtered_df, x='Country', y='Sales (Dollars)', color='Country', animation_frame='Year',
                title='Exportações em dólares por país', labels={'Sales (Dollars)': 'Total de Exportações (Dólares)'},
                template='plotly_dark')

    # Set layout properties
    fig.update_layout(showlegend=False, xaxis={'categoryorder': 'total descending'}, yaxis_title='Total de Exportações (Dólares)')

    return fig

def _quantidade_vendida_por_pais_ano(df):
    # Group the data by year and country and calculate the total quantity sold
    grouped_df = df.groupby(['Year', 'Country'])['Quantity (L)'].sum().reset_index()

    # Sort the data by year and total quantity in descending order
    sorted_df = grouped_df.sort_values(by=['Year', 'Quantity (L)'], ascending=[True, False])

    # Filter the top 10 countries for each year
    filtered_df = sorted_df.groupby('Year').head(10)

    # Create an interactive bar chart for quantity of l sold by country and year
    fig = px.bar(filtered_df, x='Country', y='Quantity (L)', color='Country', animation_frame='Year',
                title='Quantidade de L vendidos por país e ano',
                labels={'Quantity (L)': 'Quantidade de L Vendidos'},
                template='plotly_dark')

    # Set layout properties
    fig.update_layout(showlegend=False, xaxis={'categoryorder': 'total descending'}, yaxis_title='Quantidade de Kgs Vendidos')

    return fig

def _proporcao_valor_por_litro_vendido_pais_ano(df):
    # Group the data by year and country and calculate the total quantity sold and total sales
    grouped_df = df.groupby(['Year', 'Country']).agg({'Quantity (L)': 'sum', 'Sales (Dollars)': 'sum'}).reset_index()

    # Calculate the coefficient by dividing total sales by total quantity
    grouped_df['Coefficient'] = grouped_df['Sales (Dollars)'] / grouped_df['Quantity (L)']

    # Sort the data by year and coefficient in descending order
    sorted_df = grouped_df.sort_values(by=['Year', 'Coefficient'], ascending=[True, False])

    # Filter the top 10 countries for each year
    filtered_df = sorted_df.groupby('Year').head(10)

    # Create an interactive bar chart for the coefficient by country and year
    fig = px.bar(filtered_df, x='Country', y='Coefficient', color='Country', animation_frame='Year',
                title='Valor em Dólares por L vendido por país e ano',
                labels={'Coefficient': 'Coeficiente (Valor em Dólares/L)'},
                template='plotly_dark')

    # Set layout properties
    fig.update_layout(showlegend=False, xaxis={'categoryorder': 'total descending'}, yaxis_title='Coeficiente (Valor em Dólares/Kg)')

    return fig

def _exportacao_dolar_quantidade_ano(df):
    # Group the data by year and calculate the total sales and quantity
    grouped_df = df.groupby('Year').agg({'Sales (Dollars)': 'sum', 'Quantity (L)': 'sum'}).reset_index()

    # Create a figure with two y-axes
    fig = go.Figure()

    # Create a bar trace for total sales in dollars
    fig.add_trace(go.Bar(x=grouped_df['Year'], y=grouped_df['Quantity (L)'],
                        name='Quantidade de L Vendidos', marker_color='blue', yaxis='y'))

    # Create a scatter trace for total quantity in kgs
    fig.add_trace(go.Scatter(x=grouped_df['Year'], y=grouped_df['Sales (Dollars)'],
                            name='Total de Exportações (Dólares)', mode='lines+markers', marker_color='red', yaxis='y2'))

    # Set layout properties
    fig.update_layout(title='Exportações em dólares e Quantidade de L vendidos por ano',
                    xaxis_title='Ano', yaxis=dict(title='Total de Exportações (Dólares)'),
                    yaxis2=dict(title='Quantidade de L Vendidos', overlaying='y', side='right'),
                    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                    template='plotly_dark')
    
    return fig 

def _exportacoes_top10_dol(df):
    # Group the data by country and calculate the total sales
    grouped_df = df.groupby('Country')['Sales (Dollars)'].sum().reset_index()

    # Sort the data by total sales in descending order
    sorted_df = grouped_df.sort_values(by='Sales (Dollars)', ascending=False)

    # Filter the top 10 countries
    top_10_countries = sorted_df.head(10)

    # Create a bar chart for the total sales of the top 10 countries
    fig = px.bar(top_10_countries, x='Country', y='Sales (Dollars)',
                title='Total de Exportações em Dólares dos Top 10 Países nos Últimos 15 Anos',
                labels={'Sales (Dollars)': 'Total de Exportações (Dólares)'},
                template='plotly_dark')

    # Set layout properties
    fig.update_layout(showlegend=False, xaxis={'categoryorder': 'total descending'}, yaxis_title='Total de Exportações (Dólares)')

    return fig

def _exportacoes_top10_qtd(df):
    # Group the data by country and calculate the total quantity sold
    grouped_df = df.groupby('Country')['Quantity (L)'].sum().reset_index()

    # Sort the data by total quantity in descending order
    sorted_df = grouped_df.sort_values(by='Quantity (L)', ascending=False)

    # Filter the top 10 countries
    top_10_countries = sorted_df.head(10)

    # Create a bar chart for the total quantity sold of the top 10 countries
    fig = px.bar(top_10_countries, x='Country', y='Quantity (L)',
                title='Quantidade Total de L Exportados dos Top 10 Países',
                labels={'Quantity (L)': 'Quantidade Total de L Exportados'},
                template='plotly_dark')

    # Set layout properties
    fig.update_layout(showlegend=False, xaxis={'categoryorder': 'total descending'}, yaxis_title='Quantidade Total de L Exportados')

    return fig

def _credito_top10(df):
    df = df.query('metric=="domestic_credit_to_private_sector"').groupby('country').agg({'value':'sum'}).reset_index()

    df_top10 = df.sort_values(by='value', ascending=False).head(10)

    # Create a bar chart for the total quantity sold of the top 10 countries
    fig = px.bar(df_top10, x='country', y='value',
                title='Top 10 Países com Maior Crédito para o Setor Privado',
                labels={'value': 'Crédito Setor Privado'},
                template='plotly_dark')

    fig.update_yaxes(visible=True,
                    gridcolor='black',zeroline=True,
                    showticklabels=False, title='Crédito Setor Privado'
                    )
    # Set layout properties
    fig.update_layout(showlegend=False, 
                      xaxis={'categoryorder': 'total descending'})

    return fig

def _register_business_top10(df):
    df = df.query('metric=="numberof_procedures_register_business"').groupby('country').agg({'value':'sum'}).reset_index()
    df = df.loc[df['value']>0]
    df_top10 = df.sort_values(by='value', ascending=True).head(10)
    
    # Create a bar chart for the total quantity sold of the top 10 countries
    fig = px.bar(df_top10, x='country', y='value',
                template='plotly_dark')

    fig.update_yaxes(visible=True,
                    gridcolor='black',zeroline=True,
                    showticklabels=False, title='Nº de Procedimentos'
                    )
    # Set layout properties
    fig.update_layout(showlegend=False, 
                      xaxis={'categoryorder': 'total ascending'})

    fig.update_layout(title={
        'text' : f"""<b>Top 10 Países com menos procedimentos para abertura de empresas</b> 
        <br><sup>Notamos que existem países com 0 procedimentos, por isso acabamos filtrando!</sup>"""
    })
    return fig

def _crescimento_pop_top10(df):
    df = df.query('metric=="population_growth"').groupby('country').agg({'value':'sum'}).reset_index()

    df_top10 = df.sort_values(by='value', ascending=False).head(10)

    # Create a bar chart for the total quantity sold of the top 10 countries
    fig = px.bar(df_top10, x='country', y='value',
                title='Top 10 Países com Maior crescimento populacional',
                template='plotly_dark')

    fig.update_yaxes(visible=True,
                    gridcolor='black',zeroline=True,
                    showticklabels=False, title='Crescimento Populacional'
                    )
    # Set layout properties
    fig.update_layout(showlegend=False, 
                      xaxis={'categoryorder': 'total descending'})

    return fig

def _logistic_groups(df):
    df = df.query('metric=="logistic_performance_index_1to5"')
    bins = [0, 1, 2, 3, 4, 99]
    labels = ['0-1','1-2','2-3','3-4','4+']
    df['Faixa do índice'] = pd.cut(df['value'], bins = bins, labels =labels)
    df = df.groupby('Faixa do índice').agg({'country':'nunique'}).reset_index()
    df['metric'] = 'logistic_performance_index'
    
    # Create a bar chart for the total quantity sold of the top 10 countries
    fig = px.bar(df, 
                y='country', x='metric', color='Faixa do índice',
                title='Top 10 Países com Maior crescimento populacional',
                template='plotly_dark')

    fig.update_xaxes(visible=False)
                     
    fig.update_yaxes(visible=False,
                    gridcolor='black',
                    zeroline=False, showticklabels=False,
                    )
    # Set layout properties
    fig.update_layout(showlegend=True, 
                      xaxis={'categoryorder': 'total descending'})

    fig.update_layout(title={
        'text' : f"""<b>Performace Logística dos Países</b> 
        <br><sup>Quantidade de Países por faixa</sup>"""
    })
    return fig

def _logistic_bests(df):
    df = df.query('metric=="logistic_performance_index_1to5"')
    bins = [0, 1, 2, 3, 4, 99]
    labels = ['0-1','1-2','2-3','3-4','4+']
    df['Faixa do índice'] = pd.cut(df['value'], bins = bins, labels =labels)
    df = df.loc[df['Faixa do índice']=="4+"]
    
    # Create a bar chart for the total quantity sold of the top 10 countries
    fig = px.line(
        df, 
        x='year', y='value', color='country',
        symbol='country'
    )

    # hide axes
    fig.update_yaxes(visible=True,
                    gridcolor='black',zeroline=True,
                    showticklabels=False, title=''
                    )

    # remove facet/subplot labels
    # fig.update_layout(annotations=[], overwrite=True)

    # Ajustar dado do hover
    fig.update_layout(
        hovermode='x unified'
    )

    fig.update_layout(title={
        'text' : """<b>Faixa 4+</b>
        <sup>Melhores países por performance logística</sup>
        """
    })
    return fig

def _density_clima_rs(df_full, stat):

    fig = px.violin(
        df_full.loc[df_full['country_code']=='BR-RS'], 
        x='country_code', y=config.DICT_Y[stat][0], color='country_code'
        , hover_data=['year']
        , box=True
        , points='all'
    )

    # hide axes
    fig.update_xaxes(visible=True, title='')
    fig.update_yaxes(visible=True, title=''
                    )
    
    fig.update_layout(title={
        'text' : f"""<b>{config.DICT_Y[stat][1]}</b> 
        <br><sup>Distribuição nos anos</sup>"""
    })
    return fig