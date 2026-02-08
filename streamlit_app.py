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
    st.image(nome_logo, width=120)

# --- 3. DADOS DO PROJETO ---
st.write("### 📝 Dados do Orçamento")
nome_cliente = st.text_input("Nome do Cliente", placeholder="Ex: John Doe")
nome_arte = st.text_input("Nome da Arte", placeholder="Ex: NY Lion")

# Upload
arquivo_arte = st.file_uploader("Upload da Arte", type=["png", "jpg", "jpeg", "webp"], accept_multiple_files=False)

# --- TRUQUE PARA CELULAR: CONTAINER FIXO ---
placeholder_imagem = st.container()

if arquivo_arte is not None:
    with placeholder_imagem:
        # Usamos uma técnica de exibição direta
        st.write("📸 **Preview da Arte:**")
        # O parâmetro 'use_container_width=False' com 'width=280' ajuda o mobile
        st.image(arquivo_arte, width=280)
        st.success("✅ Imagem carregada!")
else:
    st.warning("⚠️ Aguardando upload da arte...")

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
    "MOLETONS": {
        "Gildan G185 Hoodie": {"price": 14.50, "markup": 2.5}
    },
    "BONÉS": {
        "Snapback Classic": {"price": 5.50, "markup": 4.0},
        "Trucker Hat": {"price": 4.20, "markup": 4.0}
    }
}

# --- 5. SELEÇÃO ---
st.write("### 🛍️ Escolha o Item")
cat = st.selectbox("Categoria", list(produtos_db.keys()))
prod = st.selectbox("Modelo", list(produtos_db[cat].keys()))
qtd = st.number_input("Quantidade", min_value=1, value=1)

c_base = produtos_db[cat][prod]["price"]
mk_base = produtos_db[cat][prod]["markup"]

st.divider()

# --- 6. ESTAMPA ---
st.write("### 📏 Medidas da Arte")
tipo_v = st.selectbox("Tipo de Vinil", list(vinis_db.keys()))
forn_v = st.selectbox("Fornecedor", list(vinis_db[tipo_v].keys()))

col1, col2 = st.columns(2)
with col1:
    w = st.number_input("Largura (in)", value=10.0)
with col2:
    h = st.number_input("Altura (in)", value=10.0)

# Cálculos
info_v = vinis_db[tipo_v][forn_v]
custo_sq_in = info_v["price"] / (info_v["width"] * (info_v["yards"] * 36))
custo_vinil_un = (w * h) * custo_sq_in * 1.2
custo_total_un = c_base + custo_vinil_un

total_bruto = (custo_total_un * mk_base) * qtd
promo = st.toggle("Aplicar 10% de Desconto")
total_final = total_bruto * 0.9 if promo else total_bruto
p_unit_final = total_final / qtd

st.divider()

# --- 7. RESUMO FINAL ---
st.subheader("🏁 Resumo")
st.info(f"👤 **Cliente:** {nome_cliente if nome_cliente else 'Zion Friend'}\n\n🎨 **Projeto:** {nome_arte if nome_arte else 'Custom'}")

col_res1, col_res2 = st.columns(2)
col_res1.metric("Unitário", f"${p_unit_final:.2f}")
col_res2.metric("Total", f"${total_final:.2f}")

# --- 8. DETALHAMENTO (BOSS MODE) ---
with st.expander("📊 Zion Only - Detalhes"):
    lucro = total_final - (custo_total_un * qtd)
    st.write(f"Custo Unitário: ${custo_total_un:.2f}")
    st.success(f"💰 **LUCRO: ${lucro:.2f}**")

st.caption("Zion Atelier - New York")
