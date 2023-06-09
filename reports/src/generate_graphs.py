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
    
    # Ajustar dado do hover
    fig.update_layout(
        hovermode='x unified',
    )
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

     # Ajustar dado do hover
    fig.update_layout(
        hovermode='x unified',
    )
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

     # Ajustar dado do hover
    fig.update_layout(
        hovermode='x unified',
    )
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
    
     # Ajustar dado do hover
    fig.update_layout(
        hovermode='x unified',
    )

    return fig 

def _exportacoes_top10_dol(df):
     # Group the data by year and calculate the total sales and quantity
    grouped_df = df.groupby('Country').agg({'Sales (Dollars)': 'sum', 'Quantity (L)': 'sum'}).reset_index()

    # Sort the data by total sales in descending order
    grouped_df = grouped_df.sort_values(by='Quantity (L)', ascending=False)

    # Create a figure with two y-axes
    fig = go.Figure()

    # Create a bar trace for total sales in dollars
    fig.add_trace(go.Bar(x=grouped_df['Country'], y=grouped_df['Quantity (L)'],
                        name='Quantidade de L Vendidos', marker_color='blue', yaxis='y'))

    # Create a scatter trace for total quantity in kgs
    fig.add_trace(go.Scatter(x=grouped_df['Country'], y=grouped_df['Sales (Dollars)'],
                            name='Total de Exportações (Dólares)', mode='lines+markers', marker_color='red', yaxis='y2'))

    # Set layout properties
    fig.update_layout(title='Exportações em dólares e Quantidade de L vendidos por país',
                    xaxis_title='País', yaxis=dict(title='Total de Exportações (Dólares)'),
                    yaxis2=dict(title='Quantidade de L Vendidos', overlaying='y', side='right'),
                    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                    template='plotly_dark')
     # Ajustar dado do hover
    fig.update_layout(
        hovermode='x unified',
    )
    return fig

def _credito_top10(df):
    df = df.query('metric=="domestic_credit_to_private_sector"').groupby('country').agg({'value':'mean'}).reset_index()
    df['value'] = [round(x, 2) for x in df['value']]
    df_top10 = df.sort_values(by='value', ascending=False).head(10)

    # Create a bar chart for the total quantity sold of the top 10 countries
    fig = px.bar(df_top10, x='country', y='value', text='value',
                title='Top 10 Países com Maior Crédito para o Setor Privado',
                labels={'value': 'Crédito Setor Privado (Média da % do PIB)'},
                template='plotly_dark')

    fig.update_yaxes(visible=True,
                    gridcolor='black',zeroline=True,
                    showticklabels=False, title='Crédito Setor Privado (Média da % do PIB)',
                    )
    
    fig.update_xaxes(visible=True,
                    gridcolor='black', title='Países',
                    )
    
    # Set layout properties
    fig.update_layout(showlegend=False, 
                      xaxis={'categoryorder': 'total descending'})

     # Ajustar dado do hover
    fig.update_layout(
        hovermode='x unified',
    )
    return fig

def _register_business_top10(df):
    df = df.query('metric=="numberof_procedures_register_business"').groupby('country').agg({'value':'sum'}).reset_index()
    df = df.loc[df['value']>0]
    df_top10 = df.sort_values(by='value', ascending=True).head(10)
    
    # Create a bar chart for the total quantity sold of the top 10 countries
    fig = px.bar(df_top10, x='country', y='value',text='value',
                template='plotly_dark')

    fig.update_yaxes(visible=True,
                    gridcolor='black',zeroline=True,
                    showticklabels=False, title='Nº de Procedimentos'
                    )
    fig.update_xaxes(visible=True,
                    gridcolor='black', title='Países',
                    )
    # Set layout properties
    fig.update_layout(showlegend=False, 
                      xaxis={'categoryorder': 'total ascending'})

    fig.update_layout(title={
        'text' : f"""<b>Top 10 Países com menos procedimentos para abertura de empresas</b> 
        <br><sup>Notamos que existem países com 0 procedimentos, por isso acabamos filtrando!</sup>"""
    })

     # Ajustar dado do hover
    fig.update_layout(
        hovermode='x unified',
    )
    return fig

