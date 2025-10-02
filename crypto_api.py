# api_crypto.py
import requests

def get_crypto_data():
    ids = ["ripple", "stellar", "hedera-hashgraph", "ondo-finance", 
           "xdce-crowd-sale", "kaspa"]
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join(ids),
        "vs_currencies": "usd,brl",  # USD e BRL
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print("Erro ao buscar dados:", e)
        return {}
