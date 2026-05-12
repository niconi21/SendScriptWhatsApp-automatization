import sys
import os
import re
import json
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.join(BASE_DIR, "tools")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
CHUNK_SIZE = 500
DELAY_MS = 4000

def srt_to_txt(srt_file, movie_name):
    for enc in ["utf-8", "latin-1", "utf-16"]:
        try:
            with open(srt_file, "r", encoding=enc) as f:
                content = f.read()
            break
        except (UnicodeDecodeError, Exception):
            continue
    else:
        print("Error: no se pudo detectar la codificacion del archivo.")
        sys.exit(1)

    lines = content.split("\n")
    clean = []
    for line in lines:
        line = line.strip()
        if re.match(r"^\d+$", line): continue
        if re.match(r"^\d{2}:\d{2}:\d{2}", line): continue
        if line == "": continue
        clean.append(line)

    text = f"{movie_name.upper()}\n\n" + "\n".join(clean)
    output_name = movie_name.lower().replace(" ", "_") + ".txt"
    output_path = os.path.join(SCRIPTS_DIR, output_name)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    return output_path

def generate_js(script_file):
    movie_name = os.path.splitext(os.path.basename(script_file))[0]
    output_path = os.path.join(OUTPUT_DIR, movie_name + ".js")

    with open(script_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    cleaned = "\n".join(line.strip() for line in lines)
    text_lines = cleaned.split("\n")
    chunks = []
    current = []
    current_len = 0
    for line in text_lines:
        if current_len + len(line) + 1 > CHUNK_SIZE and current:
            chunks.append("\n".join(current))
            current = []
            current_len = 0
        current.append(line)
        current_len += len(line) + 1
    if current:
        chunks.append("\n".join(current))

    chunks_json = json.dumps(chunks, ensure_ascii=False)

    js = f"""// ==== {movie_name.upper()} SENDER ====
// 1. Abre WhatsApp Web
// 2. Abre el chat de tu victima
// 3. Pega esto en la consola del navegador (F12 -> Console)
// ========================

const messages = {chunks_json};
let index = 0;

function getInputBox() {{
    return document.querySelector('footer div[contenteditable="true"]');
}}

function typeText(box, text) {{
    const lines = text.split('\\n');
    for (let i = 0; i < lines.length; i++) {{
        if (lines[i]) document.execCommand('insertText', false, lines[i]);
        if (i < lines.length - 1) {{
            box.dispatchEvent(new KeyboardEvent('keydown', {{ keyCode: 13, key: 'Enter', shiftKey: true, bubbles: true }}));
            box.dispatchEvent(new KeyboardEvent('keyup',  {{ keyCode: 13, key: 'Enter', shiftKey: true, bubbles: true }}));
        }}
    }}
}}

async function sendMessage(text) {{
    const box = getInputBox();
    if (!box) {{ console.error('No se encontro el cuadro de texto.'); return false; }}
    box.focus();
    typeText(box, text);
    await new Promise(r => setTimeout(r, 500));
    const sendBtn = document.querySelector('button[data-testid="send"]') ||
                    document.querySelector('span[data-icon="send"]');
    if (sendBtn) {{
        sendBtn.click();
    }} else {{
        box.dispatchEvent(new KeyboardEvent('keydown', {{ keyCode: 13, key: 'Enter', bubbles: true }}));
    }}
    return true;
}}

async function sendNext() {{
    if (index >= messages.length) {{
        console.log('LISTO. Tu amigo odia su telefono.');
        return;
    }}
    console.log(`Enviando ${{index + 1}}/${{messages.length}}...`);
    const ok = await sendMessage(messages[index]);
    if (ok) index++;
    setTimeout(sendNext, {DELAY_MS});
}}

console.log(`{movie_name} — ${{messages.length}} mensajes. Iniciando en 3 segundos...`);
setTimeout(sendNext, 3000);
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(js)

    return output_path

def main():
    if len(sys.argv) < 3:
        print("Uso: python add_movie.py <archivo.srt> \"Nombre Pelicula\"")
        print("")
        print("Ejemplo: python add_movie.py shrek2.srt \"Shrek 2\"")
        sys.exit(1)

    srt_file = sys.argv[1]
    movie_name = sys.argv[2]

    if not os.path.isfile(srt_file):
        print(f"Error: no se encontro '{srt_file}'")
        sys.exit(1)

    print("Convirtiendo subtitulos...")
    script_path = srt_to_txt(srt_file, movie_name)

    print("Generando JS...")
    js_path = generate_js(script_path)

    print()
    print("Listo.")
    print(f"  Script: {script_path}")
    print(f"  JS:     {js_path}")
    print()
    print(f"Pega el contenido de {js_path} en la consola del navegador (F12 -> Console).")

if __name__ == "__main__":
    main()
