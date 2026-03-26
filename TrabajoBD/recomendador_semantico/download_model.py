# -*- coding: utf-8 -*-
import sys
import io

# Configurar encoding para Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from sentence_transformers import SentenceTransformer

print("🔍 Iniciando descarga del modelo de IA...")
print("📦 Modelo: all-MiniLM-L6-v2")
print("⏳ Esto solo ocurre una vez. Por favor, espera...")

try:
    # Esto forzará la descarga del modelo con barra de progreso en consola
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("\n✅ ¡Modelo descargado y listo!")
except Exception as e:
    print(f"\n❌ Error al descargar: {e}")
