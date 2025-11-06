# 💠 MyViewer CryptoApp  

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-1abc9c?logo=python&logoColor=white)
![API](https://img.shields.io/badge/API-CoinGecko-orange?logo=coingecko&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?logo=open-source-initiative&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success?logo=github&logoColor=white)

---

**Visualize preços de criptomoedas em tempo real — rápido, leve e direto ao ponto.**

---

## 🪙 Sobre o projeto  

O **MyViewer CryptoApp** é um aplicação minimalista desenvolvido em **Python** com **CustomTkinter**, que exibe os preços atualizados das principais criptomoedas mais populares no mercado brasileiro.  

A aplicação consome dados diretamente da **CoinGecko API**, garantindo informações **precisas e em tempo real** sobre moedas como **Bitcoin, Ethereum, Solana, Binance Coin**, entre outras.  

---

## 🚀 Principais recursos  

- 💰 Cotação atualizada das criptomoedas mais conhecidas  
- ⚡ Atualização em tempo real via API da [CoinGecko](https://www.coingecko.com/en/api)  
- 🎨 Interface moderna e minimalista feita em **CustomTkinter**  
- 🪶 Aplicativo leve, rápido e independente (pode ser executado como `.exe`)  
- 💻 Compatível com **Windows** e **Python 3.11+**  

---

## 🧩 Tecnologias utilizadas  

| Tecnologia | Função |
|-------------|--------|
| 🐍 **Python** | Linguagem principal |
| 🎨 **CustomTkinter** | Interface gráfica moderna |
| 🌐 **CoinGecko API** | Dados de preços em tempo real |
| 📦 **PyInstaller** | Criação do executável (.exe) |

---

## 📂 Estrutura do projeto  

```
myviewer-cryptoapp/
│
├── assets/              # Arquivos de ícones e imagens
├── dist/                # Executável gerado pela aplicação
├── crypto_api.py        # Código responsável pela integração com a API
├── main.py              # Código principal da interface do app
├── requirements.txt     # Dependências Python do projeto
└── README.md            # Documentação do aplicativo
```

---

## 🧰 Instalação e execução  

Clone o repositório:  
```bash
git clone https://github.com/danilo86Python/myviewer-cryptoapp.git
```

Acesse a pasta do projeto:  
```bash
cd myviewer-cryptoapp
```

Instale as dependências:  
```bash
pip install -r requirements.txt
```

Execute o app:  
```bash
python main.py
```

---

## 🧱 Gerar executável (.exe)

Para criar um executável independente (sem precisar do Python instalado):  

1. Instale o **PyInstaller** (se ainda não tiver):  
   ```bash
   pip install pyinstaller
   ```

2. Gere o `.exe` com o comando:  
   ```bash
   pyinstaller --noconfirm --onefile --windowed --icon="assets/gota.ico" --add-data "assets;assets" --name="Aquaa CryptoView" main.py
   ```

3. O arquivo final será criado na pasta:  
   ```
   dist/Aquaa CryptoView.exe
   ```

4. Basta abrir o `.exe` e acompanhar o mercado cripto em tempo real 💹  

---

## 🪄 Exemplo visual  

*(adicione aqui uma imagem da interface do app)*  
> _Exemplo: tela principal mostrando preços atualizados das criptomoedas._

---

## 🔗 API utilizada  

Os dados são fornecidos gratuitamente pela **[CoinGecko API](https://www.coingecko.com/en/api)**.  
Nenhuma chave de API é necessária.  

---

## 🧑‍💻 Autor  

**Danilo Santos**    

🔗 **Repositório do projeto:** [myviewer-cryptoapp](https://github.com/danilo86Python/myviewer-cryptoapp)  
👤 **Perfil GitHub:** [@danilo86Python](https://github.com/danilo86Python)

---

## ⚖️ Licença  

Distribuído sob a licença **MIT** — sinta-se livre para usar, estudar e modificar.  

---

⭐ **Se este projeto te ajudou, deixe uma estrela no repositório!**  
