# -*- coding: utf-8 -*-
"""
Gestor de Embeddings y Búsqueda Semántica
=========================================

Este módulo maneja toda la lógica de embeddings y similitud:
1. Carga del modelo de embeddings
2. Generación de vectores para textos
3. Cálculo de similitud coseno
4. Búsqueda semántica

CONCEPTOS CLAVE:
- Embedding: Representación numérica (vector) del significado de un texto
- Vector: Lista de números que representa el texto en espacio multidimensional
- Similitud Coseno: Mide qué tan "cerca" están dos vectores (0 a 1)
"""

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple
import pandas as pd


class EmbeddingsManager:
    """
    Clase que gestiona embeddings y búsqueda semántica.
    
    Esta clase encapsula toda la lógica de:
    - Cargar modelo de embeddings
    - Convertir textos a vectores
    - Calcular similitudes
    - Realizar búsquedas semánticas
    """
    
    def __init__(self, modelo_nombre: str = 'all-MiniLM-L6-v2'):
        """
        Inicializa el gestor de embeddings.
        
        Args:
            modelo_nombre: Nombre del modelo a usar.
                          Se usa 'all-MiniLM-L6-v2' para MÁXIMA VELOCIDAD de carga (solo ~80MB)
                          haciendo que la app inicie instantáneamente. El español se maneja 
                          inyectando conceptos semánticos internamente.
        """
        print(f"Cargando modelo de embeddings: {modelo_nombre}")
        print("   (Esto puede tomar unos segundos la primera vez...)")
        
        # Cargar el modelo pre-entrenado
        # Este modelo ya fue entrenado con millones de textos
        self.modelo = SentenceTransformer(modelo_nombre)
        
        # Almacenar información sobre el modelo
        self.dimension_vector = self.modelo.get_sentence_embedding_dimension()
        
        print(f"Modelo cargado exitosamente")
        print(f"   Dimension de vectores: {self.dimension_vector}")
        
    def generar_embedding(self, texto: str) -> np.ndarray:
        """
        Convierte un texto en su representación vectorial (embedding).
        
        Args:
            texto: Texto a convertir en vector
            
        Returns:
            Vector numpy de dimensión self.dimension_vector
            
        Ejemplo:
            >>> manager = EmbeddingsManager()
            >>> vector = manager.generar_embedding("película triste en el espacio")
            >>> print(vector.shape)  # (384,)
            >>> print(vector[:3])    # [-0.023, 0.145, ...]
        """
        # El modelo convierte el texto en un vector de números
        # Textos con significados similares tendrán vectores similares
        embedding = self.modelo.encode(texto, convert_to_numpy=True)
        
        return embedding
    
    def generar_embeddings_batch(self, textos: List[str], 
                                 mostrar_progreso: bool = True) -> np.ndarray:
        """
        Genera embeddings para múltiples textos de forma eficiente.
        
        Args:
            textos: Lista de textos a convertir
            mostrar_progreso: Si mostrar barra de progreso
            
        Returns:
            Matriz numpy de forma (n_textos, dimension_vector)
            
        Nota: Es más eficiente procesar múltiples textos a la vez
        que uno por uno.
        """
        embeddings = self.modelo.encode(
            textos, 
            convert_to_numpy=True,
            show_progress_bar=mostrar_progreso
        )
        
        return embeddings
    
    def calcular_similitud_coseno(self, vector1: np.ndarray, 
                                  vector2: np.ndarray) -> float:
        """
        Calcula la similitud coseno entre dos vectores.
        
        La similitud coseno mide el ángulo entre dos vectores:
        - 1.0 = Vectores idénticos (mismo significado)
        - 0.0 = Vectores perpendiculares (sin relación)
        - -1.0 = Vectores opuestos (significados contrarios)
        
        En la práctica, valores > 0.5 indican buena similitud.
        
        Args:
            vector1: Primer vector
            vector2: Segundo vector
            
        Returns:
            Similitud entre 0 y 1
            
        Fórmula:
            similitud = (A · B) / (||A|| × ||B||)
            donde:
            - A · B = producto punto
            - ||A|| = norma (magnitud) del vector
        """
        # Reshape para que sklearn acepte los vectores
        v1 = vector1.reshape(1, -1)
        v2 = vector2.reshape(1, -1)
        
        # Calcular similitud coseno
        similitud = cosine_similarity(v1, v2)[0][0]
        
        return float(similitud)
    
    def buscar_similares(self, consulta: str, 
                        textos_candidatos: List[str],
                        top_k: int = 5) -> List[Tuple[int, float]]:
        """
        Busca los textos más similares a una consulta.
        
        Este es el corazón del recomendador semántico:
        1. Convierte la consulta en vector
        2. Convierte todos los candidatos en vectores
        3. Calcula similitud entre consulta y cada candidato
        4. Ordena por similitud y devuelve los top_k mejores
        
        Args:
            consulta: Texto de búsqueda (ej: "película triste en el espacio")
            textos_candidatos: Lista de textos donde buscar
            top_k: Número de resultados a devolver
            
        Returns:
            Lista de tuplas (índice, similitud) ordenadas por similitud descendente
            
        Ejemplo:
            >>> resultados = manager.buscar_similares(
            ...     "algo gracioso",
            ...     ["comedia divertida", "drama triste", "terror oscuro"]
            ... )
            >>> print(resultados)  # [(0, 0.85), (1, 0.23), (2, 0.15)]
        """
        # 1. Generar embedding de la consulta
        print(f"Generando embedding para: '{consulta}'")
        embedding_consulta = self.generar_embedding(consulta)
        
        # 2. Generar embeddings de todos los candidatos
        print(f"Generando embeddings para {len(textos_candidatos)} candidatos...")
        embeddings_candidatos = self.generar_embeddings_batch(
            textos_candidatos, 
            mostrar_progreso=False
        )
        
        # 3. Calcular similitudes
        print("Calculando similitudes...")
        # Reshape para sklearn
        consulta_2d = embedding_consulta.reshape(1, -1)
        
        # Calcular todas las similitudes de una vez (muy eficiente)
        similitudes = cosine_similarity(consulta_2d, embeddings_candidatos)[0]
        
        # 4. Obtener índices ordenados por similitud descendente
        indices_ordenados = np.argsort(similitudes)[::-1]
        
        # 5. Tomar los top_k mejores
        top_indices = indices_ordenados[:top_k]
        
        # 6. Crear lista de resultados con (índice, similitud)
        resultados = [
            (int(idx), float(similitudes[idx])) 
            for idx in top_indices
        ]
        
        print(f"Busqueda completada. Top {top_k} resultados encontrados.\n")
        
        return resultados
    
    def buscar_similares_optimizada(self, consulta: str,
                                    embeddings_precalculados: np.ndarray,
                                    top_k: int = 5) -> List[Tuple[int, float]]:
        """
        Busca textos similares usando embeddings YA calculados (más rápido).
        
        Esta versión es más eficiente porque no regenera los embeddings
        del dataset en cada búsqueda, solo genera el embedding de la consulta.
        
        Args:
            consulta: Texto de búsqueda
            embeddings_precalculados: Matriz de embeddings ya calculados
            top_k: Número de resultados a devolver
            
        Returns:
            Lista de tuplas (índice, similitud) ordenadas por similitud descendente
        """
        # 0. Expandir consulta corta para mejorar resultados
        consulta_expandida = self._expandir_consulta(consulta)
        
        # 1. Generar solo el embedding de la consulta expandida
        print(f"Generando embedding para: '{consulta}'")
        if consulta_expandida != consulta:
            print(f"   (Expandida a: '{consulta_expandida}')")
        embedding_consulta = self.generar_embedding(consulta_expandida)
        
        # 2. Calcular similitudes con embeddings pre-calculados
        print(f"Calculando similitudes con {len(embeddings_precalculados)} películas...")
        consulta_2d = embedding_consulta.reshape(1, -1)
        similitudes = cosine_similarity(consulta_2d, embeddings_precalculados)[0]
        
        # 3. Obtener índices ordenados por similitud descendente
        indices_ordenados = np.argsort(similitudes)[::-1]
        
        # DEBUG: Mostrar top 5 similitudes
        print(f"\n🔍 DEBUG - Top 5 similitudes:")
        for i in range(min(5, len(similitudes))):
            idx = indices_ordenados[i]
            print(f"   #{i+1}: Índice {idx} - Similitud: {similitudes[idx]:.4f}")
        
        # 4. Tomar los top_k mejores
        top_indices = indices_ordenados[:top_k]
        
        # 5. Crear lista de resultados
        resultados = [
            (int(idx), float(similitudes[idx])) 
            for idx in top_indices
        ]
        
        print(f"Búsqueda completada. Top {top_k} resultados encontrados.\n")
        
        return resultados
    
    def _expandir_consulta(self, consulta: str) -> str:
        """
        Expande consultas cortas para hacerlas más descriptivas.
        
        Esto mejora los resultados cuando el usuario busca de forma muy general.
        """
        # Si la consulta ya es larga, no expandir
        if len(consulta.split()) > 8:
            return consulta
        
        consulta_lower = consulta.lower()
        expansiones = []
        
        # Detectar emociones con inyecciones bilingües para máxima precisión del modelo ligero
        if any(palabra in consulta_lower for palabra in ['triste', 'tristeza', 'melancólico', 'deprimente', 'llorar']):
            expansiones.append("historia emocionalmente conmovedora y desgarradora sad emotional heartbreaking cry drama")
        if any(palabra in consulta_lower for palabra in ['divertido', 'gracioso', 'cómico', 'risa', 'comedia']):
            expansiones.append("muy divertida y entretenida llena de humor funny comedy hilarious laughs")
        if any(palabra in consulta_lower for palabra in ['miedo', 'terror', 'aterrador', 'oscuro', 'susto']):
            expansiones.append("atmósfera oscura perturbadora y aterradora horror scary thriller creepy dark")
        if any(palabra in consulta_lower for palabra in ['romántico', 'amor', 'romance', 'enamorar']):
            expansiones.append("historia de amor tierna y emotiva romantic love relationship romance")
        
        # Detectar géneros/lugares
        if any(palabra in consulta_lower for palabra in ['espacio', 'espacial', 'galaxia', 'universo', 'planeta', 'estrella', 'alien', 'cosmos']):
            expansiones.append("ambientada en el espacio profundo la galaxia space aliens sci-fi universe galaxy planets stars")
        if any(palabra in consulta_lower for palabra in ['guerra', 'bélico', 'soldado', 'batalla']):
            expansiones.append("conflicto bélico devastador militar war military battle soldiers combat historical")
        if any(palabra in consulta_lower for palabra in ['niños', 'familia', 'infantil', 'dibujos', 'animación', 'animado']):
            expansiones.append("dibujos animados y animación, apropiada para toda la familia animation kids family friendly cartoon")
        if any(palabra in consulta_lower for palabra in ['acción', 'peleas', 'disparos', 'adrenalina', 'superhéroe']):
            expansiones.append("adrenalina constante acción espectacular action superhero fights explosions martial arts fast paced")
        
        # Si hay expansiones, combinarlas con la consulta original
        if expansiones:
            return f"{consulta}. {' '.join(expansiones[:2])}"
        
        # Si no hay expansiones, agregar contexto genérico
        return f"película que sea {consulta} con temas relacionados"
    
    def interpretar_similitud(self, similitud: float) -> str:
        """
        Convierte un valor de similitud en descripción legible.
        
        Args:
            similitud: Valor entre 0 y 1
            
        Returns:
            Descripción textual del nivel de similitud
        """
        if similitud >= 0.8:
            return "🎯 Excelente coincidencia"
        elif similitud >= 0.6:
            return "✅ Muy buena coincidencia"
        elif similitud >= 0.4:
            return "👍 Buena coincidencia"
        elif similitud >= 0.2:
            return "🤔 Coincidencia moderada"
        else:
            return "❌ Baja coincidencia"
    
    def comparar_peliculas(self, descripcion1: str, descripcion2: str,
                          titulo1: str = "Película 1", 
                          titulo2: str = "Película 2") -> dict:
        """
        Compara directamente dos películas y retorna información detallada.
        
        Esta función permite un análisis "head to head" entre dos películas,
        calculando su similitud semántica y proporcionando interpretación.
        
        Args:
            descripcion1: Descripción de la primera película
            descripcion2: Descripción de la segunda película
            titulo1: Nombre de la primera película
            titulo2: Nombre de la segunda película
            
        Returns:
            Diccionario con:
            - similitud: Score de similitud (0-1)
            - interpretacion: Descripción textual
            - titulo1, titulo2: Nombres de las películas
            - embedding1, embedding2: Vectores generados
            
        Ejemplo:
            >>> resultado = manager.comparar_peliculas(
            ...     "Comedia divertida",
            ...     "Drama triste",
            ...     "Deadpool",
            ...     "Requiem for a Dream"
            ... )
            >>> print(f"Similitud: {resultado['similitud']:.2%}")
        """
        print(f"\n🆚 Comparando '{titulo1}' vs '{titulo2}'...")
        
        # Generar embeddings para ambas películas
        embedding1 = self.generar_embedding(descripcion1)
        embedding2 = self.generar_embedding(descripcion2)
        
        # Calcular similitud
        similitud = self.calcular_similitud_coseno(embedding1, embedding2)
        
        # Interpretar resultado
        interpretacion = self.interpretar_similitud(similitud)
        
        print(f"   Similitud calculada: {similitud:.4f} - {interpretacion}")
        
        return {
            'similitud': similitud,
            'interpretacion': interpretacion,
            'titulo1': titulo1,
            'titulo2': titulo2,
            'embedding1': embedding1,
            'embedding2': embedding2
        }
    
    def recomendar_diversas(self, embeddings_dataset: np.ndarray, 
                           etiquetas: List[str],
                           n: int = 5,
                           semilla: int = None) -> List[Tuple[int, str]]:
        """
        Recomienda películas maximizando la diversidad semántica.
        
        En lugar de buscar similitud, este método busca películas que sean
        lo más DIFERENTES entre sí, creando una selección variada.
        
        Algoritmo:
        1. Selecciona una película aleatoria como punto de partida
        2. Para cada nueva película, elige la que maximice la distancia
           promedio con las ya seleccionadas
        3. Repite hasta tener n películas
        
        Esto asegura una "playlist" diversa que cubre diferentes géneros,
        tonos y temas.
        
        Args:
            embeddings_dataset: Matriz de todos los embeddings
            etiquetas: Nombres de las películas
            n: Número de películas a recomendar
            semilla: Semilla para reproducibilidad (opcional)
            
        Returns:
            Lista de tuplas (índice, título) de películas seleccionadas
            
        Ejemplo:
            >>> diversas = manager.recomendar_diversas(embeddings, titulos, n=5)
            >>> print("Selección diversa:")
            >>> for idx, titulo in diversas:
            ...     print(f"  - {titulo}")
        """
        print(f"\n🎲 Generando {n} recomendaciones diversas...")
        
        # Configurar semilla para reproducibilidad si se proporciona
        if semilla is not None:
            np.random.seed(semilla)
        
        # Validar que no pidamos más películas de las disponibles
        n = min(n, len(embeddings_dataset))
        
        # Paso 1: Seleccionar primera película aleatoriamente
        primera = np.random.randint(len(embeddings_dataset))
        seleccionadas = [primera]
        print(f"   🎬 Película semilla: {etiquetas[primera]}")
        
        # Paso 2-N: Seleccionar películas maximizando diversidad
        for iteracion in range(n - 1):
            distancias = []
            
            # Calcular distancia promedio de cada película a las seleccionadas
            for i in range(len(embeddings_dataset)):
                if i in seleccionadas:
                    # Ya seleccionada, ignorar
                    distancias.append(-1)
                else:
                    # Calcular distancia promedio a todas las seleccionadas
                    # Distancia = 1 - similitud (más distancia = menos similar)
                    distancias_a_seleccionadas = [
                        1 - self.calcular_similitud_coseno(
                            embeddings_dataset[i], 
                            embeddings_dataset[j]
                        )
                        for j in seleccionadas
                    ]
                    distancia_promedio = np.mean(distancias_a_seleccionadas)
                    distancias.append(distancia_promedio)
            
            # Seleccionar la película más distante (diferente)
            siguiente = np.argmax(distancias)
            seleccionadas.append(siguiente)
            print(f"   🎬 Película {iteracion + 2}: {etiquetas[siguiente]} "
                  f"(distancia: {distancias[siguiente]:.3f})")
        
        # Crear lista de resultados con índices y títulos
        resultados = [(idx, etiquetas[idx]) for idx in seleccionadas]
        
        print(f"\n✅ Selección diversa completada: {n} películas")
        
        return resultados


