import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página para ficar bonita e responsiva
st.set_page_config(page_title="Dashboard Copa do Mundo", page_icon="🏆", layout="wide")

# Título do Painel
st.title("🏆 Estatísticas Históricas da Copa do Mundo")
st.markdown("---")

# Link para o seu arquivo matches.csv direto do seu GitHub
# (O Streamlit lê o arquivo diretamente daqui!)
url_dados = "https://raw.githubusercontent.com/priscila940/dashboard-copa-do-mundo-/main/data/raw/matches.csv"

try:
    df = pd.read_csv(url_dados)
    
    # 1. Indicadores rápidos (Cards)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Partidas Registradas", len(df))
    with col2:
        total_gols = df['gols_mandante'].sum() + df['gols_visitante'].sum()
        st.metric("Total de Gols", int(total_gols))
    with col3:
        media_gols = total_gols / len(df)
        st.metric("Média de Gols por Jogo", f"{media_gols:.2f}")
        
    st.markdown("---")
    
    # 2. Gráfico Interativo usando Plotly
    st.subheader("📊 Gols por Partida (Visualização por Ano)")
    df['total_gols_jogo'] = df['gols_mandante'] + df['gols_visitante']
    
    fig = px.bar(
        df, 
        x="id_partida", 
        y="total_gols_jogo", 
        color="fase",
        hover_data=["mandante", "visitante"],
        labels={"total_gols_jogo": "Gols no Jogo", "id_partida": "ID do Jogo"},
        title="Gols Marcados em cada Partida Cadastrada"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 3. Tabela de Dados Interativa
    st.subheader("🔍 Detalhes de Todos os Jogos")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error("Erro ao carregar os dados do GitHub. Verifique o link do arquivo matches.csv.")
