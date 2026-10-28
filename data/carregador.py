"""Leitura e validação dos arquivos JSON de dados. Camada mais baixa: não importa core nem ui."""
import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

PASTA = Path(__file__).resolve().parent
MODALIDADES_VALIDAS = {"presencial", "semipresencial", "ead"}


@dataclass(frozen=True)
class Catalogo:
    dimensoes: dict                 # sigla -> descrição (ordem define o vetor)
    areas: dict                     # id da área -> rótulo
    disciplinas: dict               # chave -> {"rotulo", "pesos"}
    atividades: dict                # chave -> {"pergunta", "pesos"}
    cursos: dict                    # nome -> {"area", "modalidades", "perfil"}
    fator_favorita: float
    fator_menos_gosta: float
    penalidade_estudo_longo: float
    cursos_estudo_longo: frozenset

    @property
    def dims(self):
        return list(self.dimensoes)


def _ler(nome):
    return json.loads((PASTA / nome).read_text(encoding="utf-8"))


def _validar_pesos(origem, pesos, dims):
    desconhecidas = set(pesos) - set(dims)
    if desconhecidas:
        raise ValueError(f"{origem}: dimensões desconhecidas {sorted(desconhecidas)}")


@lru_cache(maxsize=1)
def carregar_catalogo():
    par = _ler("parametros.json")
    cat = Catalogo(
        dimensoes=par["dimensoes"],
        areas=par["areas"],
        disciplinas=_ler("disciplinas.json"),
        atividades=_ler("atividades.json"),
        cursos=_ler("cursos.json"),
        fator_favorita=par["fator_favorita"],
        fator_menos_gosta=par["fator_menos_gosta"],
        penalidade_estudo_longo=par["penalidade_estudo_longo"],
        cursos_estudo_longo=frozenset(par["cursos_estudo_longo"]),
    )
    dims = cat.dims
    for chave, d in cat.disciplinas.items():
        _validar_pesos(f"disciplina '{chave}'", d["pesos"], dims)
    for chave, a in cat.atividades.items():
        _validar_pesos(f"atividade '{chave}'", a["pesos"], dims)
    for nome, c in cat.cursos.items():
        _validar_pesos(f"curso '{nome}'", c["perfil"], dims)
        if not any(c["perfil"].values()):
            raise ValueError(f"curso '{nome}': perfil sem nenhum peso")
        if c["area"] not in cat.areas:
            raise ValueError(f"curso '{nome}': área desconhecida '{c['area']}'")
        invalidas = set(c["modalidades"]) - MODALIDADES_VALIDAS
        if invalidas:
            raise ValueError(f"curso '{nome}': modalidades inválidas {sorted(invalidas)}")
    desconhecidos = cat.cursos_estudo_longo - set(cat.cursos)
    if desconhecidos:
        raise ValueError(f"cursos_estudo_longo desconhecidos: {sorted(desconhecidos)}")
    return cat