def _crescimento_pop_top10(df):
    df = df.query('metric=="population_growth"')
    df_max = df.groupby('country').agg({'year':'max'}).reset_index()#

    df = df.merge(df_max, on=['country','year'], how='inner').groupby('country').agg({'value':'mean'}).reset_index()

    df_top10 = df.sort_values(by='value', ascending=False).head(10)

    # Create a bar chart for the total quantity sold of the top 10 countries
    fig = px.bar(df_top10, x='country', y='value',text='value',
                title='''<b>Top 10 Países com Maior crescimento populacional médio*</b>
                <br><sup>* Considerando-se o último ano na base</sup>
                ''',
                template='plotly_dark')

    fig.update_yaxes(visible=True,
                    gridcolor='black',zeroline=True,
                    showticklabels=False, title='Crescimento Populacional'
                    )
    fig.update_xaxes(visible=True,
                    gridcolor='black', title='Países',
                    )
    # Set layout properties
    fig.update_layout(showlegend=False, 
                      xaxis={'categoryorder': 'total descending'})

     # Ajustar dado do hover
    fig.update_layout(
        hovermode='x unified',
    )
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
                y='country', x='metric', color='Faixa do índice', text='country',
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
     # Ajustar dado do hover
    fig.update_layout(
        hovermode='x unified',
    )
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

def _comercio_no_rs(df):
        # Create a figure with two y-axes
    fig = go.Figure()

    # Create a bar trace for total sales in dollars
    fig.add_trace(go.Bar(x=df['produto'], y=df['quantidade_com_rs'],
                        name='Quantidade Comercializada no RS', marker_color='blue', yaxis='y'))

    # Create a scatter trace for total quantity in kgs
    fig.add_trace(go.Scatter(x=df['produto'], y=df['representatividade'],
                            name='Representatividade', mode='lines+markers', marker_color='red', yaxis='y2'))

    # Set layout properties
    fig.update_layout(title='Comércio de produtos derivados do vinho nos últimos 15 anos',
                    xaxis_title='Produto', yaxis=dict(title='Quantidade Comercializada no RS'),
                    yaxis2=dict(title='Representatividade', overlaying='y', side='right'),
                    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                    template='plotly_dark')
    
    # Ajustar dado do hover
    fig.update_layout(
        hovermode='x unified',
    )

    return fig 

def _wine_ratings(df):

    # Ordenar o DataFrame por tipo, média e país, com points em ordem decrescente
    grouped_df = df.sort_values(by=['tipo', 'points', 'country'], ascending=[True, False, True])

    # Criar os gráficos de barra separados
    figs = []

    # Definir as cores para cada tipo de vinho
    colors = {'tinto': 'red', 'branco': 'grey', 'rosado': 'pink', 'espumante':'yellow'}


    # Gerar um gráfico de barra para cada tipo de vinho
    for tipo in grouped_df['tipo'].unique():
        data = grouped_df[grouped_df['tipo'] == tipo]

        # Encontrar a pontuação média do país "Brazil"
        brazil_mean_points = data[(data['country'] == 'Brazil')]['points'].mean()

        data = data.sort_values(by='points', ascending=False).head(5)
        
        # Criar a figura para o tipo de vinho atual
        fig = go.Figure()

        # Adicionar um trace de barra para o tipo de vinho atual
        fig.add_trace(go.Bar(x=data['country'], y=data['points'], name=tipo, marker_color=colors[tipo]))

        # Adicionar uma linha horizontal tracejada no valor da pontuação média do país "Brazil"
        fig.add_shape(
            type='line',
            x0=data['country'].iloc[0],
            x1=data['country'].iloc[-1],
            y0=brazil_mean_points,
            y1=brazil_mean_points,
            line=dict(color='black', width=3, dash='dash')
        )

        # Configurar o layout do gráfico atual
        fig.update_layout(
            title=f'''Top 5 - Média de Pontuação por País
             <br><sup>Tipo: {tipo}</sup>''',
            xaxis=dict(title='País'),
            yaxis=dict(title='Pontuação Média'),
            barmode='group'
        )

        figs.append(fig)

    # Exibir os gráficos separadamente, um abaixo do outro
    return figs

