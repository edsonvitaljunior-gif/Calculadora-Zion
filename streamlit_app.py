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
nome_arte = st.text_input("Nome da Arte", placeholder="Ex: Lion Gold Puff")
arquivo_arte = st.file_uploader("Upload da Arte", type=["png", "jpg", "jpeg", "webp"], accept_multiple_files=False)

st.divider()

# --- 4. DATABASE ---
vinis_db = {
    "EasyWeed HTV (Siser)": 34.99,
    "Puff Vinyl": 42.00,
    "Metallic": 30.99,
    "Brick 600 (Thick)": 62.99,
    "Gliter (Thick)": 37.99,
    "StripFlock Pro": 35.99
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
lista_produtos = list(produtos_db[categoria_selecionada].keys())
produto_nome = st.selectbox("Modelo", lista_produtos)
qtd = st.number_input("Quantidade", min_value=1, value=1)

dados_prod = produtos_db[categoria_selecionada][produto_nome]
c_base = dados_prod["price"]
mk_base = dados_prod["markup"]

st.divider()

# --- 6. MEDIDAS DA ESTAMPA ---
st.write("### 📏 Medidas da Arte")
tipo_v = st.selectbox("Tipo de Vinil", list(vinis_db.keys()))
col1, col2 = st.columns(2)
with col1:
    w = st.number_input("Largura (in)", value=10.0)
with col2:
    h = st.number_input("Altura (in)", value=10.0)

# Cálculo de custo (Rolo padrão 12in x 180in) + 20% margem de erro
custo_v = (w * h) * (vinis_db[tipo_v] / (12 * 180)) * 1.2
custo_unitario_total = c_base + custo_v

# --- 7. PREÇOS ---
p_unit_sugerido = custo_unitario_total * mk_base
total_bruto = p_unit_sugerido * qtd

st.write("### 💰 Promoção")
promo = st.toggle("Aplicar 10% de Desconto Especial")
total_final = total_bruto * 0.9 if promo else total_bruto
p_unit_final = total_final / qtd

st.divider()

# --- 8. RESUMO PARA O CLIENTE ---
st.subheader("🏁 Resumo do Pedido")

if arquivo_arte is not None:
    st.image(arquivo_arte, use_container_width=True)

st.info(f"👤 **Cliente:** {nome_cliente if nome_cliente else 'Zion Friend'} | 🎨 **Arte:** {nome_arte if nome_arte else 'Custom'}")

c_res1, c_res2 = st.columns(2)
c_res1.metric("Unitário", f"${p_unit_final:.2f}")
c_res2.metric("Total", f"${total_final:.2f}", delta="-10%" if promo else None)

# --- 9. 📊 ÁREA TÉCNICA (ZION ONLY) - AGORA COMPLETA ---
with st.expander("📊 Detalhes Financeiros (Zion Only)"):
    custo_total_pedido = custo_unitario_total * qtd
    lucro_liquido = total_final - custo_total_pedido
    margem_porcentagem = (lucro_liquido / total_final) * 100 if total_final > 0 else 0
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.write("**Custos:**")
        st.write(f"Peça base: ${c_base:.2f}")
        st.write(f"Vinil: ${custo_v:.2f}")
        st.write(f"Custo Total/Un: ${custo_unitario_total:.2f}")
    with col_t2:
        st.write("**Performance:**")
        st.write(f"Markup: {mk_base}x")
        st.write(f"Lucro Bruto: ${lucro_liquido:.2f}")
        st.write(f"Margem: {margem_porcentagem:.1f}%")
    
    st.divider()
    st.success(f"💰 **DINHEIRO NO BOLSO: ${lucro_liquido:.2f}**")

st.caption("Zion Atelier - New York Style By Faith")
