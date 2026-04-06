import requests
from datetime import datetime

def mostrar_menu():
    print("\n" + "=" * 40)
    print("     DASHBOARD CAMBIAL")
    print("=" * 40)
    print("USD - Dólar Americano")
    print("EUR - Euro")
    print("JPY - Iene Japonês")
    print("GBP - Libra Esterlina")
    print("CNY - Yuan Chinês")
    print("CAD - Dólar Canadense")
    print("AUD - Dólar Australiano")
    print("CHF - Franco Suíço")
    print("HKD - Dólar de Hong Kong")
    print("SGD - Dólar de Singapura")
    print("=" * 40)


def obter_moeda():
    return input("Digite o código da moeda: ").upper()


def buscar_dados(moeda):
    url = f"https://economia.awesomeapi.com.br/json/last/{moeda}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except ValueError:
        print("Erro ao buscar dados.")
        return None


def calcular(dados):
    venda = float(dados['ask'])
    compra = float(dados['bid'])

    preco_medio = (compra + venda) / 2
    variacao_api = float(dados['pctChange'])

    abertura = compra / (1 + variacao_api / 100)
    variacao_real = ((preco_medio - abertura) / abertura) * 100

    return preco_medio, variacao_api, abertura, variacao_real


def sistema_pontuacao(preco_medio, abertura, variacao_real):
    score = 0

    # Tendência
    if variacao_real > 1:
        score += 2
    elif variacao_real > 0:
        score += 1
    elif variacao_real < -1:
        score -= 2
    else:
        score -= 1

    if preco_medio > abertura:
        score += 1
    else:
        score -= 1

    if abs(variacao_real) > 2:
        score += 1

    return score


def decisao(score):
    if score >= 3:
        return "COMPRAR"
    elif score <= -2:
        return "VENDER"
    else:
        return "AGUARDAR"


def salvar_historico(dados, resultados, score, recomendacao):
    preco_medio, variacao_api, abertura, variacao_real = resultados
    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    with open("historico.txt", "a", encoding="utf-8") as arq:
        arq.write("=" * 40 + "\n")
        arq.write(f"Data: {data}\n")
        arq.write(f"Moeda: {dados['code']}\n")
        arq.write(f"Preço médio: R$ {preco_medio:.4f}\n")
        arq.write(f"Variação API: {variacao_api:.2f}%\n")
        arq.write(f"Abertura: R$ {abertura:.4f}\n")
        arq.write(f"Oscilação: {variacao_real:.2f}%\n")
        arq.write(f"Score: {score}\n")
        arq.write(f"Recomendação: {recomendacao}\n")
        arq.write("=" * 40 + "\n\n")


def mostrar(dados, resultados, score, recomendacao):
    preco_medio, variacao_api, abertura, variacao_real = resultados

    print("\n" + "=" * 40)
    print(f"Moeda: {dados['code']}")
    print(f"Preço médio: R$ {preco_medio:.4f}")
    print(f"Variação API: {variacao_api:.2f}%")
    print(f"Abertura estimada: R$ {abertura:.4f}")
    print(f"Oscilação: {variacao_real:.2f}%")
    print(f"Pontuação: {score}")
    print(f"Recomendação: {recomendacao}")
    print("=" * 40)


def main():
    while True:
        mostrar_menu()
        moeda = obter_moeda()

        dados_json = buscar_dados(moeda)

        if dados_json:
            for chave in dados_json:
                dados = dados_json[chave]

                resultados = calcular(dados)
                preco_medio, variacao_api, abertura, variacao_real = resultados

                score = sistema_pontuacao(preco_medio, abertura, variacao_real)
                recomendacao = decisao(score)

                mostrar(dados, resultados, score, recomendacao)
                salvar_historico(dados, resultados, score, recomendacao)

        continuar = input("\nDeseja consultar outra moeda? (sim/nao): ").lower()
        if continuar != 'sim':
            print("Encerrando sistema...")
            break

if __name__ == "__main__":
    main()