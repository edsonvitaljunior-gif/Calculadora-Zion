import streamlit as st
import os
import urllib.parse

# --- 1. CONFIGURAÇÃO & TEMA PREMIUM DARK GOLD ---
try:
    st.set_page_config(page_title="Zion Atelier - Master", page_icon="🗽", layout="centered")
except:
    pass

# CSS TOTAL GOLD: Fundo Preto Absoluto e Letras Douradas
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    h1, h2, h3, p, span, label, .stMarkdown { color: #d4af37 !important; }
    ::placeholder { color: rgba(212, 175, 55, 0.6) !important; opacity: 1; }
    input::placeholder { color: rgba(212, 175, 55, 0.6) !important; }
    [data-testid="stFileUploaderDropzone"] { border: 2px dashed #d4af37 !important; border-radius: 15px !important; }
    [data-testid="stFileUploader"] button { background-color: #d4af37 !important; color: #000000 !important; font-weight: bold !important; box-shadow: 0px 4px 0px #b38f2d !important; }
    div[data-testid="metric-container"] { background-color: #111111; border: 2px solid #d4af37; padding: 15px; border-radius: 12px; }
    .wa-button {
        display: block;
        text-align: center;
        background-color: #25d366 !important;
        color: white !important;
        font-weight: bold !important;
        padding: 12px;
        border-radius: 8px;
        text-decoration: none;
        box-shadow: 0px 4px 0px #128c7e !important;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. LOGO ---
nome_logo = "logo.png"
if os.path.exists(nome_logo):
   st.image(nome_logo, width=150)

# --- 3. CONTROLE DE ESTOQUE ---
if 'estoque' not in st.session_state:
    st.session_state.estoque = {
        "Gildan G500": 50, "Onesie Baby": 20, "G185 Hoodie": 15, "Vinyl Puff": 10
    }

# --- 4. DADOS DO PROJETO ---
st.write("### 📝 Solicitação de Orçamento")
nome_client = st.text_input("Nome do Cliente", placeholder="Ex: John Doe")
nome_art = st.text_input("Nome da Arte", placeholder="Ex: Zion Legacy Lion")
arquivo_art = st.file_uploader("Upload da Arte", type=["png", "jpg", "jpeg", "webp"])

if arquivo_art is not None:
    st.image(arquivo_art, use_container_width=True)

st.divider()

# --- 5. DATABASE COMPLETA ---
vinis_db = {
    "EasyWeed HTV (Siser)": {"GPI Supplies": {"price": 34.99, "width": 12}, "Heat Transfer Whse": {"price": 37.99, "width": 12}},
    "Puff Vinyl (3D)": {"GPI Supplies": {"price": 42.00, "width": 12}, "Heat Transfer Whse": {"price": 42.00, "width": 12}},
    "Metallic Gold/Silver": {"GPI Supplies": {"price": 30.99, "width": 12}, "Heat Transfer Whse": {"price": 34.99, "width": 12}},
    "Easy Glow (Dark)": {"Heat Transfer Whse": {"price": 62.99, "width": 12}},
    "Reflective Safety": {"GPI Supplies": {"price": 45.00, "width": 12}},
    "Holographic": {"GPI Supplies": {"price": 48.00, "width": 12}, "Heat Transfer Whse": {"price": 50.00, "width": 20}},
    "Brick 600 (Thick)": {"GPI Supplies": {"price": 62.99, "width": 20}, "Heat Transfer Whse": {"price": 39.99, "width": 12}},
    "Gliter (Thick)": {"GPI Supplies": {"price": 37.99, "width": 12}},
    "StripFlock Pro": {"GPI Supplies": {"price": 35.99, "width": 12}}
}

# DATABASE ATUALIZADA COM AVENTAIS E BONÉS REORGANIZADOS
produtos_db = {
    "1. TRABALHO (UNIFORMES)": {
        "Gildan G500 Heavy Cotton": {"price": 2.82, "markup": 2.5},
        "Feminina G500L Crewneck": {"price": 4.91, "markup": 2.5},
        "Polo Básica Workwear": {"price": 7.50, "markup": 2.5},
        "Avental Profissional (House Cleaner/Work)": {"price": 6.80, "markup": 2.8},
        "Trucker Hat Econômico (Uniforme)": {"price": 3.20, "markup": 3.0}
    },
    "2. URBAN STREETWEAR": {
        "Gildan G185 Hoodie": {"price": 13.77, "markup": 3.0},
        "Daddy/Mommy Oversized": {"price": 12.00, "markup": 3.0},
        "Feminina G500VL V-Neck": {"price": 6.37, "markup": 3.2},
        "Snapback Classic": {"price": 5.50, "markup": 4.0},
        "Trucker Hat Premium": {"price": 4.20, "markup": 4.0}
    },
    "3. LINHA LUXO (ZION PREMIUM)": {
        "Camiseta Zion Premium Pima": {"price": 15.50, "markup": 4.0},
        "Moletom Zion Luxury Heavy": {"price": 28.00, "markup": 4.0},
        "Onesie Baby Luxury Edition": {"price": 6.50, "markup": 4.5},
        "Avental Luxo Canvas/Couro (Zion Chef/Atelier)": {"price": 18.50, "markup": 4.0}
    }
}

# --- 6. SELEÇÃO DE ITEM ---
st.write("### 🛍️ Configure seu Item")
cat_sel = st.selectbox("Linha de Produto", list(produtos_db.keys()))
prod_nome = st.selectbox("Modelo", list(produtos_db[cat_sel].keys()))

c_base = produtos_db[cat_sel][prod_nome]["price"]
mk_base = produtos_db[cat_sel][prod_nome]["markup"]
qtd = st.number_input("Quantidade de Peças", min_value=1, value=12, step=1)

st.divider()

# --- 7. SELEÇÃO DA TÉCNICA DE ESTAMPARIA ---
st.write("### 🎨 Técnica de Estamparia")
tecnica = st.radio("Escolha a Técnica:", ["Apenas Vinil de Recorte", "Apenas Silk Screen (Serigrafia)", "Misto (Silk Screen + Vinil HTV)"])

total_custo_vinil = 0.0
custo_serigrafia_total = 0.0
detalhes_camadas = []
custo_telas_detalhe = 0.0
custo_tinta_detalhe = 0.0
num_telas = 1

# --- FUNÇÃO PARA CONFIGURAR CAMADAS DE VINIL ---
def configurar_camada(n):
    st.markdown(f"**Camada de Vinil {n}**")
    tipo = st.selectbox(f"Tipo de Vinil (C{n})", list(vinis_db.keys()), key=f"tipo{n}")
    forn = st.selectbox(f"Fornecedor (C{n})", list(vinis_db[tipo].keys()), key=f"forn{n}")
    col_w, col_h = st.columns(2)
    with col_w: w = st.number_input(f"Largura (in) {n}", value=5.0, key=f"w{n}")
    with col_h: h = st.number_input(f"Altura (in) {n}", value=5.0, key=f"h{n}")
    
    info = vinis_db[tipo][forn]
    custo_polegada = info["price"] / (info["width"] * 180) 
    custo_da_camada = (w * h) * custo_polegada * 1.3
    
    detalhes_camadas.append({"n": n, "tipo": tipo, "custo": custo_da_camada})
    return custo_da_camada

st.divider()

# --- LÓGICA DE EXIBIÇÃO DOS CAMPOS DE ACORDO COM A TÉCNICA ---
if tecnica == "Apenas Vinil de Recorte":
    st.write("### 📏 Detalhamento das Camadas de Vinil")
    total_custo_vinil += configurar_camada(1)
    if st.checkbox("Adicionar Camada 2"):
        st.divider(); total_custo_vinil += configurar_camada(2)
    if st.checkbox("Adicionar Camada 3"):
        st.divider(); total_custo_vinil += configurar_camada(3)
    if st.checkbox("Adicionar Camada 4"):
        st.divider(); total_custo_vinil += configurar_camada(4)

elif tecnica == "Apenas Silk Screen (Serigrafia)":
    st.write("### 🖼️ Configuração da Serigrafia")
    num_telas = st.slider("Quantidade de Cores (1 cor = 1 tela)", min_value=1, max_value=6, value=1)
    custo_por_tela = st.number_input("Custo de Gravação por Tela ($)", min_value=0.0, value=15.0)
    custo_tinta_peca = st.number_input("Custo de Tinta Estimado por Peça ($)", min_value=0.0, value=0.50)
    
    custo_telas_detalhe = num_telas * custo_por_tela
    custo_tinta_detalhe = custo_tinta_peca * num_telas
    custo_serigrafia_total = (custo_telas_detalhe / qtd) + custo_tinta_detalhe

else: # MISTO
    st.write("### 🖼️ Parte 1: Base em Serigrafia")
    num_telas = st.slider("Quantidade de Cores no Silk (1 cor = 1 tela)", min_value=1, max_value=6, value=1)
    custo_por_tela = st.number_input("Custo de Gravação por Tela ($)", min_value=0.0, value=15.0)
    custo_tinta_peca = st.number_input("Custo de Tinta por Peça ($)", min_value=0.0, value=0.50)
    
    custo_telas_detalhe = num_telas * custo_por_tela
    custo_tinta_detalhe = custo_tinta_peca * num_telas
    custo_serigrafia_total = (custo_telas_detalhe / qtd) + custo_tinta_detalhe
    
    st.divider()
    st.write("### 📏 Parte 2: Detalhes em Vinil HTV")
    total_custo_vinil += configurar_camada(1)
    if st.checkbox("Adicionar Camada de Vinil 2"):
        st.divider(); total_custo_vinil += configurar_camada(2)
    if st.checkbox("Adicionar Camada de Vinil 3"):
        st.divider(); total_custo_vinil += configurar_camada(3)

# --- 8. CÁLCULOS FINAIS ---
custo_un_total = c_base + total_custo_vinil + custo_serigrafia_total
p_unit_sugerido = custo_un_total * mk_base
total_bruto = p_unit_sugerido * qtd

# --- CONTROLE BOSS ---
SENHA_BOSS = "1234"
desconto_aplicado = 0.0
acesso = ""

with st.sidebar:
    st.subheader("🔐 Painel Administrativo")
    acesso = st.text_input("Chave", type="password")
    if acesso == SENHA_BOSS:
        st.success("Welcome, Boss Edson!")
        if st.toggle("Desconto 10%"):
            desconto_aplicado = 0.10
        st.write("---")
        st.write("📦 **Estoque Rápido**")
        for item, valor in st.session_state.estoque.items():
            st.write(f"{item}: {valor} un")

total_final = total_bruto * (1 - desconto_aplicado)
p_unit_final = total_final / qtd

st.divider()

# --- 9. RESUMO DE INVESTIMENTO ---
st.subheader("🏁 Valor do Investimento")
col_res1, col_res2 = st.columns(2)
col_res1.metric("Unitário", f"${p_unit_final:.2f}")
col_res2.metric("Total", f"${total_final:.2f}")

detalhe_silk_msg = f" ({num_telas} Cores)" if "Silk" in tecnica else ""
msg = f"🗽 *ZION ATELIER - NY STYLE*\n\n" \
      f"Olá {nome_client}! Segue o orçamento para o seu projeto:\n\n" \
      f"🖼️ *Arte:* {nome_art}\n" \
      f"👕 *Item:* {prod_nome} ({cat_sel})\n" \
      f"🎨 *Técnica:* {tecnica}{detalhe_silk_msg}\n" \
      f"🔢 *Qtd:* {qtd}\n" \
      f"💰 *Investimento:* ${total_final:.2f}\n\n" \
      f"Podemos avançar?"

msg_encoded = urllib.parse.quote(msg)
link_whatsapp = f"https://wa.me/?text={msg_encoded}"
st.markdown(f'<a href="{link_whatsapp}" target="_blank" class="wa-button">ENVIAR PARA WHATSAPP</a>', unsafe_allow_html=True)

# --- 10. ÁREA TÉCNICA ---
if acesso == SENHA_BOSS:
    with st.expander("📊 Detalhes Financeiros"):
        st.write(f"**Linha Selecionada:** {cat_sel}")
        st.write(f"**Peça Base ({prod_nome}):** ${c_base:.2f}")
        if custo_serigrafia_total > 0:
            st.write(f"**Serigrafia (Por Peça):** ${custo_serigrafia_total:.2f} *({num_telas} Telas Totais: ${custo_telas_detalhe:.2f} diluídas em {qtd} un + ${custo_tinta_detalhe:.2f} total tinta)*")
        if total_custo_vinil > 0:
            st.write(f"**Total Vinis (Arte):** ${total_custo_vinil:.2f}")
            for cam in detalhes_camadas:
                st.write(f"  - Camada {cam['n']} ({cam['tipo']}): ${cam['custo']:.2f}")
        st.write(f"**Markup Aplicado:** {mk_base}x")
        st.write("---")
        custo_total_pedido = custo_un_total * qtd
        lucro_liquido = total_final - custo_total_pedido
        st.success(f"💰 Lucro Líquido: ${lucro_liquido:.2f}")

st.caption("Zion Atelier - New York Style By Faith")
