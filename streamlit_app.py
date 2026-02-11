import streamlit as st
import os
import urllib.parse

# --- 1. CONFIGURAÇÃO & TEMA PREMIUM GOLDEN ---
try:
    st.set_page_config(page_title="Zion Atelier", page_icon="🗽", layout="centered")
except:
    pass

# CSS TOTAL GOLD: Forçando tudo para Dourado e Fundo Preto
st.markdown("""
    <style>
    /* Fundo Total Preto */
    .stApp { background-color: #000000; }
    
    /* Forçando todos os textos para Dourado Zion */
    h1, h2, h3, p, span, label, .stMarkdown, .stSelectbox label, .stNumberInput label, .stTextInput label { 
        color: #d4af37 !important; 
        font-weight: 500;
    }
    
    /* Valores das Métricas (Números do Investimento) */
    div[data-testid="stMetricValue"] { color: #d4af37 !important; font-weight: bold; }
    div[data-testid="stMetricLabel"] { color: #ffffff !important; } /* Rótulo em branco para contraste */
    
    /* Container das Métricas */
    div[data-testid="metric-container"] { 
        background-color: #111111; 
        border: 2px solid #d4af37; 
        padding: 15px; 
        border-radius: 12px; 
    }

    /* Campos de Input (Caixas de texto e seleção) */
    input, select, textarea {
        background-color: #1a1a1a !important;
        color: #d4af37 !important;
        border: 1px solid #d4af37 !important;
    }

    /* Botão Principal */
    .stButton>button { 
        background-color: #d4af37 !important; 
        color: #000000 !important; 
        font-weight: bold !important; 
        border-radius: 10px; 
        border: none;
        width: 100%;
        height: 50px;
    }

    /* Estilo do link do WhatsApp dentro do botão */
    .wa-button {
        text-decoration: none; 
        color: #000000 !important; 
        background-color: #d4af37; 
        padding: 12px; 
        border-radius: 10px; 
        font-weight: bold; 
        display: block; 
        text-align: center;
        border: 1px solid #d4af37;
    }
    
    /* Divisores Dourados */
    hr { border-top: 1px solid #d4af37 !important; }

    /* Estilo das tabelas de sugestão */
    table { color: #d4af37 !important; border: 1px solid #d4af37; }
    th { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

SENHA_BOSS = "zion2026"

# --- 2. LOGO ---
nome_logo = "Logo Zion Atelier com fundo tranp 68%.png"
if os.path.exists(nome_logo):
   st.image(nome_logo, width=150)

# --- 3. DADOS DO PROJETO ---
st.write("### 📝 Solicitação de Orçamento")
nome_cliente = st.text_input("Nome do Cliente", placeholder="Ex: John Doe")
nome_arte = st.text_input("Nome da Arte", placeholder="Ex: Lion Pride")

arquivo_arte = st.file_uploader("Upload da Arte", type=["png", "jpg", "jpeg", "webp"], key=f"up_{nome_cliente}")

# --- 4. GUIA DE ESTILO ZION ---
if arquivo_arte is not None:
    st.image(arquivo_arte, use_container_width=True)
    with st.expander("💡 Dica do Artista: Melhores Combinações"):
        st.write("""
        | Se você busca... | Sugestão de Camisa | Sugestão de Vinil |
        | :--- | :--- | :--- |
        | **Estilo Streetwear** | Sand ou Black | Puff (Relevo) |
        | **Destaque Noturno** | Navy ou Graphite | Glow in the Dark |
        | **Visual Luxo** | Forest Green | Metallic Gold |
        """)

st.divider()

# --- 5. DATABASE ---
vinis_db = {
    "EasyWeed HTV (Siser)": {"GPI Supplies": {"price": 34.99, "width": 12}, "Heat Transfer Whse": {"price": 37.99, "width": 12}},
    "Puff Vinyl": {"GPI Supplies": {"price": 42.00, "width": 12}, "Heat Transfer Whse": {"price": 42.00, "width": 12}},
    "Metallic": {"GPI Supplies": {"price": 30.99, "width": 12}, "Heat Transfer Whse": {"price": 34.99, "width": 12}},
    "Holographic": {"GPI Supplies": {"price": 48.00, "width": 12}, "Heat Transfer Whse": {"price": 50.00, "width": 20}},
    "Brick 600 (Thick)": {"GPI Supplies": {"price": 62.99, "width": 20}, "Heat Transfer Whse": {"price": 39.99, "width": 12}},
    "Gliter (Thick)": {"GPI Supplies": {"price": 37.99, "width": 12}},
    "Aurora (Thick)": {"GPI Supplies": {"price": 28.49, "width": 12}},
    "Easy Glow Brilha no escuro": {"Heat Transfer Whse": {"price": 62.99, "width": 12}},
    "StripFlock Pro (Thick)": {"GPI Supplies": {"price": 35.99, "width": 12}},
    "Easy Glow Cores": {"Heat Transfer Whse": {"price": 52.99, "width": 12}}
}

produtos_db = {
    "CAMISAS": {
        "Gildan G500 Unisex": {"price": 2.82, "markup": 3.0},
        "Feminina G500VL V-Neck": {"price": 6.37, "markup": 3.5},
        "Feminina G500L Crewneck": {"price": 4.91, "markup": 3.2},
        "Kids G510P Heavy Cotton": {"price": 3.93, "markup": 3.0},
        "G500B Juvenil": {"price": 2.96, "markup": 3.0}
    },
    "MOLETONS": {"Gildan G185 Hoodie": {"price": 13.77, "markup": 2.5}},
    "BONÉS": {"Snapback Classic": {"price": 5.50, "markup": 4.0}, "Trucker Hat": {"price": 4.20, "markup": 4.0}}
}

# --- 6. SELEÇÃO ---
st.write("### 🛍️ Configure seu Item")
cat_sel = st.selectbox("Categoria", list(produtos_db.keys()))
prod_nome = st.selectbox("Modelo", list(produtos_db[cat_sel].keys()))
qtd = st.number_input("Quantidade", min_value=1, value=1)

c_base = produtos_db[cat_sel][prod_nome]["price"]
mk_base = produtos_db[cat_sel][prod_nome]["markup"]

st.divider()

# --- 7. CAMADAS ---
st.write("### 📏 Personalização")
custo_v = 0.0

def configurar_camada(n):
    st.markdown(f"**Camada {n}**")
    tipo = st.selectbox(f"Tipo de Vinil (C{n})", list(vinis_db.keys()), key=f"tipo{n}")
    forn =
