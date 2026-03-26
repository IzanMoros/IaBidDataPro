# -*- coding: utf-8 -*-
"""
Visualización de Embeddings — Tema Premium Oscuro
==================================================
Gráficos interactivos de alta calidad con Plotly.
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Optional


# Paleta de colores del tema
THEME = {
    "bg":         "rgba(13,17,23,0)",
    "bg_plot":    "rgba(255,255,255,0.02)",
    "grid":       "rgba(255,255,255,0.05)",
    "font":       "#94a3b8",
    "title":      "#f1f5f9",
    "accent":     "#6366f1",
    "highlight":  "#f472b6",
    "normal":     "#6366f1",
    "selected":   "#f472b6",
}

GENRE_COLORS = [
    "#6366f1", "#a855f7", "#ec4899", "#f43f5e",
    "#f97316", "#eab308", "#22c55e", "#10b981",
    "#06b6d4", "#3b82f6", "#8b5cf6", "#d946ef",
]


class VisualizadorEmbeddings:
    """Visualizaciones premium de embeddings con tema oscuro."""

    def __init__(self):
        pass

    def _base_layout(self, titulo: str, height: int = 650) -> dict:
        """Retorna el layout base con el tema oscuro."""
        return dict(
            title=dict(text=titulo, font=dict(size=18, color=THEME["title"], family="Inter"), x=0),
            paper_bgcolor=THEME["bg"],
            plot_bgcolor=THEME["bg_plot"],
            font=dict(color=THEME["font"], family="Inter, sans-serif"),
            height=height,
            margin=dict(l=20, r=20, t=60, b=20),
        )

    def reducir_dimensiones_pca(self, embeddings: np.ndarray, n_componentes: int = 2) -> np.ndarray:
        pca = PCA(n_components=n_componentes, random_state=42)
        return pca.fit_transform(embeddings)

    def reducir_dimensiones_tsne(self, embeddings: np.ndarray, n_componentes: int = 2) -> np.ndarray:
        tsne = TSNE(
            n_components=n_componentes,
            random_state=42,
            perplexity=min(30, len(embeddings) - 1),
            n_iter=1000,
            learning_rate="auto",
            init="random",
        )
        return tsne.fit_transform(embeddings)

    def crear_grafico_2d(
        self,
        embeddings: np.ndarray,
        etiquetas: List[str],
        titulo: str = "Espacio de Embeddings 2D",
        resaltar_indices: Optional[List[int]] = None,
        metodo: str = "pca",
        generos: Optional[List[str]] = None,
    ) -> go.Figure:
        if metodo == "pca":
            coords = self.reducir_dimensiones_pca(embeddings, 2)
        else:
            coords = self.reducir_dimensiones_tsne(embeddings, 2)

        tipos = ["Normal"] * len(etiquetas)
        if resaltar_indices:
            for idx in resaltar_indices:
                tipos[idx] = "Recomendada"

        df = pd.DataFrame({
            "x": coords[:, 0],
            "y": coords[:, 1],
            "Película": etiquetas,
            "Tipo": tipos,
            "Género": generos if generos else [""] * len(etiquetas),
        })

        fig = go.Figure()

        # Puntos normales
        df_norm = df[df["Tipo"] == "Normal"]
        fig.add_trace(go.Scatter(
            x=df_norm["x"], y=df_norm["y"],
            mode="markers+text",
            name="Películas",
            text=df_norm["Película"],
            textposition="top center",
            textfont=dict(size=9, color="#64748b"),
            marker=dict(
                size=10,
                color=THEME["accent"],
                opacity=0.7,
                line=dict(width=1, color="rgba(99,102,241,0.5)"),
            ),
            hovertemplate="<b>%{text}</b><extra></extra>",
        ))

        # Puntos resaltados
        if resaltar_indices:
            df_sel = df[df["Tipo"] == "Recomendada"]
            fig.add_trace(go.Scatter(
                x=df_sel["x"], y=df_sel["y"],
                mode="markers+text",
                name="🎯 Recomendadas",
                text=df_sel["Película"],
                textposition="top center",
                textfont=dict(size=10, color="#f472b6", family="Inter"),
                marker=dict(
                    size=16,
                    color=THEME["highlight"],
                    line=dict(width=2, color="white"),
                    symbol="star",
                ),
                hovertemplate="<b>%{text}</b> ⭐<extra></extra>",
            ))

        layout = self._base_layout(titulo)
        layout.update(dict(
            xaxis=dict(
                title="Componente 1",
                gridcolor=THEME["grid"],
                zeroline=False,
                showline=False,
            ),
            yaxis=dict(
                title="Componente 2",
                gridcolor=THEME["grid"],
                zeroline=False,
                showline=False,
            ),
            showlegend=True,
            legend=dict(
                bgcolor="rgba(255,255,255,0.03)",
                bordercolor="rgba(255,255,255,0.1)",
                borderwidth=1,
                font=dict(color="#94a3b8"),
            ),
            hovermode="closest",
        ))
        fig.update_layout(layout)
        return fig

    def crear_grafico_3d(
        self,
        embeddings: np.ndarray,
        etiquetas: List[str],
        titulo: str = "Espacio de Embeddings 3D",
        resaltar_indices: Optional[List[int]] = None,
        metodo: str = "pca",
    ) -> go.Figure:
        if metodo == "pca":
            coords = self.reducir_dimensiones_pca(embeddings, 3)
        else:
            coords = self.reducir_dimensiones_tsne(embeddings, 3)

        tipos = ["Normal"] * len(etiquetas)
        if resaltar_indices:
            for idx in resaltar_indices:
                tipos[idx] = "Recomendada"

        df = pd.DataFrame({
            "x": coords[:, 0], "y": coords[:, 1], "z": coords[:, 2],
            "Película": etiquetas, "Tipo": tipos,
        })

        fig = go.Figure()

        df_norm = df[df["Tipo"] == "Normal"]
        fig.add_trace(go.Scatter3d(
            x=df_norm["x"], y=df_norm["y"], z=df_norm["z"],
            mode="markers+text",
            name="Películas",
            text=df_norm["Película"],
            textfont=dict(size=9, color="#64748b"),
            marker=dict(
                size=6,
                color=THEME["accent"],
                opacity=0.75,
                line=dict(width=0.5, color="rgba(99,102,241,0.4)"),
            ),
            hovertemplate="<b>%{text}</b><extra></extra>",
        ))

        if resaltar_indices:
            df_sel = df[df["Tipo"] == "Recomendada"]
            fig.add_trace(go.Scatter3d(
                x=df_sel["x"], y=df_sel["y"], z=df_sel["z"],
                mode="markers+text",
                name="🎯 Recomendadas",
                text=df_sel["Película"],
                textfont=dict(size=10, color="#f472b6"),
                marker=dict(
                    size=12,
                    color=THEME["highlight"],
                    symbol="diamond",
                    line=dict(width=1, color="white"),
                ),
                hovertemplate="<b>%{text}</b> ⭐<extra></extra>",
            ))

        axis_style = dict(
            backgroundcolor="rgba(13,17,23,0.5)",
            gridcolor=THEME["grid"],
            showbackground=True,
            zerolinecolor=THEME["grid"],
            tickfont=dict(color=THEME["font"]),
            titlefont=dict(color=THEME["font"]),
        )

        layout = self._base_layout(titulo, height=700)
        layout.update(dict(
            scene=dict(
                xaxis=dict(title="PC 1", **axis_style),
                yaxis=dict(title="PC 2", **axis_style),
                zaxis=dict(title="PC 3", **axis_style),
                bgcolor="rgba(13,17,23,0.3)",
            ),
            legend=dict(
                bgcolor="rgba(255,255,255,0.03)",
                bordercolor="rgba(255,255,255,0.1)",
                borderwidth=1,
                font=dict(color="#94a3b8"),
            ),
        ))
        fig.update_layout(layout)
        return fig

    def crear_mapa_calor_similitud(
        self,
        embeddings: np.ndarray,
        etiquetas: List[str],
        titulo: str = "Mapa de Calor de Similitudes Semánticas",
    ) -> go.Figure:
        matriz = cosine_similarity(embeddings)

        # Escala de colores personalizada (azul-morado-rosa)
        colorscale = [
            [0.0,  "#0a0a1a"],
            [0.3,  "#1e1b4b"],
            [0.5,  "#4c1d95"],
            [0.65, "#6d28d9"],
            [0.8,  "#a855f7"],
            [0.9,  "#ec4899"],
            [1.0,  "#fda4af"],
        ]

        fig = go.Figure(data=go.Heatmap(
            z=matriz,
            x=etiquetas,
            y=etiquetas,
            colorscale=colorscale,
            zmin=0, zmax=1,
            hovertemplate="<b>%{y}</b> vs <b>%{x}</b><br>Similitud: %{z:.3f}<extra></extra>",
            colorbar=dict(
                title="Similitud",
                titlefont=dict(color="#94a3b8"),
                tickfont=dict(color="#94a3b8"),
                outlinecolor="rgba(255,255,255,0.1)",
                outlinewidth=1,
            ),
        ))

        layout = self._base_layout(titulo, height=820)
        layout.update(dict(
            xaxis=dict(
                tickangle=-45,
                tickfont=dict(size=9, color=THEME["font"]),
                gridcolor=THEME["grid"],
                showgrid=False,
            ),
            yaxis=dict(
                tickfont=dict(size=9, color=THEME["font"]),
                gridcolor=THEME["grid"],
                showgrid=False,
                autorange="reversed",
            ),
        ))
        fig.update_layout(layout)
        return fig
