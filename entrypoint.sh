#!/bin/sh
echo "Verificando archivos en /app..."
ls -la /app
echo "Verificando si main.py existe..."
if [ -f /app/main.py ]; then
    echo "main.py encontrado!"
    echo "Ejecutando uvicorn..."
    python -m uvicorn main:app --host 0.0.0.0 --port 8000
else
    echo "ERROR: main.py no encontrado en /app"
    echo "Contenido de /app:"
    ls -la /app
    exit 1
fi
