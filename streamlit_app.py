import streamlit as st
import os
import urllib.parse

# --- 1. CONFIGURAÇÃO & TEMA PREMIUM GOLDEN 3D ---
try:
    st.set_page_config(page_title="Zion Atelier", page_icon="🗽", layout="centered")
except:
    pass

# CSS CUSTOMIZADO: Uploader Transparente com Bordas Douradas
st.markdown("""
    <style>
    /* Fundo Total Preto */
    .stApp { background-color: #000000; }
    
    /* Textos em Dourado */
    h1, h2, h3, p, span, label, .stMarkdown { color: #d4af37 !important; }
    
    /* --- CUSTOMIZAÇÃO DO UPLOADER --- */
    /* 1. Container Externo */
    [data-testid="stFileUploader"] {
        background-color: transparent !important;
        border: none !important;
        padding: 0px;
    }

    /* 2. Área de Drag and Drop (Interna) */
    [data-testid="stFileUploaderDropzone"] {
        background-color: transparent !important;
        border: 2px dashed #d4af37 !important; /* Borda dourada pontilhada */
        border-radius: 15px !important;
        transition: all 0.3s ease;
    }
    
    /* Efeito de hover na área de drop */
    [data-testid="stFileUploaderDropzone"]:hover {
        border: 2px solid #ffffff !important; /* Brilha branco ao passar o mouse/dedo */
        background-color: rgba(212, 175, 55, 0.05) !important;
    }

    /* 3. Texto "Drag and drop file here" e "Limit 200MB" */
    [data-testid="stFileUploaderDropzone"] section div {
        color: #d4af37 !important;
    }

    /* 4. Estilização do Botão 'Browse Files' 3D */
    [data-testid="stFileUploader"] button {
        background-color: #d4af37 !important;
        color: #000000 !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: none !important;
        box-shadow: 0px 4px 0px #b38f2d !important;
        transition: all 0.2s ease;
        margin-top: 10px;
    }

    [data-testid="stFileUploader"] button:active {
        box-shadow: 0px 0px 0px #b38f2d !important;
        transform: translateY(4px);
    }

    /* --- OUTROS ELEMENTOS --- */
    div[data-testid="metric-container"] { 
        background-color: #111111; 
        border: 2px solid #d4af37; 
        padding: 15px; 
        border-radius: 12px; 
    }
    div[data-testid="stMetricValue"] { color: #d4af37 !important; }

    .wa-button {
        text-decoration: none; 
        color: #000000 !important; 
        background-color: #d4af37; 
        padding: 12px; 
        border-radius: 10px; 
        font-weight: bold; 
        display: block; 
        text-align: center;
        box-shadow: 0px 5px 0px #b38f2d;
    }
    
    hr { border-top: 1px solid #d4af37 !important; }
    input, select { background-color: #1a1a1a !important; color: #d4af37 !important; border: 1px solid #d4af37 !important; }
    </style>
    """, unsafe_allow_html=True)

SENHA_BOSS = "zion2026"

# --- 2. LOGO ---
nome_logo = "Logo Zion Atelier com fundo tranp 68%.png"
if os.path.exists(nome_logo):
   st.image(nome_logo, width=150)

# --- 3. DADOS DO PROJETO ---
st.write("### 📝 Solicitação de Orçamento")
nome_cliente = st.text_input("Nome do Cliente", placeholder="Ex: John Doe")
nome_arte = st.text_input("Nome da Arte", placeholder="Ex: Lion Pride")

# Uploader com a borda dourada e fundo transparente
arquivo_arte = st.file_uploader("Upload da Arte", type=["png", "jpg", "jpeg", "webp"], key=f"up_{nome_cliente}")

# --- 4. GUIA DE ESTILO & IMAGEM ---
if arquivo_arte is not None:
    st.image(arquivo_arte, use_container_width=True)
    with st.expander("💡 Dica do Artista: Melhores Combinações"):
        st.write("""
        | Estilo | Camisa | Vinil |
        | :--- | :--- | :--- |
        | **Streetwear** | Sand / Black | Puff |
        | **Noturno** | Navy / Graphite | Glow |
        | **Luxo** | Forest Green | Gold |
        """)

st.divider()

# --- 5. DATABASE ---
vinis_db = {
    "EasyWeed HTV (Siser)": {"GPI Supplies": {"price": 34.99, "width": 12}, "Heat Transfer Whse": {"price": 37.99, "width": 12}},
    "Puff Vinyl": {"GPI Supplies": {"price": 42.00, "width": 12}, "Heat Transfer Whse": {"price": 42.00, "width": 12}},
    "Metallic": {"GPI Supplies": {"price": 30.99, "width": 12}, "Heat Transfer Whse": {"price": 34.99, "width": 12}},
    "Holographic": {"GPI Supplies": {"price": 48.00, "width": 12}, "Heat Transfer Whse": {"price": 50.00, "width": 20}},
    "Brick 600 (Thick)": {"GPI Supplies": {"price": 62.99, "width": 20}, "Heat Transfer Whse": {"price": 39.99, "width": 12}},
    "Gliter (Thick)": {"GPI Supplies": {"price": 37.99, "width": 12}},
    "Aurora (Thick)": {"GPI Supplies": {"price": 28.49, "width": 12}},
    "Easy Glow Brilha no escuro": {"Heat Transfer Whse": {"price": 62.99, "width": 12}},
    "StripFlock Pro (Thick)": {"GPI Supplies": {"price": 35.99, "width": 12}},
    "Easy Glow Cores": {"Heat Transfer Whse": {"price": 52.99, "width": 12}}
}

