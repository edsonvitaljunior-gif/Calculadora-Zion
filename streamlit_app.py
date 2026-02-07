import streamlit as st

st.set_page_config(page_title="Zion Atelier - Intelligence", page_icon="🗽")

st.title("🗽 Zion Atelier")
st.subheader("Sistema de Gestão de Custos")

# --- BANCO DE DADOS DE CAMISAS ---
fornecedores_camisas = {
    "Jiffy Shirts (Gildan Unisex)": 2.80,
    "Wordans (Gildan Unisex)": 4.94,
    "Zion Stock (Feminina Gola V)": 25.00,
    "Zion Stock (Feminina Careca)": 18.00
}

# --- BANCO DE DADOS DE VINIS (Preço por Rolo) ---
# Aqui definimos: (Preço do Rolo, Largura em pol, Comprimento em Yards)
vinis_db = {
    "EasyWeed (Siser)": {
        "GPI Supplies": {"price": 34.99, "width": 12, "yards": 5},
        "Heat Transfer Whse": {"price": 38.50, "width": 12, "yards": 5}
    },
    "Glitter (Siser)": {
        "GPI Supplies": {"price": 45.00, "width": 12, "yards": 5},
        "Heat Transfer Whse": {"price": 42.00, "width": 12, "yards": 5}
    }
}

# --- SELEÇÃO DE PRODUTO ---
st.write("### 👕 1. Escolha a Camisa")
fornecedor_camisa_sel = st.selectbox("Fornecedor da Camisa", list(fornecedores_camisas.keys()))
custo_camisa = fornecedores_camisas[fornecedor_camisa_sel]

st.divider()

# --- SELEÇÃO DE VINIL ---
st.write("### 🎨 2. Configuração do Vinil")
col_v1, col_v2 = st.columns(2)

with col_v1:
    tipo_vinil_sel = st.selectbox("Tipo de Vinil", list(vinis_db.keys()))

with col_v2:
    # Filtra os fornecedores que vendem o vinil selecionado
    fornecedores_vinil_disponiveis = list(vinis_db[tipo_vinil_sel].keys())
    fornecedor_vinil_sel = st.selectbox("Fornecedor do Vinil", fornecedores_vinil_disponiveis)

# Cálculo do custo por polegada quadrada do rolo
dados_rolo = vinis_db[tipo_vinil_sel][fornecedor_vinil_sel]
largura_rolo = dados_rolo["width"]
comprimento_pol = dados_rolo["yards"] * 36  # Converte yards para inches
area_total_rolo = largura_rolo * comprimento_pol
preco_por_sq_in = dados_rolo["price"] / area_total_rolo

st.info(f"Custo calculado deste rolo: ${preco_por_sq_in:.4f} por pol²")

st.divider()

# --- DIMENSÕES DA ARTE ---
st.write("### 📏 3. Medidas da Arte (Inches)")
def input_camada(label, key):
    c1, c2 = st.columns(2)
    w = c1.number_input(f"Largura {label}", min_value=0.0, step=0.1, key=f"w{key}")
    h = c2.number_input(f"Altura {label}", min_value=0.0, step=0.1, key=f"h{key}")
    return w * h

area1 = input_camada("Camada 1", "1")
c2_on = st.checkbox("Add Camada 2?")
area2 = input_camada("Camada 2", "2") if c2_on else 0.0
# (Pode adicionar 3 e 4 seguindo o mesmo padrão)

# --- RESULTADO ---
area_total_arte = area1 + area2
custo_material_total = area_total_arte * preco_por_sq_in
lucro_desejado = 2.5 # Multiplicador (Markup)
preco_final = custo_camisa + (custo_material_total * lucro_desejado)

st.divider()
st.metric(label="PREÇO FINAL AO CLIENTE ($)", value=f"$ {preco_final:.2f}")

with st.expander("Ver detalhes do cálculo"):
    st.write(f"Custo Camisa: ${custo_camisa:.2f}")
    st.write(f"Custo Material: ${custo_material_total:.2f}")
    st.write(f"Rolo usado: {largura_rolo}\" x {dados_rolo['yards']} yards")
