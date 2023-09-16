# -*- coding: utf-8 -*-
"""
@author: Clausius Duque Reis (clausiusreis@gmail.com)

SBGames 2022-2021

Pega somente os resumos dos artigos de cada edição do SBGames contendo palavras chave
"""

from bs4 import BeautifulSoup
import requests

url = 'https://sol.sbc.org.br/index.php/sbgames_estendido/issue/archive'

terms1 = ['mulher', 'garota', 'menina', 'feminino', 'feminina', 
          'gênero', 'woman', 'women', 'girl', 'female', 'gender']

terms2 = ['gamificação', 'gamification']


print("####################################################")
print("### Início da coleta de dados ######################")
print("####################################################\n")

totalArtigos = 0
totalSelecionados = 0

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'}

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

edicoes = soup.find_all('a', class_='title')

selectedPapers = []

for ed in edicoes:
    title = (ed.text).strip()
    link = (ed['href'])

    response = requests.get(link)    

    soupPapers = BeautifulSoup(response.text, 'html.parser')

    papers = soupPapers.find_all('div', class_='title')

    for p in papers:     
        
        totalArtigos += 1
        
        title_div = p.find('a')
        title = (title_div.text).strip()
        link = (title_div['href'])
        
        print(" . %d - %s" % (totalArtigos, title))
        
        response = requests.get(link)    
        soupAbstract = BeautifulSoup(response.text, 'html.parser')
        abstract = ((soupAbstract.find('div', class_='item abstract')).text).strip()

        soupYear = soupAbstract.find('div', class_='item published')
        year = ((soupYear.find('div', class_='value')).text).strip()[-4:]

        termsFound = ""
        term1Exist = False
        term2Exist = False
        for t in terms1:
            nTitle = title.lower().count(t.lower())
            nAbstract = abstract.lower().count(t.lower())            
            if (nTitle > 0) | (nAbstract > 0):
                term1Exist = True            
                termsFound = termsFound + ", " + t.lower()

        for t in terms2:
            nTitle = title.lower().count(t.lower())
            nAbstract = abstract.lower().count(t.lower())
            if (nTitle > 0) | (nAbstract > 0):
                term2Exist = True            
                termsFound = termsFound + ", " + t.lower()
        
        termsFound = termsFound[2:]
        
        if (term1Exist == True and term2Exist == True):
            print('\n #   Artigo: %s' % title)
            print(' #   Palavras: %s' % (termsFound))
            print(' #   Link: %s \n' % link)
                
            selectedPapers.append("%s,%s" % (year, link))
            
            totalSelecionados += 1

file = open('Coleta_SBGames_2022-2021.csv','w')
for p in selectedPapers:
	file.write("%s\n" % p)
file.close()

print("####################################################")
print("### Coleta de dados finalizada #####################")
print("###")
print("### Total de artigos: %s", totalArtigos)
print("### Artigos selecionados: %s", totalSelecionados)
print("####################################################")