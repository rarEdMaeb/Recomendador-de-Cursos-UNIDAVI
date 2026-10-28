"""Janela principal e navegação entre telas. Não contém regra de recomendação."""
import customtkinter as ctk

from core.recomendador import recomendar
from data.carregador import carregar_catalogo
from ui import tema
from ui.telas.questionario import TelaQuestionario
from ui.telas.resultado import TelaResultado

TOP_N = 3


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        tema.aplicar()
        self.title("Recomendador de Graduação")
        self.geometry("1000x760")
        self.minsize(860, 620)
        self.configure(fg_color=tema.FUNDO)
        self.catalogo = carregar_catalogo()
        self._tela = None
        self.mostrar_questionario()

    def _trocar(self, tela):
        if self._tela is not None:
            self._tela.destroy()
        self._tela = tela
        tela.pack(fill="both", expand=True)

    def mostrar_questionario(self):
        self._trocar(TelaQuestionario(self, self.catalogo, ao_enviar=self._enviar))

    def _enviar(self, respostas):
        # ValueError sobe até a tela do questionário, que exibe a mensagem.
        recomendacoes = recomendar(respostas, self.catalogo, top=TOP_N)
        self._trocar(TelaResultado(self, recomendacoes, self.catalogo,
                                   ao_refazer=self.mostrar_questionario))
