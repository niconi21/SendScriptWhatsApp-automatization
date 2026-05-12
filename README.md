# SendScriptWhatsApp

Herramienta para enviar guiones completos de películas por WhatsApp Web, directamente desde la consola del navegador.

Basado en el proyecto original de [Matt-Fontes](https://github.com/Matt-Fontes/SendScriptWhatsApp).

---

## Cómo funciona

1. Conviertes un archivo `.srt` (subtítulos) en texto plano
2. El texto se divide en chunks y se embebe en un script JS
3. Pegas el JS en la consola de WhatsApp Web → se envía solo

---

## Dónde conseguir subtítulos (.srt)

[OpenSubtitles](https://www.opensubtitles.org/es) — busca la película, filtra por idioma español, descarga el `.srt`.

---

## Requisitos

- Python 3
- WhatsApp Web abierto en Chrome/Firefox

---

## Uso

### Agregar una película nueva

```bash
./add_movie.sh <archivo.srt> "Nombre Pelicula"
```

**Ejemplo:**
```bash
./add_movie.sh shrek2.srt "Shrek 2"
```

Esto genera automáticamente:
- `scripts/shrek_2.txt` — texto limpio
- `output/shrek_2.js` — script listo para pegar en el navegador

### Enviar por WhatsApp

1. Abre Chrome → WhatsApp Web
2. Abre el chat de tu víctima
3. `F12` → pestaña **Console**
4. Copia y pega el contenido de `output/shrek_2.js`
5. Enter → empieza a enviar solo cada 4 segundos

> No necesitas mantener el navegador en foco, solo el tab abierto.

---

## Estructura

```
.
├── add_movie.sh        # CLI principal
├── tools/
│   ├── srt_to_txt.py   # Convierte .srt a .txt limpio
│   └── generate_js.py  # Genera el script JS desde el .txt
├── scripts/            # Guiones en texto plano (generados)
├── output/             # Scripts JS listos para usar (generados)
└── srt/                # Tus archivos .srt originales
```

---

## Notas

- Los archivos en `srt/`, `scripts/` y `output/` están en `.gitignore` — no se suben al repo
- Soporta codificaciones UTF-8, latin-1 y UTF-16 automáticamente
- Los chunks respetan saltos de línea (no corta palabras a la mitad)

---

## Créditos

- **[Matt-Fontes](https://github.com/Matt-Fontes/SendScriptWhatsApp)** — concepto e idea original
- **[Claude](https://claude.ai) (Anthropic)** — implementación de esta versión: conversión de SRT, generación de JS, CLI `add_movie.sh`, detección de encoding, chunking por líneas
