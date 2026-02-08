import streamlit as st
import os

# --- 1. CONFIGURAÇÃO S24 (Forçando o buffer) ---
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

# --- 5. SELEÇÃO DO PRODUTO ---
st.write("### 🛍️ Produto Base")
cat = st.selectbox("Categoria", list(produtos_db.keys()))
prod = st.selectbox("Modelo", list(produtos_db[cat].keys()))
qtd = st.number_input("Quantidade de Peças", min_value=1, value=1)

c_base = produtos_db[cat][prod]["price"]
mk_base = produtos_db[cat][prod]["markup"]

st.divider()

# --- 6. CAMADAS DE VINIL (As 4 voltaram!) ---
st.write("### 📏 Camadas de Vinil")
n_camadas = st.slider("Quantas cores/camadas de vinil?", 1, 4, 1)

custo_vinil_total_un = 0.0

for i in range(n_camadas):
    with st.expander(f"Camada {i+1}", expanded=(i==0)):
        tipo_v = st.selectbox(f"Tipo Vinil C{i+1}", list(vinis_db.keys()), key=f"v{i}")
        forn_v = st.selectbox(f"Fornecedor C{i+1}", list(vinis_db[tipo_v].keys()), key=f"f{i}")
        
        c1, c2 = st.columns(2)
        with c1: w = st.number_input(f"Largura C{i+1}", value=10.0, key=f"w{i}")
        with c2: h = st.number_input(f"Altura C{i+1}", value=10.0, key=f"h{i}")
        
        info = vinis_db[tipo_v][forn_v]
        custo_sqin = info["price"] / (info["width"] * (info["yards"] * 36))
        custo_camada = (w * h) * custo_sqin * 1.2
        custo_vinil_total_un += custo_camada
        st.write(f"Custo desta camada: ${custo_camada:.2f}")

# --- 7. CÁLCULO FINAL ---
custo_un_total = c_base + custo_vinil_total_un
p_unit_final = custo_un_total * mk_base
total_geral = p_unit_final * qtd

st.divider()

# --- 8. RESUMO ---
st.subheader("🏁 Resumo do Pedido")

# TENTATIVA FINAL PARA A FOTO:
if arquivo_arte is not None:
    # Mudamos o método de renderização para ver se o S24 aceita
    st.image(arquivo_arte, use_container_width=True)
    st.caption("✅ Imagem processada pelo servidor")

st.info(f"👤 **Cliente:** {nome_cliente if nome_cliente else 'Zion Friend'}")

col_res1, col_res2 = st.columns(2)
col_res1.metric("Unitário", f"${p_unit_final:.2f}")
col_res2.metric("Total", f"${total_geral:.2f}")

# --- 9. ZION ONLY ---
with st.expander("📊 Detalhes Financeiros"):
    lucro = total_geral - (custo_un_total * qtd)
    st.write(f"Custo Peça: ${c_base:.2f}")
