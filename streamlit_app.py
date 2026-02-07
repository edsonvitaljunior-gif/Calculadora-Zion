import streamlit as st

# Configuração da página
st.set_page_config(page_title="Zion Atelier - Pro", page_icon="🗽", layout="centered")

# Substitua o bloco do logo por este:
import os

if os.path.exists("logo.png"):
    st.image("logo.png", width=200)
else:
    st.title("🗽 Zion Atelier")

# --- BANCO DE DADOS (DATABASE) ---
fornecedores_camisas = {
    "Jiffy Shirts (Gildan Unisex)": 2.80,
    "Wordans (Gildan Unisex)": 4.94,
    "Zion Stock (Feminina Gola V)": 25.00,
    "Zion Stock (Feminina Careca)": 18.00,
    "Kids/Children Shirt": 12.00
}

vinis_db = {
    "EasyWeed (Siser)": {
        "GPI Supplies": {"price": 34.99, "width": 12, "yards": 5},
        "Heat Transfer Whse": {"price": 38.50, "width": 12, "yards": 5}
    },
    "Glitter (Siser)": {
        "GPI Supplies": {"price": 45.00, "width": 12, "yards": 5},
        "Heat Transfer Whse": {"price": 42.00, "width": 12, "yards": 5}
    },
    "Refletivo": {
        "GPI Supplies": {"price": 55.00, "width": 12, "yards": 5},
        "Heat Transfer Whse": {"price": 58.00, "width": 12, "yards": 5}
    }
}

# --- SELEÇÕES ---
st.write("### 👕 1. Camisa & Material")
col1, col2 = st.columns(2)

with col1:
    f_camisa = st.selectbox("Fornecedor da Camisa", list(fornecedores_camisas.keys()))
    custo_camisa = fornecedores_camisas[f_camisa]

with col2:
    tipo_v = st.selectbox("Tipo de Vinil", list(vinis_db.keys()))
    f_vinil = st.selectbox("Fornecedor do Vinil", list(vinis_db[tipo_v].keys()))

# Cálculo do preço por sq in (polegada quadrada)
dados_v = vinis_db[tipo_v][f_vinil]
preco_sq_in = dados_v["price"] / (dados_v["width"] * (dados_v["yards"] * 36))

st.divider()

# --- CAMADAS (LARGURA E ALTURA) ---
st.write("### 📏 2. Dimensões da Estampa (Inches)")

def input_camada(label, key):
    c1, c2 = st.columns(2)
    w = c1.number_input(f"Largura {label}", min_value=0.0, step=0.1, key=f"w{key}")
    h = c2.number_input(f"Altura {label}", min_value=0.0, step=0.1, key=f"h{key}")
    return w * h

# Camada 1
area1 = input_camada("Layer 1 (Base)", "1")

# Camadas Extras (Checkbox para habilitar)
area2 = area3 = area4 = 0.0

if st.checkbox("Adicionar Camada 2?"):
    area2 = input_camada("Layer 2", "2")

if st.checkbox("Adicionar Camada 3?"):
    area3 = input_camada("Layer 3", "3")

if st.checkbox("Adicionar Camada 4?"):
    area4 = input_camada("Layer 4", "4")

# --- CÁLCULO FINAL ---
area_total = area1 + area2 + area3 + area4
custo_vinil = area_total * preco_sq_in
markup = 2.5 # Sua margem de lucro (ajustável)
preco_final = custo_camisa + (custo_vinil * markup)

st.divider()
st.metric(label="PREÇO FINAL (SUGESTÃO)", value=f"$ {preco_final:.2f}")

with st.expander("Detalhamento do Orçamento"):
    st.write(f"**Camisa:** {f_camisa} (${custo_camisa:.2f})")
    st.write(f"**Vinil:** {tipo_v} via {f_vinil}")
    st.write(f"**Área Total:** {area_total:.2f} sq in")
    st.write(f"**Custo Material:** ${custo_vinil:.2f}")

st.caption("Zion Atelier - New York Style By Faith")
