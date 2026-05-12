#!/bin/bash

TOOL_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ "$#" -lt 2 ]; then
    echo "Uso: ./add_movie.sh <archivo.srt> \"Nombre Pelicula\""
    echo ""
    echo "Ejemplo: ./add_movie.sh shrek2.srt \"Shrek 2\""
    exit 1
fi

SRT_FILE="$1"
MOVIE_NAME="$2"

if [ ! -f "$SRT_FILE" ]; then
    echo "Error: no se encontro '$SRT_FILE'"
    exit 1
fi

echo "Convirtiendo subtitulos..."
SCRIPT_PATH=$(python3 "$TOOL_DIR/tools/srt_to_txt.py" "$SRT_FILE" "$MOVIE_NAME")
if [ $? -ne 0 ]; then echo "Error en conversion."; exit 1; fi

echo "Generando JS..."
JS_PATH=$(python3 "$TOOL_DIR/tools/generate_js.py" "$SCRIPT_PATH")
if [ $? -ne 0 ]; then echo "Error generando JS."; exit 1; fi

echo ""
echo "Listo."
echo "  Script: $SCRIPT_PATH"
echo "  JS:     $JS_PATH"
echo ""
echo "Pega el contenido de $JS_PATH en la consola del navegador (F12 -> Console)."
