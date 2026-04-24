"""
export_pdf.py – Konvertiert das Pflichtenheft von Markdown zu PDF.
Verwendung: python3 Pflichtenheft/export_pdf.py
Ausgabe:    Pflichtenheft/Pflichtenheft_HHBKTendo.pdf
"""

import os
import re
import sys

# macOS: Homebrew-Bibliotheken (libgobject, libpango) für WeasyPrint einbinden.
# SIP strippt DYLD_LIBRARY_PATH beim os.execv-Neustart, daher subprocess als Workaround.
_homebrew_lib = "/opt/homebrew/lib"
if sys.platform == "darwin" and os.path.isdir(_homebrew_lib):
    if _homebrew_lib not in os.environ.get("DYLD_LIBRARY_PATH", ""):
        import subprocess
        env = os.environ.copy()
        env["DYLD_LIBRARY_PATH"] = _homebrew_lib
        result = subprocess.run(
            [sys.executable] + sys.argv,
            env=env
        )
        sys.exit(result.returncode)

import markdown
from weasyprint import HTML, CSS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MD_FILE  = os.path.join(BASE_DIR, "Pflichtenheft_HHBKTendo.md")
PDF_FILE = os.path.join(BASE_DIR, "Pflichtenheft_HHBKTendo.pdf")

# ---------------------------------------------------------------------------
# Projektteam – Namen hier eintragen
# ---------------------------------------------------------------------------
TEAM_MEMBERS = [
    "Jamie Augustin",
    "Jesse Göllner",
    "Niklas Pingel",
    "Jakub Krause",
    "Arda Dinda",
]

# ---------------------------------------------------------------------------
# Markdown lesen und konvertieren
# ---------------------------------------------------------------------------
with open(MD_FILE, encoding="utf-8") as f:
    md_text = f.read()

html_body = markdown.markdown(
    md_text,
    extensions=["tables", "fenced_code", "toc", "nl2br"],
)

# ---------------------------------------------------------------------------
# CSS – Seitenformat, Typografie, Seitenzahlen
# ---------------------------------------------------------------------------
CSS_STRING = """
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600;700&display=swap');

/* ── Seitenformat ────────────────────────────────────────────── */
@page {
    size: A4;
    margin: 2.5cm 2.2cm 2.8cm 2.2cm;

    @bottom-center {
        font-family: 'Exo 2', sans-serif;
        font-size: 9pt;
        color: #8a9cc0;
        content: counter(page) " / " counter(pages);
    }
    @bottom-left {
        font-family: 'Exo 2', sans-serif;
        font-size: 9pt;
        color: #4a5680;
        content: "HHBKTendo Spielesammlung – Pflichtenheft";
    }
}

/* Erste Seite (Deckblatt) ohne Fußzeile */
@page :first {
    @bottom-center { content: ""; }
    @bottom-left   { content: ""; }
}

/* ── Grundlayout ────────────────────────────────────────────── */
* {
    box-sizing: border-box;
}

html, body {
    margin: 0;
    padding: 0;
    font-family: 'Exo 2', 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 10.5pt;
    line-height: 1.65;
    color: #1a1a2e;
    background: #ffffff;
}

/* ── Deckblatt ──────────────────────────────────────────────── */
.cover {
    page: cover;
    height: 26cm;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    background: #0d0f1a;
    color: #ffffff;
    page-break-after: always;
    padding: 2cm;
}

.cover h1 {
    font-family: 'Orbitron', 'Courier New', monospace;
    font-size: 32pt;
    font-weight: 900;
    color: #e8365d;
    margin: 0 0 0.3cm 0;
    letter-spacing: 2px;
}

.cover .subtitle {
    font-size: 14pt;
    color: #8a9cc0;
    margin: 0 0 1.5cm 0;
}

.cover .meta {
    font-size: 10pt;
    color: #4a5680;
    line-height: 1.8;
}

.cover .version-badge {
    display: inline-block;
    background: #e8365d;
    color: #ffffff;
    font-family: 'Orbitron', monospace;
    font-size: 9pt;
    font-weight: 700;
    padding: 4px 14px;
    border-radius: 100px;
    margin-top: 0.8cm;
    letter-spacing: 1px;
}

.cover .divider {
    width: 6cm;
    height: 2px;
    background: #6c3fc5;
    margin: 0.8cm auto;
}

.cover .team {
    font-size: 11pt;
    color: #c0c8e8;
    line-height: 1.9;
    margin: 0.6cm 0 0 0;
}

/* ── Inhalt ─────────────────────────────────────────────────── */
.content {
    padding: 0;
}

/* ── Überschriften ──────────────────────────────────────────── */
h1, h2, h3, h4 {
    font-family: 'Orbitron', 'Courier New', monospace;
    page-break-after: avoid;
}

h1 {
    font-size: 18pt;
    font-weight: 700;
    color: #e8365d;
    border-bottom: 2px solid #e8365d;
    padding-bottom: 4pt;
    margin-top: 1.2cm;
    margin-bottom: 0.4cm;
    page-break-before: always;
}

/* Erste h1 nicht umbrechen */
.content > h1:first-child {
    page-break-before: avoid;
}

h2 {
    font-size: 13pt;
    font-weight: 700;
    color: #1e2850;
    border-left: 3px solid #6c3fc5;
    padding-left: 8pt;
    margin-top: 0.8cm;
    margin-bottom: 0.3cm;
}

h3 {
    font-size: 11pt;
    font-weight: 700;
    color: #1e2850;
    margin-top: 0.6cm;
    margin-bottom: 0.2cm;
}

h4 {
    font-size: 10pt;
    font-weight: 600;
    color: #4a5680;
    margin-top: 0.4cm;
    margin-bottom: 0.15cm;
}

/* ── Absätze & Listen ───────────────────────────────────────── */
p {
    margin: 0 0 0.35cm 0;
    orphans: 3;
    widows: 3;
}

ul, ol {
    margin: 0 0 0.35cm 0;
    padding-left: 1.2cm;
}

li {
    margin-bottom: 0.1cm;
}

/* ── Trennlinie ─────────────────────────────────────────────── */
hr {
    border: none;
    border-top: 1px solid #e0e0e8;
    margin: 0.6cm 0;
}

/* ── Tabellen ───────────────────────────────────────────────── */
table {
    width: 100%;
    border-collapse: collapse;
    font-size: 9.5pt;
    margin: 0.3cm 0 0.5cm 0;
    page-break-inside: avoid;
}

thead tr {
    background: #1e2850;
    color: #ffffff;
}

thead th {
    font-family: 'Orbitron', monospace;
    font-size: 8.5pt;
    font-weight: 700;
    padding: 6pt 8pt;
    text-align: left;
    letter-spacing: 0.5px;
}

tbody tr:nth-child(even) {
    background: #f5f5fa;
}

tbody td {
    padding: 5pt 8pt;
    border-bottom: 1px solid #e0e0e8;
    vertical-align: top;
}

/* ── Code ───────────────────────────────────────────────────── */
code {
    font-family: 'Courier New', monospace;
    font-size: 9pt;
    background: #f0f0f8;
    color: #e8365d;
    padding: 1pt 4pt;
    border-radius: 3px;
}

pre {
    background: #0d0f1a;
    color: #8a9cc0;
    font-family: 'Courier New', monospace;
    font-size: 8.5pt;
    line-height: 1.5;
    padding: 12pt;
    border-radius: 6px;
    border-left: 3px solid #6c3fc5;
    overflow-wrap: break-word;
    white-space: pre-wrap;
    margin: 0.3cm 0 0.5cm 0;
    page-break-inside: avoid;
}

pre code {
    background: transparent;
    color: #8a9cc0;
    padding: 0;
    font-size: 8.5pt;
}

/* ── Fettdruck & Kursiv ─────────────────────────────────────── */
strong {
    font-weight: 700;
    color: #1a1a2e;
}

em {
    font-style: italic;
    color: #4a5680;
}

/* ── Fußzeilen-Trennlinie ───────────────────────────────────── */
.footer-rule {
    border-top: 1px solid #e0e0e8;
    margin-top: 1cm;
    padding-top: 0.3cm;
    font-size: 8.5pt;
    color: #4a5680;
    font-family: 'Exo 2', sans-serif;
}
"""

