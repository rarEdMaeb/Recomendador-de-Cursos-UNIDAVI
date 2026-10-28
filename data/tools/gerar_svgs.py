"""Gera os SVGs-base dos ícones por área (traço branco, fundo transparente)."""
import math
from pathlib import Path

DESTINO = Path(__file__).resolve().parent.parent / "assets" / "svg"
ABRE = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none" stroke="#FFFFFF" '
        'stroke-width="4" stroke-linecap="round" stroke-linejoin="round">')


def engrenagem():
    dentes = "".join(
        f'<rect x="28" y="6" width="8" height="10" rx="2" fill="#FFFFFF" stroke="none" '
        f'transform="rotate({a} 32 32)"/>' for a in range(0, 360, 45))
    return f'{dentes}<circle cx="32" cy="32" r="16"/><circle cx="32" cy="32" r="6"/>'


ICONES = {
    "saude": '<path d="M32 54C10 38 6 22 16 14c7-6 14-2 16 4 2-6 9-10 16-4 10 8 6 24-16 40z"/>'
             '<path d="M32 24v14M25 31h14"/>',
    "engenharia": engrenagem(),
    "tecnologia": '<polyline points="22,18 8,32 22,46"/><polyline points="42,18 56,32 42,46"/>'
                  '<line x1="36" y1="14" x2="28" y2="50"/>',
    "gestao": '<line x1="8" y1="54" x2="56" y2="54"/><rect x="12" y="34" width="10" height="16" rx="2"/>'
              '<rect x="27" y="24" width="10" height="26" rx="2"/><rect x="42" y="12" width="10" height="38" rx="2"/>',
    "educacao": '<polygon points="32,12 58,26 32,40 6,26"/><path d="M16 33v10c0 5 32 5 32 0V33"/>'
                '<line x1="58" y1="26" x2="58" y2="42"/>',
    "direito": '<line x1="32" y1="10" x2="32" y2="52"/><line x1="12" y1="18" x2="52" y2="18"/>'
               '<path d="M12 18L5 36h14z"/><path d="M52 18l-7 18h14z"/><line x1="20" y1="54" x2="44" y2="54"/>',
    "artes": '<path d="M32 8C16 8 6 20 6 32c0 14 12 24 24 24 6 0 6-6 3-9-3-4 0-8 5-8h8c6 0 12-4 12-12C58 18 46 8 32 8z"/>'
             '<circle cx="20" cy="30" r="2" fill="#FFFFFF"/><circle cx="28" cy="20" r="2" fill="#FFFFFF"/>'
             '<circle cx="40" cy="20" r="2" fill="#FFFFFF"/>',
    "agro": '<path d="M32 56V28"/><path d="M32 36C32 22 22 14 10 14c0 14 8 22 22 22z"/>'
            '<path d="M32 28C32 16 42 10 54 10c0 14-8 22-22 18z"/>',
}

if __name__ == "__main__":
    DESTINO.mkdir(parents=True, exist_ok=True)
    for nome, corpo in ICONES.items():
        (DESTINO / f"{nome}.svg").write_text(f"{ABRE}{corpo}</svg>\n", encoding="utf-8")
    print(f"{len(ICONES)} SVGs em {DESTINO}")
