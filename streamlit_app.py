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
nome_arte = st.text_input("Nome da Arte", placeholder="Ex: NY Lion Glow")
arquivo_arte = st.file_uploader("Upload da Arte", type=["png", "jpg", "jpeg", "webp"], accept_multiple_files=False)

st.divider()

# --- 4. DATABASE DE VINIS COMPLETA (Seu Arquivo) ---
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

produtos_db = {
    "CAMISAS": {
        "Gildan G500 Unisex": {"price": 2.82, "markup": 3.0},
        "Feminina Gola V": {"price": 6.37, "markup": 3.5},
        "Feminina Careca": {"price": 4.91, "markup": 3.2},
        "Kids Shirt": {"price": 3.93, "markup": 3.0}
    },
    "MOLETONS": {
        "Gildan G185 Hoodie": {"price": 14.50, "markup": 2.5}
    },
    "BONÉS": {
        "Snapback Classic": {"price": 5.50, "markup": 4.0},
        "Trucker Hat": {"price": 4.20, "markup": 4.0}
    }
}

# --- 5. SELEÇÃO DE PRODUTO ---
st.write("### 🛍️ Escolha o Item")
categoria_selecionada = st.selectbox("Categoria", list(produtos_db.keys()))
produto_nome = st.selectbox("Modelo", list(produtos_db[categoria_selecionada].keys()))
qtd = st.number_input("Quantidade", min_value=1, value=1)

dados_prod = produtos_db[categoria_selecionada][produto_nome]
c_base = dados_prod["price"]
mk_base = dados_prod["markup"]

st.divider()

# --- 6. MEDIDAS E VINIL (Logística de Fornecedor) ---
st.write("### 📏 Medidas da Arte")
tipo_v = st.selectbox("Tipo de Vinil", list(vinis_db.keys()))

# Novo Selectbox para o Fornecedor (muda conforme o vinil escolhido)
lista_fornecedores = list(vinis_db[tipo_v].keys())
fornecedor_v = st.selectbox("Fornecedor", lista_fornecedores)

col1, col2 = st.columns(2)
with col1:
    w = st.number_input("Largura (in)", value=10.0)
with col2:
    h = st.number_input("Altura (in)", value=10.0)

# Cálculo de custo detalhado por polegada quadrada
info_v = vinis_db[tipo_v][fornecedor_v]
# Preço / (Largura do Rolo * Comprimento total em polegadas)
custo_por_polegada = info_v["price"] / (info_v["width"] * (info_v["yards"] * 36))
# Custo da área com 20% de margem de waste
custo_vinil_final = (w * h) * custo_por_polegada * 1.2

custo_unitario_total = c_base + custo_vinil_final

# --- 7. PREÇOS E PROMO ---
p_unit_sugerido = custo_unitario_total * mk_base
total_bruto = p_unit_sugerido * qtd

promo = st.toggle("Aplicar 10% de Desconto")
total_final = total_bruto * 0.9 if promo else total_bruto
p_unit_final = total_final / qtd

st.divider()

# --- 8. RESUMO PARA O CLIENTE ---
st.subheader("🏁 Resumo do Orçamento")

if arquivo_arte is not None:
    st.image(arquivo_arte, use_container_width=True)

st.info(f"👤 **Cliente:** {nome_cliente if nome_cliente else 'Zion Friend'} | 🎨 **Arte:** {nome_arte if nome_arte else 'Custom'}")

c_res1, c_res2 = st.columns(2)
c_res1.metric("Unitário", f"${p_unit_final:.2f}")
c_res2.metric("Total", f"${total_final:.2f}", delta="-10%" if promo else None)

# --- 9. 📊 ZION ONLY ---
with st.expander("📊 Detalhes Financeiros (Zion Only)"):
    lucro_total = total_final - (custo_unitario_total * qtd)
    st.write(f"Vinil: {tipo_v} ({fornecedor_v})")
    st.write(f"Custo Unit. Material: ${custo_unitario_total:.2f}")
    st.write(f"Markup Base: {mk_base}x")
    st.divider()
    st.success(f"💰 **LUCRO ESTIMADO: ${lucro_total:.2f}**")

st.caption("Zion Atelier - New York Style By Faith")
