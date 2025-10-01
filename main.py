import customtkinter as ctk

# Configurações globais de aparência
ctk.set_appearance_mode("light") # aparência da janela (e sistema) opções: "System", "Dark", "Light"
ctk.set_default_color_theme("blue") # personalizado (poucos ajustes) temas: blue, dark-blue, green, etc.

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações da janela
        self.title("App do Danilo")            # rótulo - barra de título
        self.geometry("700x400")               # tamanho que a janela abre (atual)
        self.configure(fg_color="#FFFFFF")   # cor de fundo 
        # self.minsize(400, 300)               # tamanho mínimo (p/ minimizar)
        # self.maxsize(1000, 700)              # tamanho máximo (p/ maximizar)
        self.resizable(True, True)             # janela ajustável (agora ativado)
        self.iconbitmap()                      # inserir arquivo de ícone (opcional)

        # Transparência (alguns sistemas ignoram - usando em try/except)
        try:
            self.attributes("-alpha", 0.92)
        except Exception:
            pass

        # Conteúdo da janela
        self.create_widgets()

    def create_widgets(self):
        title = ctk.CTkLabel(
                             self, 
                             text="Testando recursos CustomTkinter", font=ctk.CTkFont(size=22, 
                             weight="bold")
        )
        # Coloca o widget na janela (pack ou grid)
        title.pack(pady=20) # ajusta altura do título

if __name__ == "__main__":
    app = App()
    app.mainloop()