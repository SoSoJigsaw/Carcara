import pandas as pd
import numpy as np
import datetime as dt
from datetime import datetime


url1 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/covid-estado-sp.csv'
url2 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/covid-municipios-sp.csv'
url4 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/vacinometro-sp.csv'
url5 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/evolucao-aplicacao-doses.csv'
url6 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/leitos-uti-enfermaria.csv'
url7 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/isolamento-social.csv'
url8 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/vacinacao-estatisticas.csv'


estatis = pd.read_csv(url8)

'''
# ---------------------------------------  CASOS E ÓBITOS DO ESTADO  ------------------------------------------------ #

covidsp = pd.read_csv(url1, dtype={'Total de casos': 'int32', 'Total de óbitos': 'int32',
                                   'Casos por dia': 'int32', 'Óbitos por dia': 'int16'})
covidsp['Data'] = pd.to_datetime(covidsp['Data'])

# GRÁFICO CASOS POR DIA (Variação nos últimos 7 dias)
data = covidsp['Data'].min().strftime('%Y-%m-%d')
if data == covidsp['Data'].min().strftime('%Y-%m-%d'):
    print('Variação de casos em comparação à 7 dias atrás: 0%')
else:
    casos = covidsp[covidsp['Data'] == data]['Casos por dia'].values[0]
    data = pd.to_datetime(data)
    casos7 = covidsp[covidsp['Data'] == (data - dt.timedelta(days=7))]['Casos por dia'].values[0] #7 dias atrás
    x = (casos*100) / casos7-100
    print('Variação de casos em comparação à 7 dias atrás: %.1f' %x, '%')

# GRÁFICO ÓBITOS POR DIA (Variação nos últimos 7 dias)
data = '2018-06-20'
if data <= covidsp['Data'].min().strftime('%Y-%m-%d'):
    print('Variação de óbitos em comparação à 7 dias atrás: 0%')
else:
    casos = covidsp[covidsp['Data'] == data]['Óbitos por dia'].values[0]
    obi = pd.to_datetime(data)
    obi7 = covidsp[covidsp['Data'] == (data - dt.timedelta(days=7))]['Óbitos por dia'].values[0] #7 dias atrás
    x = (obi * 100) / obi7 - 100
    print('Variação de óbitos em comparação à 7 dias atrás: %.1f' % x, '%')


# GRÁFICO TOTAL DE CASOS (Taxa de Incidência)
pop = 44000000 #população do estado de SP
casos = covidsp[covidsp['Data'] == data]['Casos por dia'].values[0]

inc = casos / (pop-casos) * 100000
print('Incidência de casos: %.f' %inc, 'a cada 100 mil habitantes')

# GRÁFICO TOTAL DE ÓBITOS (Taxa de Letalidade)
obtotal = covidsp[covidsp['Data'] == data]['Total de óbitos'].values[0]
casostotal = covidsp[covidsp['Data'] == data]['Total de casos'].values[0]

let = (obtotal/casostotal) * 100
print('Taxa de letalidade no Estado: %.1f' %let, '%')

# ---------------------------------------  VACINAÇÃO DO ESTADO  ------------------------------------------------ #

evoludose = pd.read_csv(url5, dtype={'1ª Dose': 'int32', '2ª Dose': 'int32', '3ª Dose': 'int32', 'Dose Única': 'int32'})
evoludose['Data'] = pd.to_datetime(evoludose['Data'])

# EVOLUÇÃO 1ª DOSE (Variação nos últimos 7 dias)
dose = evoludose[evoludose['Data'] == data]['1ª Dose'].values[0]
dose7 = evoludose[evoludose['Data'] == (data - dt.timedelta(days=7))]['1ª Dose'].values[0]

if dose7 > 100:
    evol = (dose*100) / dose7-100
    print('Taxa de aplicação da 1ª dose: Variação de %.1f' %evol, '% comparado a 7 dias atrás')
else:
    print('Taxa de aplicação da 1ª dose: Sem dados para este período')

# EVOLUÇÃO 2ª DOSE (Variação nos últimos 7 dias)
dose = evoludose[evoludose['Data'] == data]['2ª Dose'].values[0]
dose7 = evoludose[evoludose['Data'] == (data - dt.timedelta(days=7))]['2ª Dose'].values[0]

if dose7 > 100:
    evol = (dose*100) / dose7-100
    print('Taxa de aplicação da 2ª dose: Variação de %.1f' %evol, '% comparado a 7 dias atrás')
else:
    print('Taxa de aplicação da 2ª dose: Sem dados para este período')

# EVOLUÇÃO 3ª DOSE (Variação nos últimos 7 dias)

dose = evoludose[evoludose['Data'] == data]['3ª Dose'].values[0]
dose7 = evoludose[evoludose['Data'] == (data - dt.timedelta(days=7))]['3ª Dose'].values[0]

if dose7 > 100:
    evol = (dose*100) / dose7-100
    print('Taxa de aplicação da 3ª dose: Variação de %.1f' %evol, '% comparado a 7 dias atrás')
else:
    print('Taxa de aplicação da 3ª dose: Sem dados para este período')

# EVOLUÇÃO DOSE ÚNICA (Variação nos últimos 7 dias)
dose = evoludose[evoludose['Data'] == data]['Dose Única'].values[0]
dose7 = evoludose[evoludose['Data'] == (data - dt.timedelta(days=7))]['Dose Única'].values[0]

if dose7 > 100:
    evol = (dose*100) / dose7-100
    print('Taxa de aplicação da dose única: Variação de %.1f' %evol, '% comparado a 7 dias atrás')
else:
    print('Taxa de aplicação da dose única: Sem dados para este período')



# ---------------------------------------  LEITOS DO ESTADO  ------------------------------------------------ #

leitos = pd.read_csv(url6, dtype={'Departamento Regional de Saúde': 'category',
                                  'mm7d da Ocupação dos leitos de UTI e Enfermaria (%)': 'float64',
                                  'Nº de novas internações nos últimos 7 dias': 'int32',
                                  'Pacientes em tratamento na UTI': 'int16',
                                  'Total de leitos de UTI destinados à Covid': 'int16',
                                  'Ocupação dos leitos de UTI e Enfermaria (%)': 'float64',
                                  'Novos casos de internações (UTI e Enfermaria)': 'int16',
                                  'Pacientes em tratamento na Enfermaria': 'int16',
                                  'Total de leitos de Enfermaria destinados à Covid': 'int32'})
leitos['Data'] = pd.to_datetime(leitos['Data'])
leitos = leitos[leitos['Departamento Regional de Saúde'] == 'Estado de São Paulo']

# OCUPAÇÃO DOS LEITOS DE UTI E ENFERMARIA NO ESTADO (%) (Variação nos últimos 7 dias)
ocup = leitos[leitos['Data'] == data]['Ocupação dos leitos de UTI e Enfermaria (%)'].values[0]
ocup7 = leitos[leitos['Data'] == (data - dt.timedelta(days=7))]['Ocupação dos leitos de UTI e Enfermaria (%)'].values[0]

x = (ocup*100) / ocup7-100
print('Ocupação de leitos {0}%. Comparação com 7 dias atrás: {1:.2f}'.format(ocup, x), '%')

# NÚMERO DE LEITOS DE UTI E ENFERMARIA NO ESTADO (Número de leitos por pessoa no Estado)
data = leitos['Data'].max().strftime('%Y-%m-%d')
utitotal = leitos[leitos['Data'] == data]['Total de leitos de UTI destinados à Covid'].values[0]
enftotal = leitos[leitos['Data'] == data]['Total de leitos de Enfermaria destinados à Covid'].values[0]
pop = 44000000
info2_1 = pop / utitotal
info2_2 = pop / enftotal



# NOVAS INTERNAÇÕES POR DIA NO ESTADO (Variação nos últimos 7 dias)
inter = leitos[leitos['Data'] == data]['Novos casos de internações (UTI e Enfermaria)'].values[0]
inter7 = leitos[leitos['Data'] == (data - dt.timedelta(days=7))]['Novos casos de internações (UTI e Enfermaria)'].values[0]

x = (inter*100) / inter7-100
print('Novas internações: {0}. Comparação com 7 dias atrás: {1:.2f}'.format(inter, x), '%')


# ---------------------------------------  ISOLAMENTO DO ESTADO  ------------------------------------------------ #

isola = pd.read_csv(url7, dtype={'Município': 'category', 'codigo_ibge': 'category', 'Índice de Isolamento (%)': 'int8',
                                 'Dia da Semana': 'category'})
isola['Data'] = pd.to_datetime(isola['Data'])
isola = isola[isola['Município'] == 'Estado De São Paulo']

# INDICE DE ISOLAMENTO (Variação dos últimos 7 dias)
iso = isola[isola['Data'] == data]['Índice de Isolamento (%)'].values[0]
iso7 = isola[isola['Data'] == (data - dt.timedelta(days=7))]['Índice de Isolamento (%)'].values[0]

ind = (iso*100) / iso7-100
print('Isolamento no Estado em relação aos últimos 7 dias: %.1f' %ind, '%')

# ---------------------------------------  CASOS E ÓBITOS MUNICÍPIOS  -------------------------------------------- #

covidmuni = pd.read_csv(url2, dtype={'Município': 'category', 'codigo_ibge': 'category', 'Total de Casos': 'int32',
                                     'Novos Casos': 'int16', 'Total de Óbitos': 'int32', 'Novos Óbitos': 'int16',
                                     'Mesorregião': 'category', 'Microrregião': 'category'})
covidmuni['Data'] = pd.to_datetime(covidmuni['Data'])

# CASOS POR DIA (Variação dos últimos 7 dias)

# casos = covidmuni[covidmuni['Data'] == data]['Novos Casos'].values[0]
# casos7 = covidmuni[covidmuni['Data'] == (data - dt.timedelta(days=7))]['Novos Casos'].values[0] #7 dias atrás

# x = (casos*100) / casos7-100
# print('Casos em comparação a 7 dias atrás: %.1f' %x, '%')

# ÓBITOS POR DIA (Variação dos últimos 7 dias)

# obi = covidmuni[covidmuni['Data'] == data]['Novos Óbitos'].values[0]
# obi7 = covidmuni[covidmuni['Data'] == (data - dt.timedelta(days=7))]['Novos Óbitos'].values[0] #7 dias atrás

# x = (obi*100) / obi7-100
# print('Óbitos em comparação a 7 dias atrás: %.1f' %x, '%')

# TOTAL DE CASOS POR MUNICIPIO (Incidencia)

# pop = 44000000 #população do município X
# casos = covidmuni[covidmuni['Data'] == data]['Novos Casos'].values[0]

# inc = casos / (pop-casos) * 100000
# print('Incidência de casos: %.f' %inc, 'a cada 100 mil habitantes')

# TOTAL DE OBITOS POR MUNICIPIO (Letalidade)

obtotal = covidmuni[covidmuni['Data'] == data]['Total de Óbitos'].values[0]
casostotal = covidmuni[covidmuni['Data'] == data]['Total de Casos'].values[0]

let = (obtotal/casostotal) * 100
print('Taxa de letalidade do município: %.1f' %let, '%')


# ---------------------------------------  VACINA MUNICÍPIOS  -------------------------------------------- #

vacina = pd.read_csv(url4, dtype={'Município': 'category', '1ª Dose': 'int32', '2ª Dose': 'int32', '3ª Dose': 'int32',
                                  'Dose Única': 'int32', 'Doses Distribuídas': 'int32'})

# COMPARATIVO DE APLICAÇAO DAS DOSES ENTRE MUNICIPIOS (Porcentagem da população vacinada *com todas as doses*)
pop = 44000000
vac = vacina['3ª Dose'].sum()
popvac = (vac * 100) / pop
info1 = "{:.2f}".format(popvac).replace('.', ',')

# COMPARATIVO DE DOSES DISTRIBUIDAS ENTRE MUNICIPIOS (Eficácia da aplicação pelo município - Distribuídas/Aplicadas)
vac = vacina['1ª Dose'].max() + vacina['2ª Dose'].max() + vacina['3ª Dose'].max() + vacina['Dose Única'].max()
dist = vacina['Doses Distribuídas'].max()
distvac = (vac * 100) / dist
info2 = "{:.2f}".format(distvac).replace('.', ',')

vacultd = vacina['1ª Dose'].iloc[-1] + vacina['2ª Dose'].iloc[-1] + vacina['3ª Dose'].iloc[-1] + vacina['Dose Única'].iloc[-1]
vacultd = "{:,}".format(vacultd).replace(',', '.')


leitos = pd.read_csv(url6, dtype={'Departamento Regional de Saúde': 'category',
                                  'mm7d da Ocupação dos leitos de UTI e Enfermaria (%)': 'float64',
                                  'Nº de novas internações nos últimos 7 dias': 'int32',
                                  'Pacientes em tratamento na UTI': 'int16',
                                  'Total de leitos de UTI destinados à Covid': 'int16',
                                  'Ocupação dos leitos de UTI e Enfermaria (%)': 'float64',
                                  'Novos casos de internações (UTI e Enfermaria)': 'int16',
                                  'Pacientes em tratamento na Enfermaria': 'int16',
                                  'Total de leitos de Enfermaria destinados à Covid': 'int32'})
leitos['Data'] = pd.to_datetime(leitos['Data'])
leitos = leitos[leitos['Departamento Regional de Saúde'] == 'Estado de São Paulo']

leitmed = leitos['Total de leitos de Enfermaria destinados à Covid'] + leitos['Total de leitos de UTI destinados ' \
                                                                              'à Covid']
leitmed = leitmed.mean()
leitmed = int("{:.0f}".format(leitmed))
leitmed = "{:,}".format(leitmed).replace(',', '.')



isola = pd.read_csv(url7, dtype={'Município': 'category', 'codigo_ibge': 'category', 'Índice de Isolamento (%)': 'int8',
                                 'Dia da Semana': 'category'})
isola['Data'] = pd.to_datetime(isola['Data'])
isola = isola[isola['Município'] == 'Estado De São Paulo']

sem = {}
for value in isola['Dia da Semana']:
    sem[value] = isola[isola['Dia da Semana'] == value]['Índice de Isolamento (%)'].sum()

semax = max(sem, key=sem.get)
semin = min(sem, key=sem.get)
'''


url2 = '/home/sobral/Carcara/Aplicação Web/app/data/covid-municipios-sp.csv'

covidmuni = pd.read_csv(url2, dtype={'Município': 'category', 'Mesorregião': 'category', 'pop': 'int32'})
covidmuni = covidmuni.drop_duplicates(subset=['Município', 'pop', 'Mesorregião'], keep='first')


covidmuni = covidmuni.query("Mesorregião == 'Vale do Paraíba Paulista'")

print(covidmuni[covidmuni['pop'] > 85000].sort_values('pop')['Município'].head(10))

''''
Lorena
São Sebastião -
Ubatuba -
Caçapava -
Caraguatatuba -
Guaratinguetá -
Pindamonhangaba -
Jacareí -
Taubaté -
São José dos Campos -
'''