def _wine_ratings_opportunity(df):

    # Ordenar o DataFrame por tipo, média e país, com points em ordem decrescente
    grouped_df = df.sort_values(by=['tipo', 'points', 'country'], ascending=[True, False, True])

    # Criar os gráficos de barra separados
    figs = []

    # Definir as cores para cada tipo de vinho
    colors = {'tinto': 'red', 'branco': 'grey', 'rosado': 'pink', 'espumante':'yellow'}

    # Gerar um gráfico de barra para cada tipo de vinho
    for tipo in grouped_df['tipo'].unique():
        data = grouped_df[grouped_df['tipo'] == tipo]

        # Encontrar a pontuação média do país "Brazil" + tolerancia de 15%
        brazil_mean_points = (data[(data['country'] == 'Brazil')]['points'].mean()) * 1.015

        data = data[(data['points'] <= brazil_mean_points)].sort_values(by='points', ascending=False).head(6)


        # Criar a figura para o tipo de vinho atual
        fig = go.Figure()

        # Adicionar um trace de barra para o tipo de vinho atual
        fig.add_trace(go.Bar(x=data['country'], y=data['points'], name=tipo, marker_color=colors[tipo]))

        # Adicionar uma linha horizontal tracejada no valor da pontuação média do país "Brazil"
        fig.add_shape(
            type='line',
            x0=data['country'].iloc[0],
            x1=data['country'].iloc[-1],
            y0=brazil_mean_points,
            y1=brazil_mean_points,
            line=dict(color='green', width=6, dash='dash')
        )

        # Configurar o layout do gráfico atual
        fig.update_layout(
            title=f'''Top 5 - Média de Pontuação por País 
            <br><sup>Tipo: {tipo}</sup>''',
            xaxis=dict(title='País'),
            yaxis=dict(title='Pontuação Média'),
            barmode='group'
        )

        figs.append(fig)

    # Exibir os gráficos separadamente, um abaixo do outro
    return figs

def _br_density_ratings(df_full, _type='espumante'):
    fig = px.violin(
        df_full.loc[(df_full['country']=='Brazil') & (df_full['tipo']==_type)], 
        x='tipo', y='points', color='country'
        , box=True
        , points='all'
    )

    # hide axes
    fig.update_xaxes(visible=True, title='')
    fig.update_yaxes(visible=True, title='')

    fig.update_layout(title={
        'text' : f"""<b>Avaliações do Brasil - {_type}</b> 
        <br><sup>Distribuição nos anos</sup>"""
    })
    return fig

def _density_ratings(df_full, _type='espumante'):
    df_top10 = df_full.loc[df_full['country']!='Brazil'].groupby(['country'])['points'].agg(['mean','count']).reset_index()
    # Filtrar países com pelo menos 30 avaliações
    df_top10 = df_top10[df_top10['count'] >= 30].nlargest(columns='mean', n=10)

    fig = px.violin(
        df_full.loc[df_full['country'].isin(df_top10['country'].to_list())], 
        x='tipo', y='points', color='country'
        , box=True
        , points='all'
    )

    # hide axes
    fig.update_xaxes(visible=True, title='')
    fig.update_yaxes(visible=True, title=''
                    )

    fig.update_layout(title={
        'text' : f"""<b>Avaliações - {_type}</b> 
        <br><sup>Distribuição nos anos</sup>"""
    })
    return fig

def _densities_ratings(df):
    return {
        _type : {
            'Brasil':_br_density_ratings(df, _type),
            'top10':_density_ratings(df, _type)
        } for _type in df['tipo'].unique()
    }