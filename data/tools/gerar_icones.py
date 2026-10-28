"""Converte assets/svg/*.svg em assets/icones/*.png (256 px). Uso só em desenvolvimento.

Requer: pip install cairosvg  (no Windows, cairosvg precisa da biblioteca Cairo instalada).
O app em si só usa os PNGs já gerados, então quem apenas roda o app não precisa disso.
"""
from pathlib import Path

import cairosvg

RAIZ = Path(__file__).resolve().parent.parent
TAMANHO = 256

if __name__ == "__main__":
    destino = RAIZ / "assets" / "icones"
    destino.mkdir(parents=True, exist_ok=True)
    for svg in sorted((RAIZ / "assets" / "svg").glob("*.svg")):
        cairosvg.svg2png(url=str(svg), write_to=str(destino / f"{svg.stem}.png"),
                         output_width=TAMANHO, output_height=TAMANHO)
        print("ok", svg.stem)
