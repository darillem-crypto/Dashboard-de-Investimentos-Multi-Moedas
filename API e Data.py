
import requests
moedas = "USD"
url = f"https://economia.awesomeapi.com.br/json/last/{moedas}"
response = requests.get(url)
usd = response.json()


for chave_moeda in usd:
    dados = usd[chave_moeda]
    venda= float(dados['ask'])
    compra = float(dados['bid'])
    preco_final= (compra + venda) /2
    porcent_de_variação = float(dados['pctChange'])
    abertura = compra/(1 + porcent_de_variação/100)
    variação = ((preco_final - abertura)/abertura) *100
    print(f'a sua moeda escolhida foi:{dados['code']}')
    print(f'a media do preço é: {preco_final:.4f}')
    print(f'a porcentagem de variação informada pela API é: {porcent_de_variação:.2f}%')
    print(f'o valor estimado no inicio do dia foi de : R$ {abertura:.4f}')
    print(f'o preço médio oscilou em relação à abertura: {variação:.2f}%')



