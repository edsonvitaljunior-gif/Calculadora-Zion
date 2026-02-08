import streamlit as st
import os

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Zion Atelier - Pro Manager", 
    page_icon="🗽", 
    layout="centered"
)

# --- 2. LOGO ---
nome_logo = "Logo Zion Atelier com fundo tranp 68%.png"
if os.path.exists(nome_logo):
    st.image(nome_logo, width=120)
else:
    st.title("🗽 Zion Atelier")

# --- 3. DADOS DO CLIENTE E ARTE ---
st.write("### 📝 Identificação")
nome_cliente = st.text_input("Nome do Cliente", placeholder="Ex: John Doe")
nome_arte = st.text_input("Nome da Arte", placeholder="Ex: NY Lion Puff")
arquivo_arte = st.file_uploader("Upload da Arte (Foto/Print)", type=["png", "jpg", "jpeg", "webp"])

st.divider()

# --- 4. BANCO DE DADOS (Vinis e Produtos) ---
vinis_db = {
    "EasyWeed (Siser)": {"GPI Supplies": {"price": 34.99, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 37.99, "width": 12, "yards": 5}},
    "Puff Vinyl": {"GPI Supplies": {"price": 42.00, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 42.00, "width": 12, "yards": 5}},
    "Metallic": {"GPI Supplies": {"price": 30.99, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 34.99, "width": 12, "yards": 5}},
    "Brick 600 (Thick)": {"GPI Supplies": {"price": 62.99, "width": 20, "yards": 5}, "Heat Transfer Whse": {"price": 39.99, "width": 12, "yards": 5}},
    "Gliter (Thick)": {"GPI Supplies": {"price": 37.99, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 37.99, "width": 12, "yards": 5}},
    "StripFlock Pro": {"GPI Supplies": {"price": 35.99, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 45.00, "width": 12, "yards": 5}}
}

produtos_db = {
    "CAMISAS": {
        "Gildan G500 Unisex (Jiffy)": {"price": 2.82, "markup": 3.0},
        "Feminina Gola V G500VL (Jiffy)": {"price": 6.37, "markup": 3.5},
        "Feminina Careca G500L (Jiffy)": {"price": 4.91, "markup": 3.2},
        "Kids Shirt G510P (Jiffy)": {"price": 3.93, "markup": 3.0}
    },
    "MOLETONS (HOODIES)": {
        "Gildan G185 Hoodie (Jiffy)": {"price": 14.50, "markup": 2.5}
    },
    "BONÉS (HATS)": {
        "Snapback Classic (Jiffy)": {"price": 5.50, "markup": 4.0},
        "Trucker Hat (Jiffy)": {"price": 4.20, "markup": 4.0}
    }
}

# --- 5. SELEÇÃO DO PRODUTO ---
st.write("### 🛍️ Escolha o Item")
cat = st.selectbox("Categoria", list(produtos_db.keys()))
prod = st.selectbox("Modelo", list(produtos_db[cat].keys()))
qtd = st.number_input("Quantidade", min_value=1, value=1)

c_base = produtos_db[cat][prod]["price"]
mk_base = produtos_db[cat][prod]["markup"]

st.divider()

# --- 6. CONFIGURAÇÃO DA ESTAMPA ---
st.write("### 📏 Medidas da Arte")
tipo = st.selectbox("Tipo de Vinil", list(vinis_db.keys()))
forn = st.selectbox("Fornecedor", list(vinis_db[tipo].keys()))
w = st.number_input("Largura (in)", min_value=0.0, step=0.1, value=10.0)
h = st.number_input("Altura (in)", min_value=0.0, step=0.1, value=10.0)

# Cálculo do custo do vinil por polegada quadrada (com 20% de margem de perda)
d = vinis_db[tipo][forn]
taxa = (d["price"] / (d["width"] * (d["yards"] * 36))) * 1.2
custo_vinil_total = (w * h) * taxa

# --- 7. CÁLCULO DE PREÇO ---
p_unit = (c_base + custo_vinil_total) * mk_base
total_pedido = p_unit * qtd

st.write("### 💰 Promoção")
promo = st.toggle("Aplicar 10% de Desconto")
valor_final = total_pedido * 0.9 if promo else total_pedido

st.divider()

# --- 8. RESUMO PARA O CLIENTE (O Gran Finale) ---
st.subheader("🏁 Resumo do Orçamento")

# Foto no topo para o celular
if arquivo_arte is not None:
    st.image(arquivo_arte, use_container_width=True)
    st.caption(f"Projeto: {nome_arte}")

# Info do cliente
st.info(f"👤 **Cliente:** {nome_cliente if nome_cliente else 'Friend of Zion'}")

# Métricas de preço lado a lado
c1, c2 = st.columns(2)
with c1:
    st.metric("Preço Unitário", f"${p_unit:.2f}")
with c2:
    st.metric("Total Final", f"${valor_final:.2f}", delta="-10%" if promo else None)

# --- 9. ÁREA TÉCNICA (ZION ONLY) ---
with st.expander("📊 Detalhes Técnicos (Somente Interno)"):
    lucro = valor_final - ((c_base + custo_vinil_total) * qtd)
    st.write(f"Custo Unitário Total: ${(c_base + custo_vinil_total):.2f}")
    st.write(f"Markup Aplicado: {mk_base}x")
    st.write(f"**LUCRO LÍQUIDO NO PEDIDO: ${lucro:.2f}**")

st.caption("Zion Atelier - New York Style By Faith")
