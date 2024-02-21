import re

try:
    import pandas as pd
except ImportError:
    print("Pandas não encontrado")

try:
    with open('Partnership.txt', 'r') as arquivo:
        dados = {"Nomes": [], "Cotas": []}
        for linha in arquivo:
            if "CPF" in linha: #Analisa apenas as linhas que contém CPF de alguma pessoa, já que neste caso do contrato não há ambiguidades quanto ao CPF
                nome = linha.split(',')[0] #O comando split separa o conteúdo da linha em uma lista, onde os elementos da lista são determinados pelo conteúdo entre as vírgulas
                cota = linha.split(',')[5] #O número 5 corresponde as cotas
                dados["Cotas"].append(re.sub("[^0-9]", "", cota)) #Remove as letras e mantém apenas os números de cotas, salva na lista
                dados["Nomes"].append(re.sub(r'[0-9.,]', '', nome)) #Remove os números, pontos e vírgulas e mantém apenas os nomes, salva na lista
            
            #print(re.sub("[^0-9]", "", linha.split(',')[5])) Assim poderia ser feito em menos linhas, mas em linhas separadas facilita a legibilidade do código :)
        pass
except FileNotFoundError:
    print("Arquivo não encontrado.")

df = pd.DataFrame(dados) #Monta a tabela com os dados desejados

df.to_csv('Tarefa_3.csv', index=False) #Salva a tabela 3

print(df)