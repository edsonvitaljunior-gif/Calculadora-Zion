import streamlit as st
import os

# --- 1. CONFIGURAÇÃO QUE DEU CERTO (BUFFER DO ANDROID) ---
# Isso aqui é o que fez o seu S24 funcionar!
try:
    st.set_page_config(page_title="Zion Atelier", page_icon="🗽", layout="centered")
except:
    pass

# --- 2. LOGO ---
nome_logo = "Logo Zion Atelier com fundo tranp 68%.png"
if os.path.exists(nome_logo):
    st.image(nome_logo, width=150)

# --- 3. IDENTIFICAÇÃO (Organizado verticalmente para não bagunçar) ---
st.write("### 📝 Dados do Orçamento")
nome_cliente = st.text_input("Nome do Cliente", placeholder="Quem está comprando?")
nome_arte = st.text_input("Nome da Arte", placeholder="Ex: Lion Gold Puff")

# O SEU COMANDO DA VITÓRIA:
arquivo_arte = st.file_uploader("Upload da Arte", type=["png", "jpg", "jpeg", "webp"], accept_multiple_files=False)

st.divider()

# --- 4. DATABASE (Vinis e Produtos) ---
vinis_db = {
    "EasyWeed (Siser)": 34.99,
    "Puff Vinyl": 42.00,
    "Metallic": 30.99,
    "Brick 600 (Thick)": 62.99,
    "Gliter (Thick)": 37.99,
    "StripFlock Pro": 35.99
}

produtos_db = {
    "CAMISAS": {"Gildan G500": 2.82, "markup": 3.0},
    "MOLETONS": {"Gildan G185": 14.50, "markup": 2.5},
    "BONÉS": {"Snapback Classic": 5.50, "markup": 4.0}
}

# --- 5. SELEÇÃO (Campos limpos para o celular) ---
cat = st.selectbox("Escolha o Produto", list(produtos_db.keys()))
tipo_v = st.selectbox("Tipo de Vinil", list(vinis_db.keys()))
qtd = st.number_input("Quantidade de Itens", min_value=1, value=1)

# Medidas em colunas pequenas apenas para números
col1, col2 = st.columns(2)
with col1:
    w = st.number_input("Largura (in)", value=10.0)
with col2:
    h = st.number_input("Altura (in)", value=10.0)

# --- 6. CÁLCULOS ---
# Custo vinil (baseado em rolo padrão 12in x 5yds)
custo_v = (w * h) * (vinis_db[tipo_v] / (12 * 180)) * 1.2
p_unit = (produtos_db[cat][list(produtos_db[cat].keys())[0]] + custo_v) * produtos_db[cat]["markup"]
total = p_unit * qtd

# --- 7. RESUMO FINAL (Onde a imagem aparece arrumada) ---
st.divider()
st.subheader("🏁 Resumo do Pedido")

# Se a imagem subiu, ela aparece aqui centralizada
if arquivo_arte is not None:
    st.image(arquivo_arte, caption=f"Arte: {nome_arte}", use_container_width=True)
    st.success("✅ Imagem carregada!")

# Informações do Cliente em destaque
st.info(f"👤 **Cliente:** {nome_cliente if nome_cliente else 'Zion Friend'}")

# Preços grandes para fácil leitura no S24
st.metric("Preço Unitário", f"${p_unit:.2f}")
st.metric("TOTAL DO PEDIDO", f"${total:.2f}")

with st.expander("📊 Detalhes Técnicos"):
    st.write(f"Custo Material: ${custo_v:.2f}")
    st.write(f"Markup: {produtos_db[cat]['markup']}x")

st.caption("Zion Atelier - New York Style By Faith")
