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
nome_cliente = st.text_input("Nome do Cliente", placeholder="Quem está comprando?")
nome_arte = st.text_input("Nome da Arte", placeholder="Ex: NY Lion Glow")
arquivo_arte = st.file_uploader("Upload da Arte", type=["png", "jpg", "jpeg", "webp"], accept_multiple_files=False)

st.divider()

# --- 4. DATABASE COMPLETA DE VINIS (20% Waste Incluído) ---
vinis_db = {
    "EasyWeed (Siser)": {"GPI Supplies": {"price": 34.99, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 37.99, "width": 12, "yards": 5}},
    "Puff Vinyl": {"GPI Supplies": {"price": 42.00, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 42.00, "width": 12, "yards": 5}},
    "Metallic": {"GPI Supplies": {"price": 30.99, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 34.99, "width": 12, "yards": 5}},
    "Holographic": {"GPI Supplies": {"price": 48.00, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 50.00, "width": 20, "yards": 5}},
    "Brick 600 (Thick)": {"GPI Supplies": {"price": 62.99, "width": 20, "yards": 5}, "Heat Transfer Whse": {"price": 39.99, "width": 12, "yards": 5}},
    "Gliter (Thick)": {"GPI Supplies": {"price": 37.99, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 37.99, "width": 12, "yards": 5}},
    "Aurora (Thick)": {"GPI Supplies": {"price": 28.49, "width": 12, "yards": 5}},
    "Easy Glow Brilha no escuro (Thick)": {"Heat Transfer Whse": {"price": 62.99, "width": 12, "yards": 5}},
    "StripFlock Pro (Thick)": {"GPI Supplies": {"price": 35.99, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 45.00, "width": 12, "yards": 5}},
    "EasyWeed Adhesive para Foil (Thick)": {"Heat Transfer Whse": {"price": 23.50, "width": 12, "yards": 5}},
    "Easy Glow Brilha no escuro Cores (Thick)": {"Heat Transfer Whse": {"price": 52.99, "width": 12, "yards": 5}},
    "Easy Fluorecent Pro (Thick)": {"Heat Transfer Whse": {"price": 37.99, "width": 12, "yards": 5}}
}

# --- DATABASE DE PRODUTOS (Com Juvenil e Preços Jiffy) ---
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

# --- 5. SELEÇÃO DE PRODUTO ---
st.write("### 🛍️ Escolha o Item")
categoria_selecionada = st.selectbox("Categoria", list(produtos_db.keys()))
produto_nome = st.selectbox("Modelo", list(produtos_db[categoria_selecionada].keys()))
qtd = st.number_input("Quantidade", min_value=1, value=1)

c_base = produtos_db[categoria_selecionada][produto_nome]["price"]
mk_base = produtos_db[categoria_selecionada][produto_nome]["markup"]

st.divider()

# --- 6. CAMADAS DE VINIL (CLICÁVEIS) ---
st.write("### 📏 Medidas e Camadas")
custo_vinil_total = 0.0

def configurar_camada(n):
    st.markdown(f"**Configuração da Camada {n}**")
    tipo = st.selectbox(f"Tipo de Vinil (C{n})", list(vinis_db.keys()), key=f"tipo{n}")
    fornecedor = st.selectbox(f"Fornecedor (C{n})", list(vinis_db[tipo].keys()), key=f"forn{n}")
    
    col_w, col_h = st.columns(2)
    with col_w: w = st.number_input(f"Largura in (C{n})", value=10.0, key=f"w{n}")
    with col_h: h = st.number_input(f"Altura in (C{n})", value=10.0, key=f"h{n}")
    
    info = vinis_db[tipo][fornecedor]
    # Cálculo: Preço / (Largura do Rolo * 180 polegadas de 5 yards)
    custo_por_polegada = info["price"] / (info["width"] * 180)
    return (w * h) * custo_por_polegada * 1.2

# Camada 1 sempre visível
custo_vinil_total += configurar_camada(1)

# Checkboxes para camadas extras
if st.checkbox("Adicionar Camada 2"):
    st.divider()
    custo_vinil_total += configurar_camada(2)

if st.checkbox("Adicionar Camada 3"):
    st.divider()
    custo_vinil_total += configurar_camada(3)

# --- 7. CÁLCULOS FINAIS ---
custo_un_total = c_base + custo_vinil_total
p_unit_sugerido = custo_un_total * mk_base
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

# --- 9. 📊 ZION ONLY (DETALHAMENTO BOSS) ---
with st.expander("📊 Detalhes Financeiros (Zion Only)"):
    lucro_total = total_final - (custo_un_total * qtd)
    st.write(f"**Produto:** {produto_nome}")
    st.write(f"**Custo Peça (Jiffy):** ${c_base:.2f}")
    st.write(f"**Custo Total Vinis:** ${custo_vinil_total:.2f}")
    st.write(f"**Markup Base:** {mk_base}x")
    st.divider()
    st.success(f"💰 **LUCRO ESTIMADO NO BOLSO: ${lucro_total:.2f}**")

st.caption("Zion Atelier - New York Style By Faith")
