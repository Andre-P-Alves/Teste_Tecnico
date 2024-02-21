try:
    import pandas as pd
except ImportError:
    print("Pandas não encontrado")

# - Regras de Comissão:
#     - Cada vendedor recebe 10% de cada venda.
#     - Se a venda foi realizada por um canal online, 20% da comissão do vendedor vai para a equipe de marketing.
#     - Se o valor total da comissão do vendedor for maior ou igual a R$ 1.500,00, 10% dessa comissão vai para o gerente de vendas.
# - Saída Esperada: Uma tabela com o nome do vendedor, o valor da comissão, e o valor que será pago a ele, considerando as regras estabelecidas.

#FUNÇÕES

def formatador(x):
    return "R$ {:,.2f}".format(x).replace(".", ",") #Função para transformar os floats em string do tipo R$1.234,56

def calcular_comissao(dados):
    comissao_vendedor = dados['Valor da Venda'] * TAXA_COMISSAO #Observação: é enunciado que a comissão é 10% de cada venda, e não do lucro, por isso não foi subtraído o custo
    comissao_final = comissao_vendedor

    if dados['Canal de Venda'] == "Online": #Se a venda for realizada por um canal online, 20% vai para a equipe de marketing
        comissao_final -= comissao_vendedor * TAXA_MARKETING

    if comissao_vendedor >= 1500: #Se o valor da comissão ultrapassar 1500, 10% da comissão é direcionada ao gerente de vendas
        comissao_final -= comissao_vendedor * TAXA_GERENTE
        
    return comissao_vendedor, comissao_final

def teste_nulos(df):
    # Check if any null values exist in the DataFrame
    assert df.isnull().values.any() == False, "Erro: DataFrame tem valores nulos"
    print("Não há valores nulos")

#CONSTANTES

TAXA_COMISSAO = 0.1 # 10% de cada venda
TAXA_MARKETING = 0.2 # 20% da comissão
TAXA_GERENTE = 0.1 # 10% da comissão

#CÓDIGO

file_path_vendas = 'Vendas - Vendas.csv' #Caminho relativo do arquivo

try:
    # Tenta encontrar o arquivo
    dataframe = pd.read_csv(file_path_vendas) #Carregar os dados, salvos em um arquivo tipo CSV
    print("Arquivo encontrado.")
except FileNotFoundError:
    print(f"Erro: Arquivo '{file_path_vendas}' não encontrado.")
except pd.errors.ParserError:
    print(f"Erro: Não foi possível analisar o arquivo '{file_path_vendas}'.")
except Exception as e:
    print(f"Um erro inesperado aconteceu: {e}")

teste_nulos(dataframe) #Verifica se tem valores nulos

dataframe['Valor da Venda'] = dataframe['Valor da Venda'].str.replace('R$ ', '').str.replace('.', '').str.replace(',', '.').astype(float) #Transformar os campos string do tipo "R$ 1.000,0"em float

dataframe['Valor da Comissão'], dataframe['Valor Devido ao Vendedor'] = zip(*dataframe.apply(calcular_comissao, axis=1)) #A função retorna uma tupla com dois valores, zip atribui para cada coluna

tabela_final = dataframe.groupby('Nome do Vendedor').agg({
    'Valor da Comissão': 'sum',
    'Valor Devido ao Vendedor': 'sum'
}).reset_index() #Agrupa por nome de vendedor, e soma os valores das colunas escolhidas para a nova tabela agrupada

#O agrupamento é feito no final pois no enunciado é dito que é 10% em cima do valor de cada venda, além de também ter a possibilidade de algumas vendas terem regras diferentes

# - Entrada: Segunda aba da planilha (“Pagamentos”)
# - Regras de Validação:
# - Comparar os valores pagos aos vendedores com os valores calculados na Tarefa 1.
# - Identificar os pagamentos feitos incorretamente e o valor incorreto transferido.
# - Saída Esperada: Uma lista dos pagamentos feitos incorretamente, indicando o vendedor, o valor pago erroneamente e o valor correto que deveria ter sido pago.

file_path_pagamentos = 'Vendas - Pagamentos.csv' #Caminho relativo

try:
    # Tenta encontrar o arquivo
    df_pagamentos = pd.read_csv(file_path_pagamentos) #Carregar os dados, salvos em um arquivo tipo CSV
    print("Arquivo encontrado.")
except FileNotFoundError:
    print(f"Erro: Arquivo '{file_path_pagamentos}' não encontrado.")
except pd.errors.ParserError:
    print(f"Erro: Não foi possível analisar o arquivo '{file_path_pagamentos}'.")
except Exception as e:
    print(f"Um erro inesperado aconteceu: {e}")

teste_nulos(df_pagamentos) #Verifica se tem valores nulos

assert len(tabela_final) == len(df_pagamentos), "Erro: DataFrames não tem o mesmo número de linhas" #Verifica se a tabela tem o mesmo tamanho

df_pagamentos['Comissão'] = df_pagamentos['Comissão'].str.replace('R$ ', '').str.replace('.', '').str.replace(',', '.').astype(float) #Transformar os campos string do tipo "R$ 1.000,0"em float

merged_df = pd.merge(tabela_final, df_pagamentos, on="Nome do Vendedor") #Junta as duas tabelas baseado no nome dos vendedores

merged_df['Diferença'] = merged_df['Valor Devido ao Vendedor'] - merged_df['Comissão'] #Gera uma coluna com a diferença entre o valor pago e o valor correto

differences_df = merged_df[merged_df['Diferença'] != 0] #Pega apenas as linhas onde houve pagamento errado

colunas_mantidas = ["Nome do Vendedor", "Valor Devido ao Vendedor", "Comissão", "Diferença"] #Declara as colunas que eu desejo manter na tabela

tabela_final_2 = merged_df.loc[:, colunas_mantidas] #Faz uma tabela com as colunas desejadas

tabela_final['Valor Devido ao Vendedor'] = tabela_final['Valor Devido ao Vendedor'].apply(formatador) #Transformar os floats em string R$ 

tabela_final['Valor da Comissão'] = tabela_final['Valor da Comissão'].apply(formatador) 

tabela_final_2['Valor Devido ao Vendedor'] = tabela_final_2['Valor Devido ao Vendedor'].apply(formatador) 

tabela_final_2['Comissão'] = tabela_final_2['Comissão'].apply(formatador) 

tabela_final_2['Diferença'] = tabela_final_2['Diferença'].apply(formatador) 

tabela_final.to_csv('Tarefa_1.csv', index=False) #Salva a tabela 1

tabela_final_2.to_csv('Tarefa_2.csv', index=False) #Salva a tabela 2

print(tabela_final)
print("\n")
print(tabela_final_2)