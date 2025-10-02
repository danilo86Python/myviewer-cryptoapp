# main.py
import customtkinter as ctk
from crypto_api import get_crypto_data
from datetime import datetime

# Aparência global
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Mapeamento para exibir o ticker (XRP, XLM, HBAR, ...)
ID_TO_TICKER = {
    "ripple": "XRP",
    "stellar": "XLM",
    "hedera-hashgraph": "HBAR",
    "ondo-finance": "ONDO",
    "xdce-crowd-sale": "XDC",
    "kaspa": "KASPA",
}
ORDER = ["ripple", "stellar", "hedera-hashgraph", "ondo-finance", "xdce-crowd-sale", "kaspa"]

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Cotações de Criptomoedas")
        self.geometry("500x400")
        self.configure(fg_color="#FFFFFF")
        self.resizable(True, True)

        try:
            self.attributes("-alpha", 0.92)
        except Exception:
            pass

        self.table_rows = []  # referencia para destruir/atualizar widgets
        self.create_widgets()
        self.update_prices()

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(
            self,
            text="Cotações ao Vivo (USD / BRL)",
            font=ctk.CTkFont(family="Consolas", size=20, weight="bold")
        )
        self.title_label.pack(pady=14)

        # Frame que conterá a "tabela"
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(fill="x", padx=20, pady=(0, 6))

        # Cabeçalho
        header_font = ctk.CTkFont(family="Consolas", size=13, weight="bold")
        data_font = ctk.CTkFont(family="Consolas", size=13)

        self.h_name = ctk.CTkLabel(self.table_frame, text="Criptomoeda", font=header_font, anchor="w")
        self.h_usd = ctk.CTkLabel(self.table_frame, text="USD", font=header_font, anchor="e")
        self.h_brl = ctk.CTkLabel(self.table_frame, text="BRL", font=header_font, anchor="e")

        self.h_name.grid(row=0, column=0, sticky="w", padx=(8,5), pady=6)
        self.h_usd.grid(row=0, column=1, sticky="e", padx=(5,8))
        self.h_brl.grid(row=0, column=2, sticky="e", padx=(5,8))

        # Configurar colunas: a primeira expande; as outras têm largura mínima fixa
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(1, minsize=140)
        self.table_frame.grid_columnconfigure(2, minsize=140)

        # Label para mostrar hora da última atualização
        self.last_update_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=11))
        self.last_update_label.pack(pady=(2, 6))

        # Botão de atualização manual
        self.btn = ctk.CTkButton(self, text="Atualizar Agora", command=self.update_prices)
        self.btn.pack(pady=(0, 12))

    def update_prices(self):
        # limpa linhas antigas
        for w in self.table_rows:
            try:
                w.destroy()
            except Exception:
                pass
        self.table_rows.clear()

        data = get_crypto_data()
        if not data:
            self.last_update_label.configure(text="Erro ao obter dados. Tente novamente.")
            # tenta novamente depois (30s)
            self.after(30000, self.update_prices)
            return

        row = 1
        data_font = ctk.CTkFont(family="Consolas", size=13)
        for coin_id in ORDER:
            values = data.get(coin_id, {})
            usd = values.get("usd", 0.0)
            brl = values.get("brl", 0.0)

            # Formatação com símbolo colado ao número (ex: $0.51 / R$2.96)
            usd_text = f"$ {usd:,.2f}"
            brl_text = f"R$ {brl:,.2f}"

            name_text = ID_TO_TICKER.get(coin_id, coin_id.capitalize())

            lbl_name = ctk.CTkLabel(self.table_frame, text=name_text, font=data_font, anchor="w")
            lbl_usd = ctk.CTkLabel(self.table_frame, text=usd_text, font=data_font, anchor="e")
            lbl_brl = ctk.CTkLabel(self.table_frame, text=brl_text, font=data_font, anchor="e")

            lbl_name.grid(row=row, column=0, sticky="w", padx=(8,5), pady=2)
            lbl_usd.grid(row=row, column=1, sticky="e", padx=(5,8))
            lbl_brl.grid(row=row, column=2, sticky="e", padx=(5,8))

            self.table_rows.extend([lbl_name, lbl_usd, lbl_brl])
            row += 1

        # Atualiza label de última atualização
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_update_label.configure(text=f"Última atualização: {now}")

        # atualiza novamente em 30s
        self.after(30000, self.update_prices)

if __name__ == "__main__":
    app = App()
    app.mainloop()
