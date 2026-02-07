import streamlit as st

st.set_page_config(page_title="Zion Atelier - Calculadora", page_icon="🗽")

st.title("🗽 Zion Atelier")
st.subheader("Orçamento em Polegadas (inches)")

# Valor por polegada quadrada (sq in)
# Ajuste este valor conforme o custo do material nos EUA
PRECO_POR_SQ_IN = 0.25  

# --- CAMADA 1 ---
st.write("### 📏 Layer 1 (Base)")
col1, col2 = st.columns(2)
l1 = col1.number_input("Width (Largura) - pol", min_value=0.0, step=0.1, value=4.0, key="l1")
a1 = col2.number_input("Height (Altura) - pol", min_value=0.0, step=0.1, value=4.0, key="a1")
area1 = l1 * a1

st.divider()

# --- CAMADA 2 ---
add_c2 = st.checkbox("Add 2nd Layer?")
area2 = 0.0
if add_c2:
    st.write("### 🎨 Layer 2")
    col3, col4 = st.columns(2)
    l2 = col3.number_input("Width - pol", min_value=0.0, step=0.1, value=4.0, key="l2")
    a2 = col4.number_input("Height - pol", min_value=0.0, step=0.1, value=4.0, key="a2")
    area2 = l2 * a2

# --- CAMADA 3 ---
add_c3 = st.checkbox("Add 3rd Layer?")
area3 = 0.0
if add_c3:
    st.write("### 🎨 Layer 3")
    col5, col6 = st.columns(2)
    l3 = col5.number_input("Width - pol", min_value=0.0, step=0.1, value=4.0, key="l3")
    a3 = col6.number_input("Height - pol", min_value=0.0, step=0.1, value=4.0, key="a3")
    area3 = l3 * a3

# --- CAMADA 4 ---
add_c4 = st.checkbox("Add 4th Layer?")
area4 = 0.0
if add_c4:
    st.write("### 🎨 Layer 4")
    col7, col8 = st.columns(2)
    l4 = col7.number_input("Width - pol", min_value=0.0, step=0.1, value=4.0, key="l4")
    a4 = col8.number_input("Height - pol", min_value=0.0, step=0.1, value=4.0, key="a4")
    area4 = l4 * a4

# --- CÁLCULO FINAL ---
area_total = area1 + area2 + area3 + area4
preco_final = area_total * PRECO_POR_SQ_IN

st.divider()
st.metric(label="TOTAL PRICE ($)", value=f"$ {preco_final:.2f}")

with st.expander("Area Details (sq in)"):
    st.write(f"Layer 1: {area1:.2f} sq in")
    if add_c2: st.write(f"Layer 2: {area2:.2f} sq in")
    if add_c3: st.write(f"Layer 3: {area3:.2f} sq in")
    if add_c4: st.write(f"Layer 4: {area4:.2f} sq in")
    st.write(f"**Total Area:** {area_total:.2f} sq in")

st.caption("Zion Atelier - New York Style By Faith")
