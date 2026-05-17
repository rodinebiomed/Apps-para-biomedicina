import streamlit as st
from datetime import datetime
import csv
import os

# ==========================================
# CONFIGURAÇÃO DA PÁGINA DO STREAMLIT
# ==========================================
st.set_page_config(
    page_title="Contador Hematológico YouLab Tutor",
    page_icon="🔬",
    layout="centered"
)

# Estilização CSS personalizada para emular o design original
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    h1 { color: #0a3d62; font-family: 'Helvetica', sans-serif; }
    .stButton>button { width: 100%; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# INICIALIZAÇÃO DO ESTADO DA SESSÃO (STATE)
# ==========================================
if "contagem" not in st.session_state:
    st.session_state.contagem = {
        "Neutrófilos (Seg) (Z)": 0,
        "Neutrófilos (Bastão) (S)": 0,
        "Linfócitos (X)": 0,
        "Monócitos (C)": 0,
        "Eosinófilos (V)": 0,
        "Basófilos (B)": 0,
        "Outros (D)": 0
    }

if "nome_paciente" not in st.session_state:
    st.session_state.nome_paciente = ""

# Ícones e fallbacks (emojis caso a imagem falte)
icones_config = {
    "Neutrófilos (Seg) (Z)": {"arq": "neutro.png", "emoji": "🧫"},
    "Neutrófilos (Bastão) (S)": {"arq": "neutro.png", "emoji": "🥖"},
    "Linfócitos (X)": {"arq": "linfo.png", "emoji": "🧬"},
    "Monócitos (C)": {"arq": "mono.png", "emoji": "💧"},
    "Eosinófilos (V)": {"arq": "eos.png", "emoji": "🔴"},
    "Basófilos (B)": {"arq": "baso.png", "emoji": "🔵"},
    "Outros (D)": {"arq": "outros.png", "emoji": "❓"}
}

# ==========================================
# FUNÇÕES DE LÓGICA
# ==========================================
def incrementar_celula(tipo):
    total_atual = sum(st.session_state.contagem.values())
    if total_atual < 100:
        st.session_state.contagem[tipo] += 1

def resetar():
    for tipo in st.session_state.contagem:
        st.session_state.contagem[tipo] = 0

def salvar_resultado(nome, total):
    if not nome:
        st.error("⚠️ Erro: Digite o nome do paciente antes de salvar.")
        return
    if total == 0:
        st.error("⚠️ Erro: Nenhuma célula contada.")
        return

    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
    arquivo_nome = "resultados_youlab.csv"
    arquivo_existe = os.path.isfile(arquivo_nome)

    try:
        with open(arquivo_nome, "a", newline="", encoding="utf-8") as arquivo:
            writer = csv.writer(arquivo)
            if not arquivo_existe:
                writer.writerow(["Data", "Paciente"] + list(st.session_state.contagem.keys()) + ["Total"])
            writer.writerow([data_atual, nome] + list(st.session_state.contagem.values()) + [total])
        st.success("💾 Resultado salvo com sucesso no arquivo CSV!")
    except Exception as e:
        st.error(f"Erro ao salvar arquivo: {e}")

# ==========================================
# RENDERIZAÇÃO DA INTERFACE (UI)
# ==========================================

# Logo do Cabeçalho
if os.path.exists("logo.png"):
    st.image("logo.png", width=125)

# Títulos
st.title("Contador Hematológico YouLab Tutor")
st.caption("Desenvolvido por Rodinê Júnior - Biomedicina")

st.divider()

# Campo do Paciente (Vinculado ao Session State)
st.session_state.nome_paciente = st.text_input("Nome do Paciente:", value=st.session_state.nome_paciente)

st.write("### Painel de Contagem")
st.info("Clique nos botões abaixo para realizar a contagem das células.")

total_celulas = sum(st.session_state.contagem.values())

# Renderização das Linhas de Células de Forma Responsiva
for tipo, valor in st.session_state.contagem.items():
    col_img, col_nome, col_btn = st.columns([1, 5, 3])
    
    # Coluna 1: Imagem do Ícone / Emoji de escape
    with col_img:
        img_path = icones_config[tipo]["arq"]
        if os.path.exists(img_path):
            st.image(img_path, width=32)
        else:
            st.markdown(f"### {icones_config[tipo]['emoji']}")
            
    # Coluna 2: Nome do Tipo Celular
    with col_nome:
        st.markdown(f"<p style='font-size:18px; margin-top:5px;'><b>{tipo}</b></p>", unsafe_allow_html=True)
        
    # Coluna 3: Botão contador de cliques dinâmico
    with col_btn:
        # Desabilita o botão automaticamente se atingir 100
        btn_desabilitado = total_celulas >= 100
        if st.button(f"Contar (+1) | Atual: {valor}", key=tipo, disabled=btn_desabilitado):
            incrementar_celula(tipo)
            st.rerun()

st.divider()

# Exibição do Painel do Totalizador Geral
if total_celulas >= 100:
    st.error(f"## Total: {total_celulas} / 100 (Limite Atingido)")
else:
    st.metric(label="Total de Células Contadas", value=f"{total_celulas} / 100")

# Exibição do Percentual em tempo real ou quando finalizado
if total_celulas > 0:
    with st.expander("📊 Ver Resultados e Diferencial Leucocitário (%)", expanded=total_celulas == 100):
        st.markdown("### Diferencial Leucocitário")
        for tipo, valor in st.session_state.contagem.items():
            percentual = (valor / total_celulas) * 100
            st.write(f"**{tipo}:** {percentual:.1f}% ({valor} células)")

st.divider()

# ==========================================
# BOTÕES DE AÇÃO INFERIORES
# ==========================================
col_salvar, col_reset = st.columns(2)

with col_salvar:
    if st.button("💾 Salvar Resultado", type="primary"):
        salvar_resultado(st.session_state.nome_paciente, total_celulas)

with col_reset:
    if st.button("🔄 Resetar Contador"):
        resetar()
        st.rerun()

# Rodapé institucional
st.markdown("---")
st.markdown("<center style='color:gray; font-size:12px;'>YouLab Tutor © 2026 | Desenvolvido por Rodinê Júnior</center>", unsafe_allow_html=True)
