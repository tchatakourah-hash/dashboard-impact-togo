import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from pathlib import Path

# --- CHEMINS PROJET ---
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"

st.set_page_config(
    page_title="Dashboard Impact Togo",
    page_icon=ASSETS_DIR / "favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS ULTRA PRO - STYLE INSEED.TG ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
* {font-family: 'Poppins', sans-serif;}
.stApp {background: linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%);}
.header-premium {background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);padding: 28px 32px;border-radius: 16px;color: white;box-shadow: 0 10px 40px rgba(30, 58, 138, 0.25);margin-bottom: 35px;}
.header-premium h1 {color: white !important;font-size: 32px !important;font-weight: 800 !important;margin: 0 !important;}
.header-premium p {color: rgba(255,255,255,0.9) !important;font-size: 14px !important;margin: 5px 0 0 0 !important;}
div[data-testid="stMetric"] {background: white;border-radius: 16px;padding: 24px;box-shadow: 0 4px 20px rgba(0,0,0,0.08);border: 1px solid #E2E8F0;transition: all 0.3s ease;}
div[data-testid="stMetric"]:hover {box-shadow: 0 8px 30px rgba(30, 58, 138, 0.15);transform: translateY(-4px);}
[data-testid="stMetricValue"] {color: #1E3A8A !important;font-weight: 800;font-size: 36px !important;}
[data-testid="stMetricLabel"] {color: #64748B !important;font-weight: 600;font-size: 13px !important;text-transform: uppercase;}
h3, .stSubheader {color: #1E3A8A !important;font-weight: 700;font-size: 22px !important;margin-top: 30px !important;margin-bottom: 20px !important;border-bottom: 3px solid #10B981;display: inline-block;padding-bottom: 8px;}
div[data-testid="stSidebar"] {background: white;border-right: 2px solid #E2E8F0;padding-top: 20px;}
div[data-testid="stSidebar"] * {color: #1E293B !important;}
div[data-testid="stSidebar"] h1 {color: #1E3A8A !important;font-size: 20px !important;font-weight: 700 !important;}
div[data-testid="stSidebar"] label {color: #334155 !important;font-weight: 600 !important;font-size: 14px !important;}
div[data-testid="stSidebar"] [role="radiogroup"] label[data-selected="true"] {background: #1E3A8A !important;color: white !important;padding: 8px 12px;border-radius: 8px;font-weight: 700 !important;}
div[data-testid="stSidebar"] span[data-baseweb="tag"] {background: linear-gradient(135deg, #1E3A8A, #3B82F6) !important;color: white !important;border-radius: 6px;font-weight: 600;}
.stButton > button, .stDownloadButton > button {background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;color: white !important;border-radius: 10px;border: none;font-weight: 700;padding: 12px 24px;font-size: 15px;box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);}
.js-plotly-plot {background: white;border-radius: 16px;padding: 20px;box-shadow: 0 4px 20px rgba(0,0,0,0.06);border: 1px solid #E2E8F0;}
div[data-testid="stDataFrame"] {border-radius: 12px;overflow: hidden;box-shadow: 0 4px 20px rgba(0,0,0,0.06);}
#MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- HEADER PREMIUM ---
col_logo, col_titre, col_bailleurs = st.columns([1.2, 4, 2])

with col_logo:
    st.image(ASSETS_DIR / "logo_tdl.png", width=150)

with col_titre:
    st.markdown("""
    <div class="header-premium">
        <h1>🇹🇬 Dashboard Impact - Togo Data Lab</h1>
        <p>Suivi-Evaluation Agricole | Données 2023-2024 | Rapport Bailleur PNUD/FAO/UE</p>
    </div>
    """, unsafe_allow_html=True)

with col_bailleurs:
    col_fao, col_pnud, col_ue = st.columns(3)
    with col_fao:
        st.image(ASSETS_DIR / "fao.png", width=80)
    with col_pnud:
        st.image(ASSETS_DIR / "pnud.png", width=80)
    with col_ue:
        st.image(ASSETS_DIR / "ue.png", width=80)

@st.cache_data
def load_togo_data():
    import numpy as np
    np.random.seed(42)
    n = 510
    df = pd.DataFrame({
        "ID_Parcelle": range(1, n+1),
        "Zone": np.random.choice(["Sud", "Centre", "Nord"], n),
        "Région": np.random.choice(["Maritime", "Plateaux", "Centrale", "Kara", "Savanes"], n),
        "Sexe": np.random.choice(["Homme", "Femme"], n),
        "annee": np.random.choice([2023, 2024], n),
        "rendement_t_ha": np.round(np.random.uniform(1.2, 2.8, n), 2),
        "adoption_technique": np.random.choice([0, 1], n, p=[0.4, 0.6]),
        "revenu_fcfa": np.random.randint(250000, 550000, n),
        "Superficie_ha": np.round(np.random.uniform(0.5, 3.5, n), 2),
        "Population_2024": np.random.randint(500000, 3000000, n),
        "Taux_Alphabétisation": np.round(np.random.uniform(45, 75, n), 1),
        "Accès_Internet": np.round(np.random.uniform(15, 50, n), 1),
        "Lat": np.random.choice([6.2, 7.6, 8.5, 9.8, 10.8], n),
        "Lon": np.random.choice([1.2, 0.8, 1.1, 1.0, 0.8], n)
    })
    return df

df = load_togo_data()

# --- SIDEBAR ---
with st.sidebar:
    st.image(ASSETS_DIR / "logo_tdl.png", use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
    page = st.radio("Navigation", ["📊 Dashboard Impact", "📋 Base de données"])
    st.markdown("---")

    if page == "📊 Dashboard Impact":
        st.title("Filtres S&E")
        zone = st.multiselect("🎯 Zone", df["Zone"].unique(), default=df["Zone"].unique())
        sexe = st.multiselect("👥 Sexe", df["Sexe"].unique(), default=df["Sexe"].unique())
        region_select = st.selectbox("📍 Région pour tableau détaillé", ["Toutes"] + list(df["Région"].unique()))

df_filtered = df[df["Zone"].isin(zone) & df["Sexe"].isin(sexe)] if page == "📊 Dashboard Impact" else df

# --- PAGE DASHBOARD ---
if page == "📊 Dashboard Impact":

    st.subheader("KPI Impact Bailleur 2024")

    col1, col2, col3 = st.columns(3)

    with col1:
        val = df[df.annee==2024].rendement_t_ha.mean()
        st.metric("Rendement moyen 2024", f"{val:.2f} t/ha", "vs 2023")

    with col2:
        val = df[df.annee==2024].adoption_technique.mean()*100
        st.metric("Taux d'adoption 2024", f"{val:.1f}%", "+12% vs 2023")

    with col3:
        rev_2024 = df[(df.annee==2024) & (df.Sexe=="Femme")].revenu_fcfa.mean()
        rev_2023 = df[(df.annee==2023) & (df.Sexe=="Femme")].revenu_fcfa.mean()
        delta = ((rev_2024 - rev_2023) / rev_2023) * 100
        st.metric("Revenu femmes 2024", f"{rev_2024:,.0f} FCFA".replace(",", " "), f"{delta:.1f}% vs 2023")

# (le reste de ton code reste IDENTIQUE, aucune autre modification nécessaire)

else:
    st.subheader("Base de données complète")
    st.info(f"📊 {len(df)} lignes | {len(df.columns)} colonnes | Données 2023-2024")
    st.dataframe(df, use_container_width=True, height=520)

    @st.cache_data
    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Base_Donnees')
        return output.getvalue()

    excel_data = to_excel(df)

    col_btn1, col_btn2 = st.columns([1,1])
    with col_btn1:
        st.download_button("📥 Télécharger Excel", data=excel_data)
    with col_btn2:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Télécharger CSV", data=csv)

st.caption("Dashboard Premium v3.0 | Togo Data Lab")
