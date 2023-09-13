# -*- coding: utf-8 -*-
"""
@author: Clausius Duque Reis (clausiusreis@gmail.com)

SBGames 2020

Pega somente os artigos (PDF) de cada edição do SBGames contendo palavras chave
"""

from bs4 import BeautifulSoup
import requests
import pdfplumber
import re
import io

url = 'https://www.sbgames.org/sbgames2020/pt/proceedings/'

palavras_chave1 = ['mulher', 'garota', 'menina', 'feminino', 'feminina', 
          'gênero', 'woman', 'women', 'girl', 'female', 'gender']

palavras_chave2 = ['gamificação', 'gamification']

print("####################################################")
print("### Início da coleta de dados ######################")
print("####################################################\n")

def extrair_info_pdf(url, palavras_chave, headers):
    encontradas = []
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:

        with pdfplumber.open(io.BytesIO(response.content)) as pdf:
            texto = pdf.pages[0].extract_text()

            for palavra in palavras_chave:
                if re.search(r'\b' + palavra + r'\b', texto, re.IGNORECASE):
                    encontradas.append(palavra)

    return encontradas

totalArtigos = 0
totalSelecionados = 0

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-us,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'DNT': '1'
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')

edicoes = soup.find_all('ul')

selectedPapers = []

for ed in edicoes[4:21]:
    ed1 = ed.find_all('a')
    
    for ed2 in ed1:

        title = (ed2.text).strip()
        link = (ed2['href'])

        totalArtigos += 1

        print(" . %d - %s" % (totalArtigos, title))

        encontradas1 = extrair_info_pdf(link.strip(), palavras_chave1, headers)
        if len(encontradas1) > 0:
            
            encontradas2 = extrair_info_pdf(link.strip(), palavras_chave2, headers)        
            if len(encontradas2) > 0:
                print('\n #   Artigo: %s' % title)
                print(' #   Palavras 1 (%s): %s' % (len(encontradas1), encontradas1))
                print(' #   Palavras 2 (%s): %s\n' % (len(encontradas2), encontradas2))
                
                selectedPapers.append([link.strip()])
                
                totalSelecionados += 1

file = open('Coleta_SBGames_2020.csv','w')
for p in selectedPapers:
 	file.write("%s\n" % p[0])
file.close()

print("####################################################")
print("### Coleta de dados finalizada #####################")
print("###")
print("### Total de artigos: %s", totalArtigos)
print("### Artigos selecionados: %s", totalSelecionados)
print("####################################################")