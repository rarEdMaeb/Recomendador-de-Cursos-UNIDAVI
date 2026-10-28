"""Validação das respostas e construção do vetor de perfil do aluno."""


def validar(resp, catalogo):
    if not isinstance(resp.idade, int) or not 10 <= resp.idade <= 100:
        raise ValueError("Informe uma idade entre 10 e 100 anos.")
    if resp.disciplina_favorita not in catalogo.disciplinas:
        raise ValueError("Escolha a disciplina que você mais gosta.")
    if resp.disciplina_menos_gosta not in catalogo.disciplinas:
        raise ValueError("Escolha a disciplina que você menos gosta.")
    if resp.disciplina_favorita == resp.disciplina_menos_gosta:
        raise ValueError("A disciplina favorita e a que menos gosta precisam ser diferentes.")
    for chave, a in catalogo.atividades.items():
        if resp.atividades.get(chave) not in (1, 2, 3, 4, 5):
            raise ValueError(f"Dê uma nota de 1 a 5 para: {a['pergunta']}")


def construir_perfil(resp, catalogo):
    """Vetor do aluno nas dimensões do catálogo. A idade não pontua."""
    v = {d: 0.0 for d in catalogo.dims}
    for d, pts in catalogo.disciplinas[resp.disciplina_favorita]["pesos"].items():
        v[d] += catalogo.fator_favorita * pts
    for d, pts in catalogo.disciplinas[resp.disciplina_menos_gosta]["pesos"].items():
        v[d] -= catalogo.fator_menos_gosta * pts
    for chave, a in catalogo.atividades.items():
        nota = resp.atividades[chave]
        for d, w in a["pesos"].items():
            v[d] += (nota - 1) * w
    return {d: max(x, 0.0) for d, x in v.items()}
