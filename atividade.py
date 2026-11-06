import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dataset_prf = pd.read_csv('C:/Aula-Faculdade/dataset-PRF.csv', encoding="latin-1", sep=";")

# ===========================
# Explorando a Base de Dados
# ===========================
print("- Primeiras 5 linhas (.head) -")
print(dataset_prf.head()) # Mostra as primeiras linhas
print(' ')

print("- Informação dos Dados e Tipos (.info) -")
dataset_prf.info() # Mostra informações estruturais da tabela
print(' ')

print("- Estatísticas Descritivas (.describe) -")
print(dataset_prf.describe()) # Gera estatísticas descritivas
print(' ')

print("- Valores Null por Colunas -") # .isnull() - Identifica valores ausentes
print(dataset_prf.isnull().sum()) # .sum() - Soma valores ou conta ocorrências de True
print(' ')

print("- Linhas Duplicadas -") # .duplicated() - Identifica linhas duplicadas
print(dataset_prf.duplicated().sum()) # .sum() - Soma valores ou conta ocorrências de True
print(' ')

# ===========================
# CONVERSÃO DE DATAS E HORAS
# ===========================

# Convertendo a coluna de data para o formato datetime do Python
dataset_prf['data_inversa'] = pd.to_datetime(dataset_prf['data_inversa'], errors='coerce')

# Criando colunas para Ano, Mês e Dia da Semana
dataset_prf['ano'] = dataset_prf['data_inversa'].dt.year # Extrai o ano
dataset_prf['mes'] = dataset_prf['data_inversa'].dt.month # Extrai o mês

# Extraindo o nome do dia
dataset_prf['dia_semana'] = dataset_prf['data_inversa'].dt.strftime('%A') # .strftime() - Formata datas '%A' = dias da semana

# Extraindo a hora inteira (0 a 23) da sua coluna de horário
dataset_prf['hora_inteira'] = pd.to_datetime(dataset_prf['horario'], format='%H:%M:%S', errors='coerce').dt.hour # Extrai a hora

# ============================================
# 1. Evolução dos acidentes nos meses de 2025
# ============================================
print("\n- Gerando gráfico da Pergunta 1 (Linha) -")
# Filtrando apenas o ano de 2025
df_2025 = dataset_prf[dataset_prf['ano'] == 2025]

# Agrupando por mês e contando os acidentes
acidentes_mes_2025 = df_2025.groupby('mes').size() # Agrupa os dados e conta registros de cada grupo.

plt.figure(figsize=(12, 7)) # cria a área
sns.lineplot(x=acidentes_mes_2025.index, y=acidentes_mes_2025.values, marker='o', color='crimson', linewidth=2) # desenha o gráfico
plt.title('Evolução Mensal de Acidentes nas Rodovias Federais (2025)', fontsize=15) # coloca o título
plt.xlabel('Mês', fontsize=13) # identifica o eixo X
plt.ylabel('Quantidade de Acidentes', fontsize=13) # identifica o eixo Y
plt.xticks(range(1, 13)) # Força exibir os meses de 1 a 12
plt.grid(True, linestyle='--', alpha=0.6) # adiciona linhas de referência ao gráfico
plt.show() # Exibe o gráfico


# ===================================================================
# 3. Distribuição dos acidentes por dia da semana e faixa de horário
# ===================================================================

print("\n- Gerando gráfico da Pergunta 3 (Mapa de Calor) -")

# Criando os dias da semana
dias = {
    0: 'Segunda-feira',
    1: 'Terça-feira',
    2: 'Quarta-feira',
    3: 'Quinta-feira',
    4: 'Sexta-feira',
    5: 'Sábado',
    6: 'Domingo'
}

            # .dt.dayofweek - retorna um número para cada dia, de 0 para segunda-feira até 6 para domingo
dataset_prf['dia_semana'] = (dataset_prf['data_inversa'].dt.dayofweek.map(dias))
            # .map() - substitui cada número pelo nome correspondente no dicionário dias


# Definindo as faixas de horário
faixas = [-1, 5, 11, 17, 23]
nomes_faixas = ['Madrugada', 'Manhã', 'Tarde', 'Noite']


                             # pd.cut() divide valores numéricos em intervalos
