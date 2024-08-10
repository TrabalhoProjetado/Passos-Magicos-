import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from PIL import Image
import requests
from io import BytesIO

# Criar a interface do Streamlit

st.set_page_config(
    page_title='Passos Mágicos',
    page_icon = "https://img.icons8.com/?size=100&id=SS9irMJVAaEa&format=png&color=000000", #Icone de pegada
    layout="wide",
    initial_sidebar_state="auto",#"expanded"
)

#Titulo da pagina
st.markdown("""
<style>
h1 {
    text-align: center;
}
</style>
""", unsafe_allow_html=True)
st.markdown("<h1 style='font-size: 3em;'>ASSOCIAÇÃO PASSOS MÁGICOS</h1>", unsafe_allow_html=True)


# Criar os botões e links

botoes = ["Ir para o Dashboard", "Ir para o Github","Ir pro Colab"]
links = ["", "https://github.com/TrabalhoProjetado/Passos-Magicos-",""] #ADICIONAR POWER BI E COLAB


st.markdown(
    """
    <style>
    .stButton > button {
        background-color: #E99312;
        color: #FFFFFF;
        padding: 10px 20px;
        font-size: 15px; 
        
    }
    </style>
    """,
    unsafe_allow_html=True
)

colu1, colu2, colu3 = st.columns(3)
with colu1:
    if st.button(botoes[0]):
        st.markdown(f'[{botoes[0]}]({links[0]})', unsafe_allow_html=True)

with colu2:
    if st.button(botoes[1]):
        st.markdown(f'[{botoes[1]}]({links[1]})', unsafe_allow_html=True)
        
with colu3:
    if st.button(botoes[2]):
        st.markdown(f'[{botoes[2]}]({links[2]})', unsafe_allow_html=True)

#Carregar a Base
@st.cache_data
def load_data():
    tabela = pd.read_csv('https://raw.githubusercontent.com/TrabalhoProjetado/Passos-Magicos-/main/PEDE_PASSOS_DATASET_FIAP.csv', delimiter=';', dayfirst=True)
    return tabela
# Carregar os dados
data = load_data()

st.write("")
st.write("")

#Subtítulo
st.markdown("<h1 style='color: white; font-size: 2em; text-align: left; margin-left: 0;'><u>Quantidade de Alunos por categoria em 2022</u></h1>", unsafe_allow_html=True)

filtered_data = data[(data['PEDRA_2022'] == 'Topázio') & (data['PEDRA_2022'] != '#NULO!')]
# Contar a quantidade de "Topázio"
quantidade_topazio = filtered_data.shape[0]  # Conta o número de linhas

filtered2_data = data[(data['PEDRA_2022'] == 'Ametista') & (data['PEDRA_2022'] != '#NULO!')]
# Contar a quantidade de "Amestista"
quantidade_ametista = filtered2_data.shape[0]  # Conta o número de linhas

filtered3_data = data[(data['PEDRA_2022'] == 'Ágata') & (data['PEDRA_2022'] != '#NULO!')]
# Contar a quantidade de "Amestista"
quantidade_agata = filtered3_data.shape[0]  # Conta o número de linhas

filtered4_data = data[(data['PEDRA_2022'] == 'Quartzo') & (data['PEDRA_2022'] != '#NULO!')]
# Contar a quantidade de "Amestista"
quantidade_quartzo = filtered4_data.shape[0]  # Conta o número de linhas


# Exibir a quantidade no Streamlit
col1, col2, col3, col4 = st.columns(4)  # Cria duas colunas para o ícone e o texto

with col1:
    st.markdown(f"<h1 style='color: #2823bc; font-size: 1.8em;'>Topázio é: <span style='color: white;'>{quantidade_topazio}</h1>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<h1 style='color: #800080; font-size: 1.8em;'>Ametista é: <span style='color: white;'>{quantidade_ametista}</span></h1>", unsafe_allow_html=True)

with col3:
    st.markdown(f"<h1 style='color: #fc5500; font-size: 1.8em;'>Ágata é: <span style='color: white;'>{quantidade_agata}</h1>", unsafe_allow_html=True)

with col4:
    st.markdown(f"<h1 style='font-size: 1.8em;'>Quartzo é: {quantidade_quartzo}</h1>", unsafe_allow_html=True)


#GRAFICOS
st.write("")
                                                #BARRAS
st.write("")
#Quantidade de alunos durantes os anos 
                                               
# Filtrar dados para cada ano e excluir categorias indesejadas
filtered_data_2020 = data[data['PEDRA_2020'] != 'D9891/2A']
distribuicao_2020 = filtered_data_2020['PEDRA_2020'].value_counts().reset_index()
distribuicao_2020.columns = ['Categoria', 'Quantidade']
distribuicao_2020['Ano'] = '2020'

