import streamlit as st
import pandas as pd

# Configuração da página profissional
st.set_page_config(
    page_title="FIFA World Cup Dashboard",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS PESADO PARA RECRIAÇÃO DO DESIGN (Estilo FIFA) ---
st.markdown("""
    <style>
    /* Remover margens padrão do Streamlit para controle total */
    [data-testid="stHeader"] {display: none;}
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
        background-color: #7A0A26 !important; /* Cor Vinho Oficial da FIFA */
    }
    
    /* Corpo principal do app */
    .main {
        background-color: #7A0A26;
    }
    
    /* Estilo dos Containers (Cantos super arredondados e borda amarela creme) */
    .fifa-card {
        background-color: #FDF5E6 !important; /* Creme */
        border: 2px solid #D4B270; /* Borda Dourada/Creme */
        border-radius: 28px !important;
        padding: 20px !important;
        color: #4A0E17 !important; /* Vinho Escuro para os textos */
        font-family: 'Arial', sans-serif;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
        margin-bottom: 15px;
    }
    
    /* Títulos dentro dos cards */
    .fifa-card h3 {
        color: #7A0A26 !important;
        font-weight: 800;
        text-align: center;
        margin-top: 0;
        font-size: 1.3rem;
        border-bottom: 2px solid #E6D8B8;
        padding-bottom: 8px;
    }
    
    /* Subtítulos */
    .fifa-card h4 {
        color: #4A0E17 !important;
        text-align: center;
        font-weight: 700;
        margin: 5px 0;
    }

    /* Cards de estatísticas superiores */
    .top-stat {
        background-color: #FDF5E6;
        border: 2px solid #D4B270;
        border-radius: 15px;
        padding: 10px;
        text-align: center;
        color: #4A0E17;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }
    .top-stat h2 {
        margin: 0;
        font-size: 2rem;
        font-weight: bold;
        color: #222;
    }
    .top-stat p {
        margin: 0;
        font-size: 0.9rem;
        color: #7A0A26;
        font-weight: bold;
    }

    /* Tabelas personalizadas no estilo do print */
    .fifa-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
    }
    .fifa-table th {
        color: #888;
        font-size: 0.8rem;
        text-align: left;
        padding-bottom: 8px;
        border-bottom: 1px solid #E6D8B8;
    }
    .fifa-table td {
        padding: 8px 0;
        font-size: 0.9rem;
        border-bottom: 1px dotted #E6D8B8;
        color: #333;
    }
    .fifa-table tr:last-child td {
        border-bottom: none;
    }
    
    /* Imagens arredondadas de jogadores */
    .player-profile-pic {
        display: block;
        margin-left: auto;
        margin-right: auto;
        border-radius: 50%;
        width: 120px;
        height: 120px;
        object-fit: cover;
        border: 3px solid #7A0A26;
        margin-bottom: 10px;
    }
    
    /* Bandeiras dos Países */
    .flag {
        width: 20px;
        height: 14px;
        display: inline-block;
        vertical-align: middle;
        margin-right: 5px;
        border-radius: 2px;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# --- LINKS DE DADOS RAW DO SEU GITHUB ---
url_partidas = "https://raw.githubusercontent.com/priscila940/dashboard-copa-do-mundo-/main/data/raw/matches.csv"
url_jogadores = "https://raw.githubusercontent.com/priscila940/dashboard-copa-do-mundo-/main/data/raw/players.csv"
url_gols = "https://raw.githubusercontent.com/priscila940/dashboard-copa-do-mundo-/main/data/raw/goals.csv"

# Tratamento dos dados silencioso (para alimentar as tabelas)
try:
    df_matches = pd.read_csv(url_partidas)
    df_players = pd.read_csv(url_jogadores)
    df_goals = pd.read_csv(url_gols)
    df_gols_detalhado = df_goals.merge(df_players, on="id_jogador", how="left")
    artilheiros = df_gols_detalhado.groupby(["nome_jogador", "selecao"]).size().reset_index(name="gols").sort_values(by="gols", ascending=False)
except Exception as e:
    st.error("Erro na leitura das planilhas do GitHub.")
    st.stop()

# --- ESTRUTURA DE COLUNAS IDÊNTICA AO PRINT ---

# Linha 1: Logo da FIFA (Esquerda) e Cards de Stats (Direita)
col_logo, col_stat1, col_stat2, col_select = st.columns([2, 1.5, 1.5, 1.5])

with col_logo:
    # Logo oficial da Copa de 2026 (ou placeholder bonito)
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/4b/2026_FIFA_World_Cup_Logo.svg", width=120)

with col_stat1:
    st.markdown("""
        <div class="top-stat">
            <p>👥 Players</p>
            <h2>680</h2>
        </div>
    """, unsafe_allow_html=True)

with col_stat2:
    st.markdown("""
        <div class="top-stat">
            <p>📅 Average Age</p>
            <h2>27</h2>
        </div>
    """, unsafe_allow_html=True)

with col_select:
    # Dropdown no mesmo estilo do filtro superior direito
    st.selectbox("Filtrar Seleção", ["Todos", "Brasil", "Argentina", "França", "Croácia"], label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

# Linha 2: Os 3 Blocos de Conteúdo Principais
col_best, col_positions, col_tables = st.columns([1.2, 1.2, 2.5])

# --- COLUNA 1: BEST PLAYER & BEST GOALKEEPER ---
with col_best:
    st.markdown("""
        <div class="fifa-card">
            <h3>Best Player</h3>
            <img class="player-profile-pic" src="https://assets.gqindia.com/photos/639c0906cc94589311029fe0/1:1/w_1080,h_1080,c_limit/Lionel-Messi.jpg">
            <h4>Lionel Messi</h4>
            <p style="text-align:center; margin:0;"><img class="flag" src="https://flagcdn.com/w40/ar.png"> Argentina</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="fifa-card">
            <h3>Best Goalkeeper</h3>
            <img class="player-profile-pic" src="https://tmssl.akamaized.net/images/foto/galerie/emiliano-martinez-argentina-2022-1671391581-99221.jpg">
            <h4>E. Martínez</h4>
            <p style="text-align:center; margin:0;"><img class="flag" src="https://flagcdn.com/w40/ar.png"> Argentina</p>
        </div>
    """, unsafe_allow_html=True)

# --- COLUNA 2: POSITIONS & TOP SCORER ---
with col_positions:
    st.markdown("""
        <div class="fifa-card">
            <h3>Positions</h3>
            <table class="fifa-table">
                <tr><th>Position</th><th style="text-align:right;">Players</th></tr>
                <tr><td>DF (Defensores)</td><td style="text-align:right; font-weight:bold;">228</td></tr>
                <tr><td>MF (Meio-Campo)</td><td style="text-align:right; font-weight:bold;">226</td></tr>
                <tr><td>FW (Atacantes)</td><td style="text-align:right; font-weight:bold;">185</td></tr>
                <tr><td>GK (Goleiros)</td><td style="text-align:right; font-weight:bold;">41</td></tr>
            </table>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="fifa-card">
            <h3>Top Scorer</h3>
            <img class="player-profile-pic" src="https://img.olympics.com/images/image/private/t_1:1_600/f_auto/primary/vgc73t97v60gluqshfsh">
            <h4>Kylian Mbappé</h4>
            <p style="text-align:center; margin:0;"><img class="flag" src="https://flagcdn.com/w40/fr.png"> França</p>
        </div>
    """, unsafe_allow_html=True)

# --- COLUNA 3: TABELAS LATERAIS (GOLS & JOGADORES) ---
with col_tables:
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        # Tabela dinâmica de Artilharia com bandeiras dinâmicas (exemplo mapeado)
        # Mapeamento simples de bandeiras para as seleções do seu CSV
        bandeiras = {"Brasil": "br", "Argentina": "ar", "Franca": "fr", "Croacia": "hr", "Inglaterra": "gb"}
        
        tabela_gols_html = """
        <div class="fifa-card" style="height: 100%;">
            <h3>Goals</h3>
            <table class="fifa-table">
                <tr><th>Player</th><th>Flag</th><th style="text-align:right;">Goals</th></tr>
        """
        for _, row in artilheiros.iterrows():
            sigla = bandeiras.get(row['selecao'], "un")
            tabela_gols_html += f"""
                <tr>
                    <td>{row['nome_jogador']}</td>
                    <td><img class="flag" src="https://flagcdn.com/w40/{sigla}.png"></td>
                    <td style="text-align:right; font-weight:bold;">{row['gols']}</td>
                </tr>
            """
        tabela_gols_html += "</table></div>"
        st.markdown(tabela_gols_html, unsafe_allow_html=True)
        
    with col_t2:
        # Tabela lateral de listagem de jogadores por idade (simulando a do print)
        st.markdown("""
            <div class="fifa-card" style="height: 100%;">
                <h3>Players by Age</h3>
                <table class="fifa-table">
                    <tr><th>Player</th><th>Flag</th><th style="text-align:right;">Age</th></tr>
                    <tr><td>Neymar Jr</td><td><img class="flag" src="https://flagcdn.com/w40/br.png"></td><td style="text-align:right; font-weight:bold;">34</td></tr>
                    <tr><td>Lionel Messi</td><td><img class="flag" src="https://flagcdn.com/w40/ar.png"></td><td style="text-align:right; font-weight:bold;">39</td></tr>
                    <tr><td>Kylian Mbappé</td><td><img class="flag" src="https://flagcdn.com/w40/fr.png"></td><td style="text-align:right; font-weight:bold;">27</td></tr>
                    <tr><td>Luka Modrić</td><td><img class="flag" src="https://flagcdn.com/w40/hr.png"></td><td style="text-align:right; font-weight:bold;">40</td></tr>
                </table>
            </div>
        """, unsafe_allow_html=True)
