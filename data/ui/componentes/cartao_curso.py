"""Cartão de um curso recomendado. O primeiro colocado aparece maior e com borda colorida."""
import customtkinter as ctk

from ui import tema
from utils.icones import icone_area
from utils.texto import formatar_afinidade, juntar_motivos, rotulo_modalidade


class CartaoCurso(ctk.CTkFrame):
    def __init__(self, master, rec, rotulo_area, destaque=False):
        cor = tema.COR_AREA[rec.area]
        super().__init__(master, fg_color=tema.SUPERFICIE, corner_radius=16,
                         border_width=2 if destaque else 1,
                         border_color=cor if destaque else tema.BORDA)
        self.grid_columnconfigure(1, weight=1)

        lado = 96 if destaque else 64
        ctk.CTkLabel(self, text="", image=icone_area(rec.area, lado, cor)).grid(
            row=0, column=0, rowspan=4, padx=(22, 8), pady=22, sticky="n")

        ctk.CTkLabel(self, text=rec.curso, font=tema.fonte(26 if destaque else 18, "bold"),
                     text_color=tema.TEXTO, anchor="w", justify="left", wraplength=560).grid(
            row=0, column=1, sticky="w", padx=(12, 22), pady=(20, 0))

        chips = ctk.CTkFrame(self, fg_color="transparent")
        chips.grid(row=1, column=1, sticky="w", padx=(12, 22), pady=(6, 0))
        for texto in (rotulo_area, *[rotulo_modalidade(m) for m in rec.modalidades]):
            ctk.CTkLabel(chips, text=texto, font=tema.fonte(12), text_color=tema.TEXTO,
                         fg_color=tema.CHIP, corner_radius=10, padx=10, pady=2).pack(
                side="left", padx=(0, 6))

        barra = ctk.CTkFrame(self, fg_color="transparent")
        barra.grid(row=2, column=1, sticky="ew", padx=(12, 22), pady=(14, 0))
        progresso = ctk.CTkProgressBar(barra, height=8, progress_color=cor)
        progresso.set(max(0.0, min(1.0, rec.afinidade)))
        progresso.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(barra, text=f"Afinidade {formatar_afinidade(rec.afinidade)}",
                     font=tema.fonte(13, "bold"), text_color=tema.TEXTO).pack(side="left", padx=(12, 0))

        ctk.CTkLabel(self, text=f"Pesaram mais: {juntar_motivos(rec.motivos)}.",
                     font=tema.fonte(13), text_color=tema.TEXTO_SUAVE, anchor="w",
                     justify="left", wraplength=560).grid(
            row=3, column=1, sticky="w", padx=(12, 22), pady=(8, 20))
