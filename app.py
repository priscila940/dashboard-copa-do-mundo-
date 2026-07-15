import streamlit as st
import pandas as pd

# Configuração da página para tema escuro com o estilo da Copa
st.set_page_config(
    page_title="FIFA World Cup 2026",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilização CSS para deixar com as cores do print (Bordeaux / Vinho e Amarelo Creme)
st.markdown("""
    <style>
    .main {
        background-color: #800020; /* Fundo Vinho */
        color: #FDF5E6; /* Texto Creme */
    }
    div[data-testid="stMetricValue"] {
        font-size: 32px;
        color: #800020;
        font-weight: bold;
    }
    div[data-testid="stMetricLabel"] {
        color: #4A0E17;
        font-weight: bold;
    }
    /* Estilo dos blocos arredondados */
    .card {
        background-color: #FDF5E6;
        padding: 20px;
        border-radius: 20px;
        color: #333333;
        margin-bottom: 20px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
        text-align: center;
    }
    .card h3 {
        color: #800020;
        margin-bottom: 5px;
    }
    .player-img {
        border-radius: 10px;
        max-height: 150px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Links dos dados do seu GitHub (lembre de manter os arquivos atualizados lá!)
url_partidas = "https://raw.githubusercontent.com/priscila940/dashboard-copa-do-mundo-/main/data/raw/matches.csv"
url_jogadores = "https://raw.githubusercontent.com/priscila940/dashboard-copa-do-mundo-/main/data/raw/players.csv"
url_gols = "https://raw.githubusercontent.com/priscila940/dashboard-copa-do-mundo-/main/data/raw/goals.csv"

# Carregando as tabelas
try:
    df_matches = pd.read_csv(url_partidas)
    df_players = pd.read_csv(url_jogadores)
    df_goals = pd.read_csv(url_gols)
    
    # Cruzando gols com jogadores para saber quem marcou
    df_gols_detalhado = df_goals.merge(df_players, on="id_jogador", how="left")
    artilheiros = df_gols_detalhado.groupby("nome_jogador").size().reset_index(name="gols").sort_values(by="gols", ascending=False)
except Exception as e:
    st.error("Erro ao ler os arquivos do GitHub. Verifique se os nomes dos arquivos estão corretos.")
    st.stop()

# --- TOPO DO DASHBOARD ---
st.title("🏆 FIFA WORLD CUP 2026")
st.write("Acompanhe as estatísticas da Copa em tempo real!")
st.markdown("---")

# Métricas do Topo
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="card"><h3>Players</h3><h2>{len(df_players)}</h2></div>', unsafe_allow_html=True)
with col2:
    total_gols = len(df_goals)
    st.markdown(f'<div class="card"><h3>Total Goals</h3><h2>{total_gols}</h2></div>', unsafe_allow_html=True)
with col3:
    media_gols = total_gols / len(df_matches) if len(df_matches) > 0 else 0
    st.markdown(f'<div class="card"><h3>Average Goals</h3><h2>{media_gols:.2f}</h2></div>', unsafe_allow_html=True)

st.markdown("---")

# --- CONTEÚDO PRINCIPAL ---
col_esquerda, col_meio, col_direita = st.columns([1, 1, 1.5])

# Coluna 1: Melhores do Torneio
with col_esquerda:
    st.markdown("### 🌟 Destaques")
    
    # Card do Melhor Jogador (Exemplo Messi / Pode ser dinâmico depois)
    st.markdown("""
        <div class="card">
            <h3>Best Player</h3>
            <img class="player-img" src="https://assets.gqindia.com/photos/639c0906cc94589311029fe0/1:1/w_1080,h_1080,c_limit/Lionel-Messi.jpg">
            <h4>Lionel Messi</h4>
            <p>Argentina 🇦🇷</p>
        </div>
    """, unsafe_allow_html=True)

    # Card do Artilheiro
    top_scorer = artilheiros.iloc[0]['nome_jogador'] if len(artilheiros) > 0 else "Nenhum"
    gols_scorer = artilheiros.iloc[0]['gols'] if len(artilheiros) > 0 else 0
    st.markdown(f"""
        <div class="card">
            <h3>Top Scorer</h3>
            <img class="player-img" src="https://img.olympics.com/images/image/private/t_1:1_600/f_auto/primary/vgc73t97v60gluqshfsh">
            <h4>{top_scorer}</h4>
            <h2>{gols_scorer} Gols</h2>
        </div>
    """, unsafe_allow_html=True)

# Coluna 2: Tabela de Artilharia Dinâmica (Atualiza com o CSV de Gols)
with col_meio:
    st.markdown("### ⚽ Goals")
    if len(artilheiros) > 0:
        # Criando uma tabela bonita para mostrar os maiores goleadores
        st.dataframe(
            artilheiros.rename(columns={"nome_jogador": "Player", "gols": "Goals"}),
            hide_index=True,
            use_container_width=True
        )
    else:
        st.write("Nenhum gol marcado ainda.")

# Coluna 3: Partidas Recentes e Resultados
with col_direita:
    st.markdown("### 📅 Recent Matches")
    for index, row in df_matches.iterrows():
        st.markdown(f"""
            <div class="card" style="text-align: left; padding: 15px; margin-bottom: 10px;">
                <p style="font-size: 12px; color: gray; margin: 0;">{row['fase']} - {row['data']}</p>
                <h4 style="margin: 5px 0;">{row['mandante']} <b>{row['gols_mandante']}</b> x <b>{row['gols_visitante']}</b> {row['visitante']}</h4>
                <p style="font-size: 12px; color: #800020; margin: 0;">Estádio: {row['estadio']}</p>
            </div>
        """, unsafe_allow_html=True)
