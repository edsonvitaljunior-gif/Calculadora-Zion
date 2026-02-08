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
nome_cliente = st.text_input("Nome do Cliente", placeholder="Ex: John Doe")
nome_arte = st.text_input("Nome da Arte", placeholder="Ex: NY Lion")

# Upload com a configuração que funcionou no seu buffer
arquivo_arte = st.file_uploader("Upload da Arte", type=["png", "jpg", "jpeg", "webp"], accept_multiple_files=False)

st.divider()

# --- 4. DATABASE DE VINIS ---
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

# --- DATABASE DE PRODUTOS (Com Juvenil Shirts) ---
produtos_db = {
    "CAMISAS": {
        "Gildan G500 Unisex": {"price": 2.82, "markup": 3.0},
        "Feminina Gola V": {"price": 6.37, "markup": 3.5},
        "Feminina Careca": {"price": 4.91, "markup": 3.2},
        "Kids Shirt": {"price": 3.93, "markup": 3.0},
        "Juvenil Shirt": {"price": 4.50, "markup": 3.0}
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
custo_peca_mais_vinil = c_base + custo_vinil_un

p_unit_sug = custo_peca_mais_vinil * mk_base
total_bruto = p_unit_sug * qtd

promo = st.toggle("Aplicar 10% de Desconto")
total_final = total_bruto * 0.9 if promo else total_bruto
p_unit_final = total_final / qtd

st.divider()

# --- 7. RESUMO CLIENTE (Com Fix de Imagem para Celular) ---
st.subheader("🏁 Resumo do Orçamento")

if arquivo_arte:
    # width=300 mantém a imagem pequena e leve para o S24 carregar rápido
    st.image(arquivo_arte, width=300, caption="Preview da Arte")

st.info(f"👤 **Cliente:** {nome_cliente if nome_cliente else 'Zion Friend'}\n\n🎨 **Projeto:** {nome_arte if nome_arte else 'Custom'}")

c_res1, c_res2 = st.columns(2)
c_res1.metric("Unitário", f"${p_unit_final:.2f}")
c_res2.metric("Total", f"${total_final:.2f}", delta="-10%" if promo else None)

# --- 8. DETALHAMENTO FINANCEIRO (BOSS MODE) ---
with st.expander("📊 Zion Only - Detalhes do Lucro"):
    custo_material_total = custo_peca_mais_vinil * qtd
    lucro_total = total_final - custo_material_total
    
    st.write(f"**Item:** {prod}")
    st.write(f"**Vinil:** {tipo_v} ({forn_v})")
    st.divider()
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("💸 **Custos Unitários:**")
        st.write(f"Peça: ${c_base:.2f}")
        st.write(f"Vinil: ${custo_vinil_un:.2f}")
        st.write(f"Soma Custo/Un: **${custo_peca_mais_vinil:.2f}**")
    
    with col_b:
        st.write("📈 **Performance:**")
        st.write(f"Markup: {mk_base}x")
        st.write(f"Quantidade: {qtd}")
    
    st.divider()
    st.success(f"💰 **LUCRO NO BOLSO: ${lucro_total:.2f}**")

st.caption("Zion Atelier - New York Style By Faith")
