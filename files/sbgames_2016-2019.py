# -*- coding: utf-8 -*-
"""
@author: Clausius Duque Reis (clausiusreis@gmail.com)

SBGames 2016-2019

Pega somente os artigos (PDF) de cada edição do SBGames contendo palavras chave
"""

import requests
import pdfplumber
import re
import io

# Neste script é necessário informar o link de cada artigo do evento,
# pois a página do evento previne a coleta automática
url = "Fontes_SBGames_2019-2016/sbgames2019.txt"

palavras_chave1 = ['mulher', 'garota', 'menina', 'feminino', 'feminina', 
          'gênero', 'woman', 'women', 'girl', 'female', 'gender']

palavras_chave2 = ['gamificação', 'gamification']

print("####################################################")
print("### Início da coleta de dados ######################")
print("####################################################\n")

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-us,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'DNT': '1'
}

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

selectedPapers = []

with open(url, 'r', encoding='latin-1') as f:
    lines = f.readlines()
    
    for line in lines:       
        totalArtigos += 1
        
        print(" . %d - %s" % (totalArtigos, line.strip()))
        
        encontradas1 = extrair_info_pdf(line.strip(), palavras_chave1, headers)
        if len(encontradas1) > 0:
            
            encontradas2 = extrair_info_pdf(line.strip(), palavras_chave2, headers)        
            if len(encontradas2) > 0:
                
                print('\n #   Artigo: %s' % line)
                print(' #   Palavras 1 (%s): %s' % (len(encontradas1), encontradas1))
                print(' #   Palavras 2 (%s): %s\n' % (len(encontradas2), encontradas2))
                
                selectedPapers.append([line.strip()])
                
                totalSelecionados += 1

file = open('Coleta_SBGames_2019.csv','w')
for p in selectedPapers:
 	file.write("%s\n" % p[0])
file.close()

print("####################################################")
print("### Coleta de dados finalizada #####################")
print("###")
print("### Total de artigos: %s", totalArtigos)
print("### Artigos selecionados: %s", totalSelecionados)
print("####################################################")