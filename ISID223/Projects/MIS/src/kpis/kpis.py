"""
=============================================================================
     kpis.py — Módulo de KPIs para el MIS de Biblioteca
=============================================================================

Lineas 34 a 57: Carga de Tablas

- KPIS:
Lineas 58 a 66: Total Prestamos Registrados KPI 1

Lineas 67 a 90: Tasa de devolucion a tiempo KPI 2

Lineas 91 a 119: Tasa de vencimiento KPI 3

Lineas 120 a 152: Top 5 libros mas prestados KPI 4

Lineas 153 a 179: Top 5 categorias mas demandadas KPI 5

Lineas 180 a 204: Prestamos por mes (tendencia) KPI 6

Lineas 205 a 236: Libros con stock critico KPI 7

Lineas 237 a 254: Tasa de renovaciones KPI 8

=============================================================================
"""

import pandas as pd                         
from sqlalchemy import create_engine, text   
from datetime import date                    



# -----------------------------------------------------------------------------
#    CARGA DE TABLAS DESDE MYSQL
# -----------------------------------------------------------------------------

def cargar_tablas(engine) -> dict:

    #Lectura de las tablas desde la BD
    libros = pd.read_sql("SELECT * FROM libros", con=engine)
    personas = pd.read_sql("SELECT * FROM personas", con=engine)
    prestamos = pd.read_sql("SELECT * FROM prestamos", con=engine)


    for col in ["fecha_prestamo", "fecha_devolucion_esperada", "fecha_devolucion_real"]:
        prestamos[col] = pd.to_datetime(prestamos[col], errors="coerce")
        # errors='coerce' convierte valores inválidos a NaT en lugar de lanzar error

    # Normaliza los valores de 'estado' a minúsculas para comparaciones seguras
    prestamos["estado"] = prestamos["estado"].str.strip().str.lower()
    # strip() elimina espacios al inicio/fin; lower() estandariza capitalización

    # Retorna un diccionario con los tres DataFrames listos
    return {"libros": libros, "personas": personas, "prestamos": prestamos}


# =============================================================================
# KPI 1 — Total de prestamos registrados
# =============================================================================

def kpi_total_prestamos(prestamos: pd.DataFrame) -> int:
    total = len(prestamos)   # len() sobre un DataFrame cuenta sus filas
    return total


# =============================================================================
# KPI 2 — Tasa de devolucion a tiempo
# =============================================================================

def kpi_tasa_devolucion_a_tiempo(prestamos: pd.DataFrame) -> float:

    total = len(prestamos)                           # Total de préstamos
    if total == 0:                                   # Evita división por cero
        return 0.0

    # Filtra solo los préstamos con estado 'devuelto'
    devueltos = prestamos[prestamos["estado"] == "devuelto"]

    # De los devueltos, selecciona los que llegaron a tiempo (fecha real ≤ esperada)
    a_tiempo = devueltos[
        devueltos["fecha_devolucion_real"] <= devueltos["fecha_devolucion_esperada"]
    ]

    # Calcula el porcentaje respecto al total general de préstamos
    tasa = (len(a_tiempo) / total) * 100

    return round(tasa, 2)   # Redondea a 2 decimales para legibilidad


# =============================================================================
# KPI 3 — Tasa de vencimiento
# =============================================================================

def kpi_tasa_vencimiento(prestamos: pd.DataFrame) -> float:

    hoy = pd.Timestamp(date.today())   # Fecha actual como Timestamp para comparar
    total = len(prestamos)
    if total == 0:
        return 0.0
    
    
    # Condición 1: marcados explícitamente como vencidos en la BD
    cond_vencido_explicito = prestamos["estado"] == "vencido"

    # Condición 2: aún en estado "prestado" pero ya pasó la fecha de devolución
    cond_vencido_implicito = (
        (prestamos["estado"] == "prestado") &
        (prestamos["fecha_devolucion_esperada"] < hoy)
    )

    # Une ambas condiciones con OR lógico (|)
    vencidos = prestamos[cond_vencido_explicito | cond_vencido_implicito]

    tasa = (len(vencidos) / total) * 100

    return round(tasa, 2)


# =============================================================================
# KPI 4 — Top 5 libros mas prestados
# =============================================================================

def kpi_top_libros(prestamos: pd.DataFrame, libros: pd.DataFrame) -> pd.DataFrame:

    # Cuenta cuántos préstamos tiene cada libro agrupando por id_libro
    conteo = (
        prestamos
        .groupby("id_libro")           # Agrupa por identificador de libro
        .size()                        # Cuenta filas por grupo
        .reset_index(name="total_prestamos")  # Convierte la serie en DataFrame con nombre
    )

    # Une con la tabla libros para traer el título (JOIN por id_libro)
    resultado = conteo.merge(
        libros[["id_libro", "titulo"]],   # Se filtran por id y titulo
        on="id_libro",                    # Columna de unión
        how="left"                        # LEFT JOIN: mantiene todos los préstamos aunque no haya libro
    )

    # Ordena de mayor a menor préstamos y toma los primeros 5
    top5 = (
        resultado
        .sort_values("total_prestamos", ascending=False)
        .head(5)
        [["titulo", "total_prestamos"]]   # Se filtran columnas relevantes
        .reset_index(drop=True)           # Reinicia el índice desde 0
    )

    return top5


