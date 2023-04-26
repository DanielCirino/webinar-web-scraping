import requests
from bs4 import BeautifulSoup as bs4
#bibliotecas para análise de dados
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm

urlBase = "https://pokemondb.net"
CSS_INFOCARDS="div.infocard"

CSS_IMAGEM="span.infocard-lg-img a picture img"

CSS_DADOS_POKEMON="span.infocard-lg-data"
CSS_LINK=f"{CSS_DADOS_POKEMON} a.ent-name"
CSS_CLASSES=f"{CSS_DADOS_POKEMON} small a.itype"

CSS_GERACAO = "p abbr"
CSS_LINHAS_TABELAS = ".vitals-table tr"

session = requests.Session()
def fazerRequisicao(url:str):
    try:
        headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
        respostaHttp = session.get(url,headers=headers)
        assert respostaHttp.status_code==200

        conteudoHtml = respostaHttp.content
        docHtml = bs4(conteudoHtml, 'html.parser')
        return docHtml
    except Exception as e:
        print(e)
        raise e

def obterDetalhesPokemon(htmlDetalhes):
    linhasDeDados = htmlDetalhes.select(CSS_LINHAS_TABELAS)

    dados = {}
    for linha in linhasDeDados:
        titulo = linha.select_one("th")
        conteudo= linha.select_one("td")
        dados[titulo.text]=conteudo.text.strip().split("\xa0")[0]

    return dados

if __name__== "__main__":
    docHtml = fazerRequisicao(f"{urlBase}/pokedex/national")
    infocards =docHtml.select(CSS_INFOCARDS)
    htmlPokemon = infocards[90]
    CSS_IMAGEM = "img.img-fixed"

    pokemons = []
    pokemonsTipo = []

    htmlPokemons = docHtml.select(CSS_INFOCARDS)

    for htmlPokemon in htmlPokemons:
        idPokemon = htmlPokemon.select_one(f"{CSS_DADOS_POKEMON} small").text

        htmlLink = htmlPokemon.select_one(CSS_LINK)
        nomePokemon = htmlLink.text
        urlDetalhes = htmlLink.attrs["href"]

        htmlImagem = htmlPokemon.select_one(CSS_IMAGEM)
        urlImagem = htmlImagem.attrs["src"]

        htmlTipos = htmlPokemon.select(CSS_CLASSES)
        tipos = [tag.text for tag in htmlTipos]
        tipoPrimario = tipos[0]
        tipoSecundario = ""

        if len(tipos) > 1: tipoSecundario = tipos[1]

        pokemon = {
            "id": idPokemon,
            "nome": nomePokemon,
            "url_detalhes": f"{urlBase}{urlDetalhes}",
            "tipo_primario": tipoPrimario,
            "tipo_secundario": tipoSecundario,
            "url_imagem": urlImagem,
            "geracao": "",
            "especie": "",
            "altura": 0,
            "peso": 0,
            "hp": 0,
            "ataque": 0,
            "defesa": 0,
            "ataque_especial": 0,
            "defesa_especial": 0,
            "velocidade": 0,
            "stats_total": 0,
        }

        pokemons.append(pokemon)


    for pokemon in tqdm(pokemons):
        try:
            htmlDetalhes = fazerRequisicao(pokemon["url_detalhes"])
            dadosPokemon = obterDetalhesPokemon(htmlDetalhes)

            geracao = htmlDetalhes.select_one(CSS_GERACAO).text

            pokemon['geracao'] = geracao.strip()
            pokemon['especie'] = dadosPokemon['Species']
            pokemon['altura'] = float(dadosPokemon['Height'])
            pokemon['peso'] = float(dadosPokemon['Weight'])
            pokemon['hp'] = int(dadosPokemon['HP'])
            pokemon['ataque'] = int(dadosPokemon['Attack'])
            pokemon['defesa'] = int(dadosPokemon['Defense'])
            pokemon['ataque_especial'] = int(dadosPokemon['Sp. Atk'])
            pokemon['defesa_especial'] = int(dadosPokemon['Sp. Def'])
            pokemon['velocidade'] = int(dadosPokemon['Speed'])
            pokemon['stats_total'] = int(dadosPokemon['Total'])

        except Exception as e:
            print(f"\n[ERRO] Erro ao obter detalhes do pokemon {pokemon['nome']} [{pokemon['url_detalhes']}]. **{e}**\n ")

    dfPokemons = pd.DataFrame.from_dict(pokemons)
    dfPokemons.describe()

