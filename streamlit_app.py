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
st.write("### 📝 Dados do Orçamento")
nome_cliente = st.text_input("Nome do Cliente", placeholder="Quem está comprando?")
nome_arte = st.text_input("Nome da Arte", placeholder="Ex: Lion Gold Puff")
arquivo_arte = st.file_uploader("Upload da Arte", type=["png", "jpg", "jpeg", "webp"], accept_multiple_files=False)

st.divider()

# --- 4. DATABASE COMPLETA ---
vinis_db = {
    "EasyWeed (Siser)": {"GPI": {"price": 34.99, "w": 12}, "HTW": {"price": 37.99, "w": 12}},
    "Puff Vinyl": {"GPI": {"price": 42.00, "w": 12}, "HTW": {"price": 42.00, "w": 12}},
    "Metallic": {"GPI": {"price": 30.99, "w": 12}, "HTW": {"price": 34.99, "w": 12}},
    "Holographic": {"GPI": {"price": 48.00, "w": 20}, "HTW": {"price": 50.00, "w": 20}},
    "Brick 600 (Thick)": {"GPI": {"price": 62.99, "w": 20}, "HTW": {"price": 39.99, "w": 12}},
    "Gliter (Thick)": {"GPI": {"price": 37.99, "w": 12}, "HTW": {"price": 37.99, "w": 12}},
    "Aurora (Thick)": {"GPI": {"price": 28.49, "w": 12}},
    "Glow in the Dark": {"HTW": {"price": 62.99, "w": 12}},
    "StripFlock Pro": {"GPI": {"price": 35.99, "w": 12}, "HTW": {"price": 45.00, "w": 12}},
    "Easy Adhesive/Foil": {"HTW": {"price": 23.50, "w": 12}},
    "Glow Cores": {"HTW": {"price": 52.99, "w": 12}},
    "Easy Fluorecent": {"HTW": {"price": 37.99, "w": 12}}
}

produtos_db = {
    "CAMISAS": {
        "Gildan G500 Unisex": 2.82,
        "Feminina Gola V": 6.37,
        "Feminina Careca": 4.91,
        "Kids Shirt": 3.93,
        "Gildan G500B - Juvenil": 2.96
    },
    "MOLETONS": {"Gildan G185 Hoodie": 14.50},
    "BONÉS": {"Snapback Classic": 5.50, "Trucker Hat": 4.20}
}

# --- 5. SELEÇÃO PRODUTO ---
st.write("### 🛍️ Produto Base")
cat = st.selectbox("Categoria", list(produtos_db.keys()))
prod = st.selectbox("Modelo", list(produtos_db[cat].keys()))
qtd = st.number_input("Quantidade", min_value=1, value=1)
c_base = produtos_db[cat][prod]

# Markup fixo por categoria para simplificar
markups = {"CAMISAS": 3.0, "MOLETONS": 2.5, "BONÉS": 4.0}
mk_base = markups[cat]

st.divider()

# --- 6. CAMADAS CLICÁVEIS ---
st.write("### 📏 Vinis (Clique para adicionar)")
custo_v_total = 0.0

def calc_v(label):
    st.write(f"**{label}**")
    tipo = st.selectbox(f"Tipo", list(vinis_db.keys()), key=f"t_{label}")
    forn = st.selectbox(f"Loja", list(vinis_db[tipo].keys()), key=f"f_{label}")
    c1, c2 = st.columns(2)
    with c1: w = st.number_input(f"Larg (in)", value=10.0, key=f"w_{label}")
    with c2: h = st.number_input(f"Alt (in)", value=10.0, key=f"h_{label}")
    
    preço_rolo = vinis_db[tipo][forn]["price"]
    larg_rolo = vinis_db[tipo][forn]["w"]
    # Custo sq/in considerando 5 yards (180in)
    custo_sqin = preço_rolo / (larg_rolo * 180)
    return (w * h) * custo_sqin * 1.2

custo_v_total += calc_v("Camada 1")

if st.checkbox("Adicionar Camada 2"):
    custo_v_total += calc_v("Camada 2")
if st.checkbox("Adicionar Camada 3"):
    custo_v_total += calc_v("Camada 3")

# --- 7. TOTAIS ---
custo_un = c_base + custo_v_total
p_unit = custo_un * mk_base
total_geral = p_unit * qtd

st.divider()

# --- 8. RESUMO (ESTILO ONTEM) ---
st.subheader("🏁 Resumo do Orçamento")

if arquivo_arte is not None:
    st.image(arquivo_arte, use_container_width=True)

st.info(f"👤 **Cliente:** {nome_cliente if nome_cliente else 'Zion Friend'}")

c_res1, c_res2 = st.columns(2)
c_res1.metric("Unitário", f"${p_unit:.2f}")
c_res2.metric("Total", f"${total_geral:.2f}")

# --- 9. ZION ONLY ---
with st.expander("📊 Detalhes Financeiros"):
    lucro = total_geral - (custo_un * qtd)
    st.write(f"Custo Peça: ${c_base:.2f}")
    st.write(f"Custo Vinis: ${custo_v_total:.2f}")
    st.success(f"💰 **LUCRO NO BOLSO: ${lucro:.2f}**")

st.caption("Zion Atelier - NY")