dataset_prf['faixa_horario'] = pd.cut(dataset_prf['hora_inteira'], bins=faixas, labels=nomes_faixas)


# Removendo registros sem dia ou horário válido
df_calor = dataset_prf.dropna(subset=['dia_semana', 'faixa_horario']).copy()
                # .dropna(): remove as linhas com valores ausentes nas colunas especificadas
                # subset: indica quais colunas precisam estar preenchidas
                # .copy(): cria uma cópia independente dos registros selecionados


# Organizando os dias na ordem correta
ordem_dias = [
    'Segunda-feira',
    'Terça-feira',
    'Quarta-feira',
    'Quinta-feira',
    'Sexta-feira',
    'Sábado',
    'Domingo'
]

# Contando os registros por dia e faixa de horário
# Agrupa os dias e conta os registro e suas faixas de horários
tabela_calor = (
    df_calor.groupby(
        ['dia_semana', 'faixa_horario'],
        observed=False
    )
    .size()
    .unstack(fill_value=0)  # .unstack() transforma um dos níveis do agrupamento em colunas
                            # fill_value=0: preenche combinações sem registros com zero
    .reindex(index=ordem_dias, columns=nomes_faixas, fill_value=0) # garante que os dias e as faixas apareçam na ordem que definimos
)

# Criando o mapa de calor
plt.figure(figsize=(10, 6))

sns.heatmap(
    tabela_calor, # Fornece os números que serão representados pelas cores
    annot=True, # Exibe o número dentro de cada célula
    fmt='d', # Apresenta os valores como números inteiros
    cmap='YlOrRd', # Usa uma escala de cores que vai do amarelo ao vermelho
    linewidths=0.6, # Desenha pequenas linhas entre as células
    cbar_kws={'label': 'Quantidade de Registros'} # Personaliza a legenda lateral das cores
)

# Personalizando o gráfico
plt.title(
    'Distribuição dos Acidentes por Dia da Semana e Horário',
    fontsize=14
)
plt.xlabel('Faixa de Horário', fontsize=12)
plt.ylabel('Dia da Semana', fontsize=12)

plt.tight_layout()
plt.show()

# ========================================================
# 4. Quais UFs e Rodovias (br) concentram mais acidentes?
# ========================================================
print("\n- Gerando gráfico da Pergunta 4 (Barra) -")
# Substitua 'uf' e 'br' pelos nomes exatos das colunas do seu arquivo
top_ufs = dataset_prf['uf'].value_counts().head(5) # Consulta, conta e armazena os cinco estados mais frequentes.
top_rodovias = dataset_prf['br'].value_counts().head(5) # Consulta, conta e armazena as cinco BRs mais frequentes.

# Criando uma figura com 2 gráficos lado a lado
fig, axes = plt.subplots(1, 2, figsize=(14, 5)) # cria dois espaços para gráficos em uma mesma figura

# Gráfico de UFs            (axes = [0] - gráfico 1 , [1] - gráfico 2)
sns.barplot(x=top_ufs.values, y=top_ufs.index, ax=axes[0], palette='viridis') # Primeiro gráfico
axes[0].set_title('Top 5 Estados (UFs) com Mais Acidentes', fontsize=13) # define o título desse gráfico
axes[0].set_xlabel('Total de Registros') # define o nome do eixo X

# Gráfico de Rodovias       (.astype() - converte os valores para texto)
sns.barplot(x=top_rodovias.values, y=top_rodovias.index.astype(str), ax=axes[1], palette='flare') # Segundo gráfico
axes[1].set_title('Top 5 Rodovias (BR) com Mais Acidentes', fontsize=13) # define o título desse gráfico
axes[1].set_xlabel('Total de Registros') # define o nome do eixo X

plt.tight_layout() # ajusta automaticamente os espaços entre os elementos dos gráficos
plt.show()  # Exibe o gráfico

# ===================================================================
# 5. O ranking das UFs com mais acidentes muda de um mês para outro?
# ===================================================================

# Filtrando o ano de 2025 (seleciona somente as linhas de 2025)
df_ranking = dataset_prf[dataset_prf['ano'] == 2025].copy() # Cria uma cópia dos dados selecionados

