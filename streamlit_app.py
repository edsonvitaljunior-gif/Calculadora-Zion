import streamlit as st
import os

# --- 1. CONFIGURAÇÃO ---
try:
    st.set_page_config(page_title="Zion Atelier", page_icon="🗽", layout="centered")
except:
    pass

# --- 2. LOGO ---
nome_logo = "Logo Zion Atelier com fundo tranp 68%.png"
if os.path.exists(nome_logo):
   st.image(nome_logo, width=150)

# --- 3. DADOS DO PROJETO ---
st.write("### 📝 Orçamento Zion")
nome_cliente = st.text_input("Nome do Cliente", placeholder="Quem está comprando?")
nome_arte = st.text_input("Nome da Arte", placeholder="Ex: Lion Gold Puff")
arquivo_arte = st.file_uploader("Upload da Arte", type=["png", "jpg", "jpeg", "webp"], accept_multiple_files=False)

st.divider()

# --- 4. DATABASES ---
vinis_db = {
    "EasyWeed (Siser)": {"GPI Supplies": {"price": 34.99, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 37.99, "width": 12, "yards": 5}},
    "Puff Vinyl": {"GPI Supplies": {"price": 42.00, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 42.00, "width": 12, "yards": 5}},
    "Metallic": {"GPI Supplies": {"price": 30.99, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 34.99, "width": 12, "yards": 5}},
    "Holographic": {"GPI Supplies": {"price": 48.00, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 50.00, "width": 20, "yards": 5}},
    "Brick 600 (Thick)": {"GPI Supplies": {"price": 62.99, "width": 20, "yards": 5}, "Heat Transfer Whse": {"price": 39.99, "width": 12, "yards": 5}},
    "Gliter (Thick)": {"GPI Supplies": {"price": 37.99, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 37.99, "width": 12, "yards": 5}},
    "Aurora (Thick)": {"GPI Supplies": {"price": 28.49, "width": 12, "yards": 5}},
    "Easy Glow in the Dark (Thick)": {"Heat Transfer Whse": {"price": 62.99, "width": 12, "yards": 5}},
    "StripFlock Pro (Thick)": {"GPI Supplies": {"price": 35.99, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 45.00, "width": 12, "yards": 5}},
    "EasyWeed Adhesive (Thick)": {"Heat Transfer Whse": {"price": 23.50, "width": 12, "yards": 5}},
    "Easy Glow Cores (Thick)": {"Heat Transfer Whse": {"price": 52.99, "width": 12, "yards": 5}},
    "Easy Fluorecent Pro (Thick)": {"Heat Transfer Whse": {"price": 37.99, "width": 12, "yards": 5}}
}

produtos_db = {
    "CAMISAS": {
        "Gildan G500 Unisex": {"price": 2.82, "markup": 3.0},
        "Feminina Gola V": {"price": 6.37, "markup": 3.5},
        "Feminina Careca": {"price": 4.91, "markup": 3.2},
        "Kids Shirt": {"price": 3.93, "markup": 3.0},
        "Gildan G500B - Juvenil Heavy Cotton™": {"price": 2.96, "markup": 3.0}
    },
    "MOLETONS": {"Gildan G185 Hoodie": {"price": 14.50, "markup": 2.5}},
    "BONÉS": {"Snapback Classic": {"price": 5.50, "markup": 4.0}, "Trucker Hat": {"price": 4.20, "markup": 4.0}}
}

# --- 5. SELEÇÃO PRODUTO ---
st.write("### 🛍️ Produto Base")
cat = st.selectbox("Categoria", list(produtos_db.keys()))
prod = st.selectbox("Modelo", list(produtos_db[cat].keys()))
qtd = st.number_input("Quantidade de Peças", min_value=1, value=1)
c_base = produtos_db[cat][prod]["price"]
mk_base = produtos_db[cat][prod]["markup"]

st.divider()

# --- 6. CAMADAS CLICÁVEIS (Voltou!) ---
st.write("### 📏 Camadas de Estampa")
custo_vinil_total = 0.0

def config_camada(n):
    t = st.selectbox(f"Vinil Camada {n}", list(vinis_db.keys()), key=f"t{n}")
    f = st.selectbox(f"Fornecedor C{n}", list(vinis_db[t].keys()), key=f"f{n}")
    c1, c2 = st.columns(2)
    with c1: w = st.number_input(f"Largura C{n}", value=10.0, key=f"w{n}")
    with c2: h = st.number_input(f"Altura C{n}", value=10.0, key=f"h{n}")
    
    info = vinis_db[t][f]
    custo_polegada = info["price"] / (info["width"] * (info["yards"] * 36))
    return (w * h) * custo_polegada * 1.2

# Camada 1 é sempre obrigatória
st.write("📂 **Camada 1**")
custo_vinil_total += config_camada(1)

# Opções clicáveis para camadas extras
if st.checkbox("Adicionar Camada 2"):
    custo_vinil_total += config_camada(2)

if st.checkbox("Adicionar Camada 3"):
    custo_vinil_total += config_camada(3)

if st.checkbox("Adicionar Camada 4"):
    custo_vinil_total += config_camada(4)

# --- 7. CÁLCULOS ---
custo_unit_total = c_base + custo_vinil_total
total_final = (custo_unit_total * mk_base) * qtd

st.divider()

# --- 8. RESUMO E IMAGEM ---
st.subheader("🏁 Resumo")

# Tentativa de correção para o S24: Forçar exibição simples
if arquivo_arte:
    try:
        st.image(arquivo_arte, width=280)
    except:
        st.error("Erro ao carregar preview no celular")

st.info(f"👤 **Cliente:** {nome_cliente if nome_cliente else 'Zion Friend'}")

c_res1, c_res2 = st.columns(2)
c_res1.metric("Unitário", f"${(total_final/qtd):.2f}")
c_res2.metric("Total", f"${total_final:.2f}")

# --- 9. ZION ONLY ---
with st.expander("📊 Zion Only - Detalhes"):
    lucro = total_final - (custo_unit_total * qtd)
    st.write(f"Custo Peça: ${c_base:.2f}")
    st.write(f"Custo Vinis: ${custo_vinil_total:.2f}")
    st.write(f"Markup: {mk_base}x")
    st.success(f"💰 **LUCRO: ${lucro:.2f}**")

st.caption("Zion Atelier - New York Style")
