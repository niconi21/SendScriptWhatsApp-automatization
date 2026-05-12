import json
import sys
import os

CHUNK_SIZE = 500
DELAY_MS = 4000

if len(sys.argv) < 2:
    print("Uso: python3 generate_js.py <script.txt>")
    sys.exit(1)

script_file = sys.argv[1]
movie_name = os.path.splitext(os.path.basename(script_file))[0]
output_path = os.path.join(os.path.dirname(__file__), "../output", movie_name + ".js")

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

print(output_path)
