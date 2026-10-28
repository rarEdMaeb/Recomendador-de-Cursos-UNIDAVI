"""Ícones das áreas: círculo colorido com o PNG branco da área por cima."""
from functools import lru_cache
from pathlib import Path

import customtkinter as ctk
from PIL import Image, ImageDraw

PASTA = Path(__file__).resolve().parent.parent / "assets" / "icones"
SUPERAMOSTRAGEM = 4  # desenha em escala maior para suavizar a borda do círculo


@lru_cache(maxsize=None)
def icone_area(area, tamanho, cor_fundo):
    """CTkImage do ícone da área. Sem o PNG, mostra só o círculo colorido."""
    s = tamanho * SUPERAMOSTRAGEM
    base = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    ImageDraw.Draw(base).ellipse((0, 0, s - 1, s - 1), fill=cor_fundo)
    arquivo = PASTA / f"{area}.png"
    if arquivo.exists():
        glifo = Image.open(arquivo).convert("RGBA")
        lado = int(s * 0.56)
        glifo = glifo.resize((lado, lado), Image.LANCZOS)
        deslocamento = (s - lado) // 2
        base.alpha_composite(glifo, (deslocamento, deslocamento))
    base = base.resize((tamanho * 2, tamanho * 2), Image.LANCZOS)  # 2x para telas HiDPI
    return ctk.CTkImage(light_image=base, dark_image=base, size=(tamanho, tamanho))
