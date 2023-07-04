import streamlit as st
import config 
import src.generate_graphs as generate_graphs
import src.get_data as get_data
from datetime import date

st.set_page_config(
    page_title="Tech Challenge #01 - Grupo 27",
    layout="wide"
)

st.sidebar.image(config.LOGO, caption='Wine Study', use_column_width=True)

st.sidebar.title("Seleção de parâmetros")

# add a slider to select time frame to get data
with st.sidebar.expander("Selecionar time frame"):
    years_to_filter = st.slider(
        "Para qual espaço de tempo quero analisar?",
        value=[15],
        step=1, min_value=1, max_value=(date.today().year - 1970))[0]
    
st.write("""
# Tech Challenge - vinhos
""")     

# add an exapnder for the user to display more info about the app
with st.expander("Mais detalhes"):
    st.info("""
        - Para as análises climáticas, Adquirimos os dados da [NOAA global historical climatology network (daily)](https://www.kaggle.com/datasets/noaa/noaa-global-historical-climatology-network-daily), uma rede de bases de dados de resumos diários do clima de diferentes estações no nosso planeta. 
        - O dado contém a latitude e longitude da estação climatológica, e acabamos normalizando para que tenhamos o código do país (duas letras), de forma a podermos cruzar com dados dos indicadores da seção de análise macroeconômica.
        - Para normalizar o dado por país, usamos a média dos valores das estatísticas colocadas, por ano, trazendo o dado diário para a configuração anual esperada para análise em conjunto com as exportações de vinhos do estado do RS.
        - Notamos ainda, que a temperatura estava armazenada em Farenheidt, realizando a transformação para celsius, e retirando valores que sejam inferiores a -90 graus celsius (menor temperatura já registrada no planeta, na Antártida), e maiores que 57 (maior temperatura já registrada, no Death Valley, Califórnia, USA)
        - Ao chegarmos na análise das variáveis, utilizamos um ranqueamento dos países, por ano, tendo como métrica o erro percentual absoluto médio com relação ao valor máximo, mínimo e médio da variável sendo analisada. Os países que tiverem as menores diferenças estarão com o menor erro percentual dessas três métricas (mínimo, máximo e médio) da variável climática, em cada ano. Após realizar esse ranqueamento, somamos os ranques de cada país, e ordenamos do menor para o maior, realizando um novo ranqueamento, e filtrando os países que estão dentro do top 3, para precipitação (podemos ter mais de um por posição!) e top 6 para as temperaturas;
    """,
        icon="ℹ️"
    )

base_path = '..\\data\\processed'

# Layout do aplicativo
tab_precipitacao, tab_temp_media, tab_temp_min, tab_temp_max, tab_consideracoes_finais = st.tabs(["Precipitação","Temperatura Média", "Temperatura Mínima", "Temperatura Máxima", "Considerações Finais"])

