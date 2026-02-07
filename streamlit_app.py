import streamlit as st

# Configuração da página (como aparecerá no navegador do celular)
st.set_page_config(page_title="Zion Atelier - Calculadora", page_icon="🗽")

# Estilo para deixar o visual mais limpo
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_content_html=True)

# Logo e Título
st.title("🗽 Zion Atelier")
st.subheader("Calculadora de Orçamentos")

# --- LÓGICA DE PREÇOS (Você pode ajustar esses valores aqui depois) ---
# Exemplo: 0.05 significa 5 centavos por cm²
PRECO_POR_CM2 = 0.05  

with st.container():
    st.write("### 📏 Camada 1 (Principal)")
    col1, col2 = st.columns(2)
    with col1:
        largura1 = st.number_input("Largura C1 (cm)", min_value=0.0, step=0.1, value=10.0, key="l1")
    with col2:
        altura1 = st.number_input("Altura C1 (cm)", min_value=0.0, step=0.1, value=10.0, key="a1")
    
    area1 = largura1 * altura1

st.divider()

# --- BOTÃO PARA ADICIONAR CAMADA 2 ---
add_camada2 = st.checkbox("Adicionar 2ª Camada? (Borda/Fundo)")

area2 = 0.0
if add_camada2:
    st.write("### 🎨 Camada 2")
    col3, col4 = st.columns(2)
    with col3:
        largura2 = st.number_input("Largura C2 (cm)", min_value=0.0, step=0.1, value=10.0, key="l2")
    with col4:
        altura2 = st.number_input("Altura C2 (cm)", min_value=0.0, step=0.1, value=10.0, key="a2")
    area2 = largura2 * altura2

# --- CÁLCULO FINAL ---
area_total = area1 + area2
preco_final = area_total * PRECO_POR_CM2

st.divider()

# Exibição do Resultado em destaque
st.metric(label="VALOR TOTAL", value=f"R$ {preco_final:.2f}")

# Detalhes técnicos para conferência
with st.expander("Ver detalhes do cálculo"):
    st.write(f"Área Camada 1: {area1:.2f} cm²")
    if add_camada2:
        st.write(f"Área Camada 2: {area2:.2f} cm²")
    st.write(f"**Área Total:** {area_total:.2f} cm²")
    st.write(f"**Custo por cm²:** R$ {PRECO_POR_CM2:.2f}")

st.caption("Zion Atelier - New York Style By Faith")
