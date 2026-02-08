import streamlit as st
import os

st.set_page_config(page_title="Zion Atelier - Multi-Material", page_icon="🗽")

# --- LOGO ---
# Certifique-se de que o arquivo no GitHub tem EXATAMENTE este nome:
nome_logo = "Logo Zion Atelier com fundo tranp 68%.png"
if os.path.exists(nome_logo):
    st.image(nome_logo, width=150)
else:
    st.title("🗽 Zion Atelier")

# --- 📦 SEU INVENTÁRIO CADASTRADO ---
vinis_db = {
    "EasyWeed (Siser)": {
        "GPI Supplies": {"price": 34.99, "width": 12, "yards": 5},
        "Heat Transfer Whse": {"price": 37.99, "width": 12, "yards": 5}
    },
    "Puff Vinyl": {
        "GPI Supplies": {"price": 42.00, "width": 12, "yards": 5},
        "Heat Transfer Whse": {"price": 42.00, "width": 12, "yards": 5}
    },
    "Metallic": {
        "GPI Supplies": {"price": 30.99, "width": 12, "yards": 5},
        "Heat Transfer Whse": {"price": 34.99, "width": 12, "yards": 5}
    },
    "Holographic": {
        "GPI Supplies": {"price": 48.00, "width": 12, "yards": 5},
        "Heat Transfer Whse": {"price": 50.00, "width": 20, "yards": 5}
    },
    "Brick 600 (Thick)": {
        "GPI Supplies": {"price": 62.99, "width": 20, "yards": 5},
        "Heat Transfer Whse": {"price": 39.99, "width": 12, "yards": 5}
    },
    "Gliter (Thick)": {
        "GPI Supplies": {"price": 37.99, "width": 12, "yards": 5},
        "Heat Transfer Whse": {"price": 37.99, "width": 12, "yards": 5}
    },
    "Aurora (Thick)": {
        "GPI Supplies": {"price": 28.49, "width": 12, "yards": 5},
    },
    "Easy Glow in the Dark / Brilha no escuro (Thick)": {
        "Heat Transfer Whse": {"price": 62.99, "width": 12, "yards": 5}
    },
    "StripFlock Pro (Thick)": {
        "GPI Supplies": {"price": 35.99, "width": 12, "yards": 5},
        "Heat Transfer Whse": {"price": 45.00, "width": 12, "yards": 5}
    },
    "EasyWeed Adhesive para Foil (Thick)": {
        "Heat Transfer Whse": {"price": 23.50, "width": 12, "yards": 5}
    },
    "Easy Glow Brilha no escuro Cores (Thick)": {
        "Heat Transfer Whse": {"price": 52.99, "width": 12, "yards": 5}
    },
    "Easy Fluorecent Pro (Thick)": {
        "Heat Transfer Whse": {"price": 37.99, "width": 12, "yards": 5}
    }
}

fornecedores_camisas = {
    "Jiffy Shirts (Gildan G500 Unisex)": 2.82,
    "Wordans (Gildan Unisex)": 4.94,
    "Jiffy Shirts G500VL (Feminina Gola V)": 6.37,
    "Jiffy Shirts G500L (Feminina Careca)": 4.91,
    "Jiffy Shirts G510P Kids Shirt": 3.93,
    "Jiffy Shirts G510B Juvenil Shirt": 3.93
}

# --- 👕 1. PRODUTO BASE ---
st.write("### 👕 1. Produto Base")
f_camisa = st.selectbox("Selecione a Camisa", list(fornecedores_camisas.keys()))
custo_camisa = fornecedores_camisas[f_camisa]

st.divider()

# --- 📏 2. CAMADAS INDEPENDENTES ---
st.write("### 📏 2. Configuração por Camada")

def calcular_custo_camada(n):
    with st.container():
        st.markdown(f"**🎨 Camada {n}**")
        col1, col2 = st.columns(2)
        with col1:
            v_tipo = st.selectbox(f"Material C{n}", list(vinis_db.keys()), key=f"tipo{n}")
        with col2:
            opcoes_f = list(vinis_db[v_tipo].keys())
            v_forn = st.selectbox(f"Fornecedor C{n}", opcoes_f, key=f"forn{n}")
        
        col3, col4 = st.columns(2)
        w = col3.number_input(f"Largura (in) C{n}", min_value=0.0, step=0.1, key=f"w{n}")
        h = col4.number_input(f"Altura (in) C{n}", min_value=0.0, step=0.1, key=f"h{n}")
        
        # Cálculo do custo/polegada específica
        d = vinis_db[v_tipo][v_forn]
        taxa = d["price"] / (d["width"] * (d["yards"] * 36))
        custo_camada = (w * h) * taxa
        return custo_camada, v_tipo

custos_vinis = []
detalhes = []

# Camada 1
c_custo, c_nome = calcular_custo_camada(1)
custos_vinis.append(c_custo)
detalhes.append(f"C1 ({c_nome}): ${c_custo:.2f}")

# Camadas Extras
if st.checkbox("Habilitar Camada 2"):
    st.divider()
    c_custo, c_nome = calcular_custo_camada(2)
    custos_vinis.append(c_custo)
    detalhes.append(f"C2 ({c_nome}): ${c_custo:.2f}")

if st.checkbox("Habilitar Camada 3"):
    st.divider()
    c_custo, c_nome = calcular_custo_camada(3)
    custos_vinis.append(c_custo)
    detalhes.append(f"C3 ({c_nome}): ${c_custo:.2f}")

if st.checkbox("Habilitar Camada 4"):
    st.divider()
    c_custo, c_nome = calcular_custo_camada(4)
    custos_vinis.append(c_custo)
    detalhes.append(f"C4 ({c_nome}): ${c_custo:.2f}")

# --- 💰 RESULTADO FINAL ---
markup = 3.0 
custo_total_material = sum(custos_vinis)
total_final = custo_camisa + (custo_total_material * markup)

st.divider()
st.metric(label="PREÇO FINAL ESTIMADO ($)", value=f"$ {total_final:.2f}")

with st.expander("Resumo de Custos"):
    st.write(f"Camisa: ${custo_camisa:.2f}")
    for d in detalhes:
        st.write(d)
    st.write(f"Custo Real Material Total: ${custo_total_material:.2f}")

st.caption("Zion Atelier - New York Style By Faith")
