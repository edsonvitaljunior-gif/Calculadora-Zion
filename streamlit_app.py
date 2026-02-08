import streamlit as st
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
nome_logo = "Logo Zion Atelier com fundo tranp 68%.png"
fav_icon = nome_logo if os.path.exists(nome_logo) else "🗽"

st.set_page_config(
    page_title="Zion Atelier - Pro Manager", 
    page_icon=fav_icon,
    layout="centered"
)

# --- EXIBIÇÃO DA LOGO NO TOPO ---
if os.path.exists(nome_logo):
    st.image(nome_logo, width=150)
else:
    st.title("🗽 Zion Atelier")

# --- 📋 1. IDENTIFICAÇÃO DO PROJETO ---
st.write("### 📝 Dados do Orçamento")
col_cli, col_art = st.columns(2)
with col_cli:
    nome_cliente = st.text_input("Nome do Cliente", placeholder="Ex: John Doe")
with col_art:
    nome_arte = st.text_input("Nome da Arte / Projeto", placeholder="Ex: NY Faith 2026")

# Campo de Upload com suporte expandido para tipos de imagem
arquivo_arte = st.file_uploader("Upload da Arte (Opcional)", type=["png", "jpg", "jpeg", "webp"])

st.divider()

# --- 📦 DATABASE DE VINIS (Preços atualizados com 20% de perda) ---
vinis_db = {
    "EasyWeed (Siser)": {"GPI Supplies": {"price": 34.99, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 37.99, "width": 12, "yards": 5}},
    "Puff Vinyl": {"GPI Supplies": {"price": 42.00, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 42.00, "width": 12, "yards": 5}},
    "Metallic": {"GPI Supplies": {"price": 30.99, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 34.99, "width": 12, "yards": 5}},
    "Holographic": {"GPI Supplies": {"price": 48.00, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 50.00, "width": 20, "yards": 5}},
    "Brick 600 (Thick)": {"GPI Supplies": {"price": 62.99, "width": 20, "yards": 5}, "Heat Transfer Whse": {"price": 39.99, "width": 12, "yards": 5}},
    "Gliter (Thick)": {"GPI Supplies": {"price": 37.99, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 37.99, "width": 12, "yards": 5}},
    "Aurora (Thick)": {"GPI Supplies": {"price": 28.49, "width": 12, "yards": 5}},
    "Easy Glow in the Dark (Thick)": {"Heat Transfer Whse": {"price": 62.99, "width": 12, "yards": 5}},
    "StripFlock Pro (Thick)": {"GPI Supplies": {"price": 35.99, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 45.00, "width": 12, "yards": 5}}
}

# --- 🛍️ DATABASE DE PRODUTOS ---
produtos_db = {
    "CAMISAS": {
        "Gildan G500 Unisex (Jiffy)": {"price": 2.82, "markup": 3.0},
        "Gildan G500 Unisex (Wordans)": {"price": 4.94, "markup": 3.0},
        "Feminina Gola V G500VL (Jiffy)": {"price": 6.37, "markup": 3.5},
        "Feminina Careca G500L (Jiffy)": {"price": 4.91, "markup": 3.2},
        "Kids Shirt G510P (Jiffy)": {"price": 3.93, "markup": 3.0}
    },
    "MOLETONS (HOODIES)": {
        "Gildan G185 Hoodie (Jiffy)": {"price": 14.50, "markup": 2.5}
    },
    "BONÉS (HATS)": {
        "Snapback Classic (Jiffy)": {"price": 5.50, "markup": 4.0},
