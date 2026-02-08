import streamlit as st
import os
# No topo do código, logo após os imports, adicione essa configuração
# Isso ajuda o Streamlit a lidar melhor com o buffer de arquivos grandes do Android
st.config.set_option("server.maxUploadSize", 20) # Aumenta para 20MB por segurança

# E no campo de upload, vamos deixar ele o mais aberto possível:
arquivo_arte = st.file_uploader("Upload da Arte", type=["png", "jpg", "jpeg", "webp"], accept_multiple_files=False)
# --- CONFIGURAÇÃO DA PÁGINA ---
nome_logo = "Logo Zion Atelier com fundo tranp 68%.png"
fav_icon = nome_logo if os.path.exists(nome_logo) else "🗽"

st.set_page_config(
    page_title="Zion Atelier - Pro Manager", 
    page_icon=fav_icon,
    layout="centered"
)

# --- EXIBIÇÃO DA LOGO NO TOPO ---
if os.path.exists(nome_logo):
    st.image(nome_logo, width=150)
else:
    st.title("🗽 Zion Atelier")

# --- 📋 1. IDENTIFICAÇÃO DO PROJETO (Vertical para não bagunçar) ---
st.write("### 📝 Dados do Orçamento")
nome_cliente = st.text_input("Nome do Cliente", placeholder="Ex: John Doe")
nome_arte = st.text_input("Nome da Arte / Projeto", placeholder="Ex: NY Faith 2026")
arquivo_arte = st.file_uploader("Upload da Arte (Opcional)", type=["png", "jpg", "jpeg", "webp"])

st.divider()

# ... (restante do código igual) ...

# --- 🏁 RESUMO PARA O CLIENTE (Ajustado para Celular) ---
st.subheader("🏁 Resumo do Orçamento")

# Mostra a imagem primeiro no celular para dar destaque
if arquivo_arte is not None:
    st.image(arquivo_arte, use_container_width=True)
    st.caption("🎨 Preview do Projeto")

st.info(f"👤 **Cliente:** {nome_cliente if nome_cliente else 'Friend of Zion'} \n\n🎨 **Projeto:** {nome_arte if nome_arte else 'Custom Design'}")

col_res1, col_res2 = st.columns(2)
with col_res1:
    st.metric("Preço Unitário", f"${p_unit:.2f}")
with col_res2:
    st.metric("TOTAL", f"${total_final:.2f}", delta=f"-10%" if promo else None)
# --- 📦 DATABASE DE VINIS ---
vinis_db = {
    "EasyWeed (Siser)": {"GPI Supplies": {"price": 34.99, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 37.99, "width": 12, "yards": 5}},
    "Puff Vinyl": {"GPI Supplies": {"price": 42.00, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 42.00, "width": 12, "yards": 5}},
    "Metallic": {"GPI Supplies": {"price": 30.99, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 34.99, "width": 12, "yards": 5}},
    "Holographic": {"GPI Supplies": {"price": 48.00, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 50.00, "width": 20, "yards": 5}},
    "Brick 600 (Thick)": {"GPI Supplies": {"price": 62.99, "width": 20, "yards": 5}, "Heat Transfer Whse": {"price": 39.99, "width": 12, "yards": 5}},
    "Gliter (Thick)": {"GPI Supplies": {"price": 37.99, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 37.99, "width": 12, "yards": 5}},
    "Aurora (Thick)": {"GPI Supplies": {"price": 28.49, "width": 12, "yards": 5}},
    "Easy Glow in the Dark (Thick)": {"Heat Transfer Whse": {"price": 62.99, "width": 12, "yards": 5}},
    "StripFlock Pro (Thick)": {"GPI Supplies": {"price": 35.99, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 45.00, "width": 12, "yards": 5}}
}

