# Recomendador de Graduação

Recomenda cursos a partir de respostas do próprio aluno. Algoritmo determinístico (sem ML):
o perfil do aluno vira um vetor em 7 dimensões (RIASEC + saúde) e é comparado, por
similaridade de cosseno, ao perfil ideal de cada curso.

## Rodar

    pip install -r requirements.txt
    python main.py

## Testes

    python -m unittest tests.test_recomendador -v

`tests/golden.json` guarda a saída do script original; o teste garante que a lógica não muda por acidente.
Se você alterar pesos de propósito, regenere esse arquivo.

## Estrutura (dependência em uma direção: ui → core → data)

    main.py              entrada
    core/                lógica pura (sem tkinter): modelos, perfil, recomendador
    data/                JSONs editáveis + carregador/validador
    ui/                  janela, telas e componentes (customtkinter)
    utils/               ícones e formatação de texto
    assets/              svg/ (fontes) e icones/ (PNG usados pelo app)
    tools/               scripts de desenvolvimento (gerar SVG e PNG)
    tests/

## Ajustar pesos

Tudo fica em `data/*.json`, sem mexer em código:

- `cursos.json`: perfil de cada curso, área e modalidades. `"modalidades": []` = curso fora do catálogo (ignorado por padrão).
- `atividades.json` / `disciplinas.json`: perguntas e quanto cada resposta pontua em cada dimensão.
- `parametros.json`: fatores de peso, penalidade de formação longa e nomes das dimensões.

Os pesos atuais são hipóteses iniciais, ainda não calibradas com dados reais.

## Ícones

O app usa só os PNGs de `assets/icones`. Para regenerá-los: `pip install cairosvg`,
`python tools/gerar_svgs.py` e `python tools/gerar_icones.py`.
