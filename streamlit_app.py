import streamlit as st

st.set_page_config(page_title="Zion Atelier - Pro", page_icon="🗽")

st.title("🗽 Zion Atelier")
st.subheader("Orçamento Profissional")

# --- TABELAS DE PREÇOS (Você pode ajustar os valores aqui) ---
precos_vinil = {
    "Básico (Padrão)": 0.25,
    "Premium/Glitter": 0.40,
    "Refletivo/Neon": 0.50
}

precos_produtos = {
    "Camisa Unisex": 15.00,
    "Camisa Feminina (Gola Careca)": 18.00,
    "Camisa Feminina (Gola V)": 25.00,
    "Camisa para Criança": 12.00
}

# --- SELEÇÃO DE PRODUTO E MATERIAL ---
st.write("### 👕 Configuração do Produto")
col_p, col_m = st.columns(2)

with col_p:
    produto_sel = st.selectbox("Tipo de Produto", list(precos_produtos.keys()))
    preco_base_produto = precos_produtos[produto_sel]

with col_m:
    material_sel = st.selectbox("Tipo de Vinil", list(precos_vinil.keys()))
    custo_sq_in = precos_vinil[material_sel]

st.divider()

# --- CAMADAS (MANTENDO AS 4 CAMADAS EM POLEGADAS) ---
st.write("### 📏 Dimensões da Estampa (Inches)")

def input_camada(label, key):
    col_l, col_a = st.columns(2)
    w = col_l.number_input(f"Width {label} (pol)", min_value=0.0, step=0.1, value=0.0, key=f"w{key}")
    h = col_a.number_input(f"Height {label} (pol)", min_value=0.0, step=0.1, value=0.0, key=f"h{key}")
    return w * h

# Camada 1 (Obrigatória)
area1 = input_camada("Layer 1", "1")

# Camadas Extras
add_c2 = st.checkbox("Add 2nd Layer?")
area2 = input_camada("Layer 2", "2") if add_c2 else 0.0

add_c3 = st.checkbox("Add 3rd Layer?")
area3 = input_camada("Layer 3", "3") if add_c3 else 0.0

add_c4 = st.checkbox("Add 4th Layer?")
area4 = input_camada("Layer 4", "4") if add_c4 else 0.0

# --- CÁLCULO FINAL ---
area_total = area1 + area2 + area3 + area4
custo_estampa = area_total * custo_sq_in
total_geral = preco_base_produto + custo_estampa

st.divider()

# Resultado em destaque
st.metric(label="TOTAL DO ORÇAMENTO ($)", value=f"$ {total_geral:.2f}")

with st.expander("Detalhamento de Custos"):
    st.write(f"**Produto:** {produto_sel} ($ {preco_base_produto:.2f})")
    st.write(f"**Material:** {material_sel} ($ {custo_sq_in:.2f} per sq in)")
    st.write(f"**Área Total Estampada:** {area_total:.2f} sq in")
    st.write(f"**Custo da Estampa:** $ {custo_estampa:.2f}")

st.caption("Zion Atelier - New York Style By Faith")
