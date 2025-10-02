import requests   # Biblioteca usada para fazer requisições HTTP

# Função responsável por buscar os dados da API pública da CoinGecko
def get_crypto_data():
    # Lista de criptomoedas a consultar (IDs usados pela API)
    ids = ["ripple", "stellar", "hedera-hashgraph", "ondo-finance", 
           "xdce-crowd-sale", "kaspa"]

    # Endpoint (URL base) da CoinGecko
    url = "https://api.coingecko.com/api/v3/simple/price"

    # Parâmetros enviados à API
    params = {
        "ids": ",".join(ids),        # Lista de moedas separadas por vírgula
        "vs_currencies": "usd,brl",  # Moedas de comparação (USD e BRL)
    }

    try:
        # Faz a requisição GET com timeout de 10 segundos
        response = requests.get(url, params=params, timeout=10)
        # Gera exceção se a resposta não for 200 (OK)
        response.raise_for_status()
        # Retorna o JSON (dict Python com preços)
        return response.json()

    except requests.RequestException as e:
        # Captura erros de conexão, timeout ou resposta inválida
        print("Erro ao buscar dados:", e)
        # Retorna dicionário vazio (tratado pela interface)
        return {}

