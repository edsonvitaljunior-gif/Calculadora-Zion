import streamlit as st
import os

# --- 1. CONFIGURAÇÃO S24 ---
try:
    st.set_page_config(page_title="Zion Atelier", page_icon="🗽", layout="centered")
except:
    pass

# Senha mestra para abrir a Área Técnica e Descontos
SENHA_BOSS = "zion2026"

# --- 2. LOGO ---
nome_logo = "Logo Zion Atelier com fundo tranp 68%.png"
if os.path.exists(nome_logo):
   st.image(nome_logo, width=150)

# --- 3. DADOS DO PROJETO ---
st.write("### 📝 Solicitação de Orçamento")
nome_cliente = st.text_input("Nome do Cliente", placeholder="Como podemos te chamar?")
nome_arte = st.text_input("Nome da Arte / Referência", placeholder="Ex: NY Lion Glow")

# O segredo da imagem: a key muda conforme o nome do cliente, forçando o refresh do cache
arquivo_arte = st.file_uploader("Upload da Arte", type=["png", "jpg", "jpeg", "webp"], key=f"up_{nome_cliente}")

# --- 4. GUIA DE ESTILO ZION (VISÍVEL PARA INSPIRAR O CLIENTE) ---
if arquivo_arte is not None:
    st.image(arquivo_arte, use_container_width=True)
    with st.expander("💡 Dica do Artista: Melhores Combinações"):
        st.write("""
        | Se você busca... | Sugestão de Camisa | Sugestão de Vinil |
        | :--- | :--- | :--- |
        | **Estilo Streetwear** | Sand (Areia) ou Black | Puff (Relevo) |
        | **Destaque Noturno** | Navy ou Graphite | Glow in the Dark |
        | **Visual Luxo** | Forest Green | Metallic Gold |
        | **Visual Clean** | Sport Grey | EasyWeed Navy |
        """)

st.divider()

# --- 5. DATABASE ATUALIZADA (COM SEUS CÓDIGOS E PREÇOS) ---
vinis_db = {
    "EasyWeed HTV (Siser)": {"GPI Supplies": {"price": 34.99, "width": 12, "yards": 5}, "Heat Transfer Whse": {"price": 37.99, "width": 12, "yards": 5}},
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

produtos_db = {
    "CAMISAS": {
        "Gildan G500 Unisex": {"price": 2.82, "markup": 3.0},
        "Feminina Gildan G500VL Gola V": {"price": 6.37, "markup": 3.5},
        "Feminina Gildan G500L Gola Careca": {"price": 4.91, "markup": 3.2},
        "Kids Shirt Gidan G510P Heavy Cotton": {"price": 3.93, "markup": 3.0},
        "Gildan G500B - Juvenil Heavy Cotton™": {"price": 2.96, "markup": 3.0}
    },
    "MOLETONS": {"Gildan Unisex 50/50 G185 Hoodie": {"price": 13.77, "markup": 2.5}},
    "BONÉS": {"Snapback Classic": {"price": 5.50, "markup": 4.0}, "Trucker Hat": {"price": 4.20, "markup": 4.0}}
}

# --- 6. SELEÇÃO DE PRODUTO ---
st.write("### 🛍️ Configure seu Item")
cat_sel = st.selectbox("Categoria", list(produtos_db.keys()))
prod_nome = st.selectbox("Modelo", list(produtos_db[cat_sel].keys()))
qtd = st.number_input("Quantidade", min_value=1, value=1)

c_base = produtos_db[cat_sel][prod_nome]["price"]
mk_base = produtos_db[cat_sel][prod_nome]["markup"]

st.divider()

# --- 7. CAMADAS DE VINIL (CLICÁVEIS) ---
st.write("### 📏 Personalização (Camadas)")
custo_v = 0.0

def configurar_camada(n):
    st.markdown(f"**Personalização {n}**")
    tipo = st.selectbox(f"Tipo de Vinil (C{n})", list(vinis_db.keys()), key=f"tipo{n}")
    forn = st.selectbox(f"Fornecedor (C{n})", list(vinis_db[tipo].keys()), key=f"forn{n}")
    col_w, col_h = st.columns(2)
    with col_w: w = st.number_input(f"Largura in (C{n})", value=10.0, key=f"w{n}")
    with col_h: h = st.number_input(f"Altura in (C{n})", value=10.0, key=f"h{n}")
    info = vinis_db[tipo][forn]
    custo_por_polegada = info["price"] / (info["width"] * 180)
    return (w * h) * custo_por_polegada * 1.2

custo_v += configurar_camada(1)

if st.checkbox("Adicionar Camada 2"):
    st.divider(); custo_v += configurar_camada(2)
if st.checkbox("Adicionar Camada 3"):
    st.divider(); custo_v += configurar_camada(3)
if st.checkbox("Adicionar Camada 4"):
    st.divider(); custo_v += configurar_camada(4)

# --- 8. CÁLCULOS FINAIS ---
custo_unitario_total = c_base + custo_v
p_unit_sugerido = custo_unitario_total * mk_base
total_bruto = p_unit_sugerido * qtd

# --- MODO ADMIN (BOSS ONLY NA BARRA LATERAL) ---
desconto_aplicado = 0.0
with st.sidebar:
    st.write("🔒 **Área Reservada**")
    acesso = st.text_input("Chave do Boss", type="password")
    if acesso == SENHA_BOSS:
        st.success("Acesso Liberado!")
        promo = st.toggle("Aplicar 10% de Desconto")
        if promo:
            desconto_aplicado = 0.10

total_final = total_bruto * (1 - desconto_aplicado)
p_unit_final = total_final / qtd

st.divider()

# --- 9. RESUMO PARA O CLIENTE ---
st.subheader("🏁 Valor do Investimento")
st.info(f"👤 **Cliente:** {nome_cliente if nome_cliente else 'Zion Friend'} | 🎨 **Arte:** {nome_arte if nome_arte else 'Custom'}")

c_res1, c_res2 = st.columns(2)
c_res1.metric("Unitário", f"${p_unit_final:.2f}")
c_res2.metric("Total", f"${total_final:.2f}")

# --- 10. 📊 ÁREA TÉCNICA (SÓ APARECE COM A SENHA) ---
if acesso == SENHA_BOSS:
    with st.expander("📊 Detalhes Financeiros (Zion Only)"):
        custo_total_pedido = custo_unitario_total * qtd
        lucro_liquido = total_final - custo_total_pedido
        margem_porcentagem = (lucro_liquido / total_final) * 100 if total_final > 0 else 0
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.write("**Custos:**")
            st.write(f"Peça base: ${c_base:.2f}")
            st.write(f"Vinil total: ${custo_v:.2f}")
            st.write(f"Custo Total/Un: ${custo_unitario_total:.2f}")
        with col_t2:
            st.write("**Performance:**")
            st.write(f"Markup: {mk_base}x")
            st.write(f"Lucro Bruto: ${lucro_liquido:.2f}")
            st.write(f"Margem: {margem_porcentagem:.1f}%")
        
        st.divider()
        st.success(f"💰 **DINHEIRO NO BOLSO: ${lucro_liquido:.2f}**")

st.caption("Zion Atelier - New York Style By Faith")
