import os
import sys
import customtkinter as ctk
import tkinter as tk
from datetime import datetime
from crypto_api import get_crypto_data

# ---------- Função para localizar ícones (compatível com PyInstaller) ----------
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Caminhos de ícone (opcional)
ICON_ICO = resource_path(os.path.join("assets", "gota.ico"))
ICON_PNG = resource_path(os.path.join("assets", "gota.png"))

# ---------- Configuração global ----------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ---------- Mapa de nomes para exibição ----------
ID_TO_TICKER = {
    "ripple": "XRP",
    "stellar": "XLM",
    "hedera-hashgraph": "HBAR",
    "ondo-finance": "ONDO",
    "xdce-crowd-sale": "XDC",
    "kaspa": "KASPA",
}
ORDER = ["ripple", "stellar", "hedera-hashgraph", "ondo-finance", "xdce-crowd-sale", "kaspa"]


# =====================================================
# Classe principal da interface
# =====================================================
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ---------- Configuração da janela ----------
        self.title("Aquaa CryptoView (v1)")
        self.geometry("500x400")
        self.configure(fg_color="#FFFFFF")
        self.resizable(False, False) # trava janela (proibido redimensionar)
        self.attributes("-alpha", 0.92)

        # ---------- Ícone da janela ----------
        if os.path.exists(ICON_ICO):
            try:
                self.iconbitmap(ICON_ICO)
            except Exception:
                self._try_iconphoto(ICON_PNG)
        else:
            self._try_iconphoto(ICON_PNG)

        self._icon_photoimage = None

        # ---------- Inicialização da interface ----------
        self.table_rows = []
        self.create_widgets()
        self.update_prices()

    # ---------- Tentativa alternativa para ícone .png ----------
    def _try_iconphoto(self, png_path):
        if png_path and os.path.exists(png_path):
            try:
                img = tk.PhotoImage(file=png_path)
                self._icon_photoimage = img
                self.iconphoto(False, img)
            except Exception:
                pass

    # -------------------------------------------------
    # Monta os elementos fixos da interface
    # -------------------------------------------------
    def create_widgets(self):
        # Título principal
        self.title_label = ctk.CTkLabel(self, text="Cotações ao Vivo (USD / BRL)", 
                                        font=ctk.CTkFont(family="Consolas", size=20, weight="bold"))
        self.title_label.pack(pady=14)

        # Frame da tabela
        self.table_frame = ctk.CTkFrame(self, fg_color="#D8F7FF")
        self.table_frame.pack(fill="x", padx=20, pady=(0, 6))

        header_font = ctk.CTkFont(family="Consolas", size=13, weight="bold")
        data_font = ctk.CTkFont(family="Consolas", size=13)

        # Cabeçalhos
        self.h_name = ctk.CTkLabel(self.table_frame, text="Criptomoeda", font=header_font, anchor="w")
        self.h_usd = ctk.CTkLabel(self.table_frame, text="USD", font=header_font, anchor="e")
        self.h_brl = ctk.CTkLabel(self.table_frame, text="BRL", font=header_font, anchor="e")

        self.h_name.grid(row=0, column=0, sticky="w", padx=(8,5), pady=6)
        self.h_usd.grid(row=0, column=1, sticky="e", padx=(5,8))
        self.h_brl.grid(row=0, column=2, sticky="e", padx=(5,8))

        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(1, minsize=140)
        self.table_frame.grid_columnconfigure(2, minsize=140)

        # Hora da última atualização
        self.last_update_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=11))
        self.last_update_label.pack(pady=(8, 6))

        # Botão de atualização
        self.btn = ctk.CTkButton(self, text="Atualizar Agora", command=self.update_prices)
        self.btn.pack(pady=(0, 11))

        # -------------------------------------------------
        # Link "Sobre" ajustado acima, rente à direita
        # -------------------------------------------------
        self.link_sobre = ctk.CTkLabel(self, text="Sobre", text_color="#999292", cursor="hand2", 
                                       font=ctk.CTkFont(size=13))

        # Posição responsiva: canto superior direito da área inferior
        self.link_sobre.place(relx=1.0, rely=0.90, anchor="ne", x=-22)

        # Efeitos de hover
        self.link_sobre.bind("<Enter>", lambda e: self.link_sobre.configure(text_color="#666666"))
        self.link_sobre.bind("<Leave>", lambda e: self.link_sobre.configure(text_color="#999292"))

        # Ação de clique
        self.link_sobre.bind("<Button-1>", lambda e: self.abrir_janela_sobre())

    # -------------------------------------------------
    # Função de atualização da tabela
    # -------------------------------------------------
    def update_prices(self):
        for w in self.table_rows:
            try:
                w.destroy()
            except Exception:
                pass
        self.table_rows.clear()

        data = get_crypto_data()
        if not data:
            self.last_update_label.configure(text="Erro ao obter dados. Tente novamente.")
            self.after(30000, self.update_prices)
            return

        row = 1
        data_font = ctk.CTkFont(family="Consolas", size=13)
        for coin_id in ORDER:
            values = data.get(coin_id, {})
            usd = values.get("usd", 0.0)
            brl = values.get("brl", 0.0)

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

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_update_label.configure(text=f"Última atualização: {now}")

        self.after(30000, self.update_prices)

        # Remove apenas o botão de maximizar (Windows)
        if sys.platform.startswith("win"):
            import ctypes
            GWL_STYLE = -16
            WS_MAXIMIZEBOX = 0x00010000
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
            style &= ~WS_MAXIMIZEBOX  # Remove só o maximizar
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)
            ctypes.windll.user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0,
                                      0x0002 | 0x0001 | 0x0040 | 0x0020)


    # -------------------------------------------------
    # Janela popup "Sobre"
    # -------------------------------------------------
    def abrir_janela_sobre(self):
        janela_sobre = tk.Toplevel(self)
        janela_sobre.title("Sobre o Aquaa CryptoView")
        janela_sobre.config(bg="white")
        janela_sobre.attributes("-alpha", 0.93)
        janela_sobre.attributes("-topmost", True)

        popup_width, popup_height = 350, 180

        # Centraliza na tela
        screen_width = janela_sobre.winfo_screenwidth()
        screen_height = janela_sobre.winfo_screenheight()
        x = (screen_width // 2) - (popup_width // 2)
        y = (screen_height // 2) - (popup_height // 2)

        janela_sobre.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        janela_sobre.resizable(False, False)

        # Ícone
        if os.path.exists(ICON_ICO):
            try:
                janela_sobre.iconbitmap(ICON_ICO)
            except Exception:
                if os.path.exists(ICON_PNG):
                    janela_sobre._icon_img = tk.PhotoImage(file=ICON_PNG)
                    janela_sobre.iconphoto(False, janela_sobre._icon_img)

        # Remove minimizar/maximizar (Windows)
        if sys.platform.startswith("win"):
            import ctypes
            GWL_STYLE = -16
            WS_MINIMIZEBOX = 0x00020000
            WS_MAXIMIZEBOX = 0x00010000
            hwnd = ctypes.windll.user32.GetParent(janela_sobre.winfo_id())
            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
            style &= ~WS_MINIMIZEBOX
            style &= ~WS_MAXIMIZEBOX
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)
            ctypes.windll.user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0,
                                              0x0002 | 0x0001 | 0x0040 | 0x0020)

        # Conteúdo da janela
        info = (
            "Aquaa CryptoView (v1)\n\n"
            "Desenvolvido por: Danilo dos Santos Soares\n"
            "Telefone: (11) 9 4138-3504\n"
            "Interface: CustomTkinter\n"
            "Agente: Gemini (Google AI)\n\n"
            "© 2025 - Todos os direitos reservados."
        )

        label_info = ctk.CTkLabel(
            master=janela_sobre,
            text=info,
            justify="left",
            text_color="#333333",
            font=ctk.CTkFont(size=14)
        )
        label_info.pack(padx=20, pady=20)


# -------------------------------------------------
# Execução principal
# -------------------------------------------------
if __name__ == "__main__":
    app = App()
    app.mainloop()
