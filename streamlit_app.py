import streamlit as st

# Título simples e direto
st.title("🗽 Zion Atelier")
st.subheader("Calculadora de Orçamentos")

# Configuração de preço
PRECO_POR_CM2 = 0.05  

# Camada 1
st.write("### 📏 Camada 1 (Principal)")
col1, col2 = st.columns(2)
largura1 = col1.number_input("Largura C1 (cm)", min_value=0.0, step=0.1, value=10.0)
altura1 = col2.number_input("Altura C1 (cm)", min_value=0.0, step=0.1, value=10.0)
area1 = largura1 * altura1

st.divider()

# Camada 2
add_camada2 = st.checkbox("Adicionar 2ª Camada?")
area2 = 0.0
if add_camada2:
    st.write("### 🎨 Camada 2")
    col3, col4 = st.columns(2)
    largura2 = col3.number_input("Largura C2 (cm)", min_value=0.0, step=0.1, value=10.0)
    altura2 = col4.number_input("Altura C2 (cm)", min_value=0.0, step=0.1, value=10.0)
    area2 = largura2 * altura2

# Cálculo Final
area_total = area1 + area2
preco_final = area_total * PRECO_POR_CM2

st.divider()
st.metric(label="VALOR TOTAL", value=f"R$ {preco_final:.2f}")
st.caption("Zion Atelier - New York Style By Faith")
