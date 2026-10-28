"""Cores e fontes da interface. Pares (claro, escuro) seguem o modo do sistema."""
import customtkinter as ctk

AZUL = "#2B55A3"
AZUL_CLARO = "#4DA6C4"
FUNDO = ("#EEF2FA", "#161B29")
SUPERFICIE = ("#FFFFFF", "#212838")
TEXTO = ("#121B33", "#E8ECF6")
TEXTO_SUAVE = ("#55607A", "#9AA5BF")
BORDA = ("#D5DCEC", "#33405C")
CHIP = ("#E3EAF7", "#2C364D")
ERRO = ("#B3261E", "#FF8A80")

COR_AREA = {
    "saude": "#D94F6A",
    "engenharia": "#D9822B",
    "tecnologia": "#2B55A3",
    "gestao": "#2F8CA8",
    "educacao": "#7B57C2",
    "direito": "#5D6B85",
    "artes": "#C4478A",
    "agro": "#3F9460",
}


def aplicar():
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")


def fonte(tamanho=14, peso="normal"):
    return ctk.CTkFont(size=tamanho, weight=peso)
