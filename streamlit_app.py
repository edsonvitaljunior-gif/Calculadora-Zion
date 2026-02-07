import streamlit as st

st.set_page_config(page_title="Zion Atelier - Calculadora", page_icon="🗽")

st.title("🗽 Zion Atelier")
st.subheader("Calculadora de Orçamentos (Máx. 4 Camadas)")

# Valor por cm² (Ajuste aqui se o preço mudar)
PRECO_POR_CM2 = 0.05  

# --- CAMADA 1 ---
st.write("### 📏 Camada 1 (Base)")
col1, col2 = st.columns(2)
l1 = col1.number_input("Largura C1 (cm)", min_value=0.0, step=0.1, value=10.0, key="l1")
a1 = col2.number_input("Altura C1 (cm)", min_value=0.0, step=0.1, value=10.0, key="a1")
area1 = l1 * a1

st.divider()

# --- CAMADA 2 ---
add_c2 = st.checkbox("Adicionar 2ª Camada?")
area2 = 0.0
if add_c2:
    col3, col4 = st.columns(2)
    l2 = col3.number_input("Largura C2 (cm)", min_value=0.0, step=0.1, value=10.0, key="l2")
    a2 = col4.number_input("Altura C2 (cm)", min_value=0.0, step=0.1, value=10.0, key="a2")
    area2 = l2 * a2

# --- CAMADA 3 ---
add_c3 = st.checkbox("Adicionar 3ª Camada?")
area3 = 0.0
if add_c3:
    col5, col6 = st.columns(2)
    l3 = col5.number_input("Largura C3 (cm)", min_value=0.0, step=0.1, value=10.0, key="l3")
    a3 = col6.number_input("Altura C3 (cm)", min_value=0.0, step=0.1, value=10.0, key="a3")
    area3 = l3 * a3

# --- CAMADA 4 ---
add_c4 = st.checkbox("Adicionar 4ª Camada?")
area4 = 0.0
if add_c4:
    col7, col8 = st.columns(2)
    l4 = col7.number_input("Largura C4 (cm)", min_value=0.0, step=0.1, value=10.0, key="l4")
    a4 = col8.number_input("Altura C4 (cm)", min_value=0.0, step=0.1, value=10.0, key="a4")
    area4 = l4 * a4

# --- CÁLCULO FINAL ---
area_total = area1 + area2 + area3 + area4
preco_final = area_total * PRECO_POR_CM2

st.divider()
st.metric(label="VALOR TOTAL DO ORÇAMENTO", value=f"R$ {preco_final:.2f}")

with st.expander("Resumo das Áreas"):
    st.write(f"C1: {area1:.2f} cm²")
    if add_c2: st.write(f"C2: {area2:.2f} cm²")
    if add_c3: st.write(f"C3: {area3:.2f} cm²")
    if add_c4: st.write(f"C4: {area4:.2f} cm²")
    st.write(f"**Área Total:** {area_total:.2f} cm²")

st.caption("Zion Atelier - New York Style By Faith")