# Contando os acidentes de cada UF em cada mês
contagem_uf_mes = (
    df_ranking.groupby(['mes', 'uf']) # Agrupa os registros utilizando duas colunas
    .size() # Conta as linhas em cada grupo
    .reset_index(name='acidentes') # Transforma o resultado agrupado em um DataFrame organizado
)

# Ordenando cada mês do maior para o menor número de acidentes
contagem_uf_mes = contagem_uf_mes.sort_values( # .sort_values() - ordena os registros com base nas colunas informadas
    ['mes', 'acidentes', 'uf'],
    # mes: organiza os meses em ordem crescente.
    # acidentes: organiza a quantidade de acidentes dentro de cada mês.
    # uf: utiliza a sigla como critério de desempate.
    ascending=[True, False, True]
    # True para mes: janeiro vem antes de fevereiro
    # False para acidentes: os maiores totais vêm primeiro
    # True para uf: em caso de empate, a sigla é ordenada alfabeticamente
)

# Selecionando o Top 5 de cada mês
top5_mensal = (
    contagem_uf_mes.groupby('mes') # Separa a tabela por mês
    .head(5) # Seleciona as cinco primeiras linhas de cada grupo
    .copy() # Cria uma cópia do resultado selecionado.
)

# Atribuindo posições de 1º a 5º em cada mês
top5_mensal['ranking'] = ( # .cumcount() - Conta as linhas de cada grupo, começando em zero
    top5_mensal.groupby('mes').cumcount() + 1
            # + 1 - Transforma essa contagem em posições de ranking começando em 1
)

# Definindo os nomes dos meses
nomes_meses = { # cria um dicionário
    1: 'Janeiro',
    2: 'Fevereiro',
    3: 'Março',
    4: 'Abril',
    5: 'Maio',
    6: 'Junho',
    7: 'Julho',
    8: 'Agosto',
    9: 'Setembro',
    10: 'Outubro',
    11: 'Novembro',
    12: 'Dezembro'
}   # Um dicionário associa uma chave a um valor.
    # Nesse caso, a chave é o número do mês e o valor é o nome correspondente.

top5_mensal['mes_nome'] = ( # salva o resultado em uma nova coluna chamada mes_nome
    top5_mensal['mes'].map(nomes_meses) # seleciona a coluna com os números dos meses
    # .map(nomes_meses) procura cada número no dicionário e substitui o número pelo nome correspondente
)

# Exibindo a tabela com o ranking e os acidentes
print('\n--- TOP 5 DE UFs POR MÊS - ANO DE 2025 ---')

print(
    top5_mensal[
        ['mes_nome', 'ranking', 'uf', 'acidentes'] # Seleciona as 4 colunas que exibiremos
    ].to_string(index=False) # Converte a tabela em texto para impressão no terminal
)

# Criando uma tabela com as posições de cada UF
tabela_top5 = top5_mensal.pivot( # pivot() - transforma linhas em colunas, reorganizando a tabela
    index='mes', # cada linha representa um mês
    columns='uf', # cada coluna representa uma UF
    values='ranking' # cada célula contém a posição da UF naquele mês
).reindex(range(1, 13)) # gera os números de 1 até 12, sem incluir 13

# Criando uma tabela com as quantidades de acidentes
tabela_acidentes = top5_mensal.pivot( # pivot() - transforma linhas em colunas, reorganizando a tabela
    index='mes', # cada linha representa um mês
    columns='uf', # cada coluna representa uma UF
    values='acidentes' # cada célula contém a posição da UF naquele mês
).reindex(range(1, 13)) # gera os números de 1 até 12, sem incluir 13
"""
    Essas duas tabelas trabalham juntas:
        tabela_top5: informa onde desenhar cada ponto.
        tabela_acidentes: informa qual número escrever ao lado do ponto.
"""
# Criando o gráfico
plt.figure(figsize=(16, 9)) # Cria uma figura com sua largura e altura. (1 - largura, 2 - altura)