# ---------------------------------------------------------------------------
# Deckblatt extrahieren (erster H1-Titel)
# ---------------------------------------------------------------------------
# Pflichtenheft-Metadaten aus der Datei ableiten
version_match = re.search(r"\|\s*([\d.]+)\s*\|\s*(\d{4}-\d{2}-\d{2}).*Erstversion", md_text)
version = "1.5"
# Letzten Versionseintrag suchen
all_versions = re.findall(r"\|\s*([\d.]+)\s*\|\s*(\d{4}-\d{2}-\d{2})", md_text)
if all_versions:
    version, date = all_versions[-1]

sorted_members = sorted(TEAM_MEMBERS, key=lambda name: name.split()[-1].lower())
team_html = "<br>".join(sorted_members) if sorted_members else ""

cover_html = f"""
<div class="cover">
    <h1>HHBKTendo</h1>
    <p class="subtitle">Spielesammlung – Pflichtenheft</p>
    <div class="divider"></div>
    <p class="meta">
        HHBK Düsseldorf · Lernfeld 5<br>
        HHBKTendo Research Center · 2026<br>
        Strategiespiele mit MiniMax-KI (Bauernschach &amp; Tic-Tac-Toe)
    </p>
    {f'<p class="team">{team_html}</p>' if team_html else ""}
    <span class="version-badge">Version {version}</span>
</div>
"""

# ---------------------------------------------------------------------------
# Vollständiges HTML zusammenbauen
# ---------------------------------------------------------------------------
full_html = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<title>Pflichtenheft HHBKTendo</title>
</head>
<body>
{cover_html}
<div class="content">
{html_body}
</div>
</body>
</html>"""

# ---------------------------------------------------------------------------
# PDF erzeugen
# ---------------------------------------------------------------------------
print(f"Konvertiere {MD_FILE} ...")
HTML(string=full_html, base_url=BASE_DIR).write_pdf(
    PDF_FILE,
    stylesheets=[CSS(string=CSS_STRING)],
)
print(f"PDF gespeichert: {PDF_FILE}")