# =============================================================================
# KPI 5 — Top 5 categorias mas demandadas
# =============================================================================

def kpi_top_categorias(prestamos: pd.DataFrame, libros: pd.DataFrame) -> pd.DataFrame:

    # Une préstamos con libros para acceder al campo "categoria"
    df = prestamos.merge(
        libros[["id_libro", "categoria"]],  # Se filtra por categoria
        on="id_libro",
        how="left"
    )

    # Se agrupa por categoría y cuenta préstamos
    resultado = (
        df
        .groupby("categoria")
        .size()
        .reset_index(name="total_prestamos")
        .sort_values("total_prestamos", ascending=False)
        .head(5)
        .reset_index(drop=True)
    )

    return resultado


# =============================================================================
# KPI 6 — Prestamos por mes (tendencia)
# =============================================================================

def kpi_prestamos_por_mes(prestamos: pd.DataFrame) -> pd.DataFrame:

    # Crea una columna auxiliar 'mes' con el período año-mes (ej: 2024-03)
    df = prestamos.copy()                                      # Copia para no modificar el original
    df["mes"] = df["fecha_prestamo"].dt.to_period("M")        # Convierte fecha a período mensual

    # Agrupa por mes y cuenta préstamos
    resultado = (
        df
        .groupby("mes")
        .size()
        .reset_index(name="total_prestamos")
        .sort_values("mes")              # Ordena cronológicamente
    )

    # Convierte el período a string para compatibilidad con gráficos (ej: "2024-03")
    resultado["mes"] = resultado["mes"].astype(str)

    return resultado


# =============================================================================
# KPI 7 — Libros con stock critico
# =============================================================================

def kpi_stock_critico(libros: pd.DataFrame, umbral: float = 0.20) -> pd.DataFrame:

    df = libros.copy()

    # Calcula el porcentaje de disponibilidad por libro
    df["pct_disponible"] = df["cantidad_disponible"] / df["cantidad_total"]
    # División segura: si cantidad_total == 0 generaría NaN; se maneja con fillna
    df["pct_disponible"] = df["pct_disponible"].fillna(0)

    # Filtra solo los libros activos con stock por debajo del umbral
    criticos = df[
        (df["activo"] == 1) &                        # Solo libros activos en el sistema
        (df["pct_disponible"] < umbral)              # Con disponibilidad menor al umbral
    ]

    # Selecciona y formatea las columnas de salida
    resultado = (
        criticos[["titulo", "cantidad_total", "cantidad_disponible", "pct_disponible"]]
        .sort_values("pct_disponible")               # Ordena de más crítico a menos
        .reset_index(drop=True)
    )

    # Convierte pct_disponible a porcentaje legible (0.15 → 15.0)
    resultado["pct_disponible"] = (resultado["pct_disponible"] * 100).round(1)

    return resultado


# =============================================================================
# KPI 8 — Tasa de renovaciones
# =============================================================================

def kpi_tasa_renovaciones(prestamos: pd.DataFrame) -> float:

    total = len(prestamos)
    if total == 0:
        return 0.0

    # Filtra préstamos con estado exactamente igual a 'renovado'
    renovados = prestamos[prestamos["estado"] == "renovado"]

    tasa = (len(renovados) / total) * 100

    return round(tasa, 2)


# =============================================================================
# FUNCIÓN MAESTRA — Calcula todos los KPIs de una sola vez
# =============================================================================

def calcular_todos_los_kpis(engine) -> dict:

    # Carga las tres tablas desde MySQL
    tablas = cargar_tablas(engine)
    libros    = tablas["libros"]
    prestamos = tablas["prestamos"]

    # Calcula cada KPI y los almacena en un diccionario
    kpis = {
        "kpi1_total_prestamos"       : kpi_total_prestamos(prestamos),
        "kpi2_tasa_devolucion"       : kpi_tasa_devolucion_a_tiempo(prestamos),
        "kpi3_tasa_vencimiento"      : kpi_tasa_vencimiento(prestamos),
        "kpi4_top_libros"           : kpi_top_libros(prestamos, libros),
        "kpi5_top_categorias"       : kpi_top_categorias(prestamos, libros),
        "kpi6_prestamos_por_mes"     : kpi_prestamos_por_mes(prestamos),
        "kpi7_stock_critico"         : kpi_stock_critico(libros),
        "kpi8_tasa_renovaciones"     : kpi_tasa_renovaciones(prestamos),
    }

    return kpis  # Retorna el diccionario completo de resultados
