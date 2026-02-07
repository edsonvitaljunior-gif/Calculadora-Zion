import streamlit as st

st.set_page_config(page_title="Zion Atelier - Pro Manager", page_icon="🗽")

st.title("🗽 Zion Atelier")
st.subheader("Professional Quote Manager (US Standard)")

# --- DATABASE DE FORNECEDORES E PREÇOS ---
# Preços médios informados por você (ajustáveis abaixo)
fornecedores_camisas = {
    "Jiffy Shirts (Gildan Unisex)": 2.80,
    "Wordans (Gildan Unisex)": 4.94,
    "Zion Stock (Feminina Gola V)": 25.00,
    "Zion Stock (Feminina Careca)": 18.00,
    "Kids/Children Shirt": 12.00
}

fornecedores_vinil = {
    "GPI Supplies (Standard Roll)": 0.22, # Custo aprox. por sq in baseado no rolo
    "Heat Transfer Whse (Premium)": 0.35,
    "Specialty Vinyl (Glitter/Reflective)": 0.50
}

# --- SEÇÃO 1: SELEÇÃO DE FORNECEDOR ---
st.write("### 🛒 Supplier & Product")
col_prov, col_vin = st.columns(2)

with col_prov:
    fornecedor_sel = st.selectbox("Select Shirt Supplier", list(fornecedores_camisas.keys()))
    custo_base_camisa = fornecedores_camisas[fornecedor_sel]

with col_vin:
    vinil_sel = st.selectbox("Select Vinyl Supplier", list(fornecedores_vinil.keys()))
    custo_sq_in = fornecedores_vinil[vinil_sel]

st.divider()

# --- SEÇÃO 2: DIMENSÕES (POLEGADAS) ---
st.write("### 📏 Layer Dimensions (Inches)")

def input_camada(label, key):
    c1, c2 = st.columns(2)
    w = c1.number_input(f"W {label}", min_value=0.0, step=0.1, value=0.0, key=f"w{key}")
    h = c2.number_input(f"H {label}", min_value=0.0, step=0.1, value=0.0, key=f"h{key}")
    return w * h

# Camada 1
area1 = input_camada("Layer 1 (Base)", "1")

# Camadas Ocionais
c2_on = st.checkbox("Add 2nd Layer?")
area2 = input_camada("Layer 2", "2") if c2_on else 0.0

c3_on = st.checkbox("Add 3rd Layer?")
area3 = input_camada("Layer 3", "3") if c3_on else 0.0

c4_on = st.checkbox("Add 4th Layer?")
area4 = input_camada("Layer 4", "4") if c4_on else 0.0

# --- CÁLCULOS ---
area_total = area1 + area2 + area3 + area4
custo_vinil_total = area_total * custo_sq_in
# Adicionando uma margem de lucro de 40% sobre o material ou ajuste como preferir
markup = 2.0 
total_final = custo_base_camisa + (custo_vinil_total * markup)

st.divider()

# --- RESULTADO FINAL ---
st.metric(label="FINAL PRICE TO CUSTOMER ($)", value=f"$ {total_final:.2f}")

with st.expander("📊 Cost Breakdown (Detailed)"):
    st.write(f"**Shirt Cost:** ${custo_base_camisa:.2f} ({fornecedor_sel})")
    st.write(f"**Vinyl Cost:** ${custo_vinil_total:.2f} ({vinil_sel})")
    st.write(f"**Total Area Used:** {area_total:.2f} sq in")
    st.caption("Note: Price includes material markup and labor.")

st.caption("Zion Atelier - New York Style By Faith")
