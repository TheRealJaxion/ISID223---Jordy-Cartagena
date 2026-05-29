# =============================================================================
# main.py — Punto de entrada del MIS Biblioteca
# =============================================================================
 
import sys
import os
from sqlalchemy import create_engine, text
 
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
 
from kpis.kpis import calcular_todos_los_kpis

if __name__ == "__main__":
    url = f"mysql+pymysql://root:PjAYqFuPDdzUTLfBqKmVFfwYIVeJoEzR@zephyr.proxy.rlwy.net:53485/biblioteca?charset=utf8mb4"

    engine = create_engine(url, echo=False)
    print("=" * 55)
    print("   MIS BIBLIOTECA — Cálculo de KPIs")
    print("=" * 55)

    kpis   = calcular_todos_los_kpis(engine)
 
    print(f"\n  KPI 1 — Total préstamos        : {kpis['kpi1_total_prestamos']}")
    print(f"  KPI 2 — Devolución a tiempo    : {kpis['kpi2_tasa_devolucion']}%")
    print(f"  KPI 3 — Tasa de vencimiento    : {kpis['kpi3_tasa_vencimiento']}%")
    print(f"  KPI 8 — Tasa de renovaciones   : {kpis['kpi8_tasa_renovaciones']}%")
    print(f"  KPI 7 — Libros stock crítico   : {len(kpis['kpi7_stock_critico'])} libros")
 
    print("\n  Top 5 Libros más prestados:")
    print(kpis["kpi4_top_libros"].to_string(index=False))
 
    print("\n  Top 5 Categorías más demandadas:")
    print(kpis["kpi5_top_categorias"].to_string(index=False))
 
    print("\n  Préstamos por mes (últimos 6):")
    print(kpis["kpi6_prestamos_por_mes"].tail(6).to_string(index=False))
 
    print("\n" + "=" * 60)
    print("  Para el dashboard: streamlit run dashboard/dashboard.py")
    print("=" * 60)
 
