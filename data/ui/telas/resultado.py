"""Tela com os cursos recomendados."""
import customtkinter as ctk

from ui import tema
from ui.componentes.cartao_curso import CartaoCurso


class TelaResultado(ctk.CTkFrame):
    def __init__(self, master, recomendacoes, catalogo, ao_refazer):
        super().__init__(master, fg_color=tema.FUNDO, corner_radius=0)

        topo = ctk.CTkFrame(self, fg_color="transparent")
        topo.pack(fill="x", padx=32, pady=(28, 12))
        ctk.CTkLabel(topo, text="Seus cursos com mais afinidade", font=tema.fonte(28, "bold"),
                     text_color=tema.TEXTO, anchor="w").pack(fill="x")
        ctk.CTkLabel(topo, text="Do mais para o menos alinhado às suas respostas. "
                                "Use como ponto de partida para pesquisar, não como veredito.",
                     font=tema.fonte(14), text_color=tema.TEXTO_SUAVE, anchor="w",
                     justify="left", wraplength=800).pack(fill="x", pady=(6, 0))

        lista = ctk.CTkScrollableFrame(self, fg_color="transparent")
        lista.pack(fill="both", expand=True, padx=20)
        for i, rec in enumerate(recomendacoes):
            CartaoCurso(lista, rec, catalogo.areas[rec.area], destaque=(i == 0)).pack(
                fill="x", padx=12, pady=(0, 14))

        rodape = ctk.CTkFrame(self, fg_color="transparent")
        rodape.pack(fill="x", padx=32, pady=(8, 24))
        ctk.CTkButton(rodape, text="Refazer o questionário", command=ao_refazer, height=40,
                      fg_color="transparent", border_width=2, border_color=tema.AZUL,
                      text_color=(tema.AZUL, "#9DB7EA"), hover_color=tema.CHIP).pack(side="right")