produtos_db = {
    "CAMISAS": {
        "Gildan G500 Unisex": {"price": 2.82, "markup": 3.0},
        "Feminina G500VL V-Neck": {"price": 6.37, "markup": 3.5},
        "Feminina G500L Crewneck": {"price": 4.91, "markup": 3.2},
        "Kids G510P Heavy Cotton": {"price": 3.93, "markup": 3.0},
        "G500B Juvenil": {"price": 2.96, "markup": 3.0}
    },
    "MOLETONS": {"Gildan G185 Hoodie": {"price": 13.77, "markup": 2.5}},
    "BONÉS": {"Snapback Classic": {"price": 5.50, "markup": 4.0}, "Trucker Hat": {"price": 4.20, "markup": 4.0}}
}

# --- 6. SELEÇÃO ---
st.write("### 🛍️ Configure seu Item")
cat_sel = st.selectbox("Categoria", list(produtos_db.keys()))
prod_nome = st.selectbox("Modelo", list(produtos_db[cat_sel].keys()))
qtd = st.number_input("Quantidade", min_value=1, value=1)

c_base = produtos_db[cat_sel][prod_nome]["price"]
mk_base = produtos_db[cat_sel][prod_nome]["markup"]

st.divider()

# --- 7. CAMADAS ---
st.write("### 📏 Personalização")
custo_v = 0.0

def configurar_camada(n):
    st.markdown(f"**Camada {n}**")
    tipo = st.selectbox(f"Tipo de Vinil (C{n})", list(vinis_db.keys()), key=f"tipo{n}")
    forn = st.selectbox(f"Fornecedor (C{n})", list(vinis_db[tipo].keys()), key=f"forn{n}")
    col_w, col_h = st.columns(2)
    with col_w: w = st.number_input(f"Largura (in) {n}", value=10.0, key=f"w{n}")
    with col_h: h = st.number_input(f"Altura (in) {n}", value=10.0, key=f"h{n}")
    info = vinis_db[tipo][forn]
    custo_por_polegada = info["price"] / (info["width"] * 180)
    return (w * h) * custo_por_polegada * 1.2

custo_v += configurar_camada(1)

if st.checkbox("Adicionar Camada 2"):
    st.divider(); custo_v += configurar_camada(2)
if st.checkbox("Adicionar Camada 3"):
    st.divider(); custo_v += configurar_camada(3)

# --- 8. CÁLCULOS FINAIS ---
custo_un_total = c_base + custo_v
p_unit_sugerido = custo_un_total * mk_base
total_bruto = p_unit_sugerido * qtd

desconto_aplicado = 0.0
with st.sidebar:
    st.write("🔒 **Boss Only**")
    acesso = st.text_input("Chave", type="password")
    if acesso == SENHA_BOSS:
        st.success("Welcome!")
        if st.toggle("Desconto 10%"):
            desconto_aplicado = 0.10

total_final = total_bruto * (1 - desconto_aplicado)
p_unit_final = total_final / qtd

st.divider()

# --- 9. RESUMO & WHATSAPP ---
st.subheader("🏁 Valor do Investimento")
col_res1, col_res2 = st.columns(2)
col_res1.metric("Unitário", f"${p_unit_final:.2f}")
col_res2.metric("Total", f"${total_final:.2f}")

msg = f"Olá {nome_cliente}! Segue orçamento da Zion Atelier:\n\n" \
      f"🎨 Arte: {nome_arte}\n" \
      f"👕 Item: {prod_nome}\n" \
      f"🔢 Quantidade: {qtd}\n" \
      f"💰 Valor Total: ${total_final:.2f}\n\n" \
      f"Podemos fechar?"
      
msg_encoded = urllib.parse.quote(msg)
link_whatsapp = f"https://wa.me/?text={msg_encoded}"

st.write("")
st.markdown(f'<a href="{link_whatsapp}" target="_blank" class="wa-button">ENVIAR AGORA NO WHATSAPP</a>', unsafe_allow_html=True)

# --- 10. ÁREA TÉCNICA ---
if acesso == SENHA_BOSS:
    with st.expander("📊 Detalhes Financeiros"):
        custo_total_pedido = custo_un_total * qtd
        lucro_liquido = total_final - custo_total_pedido
        st.success(f"💰 Lucro: ${lucro_liquido:.2f}")

st.caption("Zion Atelier - New York Style By Faith")
