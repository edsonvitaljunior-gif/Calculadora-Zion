import streamlit as st
import os

# Configuração
st.set_page_config(page_title="Zion Atelier - Pro", page_icon="🗽")

# --- EXIBIÇÃO DA LOGO ---
if os.path.exists("Logo Zion Atelier com fundo tranp 68%.png"):
    st.image("Logo Zion Atelier com fundo tranp 68%.png", width=120) # Tamanho reduzido como você pediu
else:
    st.title("🗽 Zion Atelier")

st.subheader("Professional Cost Management")

# --- 📦 CADASTRO DE VINIS (Adicione novos aqui!) ---
vinis_db = {
    "EasyWeed (Siser)": {
        "GPI Supplies": {"price": 34.99, "width": 12, "yards": 5},
        "Heat Transfer Whse": {"price": 38.50, "width": 12, "yards": 5}
    },
    "Puff Vinyl": {
        "GPI Supplies": {"price": 42.00, "width": 12, "yards": 5},
        "Heat Transfer Whse": {"price": 45.00, "width": 12, "yards": 5}
    },
    "Metallic": {
        "GPI Supplies": {"price": 39.00, "width": 12, "yards": 5},
        "Heat Transfer Whse": {"price": 41.00, "width": 12, "yards": 5}
    },
    "Holographic": {
        "GPI Supplies": {"price": 48.00, "width": 12, "yards": 5},
        "Heat Transfer Whse": {"price": 50.00, "width": 20, "yards": 5}
    },
    "Brick 600 (Thick)": {
        "Heat Transfer Whse": {"price": 55.00, "width": 12, "yards": 5}
    }
}

# --- 👕 CADASTRO DE CAMISAS ---
fornecedores_camisas = {
    "Jiffy Shirts (Gildan Unisex)": 2.80,
    "Wordans (Gildan Unisex)": 4.94,
    "Zion Stock (Feminina Gola V)": 25.00,
    "Zion Stock (Feminina Careca)": 18.00,
    "Kids Shirt": 12.00
}

# --- SELEÇÕES NO APP ---
st.write("### 👕 1. Produto e Material")
c1, c2 = st.columns(2)

with c1:
    f_camisa = st.selectbox("Camisa/Fornecedor", list(fornecedores_camisas.keys()))
    custo_camisa = fornecedores_camisas[f_camisa]

with c2:
    tipo_v = st.selectbox("Tipo de Vinil", list(vinis_db.keys()))
    f_vinil = st.selectbox("Fornecedor do Vinil", list(vinis_db[tipo_v].keys()))

# Cálculo matemático do custo por polegada quadrada
dados_v = vinis_db[tipo_v][f_vinil]
# Preço / (Largura * (Jardas * 36 polegadas))
preco_sq_in = dados_v["price"] / (dados_v["width"] * (dados_v["yards"] * 36))

st.divider()

# --- MEDIDAS ---
st.write("### 📏 2. Medidas da Estampa (Inches)")

def input_camada(label, key):
    col_w, col_h = st.columns(2)
    w = col_w.number_input(f"Largura {label}", min_value=0.0, step=0.1, key=f"w{key}")
    h = col_h.number_input(f"Altura {label}", min_value=0.0, step=0.1, key=f"h{key}")
    return w * h

area1 = input_camada("Layer 1", "1")
area2 = input_camada("Layer 2", "2") if st.checkbox("Add Layer 2?") else 0.0
area3 = input_camada("Layer 3", "3") if st.checkbox("Add Layer 3?") else 0.0
area4 = input_camada("Layer 4", "4") if st.checkbox("Add Layer 4?") else 0.0

# --- PRECIFICAÇÃO ---
area_total = area1 + area2 + area3 + area4
custo_vinil_total = area_total * preco_sq_in

# MARKUP: Multiplicador sobre o custo do vinil para cobrir mão de obra e lucro
# Exemplo: 3.0 significa que você cobra 3x o custo do material
markup = 3.0 
preco_final = custo_camisa + (custo_vinil_total * markup)

st.divider()
st.metric(label="PREÇO ESTIMADO ($)", value=f"$ {preco_final:.2f}")

with st.expander("Detalhamento"):
    st.write(f"Custo Base Camisa: ${custo_camisa:.2f}")
    st.write(f"Custo Real Material: ${custo_vinil_total:.4f}")
    st.write(f"Área Total: {area_total:.2f} sq in")

st.caption("Zion Atelier - New York Style By Faith")
