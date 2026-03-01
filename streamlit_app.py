import streamlit as st
import os
import urllib.parse

# --- 1. CONFIGURAÇÃO & TEMA PREMIUM DARK GOLD ---
try:
    st.set_page_config(page_title="Zion Atelier - Master", page_icon="🗽", layout="centered")
except:
    pass

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    h1, h2, h3, p, span, label, .stMarkdown { color: #d4af37 !important; }
    ::placeholder { color: rgba(212, 175, 55, 0.6) !important; opacity: 1; }
    [data-testid="stFileUploaderDropzone"] { border: 2px dashed #d4af37 !important; border-radius: 15px !important; }
    [data-testid="stFileUploader"] button { background-color: #d4af37 !important; color: #000000 !important; font-weight: bold !important; box-shadow: 0px 4px 0px #b38f2d !important; }
    div[data-testid="metric-container"] { background-color: #111111; border: 2px solid #d4af37; padding: 15px; border-radius: 12px; }
    div[data-testid="stMetricValue"] { color: #d4af37 !important; font-weight: bold; }
    .wa-button { text-decoration: none; color: #000000 !important; background-color: #d4af37; padding: 15px; border-radius: 10px; font-weight: bold; display: block; text-align: center; box-shadow: 0px 5px 0px #b38f2d; font-size: 18px; }
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
nome_client = st.text_input("Nome do Cliente", placeholder="Ex: John Doe")
nome_art = st.text_input("Nome da Arte", placeholder="Ex: Zion Legacy Lion")
arquivo_art = st.file_uploader("Upload da Arte", type=["png", "jpg", "jpeg", "webp"])

if arquivo_art is not None:
    st.image(arquivo_art, use_container_width=True)

st.divider()

# --- 4. DATABASE COMPLETA (INCLUINDO LEGACY & NOVOS VINIS) ---
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

produtos_db = {
    "ZION KIDS & BABY": {
        "Baby Onesie (Body)": {"price": 4.50, "markup": 4.0},
        "Toddler Tee (2-5y)": {"price": 5.20, "markup": 3.8},
        "Youth Heavy Cotton": {"price": 3.93, "markup": 3.5}
    },
    "LEGACY COLLECTION": {
        "Grandpa/Grandma Luxury": {"price": 7.50, "markup": 3.5},
        "Daddy/Mommy Oversized": {"price": 12.00, "markup": 3.0},
        "Auntie Special Edition": {"price": 8.50, "markup": 3.5}
    },
    "CAMISAS ADULTO": {
        "Gildan G500 Unisex": {"price": 2.82, "markup": 3.0},
        "Feminina G500VL V-Neck": {"price": 6.37, "markup": 3.5},
        "Feminina G500L Crewneck": {"price": 4.91, "markup": 3.2}
    },
    "MOLETONS & BONES": {
        "Gildan G185 Hoodie": {"price": 13.77, "markup": 2.5},
        "Snapback Classic": {"price": 5.50, "markup": 4.0},
        "Trucker Hat": {"price": 4.20, "markup": 4.0}
    }
}

# --- 5. SELEÇÃO DE ITEM ---
st.write("### 🛍️ Configure seu Item")
cat_sel = st.selectbox("Categoria", list(produtos_db.keys()))
prod_nome = st.selectbox("Modelo", list(produtos_db[cat_sel].keys()))
qtd = st.number_input("Quantidade", min_value=1, value=1)

c_base = produtos_db[cat_sel][prod_nome]["price"]
mk_base = produtos_db[cat_sel][prod_nome]["markup"]

st.divider()

# --- 6. SISTEMA DE 4 CAMADAS (RESTAURADO) ---
st.write("### 📏 Detalhamento das Camadas")
total_custo_vinil = 0.0
detalhes_camadas = []

def configurar_camada(n):
    st.markdown(f"**Camada {n}**")
    tipo = st.selectbox(f"Tipo de Vinil (C{n})", list(vinis_db.keys()), key=f"tipo{n}")
    forn = st.selectbox(f"Fornecedor (C{n})", list(vinis_db[tipo].keys()), key=f"forn{n}")
    col_w, col_h = st.columns(2)
    with col_w: w = st.number_input(f"Largura (in) {n}", value=5.0, key=f"w{n}")
    with col_h: h = st.number_input(f"Altura (in) {n}", value=5.0, key=f"h{n}")
    
    info = vinis_db[tipo][forn]
    # Cálculo: (Área / Área Total do Rolo) * Preço do Rolo
    custo_polegada = info["price"] / (info["width"] * 180) 
    custo_da_camada = (w * h) * custo_polegada * 1.3 # 30% margem de perda
    
    detalhes_camadas.append({"n": n, "tipo": tipo, "custo": custo_da_camada})
    return custo_da_camada

total_custo_vinil += configurar_camada(1)

if st.checkbox("Adicionar Camada 2"):
    st.divider(); total_custo_vinil += configurar_camada(2)
if st.checkbox("Adicionar Camada 3"):
    st.divider(); total_custo_vinil += configurar_camada(3)
if st.checkbox("Adicionar Camada 4"):
    st.divider(); total_custo_vinil += configurar_camada(4)

# --- 7. CÁLCULOS FINAIS ---
custo_un_total = c_base + total_custo_vinil
p_unit_sugerido = custo_un_total * mk_base
total_bruto = p_unit_sugerido * qtd

desconto_aplicado = 0.0
with st.sidebar:
    st.write("🔒 **Boss Mode**")
    acesso = st.text_input("Chave", type="password")
    if acesso == SENHA_BOSS:
        st.success("Welcome, Boss Edson!")
        if st.toggle("Desconto 10%"):
            desconto_aplicado = 0.10

total_final = total_bruto * (1 - desconto_aplicado)
p_unit_final = total_final / qtd

st.divider()

# --- 8. RESUMO DE INVESTIMENTO ---
st.subheader("🏁 Valor do Investimento")
col_res1, col_res2 = st.columns(2)
col_res1.metric("Unitário", f"${p_unit_final:.2f}")
col_res2.metric("Total", f"${total_final:.2f}")

msg = f"🗽 *ZION ATELIER - NY STYLE*\n\n" \
      f"Olá {nome_client}! Segue o orçamento para o seu projeto:\n\n" \
      f"🖼️ *Arte:* {nome_art}\n" \
      f"👕 *Item:* {prod_nome}\n" \
      f"🔢 *Qtd:* {qtd}\n" \
      f"💰 *Investimento:* ${total_final:.2f}\n\n" \
      f"Podemos avançar?"
      
msg_encoded = urllib.parse.quote(msg)
link_whatsapp = f"https://wa.me/?text={msg_encoded}"
st.markdown(f'<a href="{link_whatsapp}" target="_blank" class="wa-button">ENVIAR ORÇAMENTO VIA WHATSAPP</a>', unsafe_allow_html=True)

# --- 9. ÁREA TÉCNICA (DETALHAMENTO DE INSUMOS RECUPERADO) ---
if acesso == SENHA_BOSS:
    with st.expander("📊 Detalhamento de Insumos & Lucro"):
        st.write(f"**Peça Base ({prod_nome}):** ${c_base:.2f}")
        st.write(f"**Total Vinis (Arte):** ${total_custo_vinil:.2f}")
        for cam in detalhes_camadas:
            st.write(f"  - Camada {cam['n']} ({cam['tipo']}): ${cam['custo']:.2f}")
        st.write(f"**Markup Aplicado:** {mk_base}x")
        st.write("---")
        custo_total_pedido = custo_un_total * qtd
        lucro_liquido = total_final - custo_total_pedido
        st.success(f"💰 Lucro Líquido: ${lucro_liquido:.2f}")

st.caption("Zion Atelier - New York Style By Faith")
