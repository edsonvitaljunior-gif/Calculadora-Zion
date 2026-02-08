import streamlit as st
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
nome_logo = "Logo Zion Atelier com fundo tranp 68%.png"

# Verificamos se o arquivo existe para definir o ícone da aba
if os.path.exists(nome_logo):
    fav_icon = nome_logo
else:
    fav_icon = "🗽"

st.set_page_config(
    page_title="Zion Atelier - Sales Pro", 
    page_icon=fav_icon,
    layout="centered"
)

# --- EXIBIÇÃO DA LOGO NO TOPO ---
if os.path.exists(nome_logo):
    st.image(nome_logo, width=150)
else:
    st.title("🗽 Zion Atelier")

# --- DATABASE DE VINIS (20% Waste Incluído) ---
vinis_db = {
    "EasyWeed (Siser)": {"GPI Supplies": {"price": 34.99, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 37.99, "width": 12, "yards": 5}},
    "Puff Vinyl": {"GPI Supplies": {"price": 42.00, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 42.00, "width": 12, "yards": 5}},
    "Metallic": {"GPI Supplies": {"price": 30.99, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 34.99, "width": 12, "yards": 5}},
    "Holographic": {"GPI Supplies": {"price": 48.00, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 50.00, "width": 20, "yards": 5}},
    "Brick 600 (Thick)": {"GPI Supplies": {"price": 62.99, "width": 20, "yards": 5}, "Heat Transfer Whse": {"price": 39.99, "width": 12, "yards": 5}},
    "Gliter (Thick)": {"GPI Supplies": {"price": 37.99, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 37.99, "width": 12, "yards": 5}},
    "Aurora (Thick)": {"GPI Supplies": {"price": 28.49, "width": 12, "yards": 5}},
    "Easy Glow in the Dark / Brilha no escuro (Thick)": {"Heat Transfer Whse": {"price": 62.99, "width": 12, "yards": 5}},
    "StripFlock Pro (Thick)": {"GPI Supplies": {"price": 35.99, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 45.00, "width": 12, "yards": 5}},
    "EasyWeed Adhesive para Foil (Thick)": {"Heat Transfer Whse": {"price": 23.50, "width": 12, "yards": 5}},
    "Easy Glow Brilha no escuro Cores (Thick)": {"Heat Transfer Whse": {"price": 52.99, "width": 12, "yards": 5}},
    "Easy Fluorecent Pro (Thick)": {"Heat Transfer Whse": {"price": 37.99, "width": 12, "yards": 5}}
}

# --- 👕 DATABASE DE CAMISAS ---
fornecedores_camisas = {
    "Jiffy Shirts (Gildan G500 Unisex)": {"price": 2.82, "markup": 3.0},
    "Wordans (Gildan Unisex)": {"price": 4.94, "markup": 3.0},
    "Jiffy Shirts G500VL (Feminina Gola V)": {"price": 6.37, "markup": 3.5},
    "Jiffy Shirts G500L (Feminina Careca)": {"price": 4.91, "markup": 3.2},
    "Jiffy Shirts G510P Kids Shirt": {"price": 3.93, "markup": 3.0},
    "Jiffy Shirts G510B Juvenil Shirt": {"price": 3.93, "markup": 3.0}
}

# --- 👕 1. PRODUTO E QUANTIDADE ---
st.write("### 👕 1. Pedido Principal")
col_cam, col_qtd = st.columns([2, 1])

with col_cam:
    f_camisa = st.selectbox("Modelo da Camisa", list(fornecedores_camisas.keys()))
    custo_camisa = fornecedores_camisas[f_camisa]["price"]
    markup_camisa = fornecedores_camisas[f_camisa]["markup"]

with col_qtd:
    quantidade = st.number_input("Qtd Camisas", min_value=1, step=1, value=1)

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
        w = col3.number_input(f"Width (in) C{n}", min_value=0.0, step=0.1, key=f"w{n}")
        h = col4.number_input(f"Height (in) C{n}", min_value=0.0, step=0.1, key=f"h{n}")
        
        d = vinis_db[v_tipo][v_forn]
        taxa = (d["price"] / (d["width"] * (d["yards"] * 36))) * 1.2
        return (w * h) * taxa, v_tipo

custos_vinis = []
detalhes = []

# Camada 1
c_custo, c_nome = calcular_custo_camada(1)
custos_vinis.append(c_custo)
detalhes.append(f"C1 ({c_nome}): ${c_custo:.2f}")

# Camadas Opcionais
for i in [2, 3, 4]:
    if st.checkbox(f"Add Camada {i}", key=f"check{i}"):
        c_custo, c_nome = calcular_custo_camada(i)
        custos_vinis.append(c_custo)
        detalhes.append(f"C{i} ({c_nome}): ${c_custo:.2f}")

# --- 💰 CÁLCULO E PROMOÇÃO ---
st.divider()
st.write("### 💰 3. Fechamento")

custo_total_material = sum(custos_vinis)
preco_unitario = (custo_camisa + custo_total_material) * markup_camisa
total_bruto = preco_unitario * quantidade

aplicar_desconto = st.toggle("Aplicar Desconto de 10% (Promoção Combo)")

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
    st.success(f"🔥 Desconto de 10% aplicado!")

with st.expander("Ver detalhes do custo real"):
    st.write(f"Custo Real Camisa (un): ${custo_camisa:.2f}")
    st.write(f"Custo Real Material (un): ${custo_total_material:.2f}")
    st.write(f"Seu Lucro Estimado: ${(total_final - (custo_camisa + custo_total_material) * quantidade):.2f}")

st.caption("Zion Atelier - New York Style By Faith")
