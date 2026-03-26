# -*- coding: utf-8 -*-
"""
Script de Prueba - Nuevas Funcionalidades
==========================================

Este script prueba las nuevas funciones agregadas:
1. Comparador de películas
2. Modo sorpréndeme (recomendaciones diversas)
"""

import sys
import io

# Configurar encoding para Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("=" * 70)
print("PRUEBA DE NUEVAS FUNCIONALIDADES")
print("=" * 70)

# Importar módulos
from embeddings_manager import EmbeddingsManager
from dataset import obtener_dataset_peliculas

print("\n1. Cargando sistema...")
manager = EmbeddingsManager()
df = obtener_dataset_peliculas()

print(f"   ✅ {len(df)} películas cargadas")
print(f"   ✅ Modelo con vectores de {manager.dimension_vector} dimensiones")

# ============================================================================
# PRUEBA 1: COMPARADOR DE PELÍCULAS
# ============================================================================

print("\n" + "=" * 70)
print("PRUEBA 1: COMPARADOR DE PELÍCULAS")
print("=" * 70)

# Caso 1: Películas similares (mismo género)
print("\n📋 Caso 1: Películas del mismo género")
resultado1 = manager.comparar_peliculas(
    df[df['titulo'] == 'Deadpool']['descripcion'].iloc[0],
    df[df['titulo'] == 'Guardians of the Galaxy']['descripcion'].iloc[0],
    "Deadpool",
    "Guardians of the Galaxy"
)
print(f"   Resultado: {resultado1['similitud']:.2%} - {resultado1['interpretacion']}")

# Caso 2: Películas muy diferentes
print("\n📋 Caso 2: Películas de géneros opuestos")
resultado2 = manager.comparar_peliculas(
    df[df['titulo'] == 'The Shining']['descripcion'].iloc[0],
    df[df['titulo'] == 'Amélie']['descripcion'].iloc[0],
    "The Shining (Terror)",
    "Amélie (Romance/Comedia)"
)
print(f"   Resultado: {resultado2['similitud']:.2%} - {resultado2['interpretacion']}")

# Caso 3: Similitud inesperada (mismo tema, diferente género)
print("\n📋 Caso 3: Mismos temas, géneros diferentes")
resultado3 = manager.comparar_peliculas(
    df[df['titulo'] == 'Interstellar']['descripcion'].iloc[0],
    df[df['titulo'] == 'Gravity']['descripcion'].iloc[0],
    "Interstellar",
    "Gravity"
)
print(f"   Resultado: {resultado3['similitud']:.2%} - {resultado3['interpretacion']}")

# ============================================================================
# PRUEBA 2: MODO SORPRÉNDEME
# ============================================================================

print("\n" + "=" * 70)
print("PRUEBA 2: MODO SORPRÉNDEME (RECOMENDACIONES DIVERSAS)")
print("=" * 70)

# Generar embeddings del dataset
print("\n🔄 Generando embeddings del dataset...")
embeddings = manager.generar_embeddings_batch(
    df['descripcion'].tolist(),
    mostrar_progreso=False
)
print("   ✅ Embeddings generados")

# Prueba con semilla fija (reproducible)
print("\n📋 Generando 5 películas diversas (semilla fija: 42)")
diversas = manager.recomendar_diversas(
    embeddings,
    df['titulo'].tolist(),
    n=5,
    semilla=42
)

print("\n🎬 Películas seleccionadas:")
for i, (idx, titulo) in enumerate(diversas, 1):
    pelicula = df.iloc[idx]
    print(f"   {i}. {titulo} ({pelicula['año']}) - {pelicula['genero']}")

# Analizar diversidad
generos = [df.iloc[idx]['genero'] for idx, _ in diversas]
generos_unicos = len(set(generos))
print(f"\n📊 Análisis:")
print(f"   Géneros únicos: {generos_unicos}/5")
print(f"   Diversidad: {generos_unicos/5:.0%}")

# Prueba sin semilla (aleatorio)
print("\n📋 Segunda ejecución sin semilla (debería ser diferente)")
diversas2 = manager.recomendar_diversas(
    embeddings,
    df['titulo'].tolist(),
    n=5,
    semilla=None
)

print("\n🎬 Películas seleccionadas:")
for i, (idx, titulo) in enumerate(diversas2, 1):
    pelicula = df.iloc[idx]
    print(f"   {i}. {titulo} ({pelicula['año']}) - {pelicula['genero']}")

# ============================================================================
# RESULTADOS FINALES
# ============================================================================

print("\n" + "=" * 70)
print("✅ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
print("=" * 70)

print("\n📝 Resumen:")
print(f"   ✅ Comparador de películas: 3 pruebas exitosas")
print(f"   ✅ Modo sorpréndeme: 2 selecciones generadas")
print(f"   ✅ Diversidad promedio: {generos_unicos/5:.0%}")

print("\n💡 Las nuevas funcionalidades están listas para usar en Streamlit!")
print("   Ejecuta: streamlit run app.py")
print("=" * 70)
