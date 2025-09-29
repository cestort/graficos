import plotly.graph_objects as go
from typing import Optional, List


def grafico_kpi_sentimiento(
    positivos: int,
    negativos: int,
    neutros: int,
    objetivo_positivo: float = 70.0,
    titulo: str = 'KPI: Sentimiento Positivo',
    mostrar_desglose: bool = True,
    colores_gauge: Optional[List[str]] = None
) -> go.Figure:
    """
    Crea un indicador tipo velocímetro (gauge) para visualizar KPI de sentimiento.
    
    Args:
        positivos: Número de comentarios/textos con sentimiento positivo
        negativos: Número de comentarios/textos con sentimiento negativo
        neutros: Número de comentarios/textos con sentimiento neutro
        objetivo_positivo: Porcentaje objetivo de sentimientos positivos (0-100)
        titulo: Título que aparecerá en la parte superior del gauge
        mostrar_desglose: Si es True, muestra una caja con el desglose detallado
        colores_gauge: Lista opcional de 3 colores [bajo, medio, alto]
    
    Returns:
        Figura de Plotly lista para mostrar con .show()
    """
    
    # ===== CONFIGURACIÓN DE COLORES =====
    if colores_gauge is None:
        colores_gauge = [
            '#e74c3c',  # Rojo para zona baja (0-40%)
            '#f39c12',  # Amarillo para zona media (40-70%)
            '#2ecc71'   # Verde para zona alta (70-100%)
        ]
    
    # ===== CÁLCULO DE MÉTRICAS =====
    total = positivos + negativos + neutros
    
    if total == 0:
        raise ValueError("El total de sentimientos no puede ser 0")
    
    # Calculamos porcentajes
    pct_positivo = (positivos / total) * 100
    pct_negativo = (negativos / total) * 100
    pct_neutro = (neutros / total) * 100
    
    # ===== COLOR DINÁMICO DE LA BARRA =====
    # El color cambia según el rendimiento
    if pct_positivo >= objetivo_positivo:
        color_barra = colores_gauge[2]  # Verde: alcanzamos objetivo
    elif pct_positivo >= objetivo_positivo * 0.7:
        color_barra = colores_gauge[1]  # Amarillo: estamos cerca
    else:
        color_barra = colores_gauge[0]  # Rojo: necesitamos mejorar
    
    # ===== CREACIÓN DEL GAUGE =====
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=pct_positivo,
        domain={'x': [0, 1], 'y': [0.1, 1]},  # Ajustado para dejar espacio abajo
        
        # Título del gráfico
        title={
            'text': titulo,
            'font': {'size': 26, 'color': '#2c3e50'}
        },
        
        # Número principal (porcentaje)
        number={
            'suffix': '%',
            'font': {'size': 50, 'color': color_barra}
        },
        
        # Delta (diferencia con objetivo)
        delta={
            'reference': objetivo_positivo,
            'increasing': {'color': colores_gauge[2]},
            'decreasing': {'color': colores_gauge[0]},
            'suffix': '%',
            'font': {'size': 20}
        },
        
        # Configuración del velocímetro
        gauge={
            'axis': {
                'range': [0, 100],
                'tickwidth': 2,
                'tickcolor': "darkgray",
                'tickmode': 'linear',
                'tick0': 0,
                'dtick': 20  # Marca cada 20%
            },
            'bar': {
                'color': color_barra,
                'thickness': 0.75
            },
            'bgcolor': "white",
            'borderwidth': 3,
            'bordercolor': "#34495e",
            
            # Zonas de colores de fondo
            'steps': [
                {'range': [0, 40], 'color': 'rgba(231, 76, 60, 0.2)'},
                {'range': [40, 70], 'color': 'rgba(243, 156, 18, 0.2)'},
                {'range': [70, 100], 'color': 'rgba(46, 204, 113, 0.2)'}
            ],
            
            # Línea roja que marca el objetivo
            'threshold': {
                'line': {'color': "#e74c3c", 'width': 4},
                'thickness': 0.75,
                'value': objetivo_positivo
            }
        }
    ))
    
    # ===== DESGLOSE DETALLADO =====
    if mostrar_desglose:
        desglose_texto = (
            f"<b>Desglose Total: {total}</b><br>"
            f"✅ Positivos: {positivos} ({pct_positivo:.1f}%)<br>"
            f"❌ Negativos: {negativos} ({pct_negativo:.1f}%)<br>"
            f"⚪ Neutros: {neutros} ({pct_neutro:.1f}%)<br>"
            f"<b>Objetivo: {objetivo_positivo}%</b>"
        )
        
        fig.add_annotation(
            text=desglose_texto,
            xref="paper", yref="paper",
            x=0.5, y=-0.25,  # Movido más abajo para evitar superposición
            showarrow=False,
            font=dict(size=14, color="#34495e"),
            align="center",
            bgcolor="rgba(255, 255, 255, 0.9)",  # Más opaco para mejor legibilidad
            bordercolor="#bdc3c7",
            borderwidth=2,
            borderpad=10
        )
    
    # ===== LAYOUT FINAL =====
    fig.update_layout(
        height=550,  # Aumentada para dar más espacio
        margin=dict(l=40, r=40, t=80, b=150),  # Margen inferior aumentado
        paper_bgcolor='white',
        font={'family': 'Arial, sans-serif'}
    )
    
    return fig


