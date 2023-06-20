import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

def _metricas_noaa(df_noaa_global, stat):
    dict_y_title={
          'PRCP':('value_mean','Média da Precipitação')
        , 'TAVG':('value_mean','Média da Temperatura')
        , 'TMAX':('value_max','Máxima da Temperatura')
        , 'TMIN':('value_min','Mínima da Temperatura')
    }

    fig = go.Figure()

    fig = px.line(
        df_noaa_global.loc[df_noaa_global['stat']==stat], 
        x='year', y=dict_y_title[stat][0], color='country_code'
        , custom_data=['year', 'value_min','value_mean','value_median','value_max', 'country_code']
    )

    # hide axes
    fig.update_xaxes(visible=True, title='')
    fig.update_yaxes(visible=True,
                    gridcolor='white',zeroline=True,
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

    fig.update_traces(
        hovertemplate="""
        <b>Min.:</b> %{customdata[1]} 
        <b>Med.:</b> %{customdata[2]} 
        <b>Mediana:</b> %{customdata[3]} 
        <b>Max.:</b> %{customdata[4]} 
        """
    )

    # strip down the rest of the plot
    fig.update_layout(
        showlegend=True,
        plot_bgcolor="white",
        margin=dict(l=10,b=10,r=10)
    )

    fig.update_layout(title={
        'text' : f"""<b>{dict_y_title[stat][1]}</b> 
        <br><sup>Comparativo nos anos, a partir de 1970</sup>"""
    })
    return fig

def _density_noaa(df_noaa_global, stat):
    dict_y_title={
          'PRCP':('value_mean','Média da Precipitação')
        , 'TAVG':('value_mean','Média da Temperatura')
        , 'TMAX':('value_max','Máxima da Temperatura')
        , 'TMIN':('value_min','Mínima da Temperatura')
    }

    fig = px.violin(
        df_noaa_global.loc[df_noaa_global['stat']==stat], 
        x='country_code', y=dict_y_title[stat][0], color='country_code'
        , hover_data=['year']
        , box=True
        , points='all'
    )

    # hide axes
    fig.update_xaxes(visible=True, title='')
    fig.update_yaxes(visible=True, title=''
                    )
    
    fig.update_layout(title={
        'text' : f"""<b>{dict_y_title[stat][1]}</b> 
        <br><sup>Distribuição nos anos, a partir de 1970</sup>"""
    })
    return fig