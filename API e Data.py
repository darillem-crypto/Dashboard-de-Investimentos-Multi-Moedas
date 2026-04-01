
import requests

url = "GET https://economia.awesomeapi.com.br/json/last/{moedas}?token=SEU_API_KEY"

response = requests.get(url)

usd = response.json()