# ============================================================================
# 🎨 VARIABLES PARA PERSONALIZAR - MODIFICA ESTOS VALORES
# ============================================================================

# Cantidades de cada tipo de sentimiento
POSITIVOS = 120          # Número de comentarios positivos
NEGATIVOS = 30           # Número de comentarios negativos  
NEUTROS = 50             # Número de comentarios neutros

# Objetivo del KPI (en porcentaje)
OBJETIVO = 70.0          # Meta: queremos alcanzar 70% de positividad

# Personalización visual
TITULO_GRAFICO = 'Análisis de Sentimiento - Redes Sociales'

# Colores personalizados (opcional - descomenta para usar)
# MIS_COLORES = ['#ff6b6b', '#ffd93d', '#6bcf7f']  # Rojo, Amarillo, Verde


# ============================================================================
# 📊 GENERAR Y MOSTRAR EL GRÁFICO
# ============================================================================

if __name__ == "__main__":
    
    # Calcular el resultado esperado
    total = POSITIVOS + NEGATIVOS + NEUTROS
    porcentaje_actual = (POSITIVOS / total) * 100
    
    # Mostrar información en consola
    print("=" * 60)
    print("📊 GENERANDO GRÁFICO DE KPI DE SENTIMIENTO")
    print("=" * 60)
    print(f"\n📝 Datos configurados:")
    print(f"   Positivos: {POSITIVOS}")
    print(f"   Negativos: {NEGATIVOS}")
    print(f"   Neutros: {NEUTROS}")
    print(f"   Total: {total}")
    print(f"\n🎯 Objetivo: {OBJETIVO}%")
    print(f"📈 Resultado actual: {porcentaje_actual:.1f}%")
    
    # Determinar estado
    if porcentaje_actual >= OBJETIVO:
        estado = "✅ ¡OBJETIVO ALCANZADO!"
        color_estado = "verde"
    elif porcentaje_actual >= OBJETIVO * 0.7:
        estado = "⚠️  Cerca del objetivo"
        color_estado = "amarillo"
    else:
        estado = "❌ Por debajo del objetivo"
        color_estado = "rojo"
    
    print(f"\n{estado}")
    print(f"Diferencia: {porcentaje_actual - OBJETIVO:+.1f} puntos porcentuales")
    print("\n" + "=" * 60)
    print("🚀 Abriendo gráfico en el navegador...")
    print("=" * 60 + "\n")
    
    # Crear el gráfico con las variables definidas arriba
    fig = grafico_kpi_sentimiento(
        positivos=POSITIVOS,
        negativos=NEGATIVOS,
        neutros=NEUTROS,
        objetivo_positivo=OBJETIVO,
        titulo=TITULO_GRAFICO,
        mostrar_desglose=True
        # colores_gauge=MIS_COLORES  # Descomenta para usar colores personalizados
    )
    
    # Mostrar el gráfico
    fig.show()
    
    # Guardar el gráfico (opcional)
    # fig.write_html("mi_kpi_sentimiento.html")
    # print("💾 Gráfico guardado como 'mi_kpi_sentimiento.html'")