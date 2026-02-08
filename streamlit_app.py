import streamlit as st
import os

# --- 1. CONFIGURAÇÃO S24 ---
try:
    st.set_page_config(page_title="Zion Atelier", page_icon="🗽", layout="centered")
except:
    pass

# --- 2. LOGO ---
nome_logo = "Logo Zion Atelier com fundo tranp 68%.png"
if os.path.exists(nome_logo):
    st.image(nome_logo, width=150)

# --- 3. DADOS DO PROJETO ---
st.write("### 📝 Dados do Orçamento")
nome_cliente = st.text_input("Nome do Cliente", placeholder="Quem está comprando?")
nome_arte = st.text_input("Nome da Arte", placeholder="Ex: Lion Gold Puff")
arquivo_arte = st.file_uploader("Upload da Arte", type=["png", "jpg", "jpeg", "webp"], accept_multiple_files=False)

st.divider()

# --- 4. DATABASE COMPLETA ---
vinis_db = {
    "EasyWeed (Siser)": 34.99,
    "Puff Vinyl": 42.00,
    "Metallic": 30.99,
    "Brick 600 (Thick)": 62.99,
    "Gliter (Thick)": 37.99,
    "StripFlock Pro": 35.99
}

produtos_db = {
    "CAMISAS": {
        "Gildan G500 Unisex": {"price": 2.82, "markup": 3.0},
        "Feminina Gola V": {"price": 6.37, "markup": 3.5},
        "Feminina Careca": {"price": 4.91, "markup": 3.2},
        "Kids Shirt": {"price": 3.93, "markup": 3.0}
    },
    "MOLETONS": {
        "Gildan G185 Hoodie": {"price": 14.50, "markup": 2.5}
    },
    "BONÉS": {
        "Snapback Classic": {"price": 5.50, "markup": 4.0},
        "Trucker Hat": {"price": 4.20, "markup": 4.0}
    }
}

# --- 5. SELEÇÃO DE PRODUTO (CORRIGIDO) ---
st.write("### 🛍️ Escolha o Item")
categoria_selecionada = st.selectbox("Categoria", list(produtos_db.keys()))

# Aqui está o segredo: os produtos mudam de acordo com a categoria
lista_produtos = list(produtos_db[categoria_selecionada].keys())
produto_nome = st.selectbox("Modelo", lista_produtos)

qtd = st.number_input("Quantidade", min_value=1, value=1)

# Puxa o preço e o markup do produto selecionado
dados_prod = produtos_db[categoria_selecionada][produto_nome]
c_base = dados_prod["price"]
mk_base = dados_prod["markup"]

st.divider()

# --- 6. MEDIDAS DA ESTAMPA ---
st.write("### 📏 Medidas da Arte")
tipo_v = st.selectbox("Tipo de Vinil", list(vinis_db.keys()))
col1, col2 = st.columns(2)
with col1:
    w = st.number_input("Largura (in)", value=10.0)
with col2:
    h = st.number_input("Altura (in)", value=10.0)

# Cálculo de custo
custo_v = (w * h) * (vinis_db[tipo_v] / (12 * 180)) * 1.2
p_unit = (c_base + custo_v) * mk_base
total = p_unit * qtd

# --- 7. RESUMO FINAL ---
st.divider()
st.subheader("🏁 Resumo do Pedido")

if arquivo_arte is not None:
    st.image(arquivo_arte, use_container_width=True)

st.info(f"👤 **Cliente:** {nome_cliente if nome_cliente else 'Zion Friend'} | 🎨 **Arte:** {nome_arte if nome_arte else 'Custom'}")

st.metric("Preço Unitário", f"${p_unit:.2f}")
st.metric("TOTAL DO PEDIDO", f"${total:.2f}")

with st.expander("📊 Zion Only"):
    st.write(f"Custo Unitário Real: ${(c_base + custo_v):.2f}")
    st.write(f"Markup Aplicado: {mk_base}x")

st.caption("Zion Atelier - New York Style By Faith")
