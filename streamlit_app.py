import streamlit as st
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Zion Atelier", page_icon="🗽", layout="centered")

# --- LOGO ---
nome_logo = "Logo Zion Atelier com fundo tranp 68%.png"
if os.path.exists(nome_logo):
    st.image(nome_logo, width=120)

# --- 📋 IDENTIFICAÇÃO ---
st.write("### 📝 Dados do Orçamento")
nome_cliente = st.text_input("Nome do Cliente")
nome_arte = st.text_input("Nome da Arte")

# Usando uma chave (key) única para forçar o Android a manter o arquivo
arquivo_arte = st.file_uploader("Upload da Arte (JPG/PNG)", type=["jpg", "jpeg", "png"], key="upload_s24")

st.divider()

# --- 📦 BANCO DE DADOS ---
vinis_db = {
    "EasyWeed (Siser)": {"price": 34.99, "width": 12, "yards": 5},
    "Puff Vinyl": {"price": 42.00, "width": 12, "yards": 5},
    "Metallic": {"price": 30.99, "width": 12, "yards": 5}
}

produtos_db = {
    "CAMISAS": {"Gildan G500": {"price": 2.82, "markup": 3.0}},
    "MOLETONS": {"Gildan G185": {"price": 14.50, "markup": 2.5}},
    "BONÉS": {"Snapback": {"price": 5.50, "markup": 4.0}}
}

# --- 🛍️ SELEÇÃO ---
cat = st.selectbox("Categoria", list(produtos_db.keys()))
prod = st.selectbox("Modelo", list(produtos_db[cat].keys()))
qtd = st.number_input("Quantidade", min_value=1, value=1)

# --- 📏 MEDIDAS ---
tipo = st.selectbox("Material", list(vinis_db.keys()))
w = st.number_input("Largura (in)", value=10.0)
h = st.number_input("Altura (in)", value=10.0)

# --- 💰 CÁLCULOS ---
d = vinis_db[tipo]
taxa = (d["price"] / (d["width"] * (d["yards"] * 36))) * 1.2
custo_vinil = (w * h) * taxa
p_unit = (produtos_db[cat][prod]["price"] + custo_vinil) * produtos_db[cat][prod]["markup"]
promo = st.toggle("10% OFF")
valor_final = (p_unit * qtd) * 0.9 if promo else (p_unit * qtd)

st.divider()

# --- 🏁 RESUMO (COM FIX DE EXIBIÇÃO) ---
st.subheader("🏁 Orçamento Zion")

# Se o arquivo existe, tentamos ler os bytes dele diretamente
if arquivo_arte is not None:
    bytes_data = arquivo_arte.getvalue()
    st.image(bytes_data, use_container_width=True)
    st.success("✅ Imagem carregada!")
else:
    st.warning("⚠️ Selecione uma imagem para o preview.")

st.info(f"👤 **Cliente:** {nome_cliente}\n\n🎨 **Arte:** {nome_arte}")

col1, col2 = st.columns(2)
col1.metric("Unitário", f"${p_unit:.2f}")
col2.metric("Total", f"${valor_final:.2f}")

st.caption("Zion Atelier - New York Style By Faith")
