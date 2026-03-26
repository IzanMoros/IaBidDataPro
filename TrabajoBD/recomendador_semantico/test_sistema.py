"""
Script de Prueba - Recomendador Semantico
=========================================

Este script prueba todas las funcionalidades del sistema
sin necesidad de la interfaz Streamlit.
"""

import sys
import io

# Configurar encoding para Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("=" * 70)
print("SCRIPT DE PRUEBA - Recomendador Semantico")
print("=" * 70)

print("\nPaso 1: Verificando dependencias...")

try:
    import numpy as np
    print("   OK: NumPy")
except ImportError:
    print("   ERROR: NumPy")
    exit(1)

try:
    import pandas as pd
    print("   OK: Pandas")
except ImportError:
    print("   ERROR: Pandas")
    exit(1)

try:
    from sentence_transformers import SentenceTransformer
    print("   OK: Sentence Transformers")
except ImportError:
    print("   ERROR: Sentence Transformers")
    exit(1)

from dataset import obtener_dataset_peliculas, estadisticas_dataset
from embeddings_manager import EmbeddingsManager

print("\nPaso 2: Probando carga de dataset...")
estadisticas_dataset()

print("\nPaso 3: Probando generacion de embeddings...")
manager = EmbeddingsManager()
texto_test = "Una pelicula triste en el espacio"
embedding = manager.generar_embedding(texto_test)
print(f"Texto: '{texto_test}'")
print(f"Embedding shape: {embedding.shape}")

print("\nPaso 4: Probando busqueda semantica...")
df = obtener_dataset_peliculas()
consulta = "una pelicula triste que ocurre en el espacio"
resultados = manager.buscar_similares(consulta, df['descripcion'].tolist(), top_k=3)

for idx, similitud in resultados:
    p = df.iloc[idx]
    print(f"- {p['titulo']} ({p['año']}): {similitud:.4f}")

print("\nTODAS LAS PRUEBAS COMPLETADAS")
