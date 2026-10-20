import streamlit as st
import pandas as pd
import plotly.express as px
 
st.set_page_config(
    page_title="Dashboard de Dados",
    layout="wide"
)
 
st.title("⚡ Dashboard de Energia Vertida Turbinável")
 
with st.container(border=True):
        st.markdown("### O que podemos observar?")
        st.write("""
        Este dashboard apresenta uma análise dos dados de geração deenergia hidrelétrica no Brasil, utilizando informações sobrereservatórios, empresas responsáveis pela geração e subsistemasde energia.O objetivo é compreender como a geração de energia estádistribuída entre os reservatórios e as empresas, identificarquais apresentam maior geração e produtividade e facilitara interpretação dos dados por meio de indicadores e gráficos.
    """)
 
st.divider()
 
st.markdown("""
<style>
 
.stApp {
    background-color: #0e1117;
}
 
h1,h2,h3 {
    color: #f700ff54 !important;
}
 
[data-testid="stMetric"] {
    background: #1c1f26;
    border: 1px solid #f700ff54;
    border-radius: 30px;
    padding: 20px;
    box-shadow: 0 0 15px rgba(247, 0, 255, 0.5);
}
 
</style>
""", unsafe_allow_html=True)
 
arquivo = st.file_uploader(
    "Envie um arquivo CSV",
    type=["csv"]
)
if arquivo is not None:
    df = pd.read_csv(
    arquivo,
    sep=";",
    encoding="utf-8"
)
 
    #___________________________________________________
    #COLUNAS
    #___________________________________________________
    df["din_instante"] = pd.to_datetime(
        df["din_instante"],
        errors="coerce"
    )
 
    # =====================================
    # FILTROS
    # =====================================
 
    st.sidebar.title("⚙️ Filtros")
 
    empresa = st.sidebar.selectbox(
        "🏢 Empresa",
        ["Todas"] + sorted(list(df["nom_agente"].unique()))
    )
 
    subsistema = st.sidebar.selectbox(
        "⚡ Subsistema",
        ["Todos"] + sorted(list(df["nom_subsistema"].unique()))
    )
 
    if empresa != "Todas":
        df = df[df["nom_agente"] == empresa]
 
    if subsistema != "Todos":
        df = df[df["nom_subsistema"] == subsistema]
 
 
    col1, col2, col3, col4, col5, col6 = st.columns(6)
 
    col1.metric(
        "Geração Média",
        round(df["val_geracao"].mean(), 2)
    )
 
    col2.metric(
        "Maior Geração",
        round(df["val_geracao"].max(), 2)
    )
 
    col3.metric(
        "Menor Geração",
        round(df["val_geracao"].min(), 2)
    )
 
    col4.metric(
        "Quantidade de Usinas",
        df["nom_reservatorio"].nunique()
    )
 
    col5.metric(
        "Quantidade de Empresas",
        df["nom_agente"].nunique()
    )
 
    col6.metric(
        "Subsistemas",
        df["nom_subsistema"].nunique()
    )
 
    st.subheader(" Verificação de Qualidade")
    #____________________________________________________
    #COLUNAS DE VERIFICAÇÃO DE QUALIDADE
    #____________________________________________________
 
    col1, col2 = st.columns(2)
 
    nulos = pd.DataFrame({
        "Coluna": df.columns,
        "Valores Nulos": df.isnull().sum().values
    })
 
    tipos = pd.DataFrame({
            "Coluna": df.columns,
            "Tipo": df.dtypes.astype(str).values
    })
 
    with col1:
        st.markdown("### Valores Nulos")
        st.dataframe(
            nulos,
            use_container_width=True,
            hide_index=True
    )
 
    with col2:
        st.markdown("### Tipos das Colunas")
        st.dataframe(
            tipos,
            use_container_width=True,
            hide_index=True
    )
 
    #_____________________________________________________
    #GRAFICOS
    #_____________________________________________________
 
    st.subheader("Geração Total por Subsistema")
 
    geracao_reservatorio = (
        df.groupby("nom_reservatorio", as_index=False)["val_geracao"]
      .sum()
      .sort_values("val_geracao", ascending=False)
      .head(10)
    )
 
    fig_reservatorio = px.bar(
        geracao_reservatorio,
        x="nom_reservatorio",
        y="val_geracao",
        color="val_geracao",
        color_continuous_scale="Electric",
        title="⚡ Top 10 Reservatórios por Geração"
    )
 
    fig_reservatorio.update_layout(
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font_color="white"
    )
 
    produtividade_empresa = (
        df.groupby("nom_agente", as_index=False)["val_produtividade"]
      .mean()
      .sort_values("val_produtividade", ascending=False)
    )
 
    fig_produtividade = px.bar(
        produtividade_empresa.head(10),
        x="val_produtividade",
        y="nom_agente",
        orientation="h",
        color="val_produtividade",
        color_continuous_scale="Electric",
        title="⚡ Top 10 Empresas por Produtividade Média"
    )
 
    fig_produtividade.update_layout(
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font_color="white"
    )
   
    col1, col2 = st.columns(2)
 
    #_______________________________________________
    #TEXTO
    #_______________________________________________
 
    with col1:
        st.plotly_chart(fig_reservatorio, use_container_width=True)
    st.info("""
    **O que podemos observar?**
 
    O gráfico 1 apresenta a geração de energia dos 10 maiores reservatórios, mostrando que Itaipu se destaca com uma produção superior a 4 milhões, muito acima dos demais, que geram entre 400 mil e 800 mil. Essa diferença mostra que Itaipu ocupa uma posição de destaque na geração de energia em comparação aos outros reservatórios analisados.
    """)
 
    with col2:
        st.plotly_chart(fig_produtividade, use_container_width=True)
    st.info("""
    **O que podemos observar?**
 
    O gráfico 2 apresenta a produtividade média das empresas, destacando a EMAE, que apresenta um resultado cerca de duas vezes maior que o da segunda colocada. As demais empresas possuem níveis de produtividade mais próximos entre si, indicando que a EMAE se diferencia das outras empresas nesse indicador.
    """)
 
    with st.container(border=True):
        st.markdown("### O que podemos observar?")
        st.write("""
        O que precisávamos resolver?
        Correções de problemas
 
        Qual pergunta fizemos para a IA?
        O porque estava errado
 
        O que ela sugeriu?
        correção no código
 
        A sugestão funcionou?
        Sim
 
        Foi necessário modificar alguma coisa?
        Em alguns momentos sim
 
        Como verificamos se estava correta?
        Rodando o código
        """)
 
    st.markdown("""
    Feito por: Ana Vitoria, Daniela Parrillo, Paola Silvestre, Paula Alvez, Thais Santos 2CDD01
    """)