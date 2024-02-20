import pandas as pd
import numpy as np

# - Regras de Comissão:
#     - Cada vendedor recebe 10% de cada venda.
#     - Se a venda foi realizada por um canal online, 20% da comissão do vendedor vai para a equipe de marketing.
#     - Se o valor total da comissão do vendedor for maior ou igual a R$ 1.500,00, 10% dessa comissão vai para o gerente de vendas.
# - Saída Esperada: Uma tabela com o nome do vendedor, o valor da comissão, e o valor que será pago a ele, considerando as regras estabelecidas.

TAXA_COMISSAO = 0.1 # 10% de cada venda
TAXA_MARKETING = 0.2 # 20% da comissão
TAXA_GERENTE = 0.1 # 10% da comissão

def calcular_comissao(dados):
    comissao_vendedor = dados['Valor da Venda'] * TAXA_COMISSAO #Observação: é enunciado que a comissão é 10% de cada venda, e não do lucro, por isso não foi subtraído o custo
    comissao_final = comissao_vendedor

    if dados['Canal de Venda'] == "Online": #Se a venda for realizada por um canal online, 20% vai para a equipe de marketing
        comissao_final -= comissao_vendedor * TAXA_MARKETING

    if comissao_vendedor >= 1500: #Se o valor da comissão ultrapassar 1500, 10% da comissão é direcionada ao gerente de vendas
        comissao_final -= comissao_vendedor * TAXA_GERENTE
        
    return comissao_vendedor, comissao_final

dataframe = pd.read_csv('Vendas - Vendas.csv') #Carregar os dados, salvos em um arquivo tipo CSV

dataframe['Valor da Venda'] = dataframe['Valor da Venda'].str.replace('R$ ', '').str.replace('.', '').str.replace(',', '.').astype(float) #Transformar os campos string do tipo "R$ 1.000,0"em float

dataframe['Valor da Comissão'], dataframe['Valor Pago ao Vendedor'] = zip(*dataframe.apply(calcular_comissao, axis=1)) #A função retorna uma tupla com dois valores, zip atribui para cada coluna

tabela_final = dataframe.groupby('Nome do Vendedor').agg({
    'Valor da Comissão': 'sum',
    'Valor Pago ao Vendedor': 'sum'
}).reset_index() #Agrupa por nome de vendedor, e soma os valores das colunas escolhidas para a nova tabela agrupada

#O agrupamento é feito no final pois no enunciado é dito que é 10% em cima do valor de cada venda, além de também ter a possibilidade de algumas vendas terem regras diferentes

tabela_final['Valor Pago ao Vendedor'] = tabela_final['Valor Pago ao Vendedor'].apply(lambda x: "${:,.2f}".format(x).replace(".", ",")) #Transformar os floats em string R$ 

tabela_final['Valor da Comissão'] = tabela_final['Valor da Comissão'].apply(lambda x: "${:,.2f}".format(x).replace(".", ",")) #Transformar os floats em string R$ 

tabela_final.to_csv('Tarefa_1.csv', index=False)