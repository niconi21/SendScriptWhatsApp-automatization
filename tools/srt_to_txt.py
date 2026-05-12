import re
import sys
import os

if len(sys.argv) < 3:
    print("Uso: python3 srt_to_txt.py <archivo.srt> <nombre_pelicula>")
    sys.exit(1)

srt_file = sys.argv[1]
movie_name = sys.argv[2]
output_name = movie_name.lower().replace(" ", "_") + ".txt"
output_path = os.path.join(os.path.dirname(__file__), "../scripts", output_name)

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

with open(output_path, "w", encoding="utf-8") as f:
    f.write(text)

print(output_path)