with tab_precipitacao:
    st.plotly_chart(
    generate_graphs._metricas_noaa(get_data.DF_PRECP_COMPARATIVE(
                  df_clima_rs=get_data.DF_RS(years_to_filter)
                , df_noaa_global=get_data.DF_NOAA_GLOBAL()
                , stat='PRCP', thresold_filter = 3
            ),'PRCP')
    , use_container_width=True)

    st.write("""
            Ao compararmos a precipitação média, notamos uma maior presença de países da América do Sul, em uma faixa de clima muito parecida com a nossa, como Argentina, Venezuela e Equador.
            Nova Caledônia, Nova Zelândia e Ilhas Marshall estão em uma faixa muito parecida com o Rio Grande do Sul do mundo - tendo uma boa parte do clima com grandes semelhanças ao estado do Brasil.
            Malta se encontra em uma região de clima mais tropical, estando logo acima da África, na região central do Mediterrâneo, e também possui um clima ameno.
            Já Finlândia, possui um clima temperado continental, tendo verões bem chuvosos, com os 4 climas bem definidos, como no Brasil, mas com um Inverno mais rigoroso ao norte.
            A Polônia estaria no limite de semelhança, tendo o clima temperado, com um verão bem quente e curto, e um inverno longo e frio. obtendo médias mais baixas por ano, sendo semelhante a Finlândia e Malta.

            
        """,
        icon="ℹ️")
    st.divider() # ------------------------------------------------------
    col1, col2 = st.columns([1,3])
    with col1:
        df_precp = get_data.DF_PRECP_COMPARATIVE(
                df_clima_rs=get_data.DF_RS(years_to_filter)
                , df_noaa_global=get_data.DF_NOAA_GLOBAL()
                , stat='PRCP', thresold_filter = 3
            )
        st.plotly_chart(
        generate_graphs._density_clima_rs(
            df_full=df_precp
            , stat='PRCP'
            )
        , use_container_width=True)

    with col2:
        st.plotly_chart(
        generate_graphs._density_noaa(
            get_data.DF_PRECP_COMPARATIVE(
                  df_clima_rs=get_data.DF_RS(years_to_filter)
                , df_noaa_global=get_data.DF_NOAA_GLOBAL(years_to_filter)
                , stat='PRCP', thresold_filter = 3
            ),'PRCP')
        , use_container_width=True)

    st.write("""
            Na análise da distribuição dos dados de precipitação, notamos o quão semelhante são os países da América do Sul novamente, com distribuições um pouco diversas, mas que refletem os pontos médios e máximos do RS, com concentrações em 
            60 (para Argentina), e entre 50 e 80 (para Venezuela e Equador). Os demais países estão em uma faixa mais baixa de precipitação média, com valores entre 15 e 30, sendo que o RS possui uma maior concentração em 20 e 40 mm, compreendendo tais faixas da mesma maneira.

            No quesito precipitação, todos os países mencionados parecem fazer sentido como sendo boas escolhas, levando em consideração que o clima, a sensação térmica e a temperatura são altamente influenciados pela mesma, e quem não gosta de um vinho no friozinho!
        """,
        icon="ℹ️")

with tab_temp_media:

    st.write("""
            Novamente, ao analisarmos as Temperaturas Médias, encontramos as Ilhas Marshal, e um país da América do Sul, a Bolívia.
            Ainda, a presença da África do Sul, estando em uma faixa parecida com o RS no globo terrestre;
            A Áustria conta com estações bem definidas durante o ano, chegando a ter temperaturas perto de 30º C no verão, mas com invernos rigorosos em algumas regiões.
            A Itália, conforme vemos abaixo, tem uma média de temperatura anual muito parecida com o RS - será por isso que temos uma grande presença de imigrantes italianos, e uma grande produção de vinhos na região do RS? Será que seria um bom país para oferecermos e aumentarmos a nossa presença, com vinhos de qualidade?
            Aqui, Hong Kong aparece também com muita semelhança com o clima do RS, tendo em vista que também possui clima subtropical, e a República Tcheca, que possui um clima temperado, com estações do ano bem definidas, mas um verão menos ameno, e invernos com uma constância de temperaturas abaixo de zero; Novamente, uma grande oportunidade pra apresentar vinhos mais quentes e secos!
            
        """,
        icon="ℹ️")

    st.plotly_chart(
    generate_graphs._metricas_noaa(get_data.DF_PRECP_COMPARATIVE(
                  df_clima_rs=get_data.DF_RS(years_to_filter)
                , df_noaa_global=get_data.DF_NOAA_GLOBAL()
                , stat='TAVG', thresold_filter = 6
            ),'TAVG')
    , use_container_width=True)

    st.divider() # ------------------------------------------------------
    col1, col2 = st.columns([1,3])
    with col1:
        st.plotly_chart(
        generate_graphs._density_clima_rs(
            df_full=get_data.DF_PRECP_COMPARATIVE(
                df_clima_rs=get_data.DF_RS(years_to_filter)
                , df_noaa_global=get_data.DF_NOAA_GLOBAL()
                , stat='TAVG'
            )
            , stat='TAVG'
            )
        , use_container_width=True)

    with col2:
        df_tavg = get_data.DF_PRECP_COMPARATIVE(
                  df_clima_rs=get_data.DF_RS(years_to_filter)
                , df_noaa_global=get_data.DF_NOAA_GLOBAL(years_to_filter)
                , stat='TAVG', thresold_filter = 6
            )
        
        st.plotly_chart(
        generate_graphs._density_noaa(df_tavg
            ,'TAVG')
        , use_container_width=True)

