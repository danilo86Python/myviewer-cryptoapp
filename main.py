import customtkinter as ctk       # importa a biblioteca CustomTkinter (interface moderna baseada no Tkinter)
from crypto_api import get_crypto_data   # importa a função que faz a requisição à API CoinGecko
from datetime import datetime      # usada para exibir a hora da última atualização

# ---------- CONFIGURAÇÃO GLOBAL DE APARÊNCIA ----------
ctk.set_appearance_mode("light")    # define o tema claro (pode ser 'dark', 'light' ou 'system')
ctk.set_default_color_theme("blue") # define o esquema de cores padrão (blue, dark-blue, etc.)

# ---------- MAPA DE NOMES PARA EXIBIÇÃO ----------
ID_TO_TICKER = {
    "ripple": "XRP",
    "stellar": "XLM",
    "hedera-hashgraph": "HBAR",
    "ondo-finance": "ONDO",
    "xdce-crowd-sale": "XDC",
    "kaspa": "KASPA",
}
# Ordem em que as moedas aparecerão na interface
ORDER = ["ripple", "stellar", "hedera-hashgraph", "ondo-finance", "xdce-crowd-sale", "kaspa"]

# =====================================================
# CLASSE PRINCIPAL DA INTERFACE (HERDA DE ctk.CTk)
# =====================================================
class App(ctk.CTk):
    def __init__(self):
        super().__init__()  # inicializa a janela principal do CustomTkinter

        # ---------- CONFIGURAÇÕES DA JANELA ----------
        self.title("As melhores criptos para investir")   # título da janela
        self.geometry("500x400")                 # tamanho inicial
        self.configure(fg_color="#FFFFFF")     # cor de fundo branca
        self.resizable(True, True)               # permite redimensionar a janela

        # Define transparência da janela (caso o sistema suporte)
        try:
            self.attributes("-alpha", 0.92)
        except Exception:
            pass  # evita erro se o SO não suportar essa flag

        # Lista usada para guardar widgets que exibem as linhas da tabela
        # (permite apagar e recriar os dados a cada atualização)
        self.table_rows = []

        # Cria todos os widgets da interface
        self.create_widgets()

        # Faz a primeira atualização de preços (chamada inicial da API)
        self.update_prices()

    # -------------------------------------------------
    # MONTA TODOS OS ELEMENTOS FIXOS DA INTERFACE
    # -------------------------------------------------
    def create_widgets(self):
        # Título principal
        self.title_label = ctk.CTkLabel(
            self,
            text="Cotações ao Vivo (USD / BRL)",
            font=ctk.CTkFont(family="Consolas", size=20, weight="bold")
        )
        self.title_label.pack(pady=14) # cria 14 pixels de espaço acima e 14 abaixo da label

        # Frame que conterá a "tabela" com os dados
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(fill="x", padx=20, pady=(0, 6))

        # Fontes para cabeçalho e dados
        header_font = ctk.CTkFont(family="Consolas", size=13, weight="bold")
        data_font = ctk.CTkFont(family="Consolas", size=13)

        # Cabeçalhos das colunas
        self.h_name = ctk.CTkLabel(self.table_frame, text="Criptomoeda", font=header_font, anchor="w")
        self.h_usd = ctk.CTkLabel(self.table_frame, text="USD", font=header_font, anchor="e")
        self.h_brl = ctk.CTkLabel(self.table_frame, text="BRL", font=header_font, anchor="e")

        # Posicionamento dos cabeçalhos na grade (linha 0)
        self.h_name.grid(row=0, column=0, sticky="w", padx=(8,5), pady=6)
        self.h_usd.grid(row=0, column=1, sticky="e", padx=(5,8))
        self.h_brl.grid(row=0, column=2, sticky="e", padx=(5,8))

        # Configura comportamento das colunas do grid:
        # a 1ª se expande, as demais têm largura fixa
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(1, minsize=140)
        self.table_frame.grid_columnconfigure(2, minsize=140)

        # Exibe hora da última atualização
        self.last_update_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=11))
        self.last_update_label.pack(pady=(2, 6))

        # Botão manual para atualizar dados (chama update_prices)
        self.btn = ctk.CTkButton(self, text="Atualizar Agora", command=self.update_prices)
        self.btn.pack(pady=(0, 12))

    # -------------------------------------------------
    # FUNÇÃO PRINCIPAL DE ATUALIZAÇÃO DE PREÇOS
    # (Chama a API e atualiza a tabela)
    # -------------------------------------------------
    def update_prices(self):
        # Limpa todas as linhas antigas
        for w in self.table_rows:
            try:
                w.destroy()
            except Exception:
                pass
        self.table_rows.clear()

        # Faz a chamada à API (função externa em crypto_api.py)
        data = get_crypto_data()

        # Se a resposta for vazia ou houver erro na API
        if not data:
            self.last_update_label.configure(text="Erro ao obter dados. Tente novamente.")
            # Reagenda nova tentativa após 30 segundos
            self.after(30000, self.update_prices)
            return

        # Preenche a "tabela" com os dados recebidos
        row = 1
        data_font = ctk.CTkFont(family="Consolas", size=13)
        for coin_id in ORDER:  # Mantém a ordem definida no topo
            values = data.get(coin_id, {})
            usd = values.get("usd", 0.0)
            brl = values.get("brl", 0.0)

            # Formata valores monetários (ex: $ 0.51 / R$ 2.96)
            usd_text = f"$ {usd:,.2f}"
            brl_text = f"R$ {brl:,.2f}"

            # Converte ID da API (ex: ripple) para ticker exibido (ex: XRP)
            name_text = ID_TO_TICKER.get(coin_id, coin_id.capitalize())

            # Cria as labels de cada linha
            lbl_name = ctk.CTkLabel(self.table_frame, text=name_text, font=data_font, anchor="w")
            lbl_usd = ctk.CTkLabel(self.table_frame, text=usd_text, font=data_font, anchor="e")
            lbl_brl = ctk.CTkLabel(self.table_frame, text=brl_text, font=data_font, anchor="e")

            # Posiciona na tabela
            lbl_name.grid(row=row, column=0, sticky="w", padx=(8,5), pady=2)
            lbl_usd.grid(row=row, column=1, sticky="e", padx=(5,8))
            lbl_brl.grid(row=row, column=2, sticky="e", padx=(5,8))

            # Guarda as referências (para destruir depois)
            self.table_rows.extend([lbl_name, lbl_usd, lbl_brl])
            row += 1

        # Atualiza o horário da última atualização
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_update_label.configure(text=f"Última atualização: {now}")

        # Programa uma nova atualização automática a cada 30 segundos
        self.after(30000, self.update_prices)

# -------------------------------------------------
# PONTO DE ENTRADA DA APLICAÇÃO
# -------------------------------------------------
if __name__ == "__main__":
    app = App()         # Cria a instância da interface
    app.mainloop()      # Inicia o loop principal do Tkinter
