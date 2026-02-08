import streamlit as st
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
nome_logo = "Logo Zion Atelier com fundo tranp 68%.png"
fav_icon = nome_logo if os.path.exists(nome_logo) else "🗽"

st.set_page_config(
    page_title="Zion Atelier - Sales Pro", 
    page_icon=fav_icon,
    layout="centered"
)

# --- EXIBIÇÃO DA LOGO ---
if os.path.exists(nome_logo):
    st.image(nome_logo, width=150)
else:
    st.title("🗽 Zion Atelier")

# --- 📦 DATABASE DE VINIS (20% Waste Incluído) ---
vinis_db = {
    "EasyWeed (Siser)": {"GPI Supplies": {"price": 34.99, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 37.99, "width": 12, "yards": 5}},
    "Puff Vinyl": {"GPI Supplies": {"price": 42.00, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 42.00, "width": 12, "yards": 5}},
    "Metallic": {"GPI Supplies": {"price": 30.99, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 34.99, "width": 12, "yards": 5}},
    "Holographic": {"GPI Supplies": {"price": 48.00, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 50.00, "width": 20, "yards": 5}},
    "Brick 600 (Thick)": {"GPI Supplies": {"price": 62.99, "width": 20, "yards": 5}, "Heat Transfer Whse": {"price": 39.99, "width": 12, "yards": 5}},
    "Gliter (Thick)": {"GPI Supplies": {"price": 37.99, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 37.99, "width": 12, "yards": 5}},
    "Aurora (Thick)": {"GPI Supplies": {"price": 28.49, "width": 12, "yards": 5}},
    "Easy Glow in the Dark (Thick)": {"Heat Transfer Whse": {"price": 62.99, "width": 12, "yards": 5}},
    "StripFlock Pro (Thick)": {"GPI Supplies": {"price": 35.99, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 45.00, "width": 12, "yards": 5}}
}

# --- 👕 DATABASE DE PRODUTOS EXPANDIDA (Camisas, Hoodies, Bonés) ---
# Você pode ajustar esses preços e markups conforme sua realidade
produtos_db = {
    "CAMISAS": {
        "Gildan G500 Unisex (Jiffy)": {"price": 2.82, "markup": 3.0},
        "Gildan G500 Unisex (Wordans)": {"price": 4.94, "markup": 3.0},
        "Feminina Gola V G500VL (Jiffy)": {"price": 6.37, "markup": 3.5},
        "Feminina Careca G500L (Jiffy)": {"price": 4.91, "markup": 3.2},
        "Kids Shirt G510P (Jiffy)": {"price": 3.93, "markup": 3.0}
    },
    "MOLETONS (HOODIES)": {
        "Gildan G185 Hoodie (Jiffy)": {"price": 14.50, "markup": 2.5},
        "Heavy Blend Hoodie (Wordans)": {"price": 16.80, "markup": 2.5}
    },
    "BONÉS (HATS)": {
        "Snapback Classic (Jiffy)": {"price": 5.50, "markup": 4.0},
        "Trucker Hat (Jiffy)": {"price": 4.20, "markup": 4.0}
    }
}

# --- 🛍️ 1. SELEÇÃO DO PRODUTO ---
st.write("### 🛍️ 1. Seleção do Produto")
categoria = st.selectbox("Categoria", list(produtos_db.keys()))
produto_nome = st.selectbox("Modelo", list(produtos_db[categoria].keys()))

custo_base = produtos_db[categoria][produto_nome]["price"]
markup_base = produtos_db[categoria][produto_nome]["markup"]
quantidade = st.number_input("Quantidade", min_value=1, value=1)

st.divider()

# --- 📏 2. CONFIGURAÇÃO POR CAMADA ---
st.write("### 📏 2. Materiais da Estampa")

def calcular_custo_camada(n):
    with st.expander(f"Configurar Camada {n}", expanded=(n==1)):
        col1, col2 = st.columns(2)
        with col1:
            v_tipo = st.selectbox(f"Material C{n}", list(vinis_db.keys()), key=f"tipo{n}")
        with col2:
            opcoes_f = list(vinis_db[v_tipo].keys())
            v_forn = st.selectbox(f"Fornecedor C{n}", opcoes_f, key=f"forn{n}")
        
        col3, col4 = st.columns(2)
        w = col3.number_input(f"Largura (in) C{n}", min_value=0.0, step=0.1, key=f"w{n}")
        h = col4.number_input(f"Altura (in) C{n}", min_value=0.0, step=0.1, key=f"h{n}")
        
        d = vinis_db[v_tipo][v_forn]
        taxa = (d["price"] / (d["width"] * (d["yards"] * 36))) * 1.2
        return (w * h) * taxa, v_tipo

custos_vinis = []
detalhes = []

c_custo, c_nome = calcular_custo_camada(1)
custos_vinis.append(c_custo)
detalhes.append(f"C1 ({c_nome}): ${c_custo:.2f}")

for i in [2, 3, 4]:
    if st.checkbox(f"Add Camada {i}", key=f"check{i}"):
        c_custo, c_nome = calcular_custo_camada(i)
        custos_vinis.append(c_custo)
        detalhes.append(f"C{i} ({c_nome}): ${c_custo:.2f}")

# --- 💰 3. CÁLCULO E FECHAMENTO ---
st.divider()
st.write("### 💰 3. Fechamento")

custo_total_material = sum(custos_vinis)
# Preço Unitário = (Custo Base + Material) * Markup
preco_unitario = (custo_base + custo_total_material) * markup_base
total_bruto = preco_unitario * quantidade

aplicar_desconto = st.toggle("Aplicar Desconto de 10% (Promoção Zion)")

if aplicar_desconto:
    total_final = total_bruto * 0.90
    desconto_valor = total_bruto * 0.10
else:
    total_final = total_bruto
    desconto_valor = 0.0

# --- EXIBIÇÃO FINAL ---
c1, c2 = st.columns(2)
c1.metric("Preço Unitário", f"${preco_unitario:.2f}")
c2.metric("TOTAL DO PEDIDO", f"${total_final:.2f}", delta=f"-${desconto_valor:.2f}" if aplicar_desconto else None)

if aplicar_desconto:
    st.success(f"🔥 Promoção ativada! Cliente economiza ${desconto_valor:.2f}")

with st.expander("Resumo de Custos Reais (Zion Atelier)"):
    st.write(f"Custo Base do Produto: ${custo_base:.2f}")
    st.write(f"Custo Material por Unidade: ${custo_total_material:.2f}")
    st.write(f"Lucro Estimado do Pedido: ${(total_final - (custo_base + custo_total_material) * quantidade):.2f}")

st.caption("Zion Atelier - New York Style By Faith")