for uf in tabela_top5.columns: # contém os nomes das colunas, que representam as UFs que estaram no Top 5
# O 'for' percorre as siglas uma por vez. Para cada UF, o código desenha sua linha e adiciona os totais correspondentes


    # Desenhando a linha da UF no ranking
    plt.plot( # desenha a linha da UF que está sendo processada pelo 'for'
        tabela_top5.index, # fornece os números dos meses para o eixo horizontal
        tabela_top5[uf], # fornece as posições no ranking para o eixo vertical
        marker='o', # coloca um círculo em cada ponto mensal
        linewidth=2, # define a espessura da linha
        markersize=5, # define o tamanho dos círculos
        label=uf # associa a sigla da UF à linha, para aparecer na legenda
    )

    # Adicionando a quantidade de acidentes ao lado de cada ponto
    for mes in tabela_top5.index: # Esse segundo for está dentro do primeiro,
        # Isso significa que, para cada UF, o código percorre os meses de janeiro a dezembro.
        # Na prática, o primeiro for percorre as UFs; o segundo percorre os meses de cada UF.

        posicao = tabela_top5.loc[mes, uf]
        # .loc[] permite localizar um valor utilizando os rótulos da linha e da coluna
        """ Neste caso:
            mes: seleciona a linha correspondente ao mês.
            uf: seleciona a coluna correspondente à UF.

            O resultado é armazenado na variável 'posicao'
        """

        # Ignorar meses em que a UF não ficou no Top 5
        if pd.notna(posicao): # verifica se a posição encontrada não é um valor ausente.
            """
            pd.notna(posicao) retorna True se houver uma posição válida.
            Retorna False se a UF não aparecer no Top 5 daquele mês.

            o código só adiciona um número quando existe um ponto válido no gráfico
            """

            total = tabela_acidentes.loc[mes, uf]
            # procura o total de acidentes da UF naquele mês e armazena na variável 'total'.
            # A variável total será usada para escrever o número ao lado do ponto.

            plt.annotate( # Adiciona uma anotação de texto em uma posição específica
                f'{int(total)}', # Transforma o total em texto para que possa ser exibido
                (mes, posicao), # Define as coordenadas do ponto ao qual o texto está associado
                textcoords='offset points', # Indica que o deslocamento do texto será medido em pontos tipográficos, e não em coordenadas dos dados.
                xytext=(0, 8), # Posiciona o texto = 0 - sem deslocamento horizontal , 8 - oito pontos acima do ponto.
                ha='center', # Centraliza horizontalmente o texto em relação ao ponto
                fontsize=8 # Define o tamanho da fonte como 8, ajudando a manter os números compactos
            )

# Personalizando o gráfico
plt.title( # define o título principal.
    'Top 5 Mensal de Acidentes por UF - 2025',
    fontsize=14 # tamanho da fonte
)

plt.xlabel('Mês', fontsize=12) # define o eixo horizontal como “Mês”
plt.ylabel('Posição no Ranking', fontsize=12) # define o eixo vertical como “Posição no Ranking”.
# O eixo horizontal representa os meses; o vertical representa as posições de 1 a 5

plt.xticks(
    range(1, 13), # gera as posições de 1 a 12, excluindo o 13
    list(nomes_meses.values()), # obtém os nomes dos meses do dicionário e os converte em uma lista
    rotation=45 # gira os nomes dos meses em 45 graus
)

# Colocar o 1º lugar no topo
plt.yticks(range(1, 6)) # Define as posições exibidas no eixo vertical: 1, 2, 3, 4 e 5
plt.gca().invert_yaxis() # Inverte a orientação do eixo vertical, em um ranking, o 1º lugar deve aparecer no topo e o 5º lugar mais abaixo

plt.grid( # exibe linhas de grade para ajudar na leitura do gráfico
    True, # ativa a grade
    linestyle='--', # utiliza linhas tracejadas
    alpha=0.4) # deixa as linhas parcialmente transparentes

plt.legend( # identifica qual linha pertence a cada UF
    title='UF', # define o título da legenda.
    bbox_to_anchor=(1.02, 1), # posiciona a legenda fora da área principal, à direita
    loc='upper left' # utiliza o canto superior esquerdo da legenda como referência para posicioná-la
)

plt.tight_layout() # Ajusta automaticamente o espaçamento entre os elementos do gráfico
plt.show() # exibe o gráfico na tela