# --- 🛍️ DATABASE DE PRODUTOS (Corrigido) ---
produtos_db = {
    "CAMISAS": {
        "Gildan G500 Unisex (Jiffy)": {"price": 2.82, "markup": 3.0},
        "Feminina Gola V G500VL (Jiffy)": {"price": 6.37, "markup": 3.5},
        "Feminina Careca G500L (Jiffy)": {"price": 4.91, "markup": 3.2},
        "Kids Shirt G510P (Jiffy)": {"price": 3.93, "markup": 3.0}
    },
    "MOLETONS (HOODIES)": {
        "Gildan G185 Hoodie (Jiffy)": {"price": 14.50, "markup": 2.5}
    },
    "BONÉS (HATS)": {
        "Snapback Classic (Jiffy)": {"price": 5.50, "markup": 4.0},
        "Trucker Hat (Jiffy)": {"price": 4.20, "markup": 4.0}
    }
}

# --- 🛍️ 2. SELEÇÃO DO PRODUTO ---
st.write("### 🛍️ 2. Detalhes do Produto")
cat = st.selectbox("Categoria", list(produtos_db.keys()))
prod = st.selectbox("Modelo", list(produtos_db[cat].keys()))
qtd = st.number_input("Quantidade de Itens", min_value=1, value=1)

c_base = produtos_db[cat][prod]["price"]
mk_base = produtos_db[cat][prod]["markup"]

st.divider()

# --- 📏 3. MATERIAIS ---
st.write("### 📏 3. Materiais")

def calc_camada(n):
    with st.expander(f"Configurar Camada {n}", expanded=(n==1)):
        c1, c2 = st.columns(2)
        tipo = c1.selectbox(f"Material C{n}", list(vinis_db.keys()), key=f"t{n}")
        forn = c2.selectbox(f"Fornecedor C{n}", list(vinis_db[tipo].keys()), key=f"f{n}")
        c3, c4 = st.columns(2)
        w = c3.number_input(f"Largura (in) C{n}", min_value=0.0, step=0.1, key=f"w{n}")
        h = c4.number_input(f"Altura (in) C{n}", min_value=0.0, step=0.1, key=f"h{n}")
        d = vinis_db[tipo][forn]
        taxa = (d["price"] / (d["width"] * (d["yards"] * 36))) * 1.2
        return (w * h) * taxa, tipo

custos, nomes = [], []
for i in range(1, 5):
    if i == 1 or st.checkbox(f"Add Camada {i}", key=f"cb{i}"):
        v, n = calc_camada(i)
        custos.append(v)
        nomes.append(n)

# --- 💰 4. CÁLCULOS FINAIS ---
st.divider()
total_mat = sum(custos)
p_unit = (c_base + total_mat) * mk_base
total_bruto = p_unit * qtd

st.write("### 💰 4. Fechamento e Desconto")
promo = st.toggle("Aplicar Desconto Especial (10% OFF)")
total_final = total_bruto * 0.9 if promo else total_bruto

# --- 🏁 RESUMO COM IMAGEM ---
st.subheader("🏁 Resumo do Orçamento")

res_col1, res_col2 = st.columns([1.5, 1])

with res_col1:
    st.info(f"👤 **Cliente:** {nome_cliente if nome_cliente else 'Friend of Zion'} \n\n🎨 **Projeto:** {nome_arte if nome_arte else 'Custom Design'}")
    st.metric("Preço Unitário", f"${p_unit:.2f}")
    st.metric("TOTAL DO PEDIDO", f"${total_final:.2f}", delta=f"-10%" if promo else None)

with res_col2:
    # O SEGREDO ESTÁ AQUI: 
    if arquivo_arte is not None:
        # Mostra a imagem que foi carregada lá no topo
        st.image(arquivo_arte, caption="Preview da Arte", use_container_width=True)
    else:
        st.warning("🖼️ Aguardando imagem...")

with st.expander("📊 Detalhes Técnicos (Zion Only)"):
    lucro_total = total_final - ((c_base + total_mat) * qtd)
    st.write(f"Custo Real Unitário: ${(c_base + total_mat):.2f}")
    st.write(f"**LUCRO LÍQUIDO NO PEDIDO: ${lucro_total:.2f}**")

st.caption("Zion Atelier - New York Style By Faith")