with tab_temp_min:
    
    st.write("""
            Chegando nas temperaturas mínimas, vemos países da América do sul, como Bolívia, Colômbia, Peru e Equador, dominando nas semelhanças; Muito embora, ao analisar as distribuições, Equador e Colômbia tem seus valores em faixas mais próximas de 0, uma faixa mais fácil de ser encontrada no RS. 
            Os demais países aparecem aqui, provavelmente, por suas temperaturas no decorrer dos anos terem mais se aproximado dos valores mínimos, na faixa entre 0 e 8ºC, mas não possuem uma distribuição tão parecida com o RS.
        """,
        icon="ℹ️")

    st.plotly_chart(
    generate_graphs._metricas_noaa(get_data.DF_PRECP_COMPARATIVE(
                  df_clima_rs=get_data.DF_RS(years_to_filter)
                , df_noaa_global=get_data.DF_NOAA_GLOBAL()
                , stat='TMIN', thresold_filter = 6
            ),'TMIN')
    , use_container_width=True)

    st.divider() # ------------------------------------------------------
    col1, col2 = st.columns([1,3])
    with col1:
        st.plotly_chart(
        generate_graphs._density_clima_rs(
            df_full=get_data.DF_PRECP_COMPARATIVE(
                df_clima_rs=get_data.DF_RS(years_to_filter)
                , df_noaa_global=get_data.DF_NOAA_GLOBAL()
                , stat='TMIN'
            )
            , stat='TMIN'
            )
        , use_container_width=True)

    with col2:
        df_tmin = get_data.DF_PRECP_COMPARATIVE(
                  df_clima_rs=get_data.DF_RS(years_to_filter)
                , df_noaa_global=get_data.DF_NOAA_GLOBAL(years_to_filter)
                , stat='TMIN', thresold_filter = 6
            )
        st.plotly_chart(
        generate_graphs._density_noaa(df_tmin
            ,'TMIN')
        , use_container_width=True)

with tab_temp_max:

    st.write("""
           Chegando nas máximas, vemos a Austrália, vizinha da Nova Zelândia, com uma distribuição (inclusive) muito semelhante ao RS;
           Novamente, Itália e Áustria aparecem com pontos semelhantes ao RS, e Reino Unido e Suécia aparecem pela primeira vez, com faixas de temperatura entre 20 e 40 graus, trazendo alguma semelhança com a media geral por perto de 29ºC do RS.
        """,
        icon="ℹ️")

    st.plotly_chart(
    generate_graphs._metricas_noaa(get_data.DF_PRECP_COMPARATIVE(
                  df_clima_rs=get_data.DF_RS(years_to_filter)
                , df_noaa_global=get_data.DF_NOAA_GLOBAL()
                , stat='TMAX', thresold_filter = 4
            ),'TMAX')
    , use_container_width=True)

    st.divider() # ------------------------------------------------------
    col1, col2 = st.columns([1,3])
    with col1:
        st.plotly_chart(
        generate_graphs._density_clima_rs(
            df_full=get_data.DF_PRECP_COMPARATIVE(
                df_clima_rs=get_data.DF_RS(years_to_filter)
                , df_noaa_global=get_data.DF_NOAA_GLOBAL()
                , stat='TMAX'
            )
            , stat='TMAX'
            )
        , use_container_width=True)

    with col2:
        df_tmax = get_data.DF_PRECP_COMPARATIVE(
                  df_clima_rs=get_data.DF_RS(years_to_filter)
                , df_noaa_global=get_data.DF_NOAA_GLOBAL(years_to_filter)
                , stat='TMAX', thresold_filter = 4
            )

        st.plotly_chart(
        generate_graphs._density_noaa(df_tmax
            ,'TMAX')
        , use_container_width=True)

with tab_consideracoes_finais:
    st.write(
        f"""
        Na nossa análise, os seguintes países apareceram em evidência:

        {", ".join(get_data.LISTA_PAISES(years_to_filter))}

        Iremos conduzir uma análise do cenário macroeconômico, tendo em vista realizar uma abertura de empresa, ou maior investimento nesses países.
        """)