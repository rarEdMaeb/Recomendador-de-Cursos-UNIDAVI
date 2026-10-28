"""Tela do questionário. Só coleta as respostas; a pontuação fica em core."""
import customtkinter as ctk

from core.modelos import Respostas
from ui import tema
from utils.texto import rotulo_nota

SELECIONE = "Selecione…"


class TelaQuestionario(ctk.CTkFrame):
    def __init__(self, master, catalogo, ao_enviar):
        super().__init__(master, fg_color=tema.FUNDO, corner_radius=0)
        self.catalogo = catalogo
        self.ao_enviar = ao_enviar
        self._chave_por_rotulo = {d["rotulo"]: k for k, d in catalogo.disciplinas.items()}
        self._sliders = {}

        topo = ctk.CTkFrame(self, fg_color="transparent")
        topo.pack(fill="x", padx=32, pady=(28, 8))
        ctk.CTkLabel(topo, text="Qual graduação combina com você?", font=tema.fonte(28, "bold"),
                     text_color=tema.TEXTO, anchor="w").pack(fill="x")
        ctk.CTkLabel(topo, text="Responda com sinceridade: não há resposta certa. "
                                "Leva cerca de dois minutos.",
                     font=tema.fonte(14), text_color=tema.TEXTO_SUAVE, anchor="w").pack(
            fill="x", pady=(6, 0))

        corpo = ctk.CTkScrollableFrame(self, fg_color="transparent")
        corpo.pack(fill="both", expand=True, padx=20, pady=(8, 0))
        self._secao_sobre_voce(corpo)
        self._secao_atividades(corpo)
        self._secao_formacao(corpo)

        rodape = ctk.CTkFrame(self, fg_color=tema.SUPERFICIE, corner_radius=0)
        rodape.pack(fill="x")
        self.erro = ctk.CTkLabel(rodape, text="", font=tema.fonte(14), text_color=tema.ERRO,
                                 anchor="w", justify="left", wraplength=620)
        self.erro.pack(side="left", padx=32, pady=16, fill="x", expand=True)
        ctk.CTkButton(rodape, text="Ver recomendações", command=self._enviar, height=42,
                      font=tema.fonte(15, "bold"), fg_color=tema.AZUL).pack(
            side="right", padx=32, pady=16)

    # --- construção -----------------------------------------------------------------------
    def _secao(self, master, titulo):
        quadro = ctk.CTkFrame(master, fg_color=tema.SUPERFICIE, corner_radius=16,
                              border_width=1, border_color=tema.BORDA)
        quadro.pack(fill="x", padx=12, pady=(0, 14))
        quadro.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(quadro, text=titulo, font=tema.fonte(18, "bold"), text_color=tema.TEXTO,
                     anchor="w").grid(row=0, column=0, columnspan=3, sticky="w", padx=22, pady=(18, 8))
        return quadro

    def _campo(self, quadro, linha, rotulo, widget):
        ctk.CTkLabel(quadro, text=rotulo, font=tema.fonte(14), text_color=tema.TEXTO, anchor="w",
                     justify="left", wraplength=360).grid(row=linha, column=0, sticky="w",
                                                         padx=22, pady=8)
        widget.grid(row=linha, column=1, columnspan=2, sticky="e", padx=22, pady=8)

    def _secao_sobre_voce(self, master):
        q = self._secao(master, "Sobre você")
        self.idade = ctk.CTkEntry(q, width=120, placeholder_text="ex.: 17")
        self._campo(q, 1, "Sua idade", self.idade)
        rotulos = sorted(self._chave_por_rotulo)
        self.fav = ctk.CTkOptionMenu(q, values=[SELECIONE, *rotulos], width=260, fg_color=tema.AZUL)
        self.fav.set(SELECIONE)
        self._campo(q, 2, "Disciplina da escola que você mais gosta", self.fav)
        self.pior = ctk.CTkOptionMenu(q, values=[SELECIONE, *rotulos], width=260, fg_color=tema.AZUL)
        self.pior.set(SELECIONE)
        self._campo(q, 3, "Disciplina da escola que você menos gosta", self.pior)
        ctk.CTkFrame(q, height=10, fg_color="transparent").grid(row=4, column=0)

    def _secao_atividades(self, master):
        q = self._secao(master, "O que você gosta de fazer")
        for i, (chave, a) in enumerate(self.catalogo.atividades.items(), start=1):
            ctk.CTkLabel(q, text=a["pergunta"], font=tema.fonte(14), text_color=tema.TEXTO,
                         anchor="w", justify="left", wraplength=360).grid(
                row=i, column=0, sticky="w", padx=22, pady=8)
            valor = ctk.CTkLabel(q, text=rotulo_nota(3), width=72, font=tema.fonte(13, "bold"),
                                 text_color=tema.TEXTO_SUAVE, anchor="e")
            slider = ctk.CTkSlider(
                q, from_=1, to=5, number_of_steps=4, width=220, progress_color=tema.AZUL,
                button_color=tema.AZUL, button_hover_color=tema.AZUL_CLARO,
                command=lambda v, rotulo=valor: rotulo.configure(text=rotulo_nota(int(round(v)))))
            slider.set(3)
            slider.grid(row=i, column=1, sticky="e", padx=(8, 4), pady=8)
            valor.grid(row=i, column=2, sticky="e", padx=(4, 22), pady=8)
            self._sliders[chave] = slider
        ctk.CTkFrame(q, height=10, fg_color="transparent").grid(row=len(self._sliders) + 1, column=0)

    def _secao_formacao(self, master):
        q = self._secao(master, "Formação")
        self.estudo_longo = ctk.CTkSwitch(q, text="", progress_color=tema.AZUL)
        self.estudo_longo.select()
        self._campo(q, 1, "Topo uma formação longa (mais de 6 anos, como Medicina)", self.estudo_longo)
        ctk.CTkFrame(q, height=10, fg_color="transparent").grid(row=2, column=0)

    # --- envio ----------------------------------------------------------------------------
    def _enviar(self):
        self.erro.configure(text="")
        texto_idade = self.idade.get().strip()
        if not texto_idade.isdigit():
            self.erro.configure(text="Informe sua idade usando só números.")
            return
        respostas = Respostas(
            idade=int(texto_idade),
            disciplina_favorita=self._chave_por_rotulo.get(self.fav.get(), ""),
            disciplina_menos_gosta=self._chave_por_rotulo.get(self.pior.get(), ""),
            atividades={k: int(round(s.get())) for k, s in self._sliders.items()},
            aceita_estudo_longo=bool(self.estudo_longo.get()),
        )
        try:
            self.ao_enviar(respostas)
        except ValueError as e:
            self.erro.configure(text=str(e))