filtered_data_2021 = data[data['PEDRA_2021'] != '#NULO!']
distribuicao_2021 = filtered_data_2021['PEDRA_2021'].value_counts().reset_index()
distribuicao_2021.columns = ['Categoria', 'Quantidade']
distribuicao_2021['Ano'] = '2021'

filtered_data_2022 = data[data['PEDRA_2022'] != '#NULO!']
distribuicao_2022 = filtered_data_2022['PEDRA_2022'].value_counts().reset_index()
distribuicao_2022.columns = ['Categoria', 'Quantidade']
distribuicao_2022['Ano'] = '2022'

# Concatenar os dados de todos os anos
distribuicao_total = pd.concat([distribuicao_2020, distribuicao_2021, distribuicao_2022])

# Criar o gráfico com Plotly
fig = px.bar(distribuicao_total, 
             x='Categoria', 
             y='Quantidade', 
             color='Ano', 
             hover_data=({'Quantidade': True, 'Categoria': True, 'Ano': True}),  # Colunas para o tooltip
             barmode='group',
             title='Quantidade de Alunos por Categoria de Pedra (2020, 2021 e 2022)',
             labels={'Quantidade': 'Quantidade de Alunos', 'Categoria': 'Categoria de Pedra'})
# Personalizar os tooltips
fig.update_traces(
    hovertemplate='<b>Categoria:</b> %{x}<br>' +
                  '<b>Quantidade:</b> %{y}<br>' +
                 '<extra></extra>',  # Remove a linha padrão do tooltip
    customdata=distribuicao_total[['Ano']].values  # Adiciona dados personalizados
)
# Ajustes nos gráficos
fig.update_layout(
    title_font=dict(size=30),  # Tamanho do Título
    xaxis_title_font=dict(size=20),  # Tamanho do Eixo x
    yaxis_title_font=dict(size=20),   # Tamanho do Eixo y
    legend_font=dict(size=20),  # Tamanho da Legenda
    width=1500,  # Tamanho da Largura
    height=1000  # Tamanho da Altura
)

# Mostrar o gráfico no Streamlit
st.plotly_chart(fig)

st.write("")
                                                    #LINHA
st.write("")

#Variação da Quantidade de alunos

# Filtrar dados para cada ano e excluir categorias indesejadas
filtered_data_2020 = data[data['PEDRA_2020'] != 'D9891/2A']
distribuicao_2020 = filtered_data_2020['PEDRA_2020'].value_counts().reset_index()
distribuicao_2020.columns = ['Categoria', 'Quantidade']
distribuicao_2020['Ano'] = '2020'

filtered_data_2021 = data[data['PEDRA_2021'] != '#NULO!']
distribuicao_2021 = filtered_data_2021['PEDRA_2021'].value_counts().reset_index()
distribuicao_2021.columns = ['Categoria', 'Quantidade']
distribuicao_2021['Ano'] = '2021'

filtered_data_2022 = data[data['PEDRA_2022'] != '#NULO!']
distribuicao_2022 = filtered_data_2022['PEDRA_2022'].value_counts().reset_index()
distribuicao_2022.columns = ['Categoria', 'Quantidade']
distribuicao_2022['Ano'] = '2022'

# Concatenar os dados de todos os anos
distribuicao_total = pd.concat([distribuicao_2020, distribuicao_2021, distribuicao_2022])

# Criar o gráfico de variação entre anos
fig = px.line(distribuicao_total, 
              x='Categoria', 
              y='Quantidade', 
              color='Ano', 
              hover_data=({'Quantidade': True, 'Categoria': True, 'Ano': True}),  # Colunas para o tooltip
              markers=True,
              title='Variação da Quantidade de Alunos por Categoria de Pedra (2020, 2021 e 2022)',
              labels={'Quantidade': 'Quantidade de Alunos', 'Categoria': 'Categoria de Pedra'})

fig.update_traces(
    hovertemplate='<b>Categoria:</b> %{x}<br>' +
                  '<b>Quantidade:</b> %{y}<br>' +
                 '<extra></extra>',  # Remove a linha padrão do tooltip
    customdata=distribuicao_total[['Ano']].values  # Adiciona dados personalizados
)

# Adicionar os valores das quantidades no gráfico
fig.update_traces(
    text=distribuicao_total['Quantidade'], 
    textposition='top center',  # Posição do texto
    textfont=dict(size=12)  # Tamanho da fonte do texto
)

# Ajustar o layout do gráfico para mudar o tamanho da fonte do título, eixos e legenda
fig.update_layout(
    title_font=dict(size=30),  # Tamanho do Título
    xaxis_title_font=dict(size=20),  # Tamanho do Eixo x
    yaxis_title_font=dict(size=20),   # Tamanho do Eixo y
    legend_font=dict(size=20),  # Tamanho da Legenda
    width=1500,  # Tamanho da Largura
    height=1000  # Tamanho da Altura
)
# Mostrar o gráfico no Streamlit
st.plotly_chart(fig)