def demo_embeddings():
    """
    Demostración educativa de cómo funcionan los embeddings.
    Ejecuta esta función para ver ejemplos paso a paso.
    """
    print("=" * 70)
    print("🎓 DEMOSTRACIÓN: Cómo funcionan los Embeddings y Similitud Coseno")
    print("=" * 70)
    
    # Crear el gestor
    manager = EmbeddingsManager()
    
    print("\n📝 Paso 1: Generar embeddings para textos de ejemplo")
    print("-" * 70)
    
    textos = [
        "Una película muy triste que me haga llorar",
        "Una historia dramática y melancólica",
        "Comedia divertidísima que me haga reír",
        "Terror que dé mucho miedo"
    ]
    
    for i, texto in enumerate(textos, 1):
        embedding = manager.generar_embedding(texto)
        print(f"\n{i}. '{texto}'")
        print(f"   Vector (primeros 5 valores): {embedding[:5]}")
        print(f"   Dimensión total: {len(embedding)}")
    
    print("\n\n🧮 Paso 2: Calcular similitudes entre textos")
    print("-" * 70)
    
    # Generar todos los embeddings
    embeddings = manager.generar_embeddings_batch(textos, mostrar_progreso=False)
    
    # Comparar primer texto con los demás
    texto_referencia = textos[0]
    embedding_ref = embeddings[0]
    
    print(f"\nTexto de referencia: '{texto_referencia}'\n")
    
    for i, (texto, embedding) in enumerate(zip(textos, embeddings)):
        similitud = manager.calcular_similitud_coseno(embedding_ref, embedding)
        interpretacion = manager.interpretar_similitud(similitud)
        print(f"  vs '{texto}'")
        print(f"  → Similitud: {similitud:.4f} {interpretacion}\n")
    
    print("\n💡 Observaciones:")
    print("  - Textos similares tienen similitud alta (cercana a 1)")
    print("  - Textos diferentes tienen similitud baja (cercana a 0)")
    print("  - Los embeddings capturan el SIGNIFICADO, no las palabras exactas")
    print("=" * 70)


# Si se ejecuta directamente, mostrar demostración educativa
if __name__ == "__main__":
    demo_embeddings()
