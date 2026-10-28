"""Ranking determinístico: mesma entrada, mesma saída. Sem ML, sem aleatoriedade.

Afinidade = similaridade de cosseno entre o perfil do aluno e o perfil ideal do curso.
Empates são resolvidos por ordem alfabética do nome do curso.
"""
from math import sqrt

from core.modelos import Recomendacao
from core.perfil import construir_perfil, validar
from data.carregador import carregar_catalogo


def _norma(v, dims):
    return sqrt(sum(v.get(d, 0.0) ** 2 for d in dims))


def recomendar(resp, catalogo=None, top=3, apenas_ofertados=True):
    catalogo = catalogo or carregar_catalogo()
    validar(resp, catalogo)
    dims = catalogo.dims
    p = construir_perfil(resp, catalogo)
    np_ = _norma(p, dims)
    if np_ == 0:
        raise ValueError("Suas respostas não deixaram nenhuma preferência marcada. "
                         "Dê notas acima de 1 para o que você gosta de fazer.")
    resultado = []
    for nome, curso in catalogo.cursos.items():
        if apenas_ofertados and not curso["modalidades"]:
            continue
        c = curso["perfil"]
        nc = _norma(c, dims)
        contrib = {d: (p[d] / np_) * (c.get(d, 0.0) / nc) for d in dims}
        score = sum(contrib.values())
        if nome in catalogo.cursos_estudo_longo and not resp.aceita_estudo_longo:
            score *= catalogo.penalidade_estudo_longo
        motivos = tuple(catalogo.dimensoes[d]
                        for d, _ in sorted(contrib.items(), key=lambda x: -x[1])[:2])
        resultado.append((round(score, 4), nome, motivos))
    resultado.sort(key=lambda r: (-r[0], r[1]))
    return [Recomendacao(curso=n, afinidade=s, motivos=m,
                         modalidades=tuple(catalogo.cursos[n]["modalidades"]),
                         area=catalogo.cursos[n]["area"])
            for s, n, m in resultado[:top]]
