import streamlit as st
import os

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Zion Atelier", page_icon="🗽")

# --- LOGO ---
nome_logo = "Logo Zion Atelier com fundo tranp 68%.png"
if os.path.exists(nome_logo):
    st.image(nome_logo, width=120)

# --- 📋 ENTRADA DE DADOS ---
st.write("### 📝 Orçamento")
nome_cliente = st.text_input("Cliente")
nome_arte = st.text_input("Projeto")

# O segredo: Colocar o upload em um lugar de destaque
arquivo_arte = st.file_uploader("Escolha a Arte", type=["jpg", "jpeg", "png"], key="s24_upload")

st.divider()

# --- 📦 DATABASE SIMPLIFICADA ---
vinis_db = {"EasyWeed": 34.99, "Puff": 42.00, "Metallic": 30.99}
produtos_db = {"CAMISAS": 2.82, "MOLETONS": 14.50, "BONÉS": 5.50}

# --- 🛍️ SELEÇÕES ---
cat = st.selectbox("Item", list(produtos_db.keys()))
tipo_v = st.selectbox("Vinil", list(vinis_db.keys()))
qtd = st.number_input("Qtd", min_value=1, value=1)

# Medidas
col_w, col_h = st.columns(2)
w = col_w.number_input("Larg (in)", value=10.0)
h = col_h.number_input("Alt (in)", value=10.0)

# --- 💰 CÁLCULOS ---
custo_v = (w * h) * (vinis_db[tipo_v] / (12 * 180)) * 1.2
p_unit = (produtos_db[cat] + custo_v) * 3.0
total = p_unit * qtd

# --- 🏁 RESUMO (ESTRUTURA QUE FUNCIONA NO MOBILE) ---
st.divider()
st.subheader("🏁 Resultado")

# Se subir a imagem, ela aparece aqui primeiro
if arquivo_arte is not None:
    st.image(arquivo_arte, caption="Arte Selecionada", use_container_width=True)
    st.success("✅ Imagem carregada com sucesso!")

st.info(f"👤 {nome_cliente} | 🎨 {nome_arte}")

# No celular, as métricas ficam melhores assim:
st.metric("Preço Unitário", f"${p_unit:.2f}")
st.metric("TOTAL DO PEDIDO", f"${total:.2f}")

st.caption("Zion Atelier - New York Style By Faith")
