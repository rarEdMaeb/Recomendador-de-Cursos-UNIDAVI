"""Estruturas de entrada e saída da lógica. Sem dependência de interface."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Respostas:
    idade: int                      # coletada, mas não pontua
    disciplina_favorita: str        # chave em disciplinas.json
    disciplina_menos_gosta: str
    atividades: dict                # chave em atividades.json -> nota de 1 a 5
    aceita_estudo_longo: bool = True


@dataclass(frozen=True)
class Recomendacao:
    curso: str
    afinidade: float                # similaridade de cosseno, 0 a 1
    motivos: tuple                  # as duas dimensões que mais pesaram
    modalidades: tuple
    area: str
