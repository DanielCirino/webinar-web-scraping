import requests
from bs4 import BeautifulSoup as bs4
#bibliotecas para análise de dados
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__== "__main__":
    urlBase = "https://pokemondb.net/pokedex/national"
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
        respostaHttp = requests.get(urlBase, headers=headers)
        assert respostaHttp.status_code == 200

        conteudoHtml = respostaHttp.content
        soup = bs4(conteudoHtml, 'html.parser')
        geracoes = soup.select("ul.list-nav li a")
        print(geracoes)
    except Exception as e:
        print(e)
