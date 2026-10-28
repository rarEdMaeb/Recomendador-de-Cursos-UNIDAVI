"""Formatação de texto para exibição. Sem dependência de interface."""

_MODALIDADES = {"presencial": "Presencial", "semipresencial": "Semipresencial", "ead": "EAD+"}
_NOTAS = {1: "Nada", 2: "Pouco", 3: "Médio", 4: "Bastante", 5: "Muito"}


def rotulo_modalidade(modalidade):
    return _MODALIDADES.get(modalidade, modalidade)


def rotulo_nota(nota):
    return _NOTAS[nota]


def formatar_afinidade(valor):
    """0.9412 -> '0,94' (decimal brasileiro)."""
    return f"{valor:.2f}".replace(".", ",")


def juntar_motivos(motivos):
    return " e ".join(motivos)
