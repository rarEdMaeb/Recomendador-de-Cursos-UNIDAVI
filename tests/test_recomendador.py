"""Rodar da raiz do projeto: python -m unittest tests.test_recomendador -v"""
import json
import unittest
from pathlib import Path

from core.modelos import Respostas
from core.recomendador import recomendar
from data.carregador import carregar_catalogo

GOLDEN = json.loads((Path(__file__).parent / "golden.json").read_text(encoding="utf-8"))


def _respostas(caso):
    r = caso["resposta"]
    return Respostas(
        idade=r["idade"], disciplina_favorita=r["disciplina_favorita"],
        disciplina_menos_gosta=r["disciplina_menos_gosta"], atividades=r["atividades"],
        aceita_estudo_longo=caso["opcoes"].get("aceita_estudo_longo", True))


class Regressao(unittest.TestCase):
    """A saída precisa ser idêntica à do script original (recomendador_curso.py)."""

    def test_golden(self):
        for caso in GOLDEN:
            with self.subTest(caso["nome"]):
                op = caso["opcoes"]
                obtido = recomendar(_respostas(caso), top=op.get("top", 3),
                                    apenas_ofertados=op.get("apenas_ofertados", True))
                self.assertEqual([r.curso for r in obtido], [e["curso"] for e in caso["esperado"]])
                for r, e in zip(obtido, caso["esperado"]):
                    self.assertAlmostEqual(r.afinidade, e["afinidade"], places=9)
                    self.assertEqual(list(r.motivos), e["motivos"])
                    self.assertEqual(list(r.modalidades), e["modalidades"])


class Propriedades(unittest.TestCase):
    def test_deterministico(self):
        resp = _respostas(GOLDEN[0])
        self.assertEqual(recomendar(resp, top=10), recomendar(resp, top=10))

    def test_catalogo(self):
        cat = carregar_catalogo()
        ofertados = [n for n, c in cat.cursos.items() if c["modalidades"]]
        self.assertEqual(len(ofertados), 34)
        self.assertEqual(len(set(ofertados)), len(ofertados))

    def test_validacoes(self):
        base = GOLDEN[0]["resposta"]
        ruins = [dict(base, idade=5), dict(base, disciplina_favorita="xyz"),
                 dict(base, disciplina_menos_gosta=base["disciplina_favorita"]),
                 dict(base, atividades={**base["atividades"], "criar": 9})]
        for r in ruins:
            with self.subTest(r), self.assertRaises(ValueError):
                recomendar(Respostas(**r))


if __name__ == "__main__":
    unittest.main()
