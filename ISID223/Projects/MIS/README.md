# Kinetix - Proyecto MIS

## Diseño de una Solución de MIS a partir de un TPS

### Acerca De Nosotros:

Kinetix, empresa ecuatoriana enfocada a brindar  servicios para empresas que buscan la correcta gestion de datos a gran escala, analitica predictiva y optimizacion de flujo de datos en tiempo real. Su nombre un derivado Kinetic, relativo al movimiento, pues toma los datos como un activo dinámico, vivo, y en constante evolución, que impulsa el crecimiento de un necogio.

**Misión:** Promover y difundir el conomiento relacionado a la ciencia de datos, mediante el trabajo cooperativo junto diferentes empresas, con estrategias como analsis predictivo, para evidenciar como un correcto manejo de la informacion puede ayudar a crecer un negocio.

**Visión:** Ser la empresa número uno en gestion de datos del ecuador, reconocida por un trabajo eeficiente,  y la capacidad de innovación en la optimizacion de datos.

**Objetivos Especificos:**
- Desarroolar e implementar arquitecturas de datos que reduzacan la velocidad para el tiempo de procesamiento de datos
- Alcanzar indices de 95% o superiores en saisfaccion a clientes en los proyectos.
- Asegurar que el 100% de las soluciones de gestión de información diseñadas cumplan estrictamente con las normativas internacionales de protección de datos y gobernanza vigentes.

## Descripcion General del Proyecto
### Estructura Principal de los Directorios

El proyecto se estructuró basandose en la plantilla de Cookiecutter Data Science (una plantilal para proyectos de ciencia de datos), organizando los archivos segun su funcionalidad, utilidad e implementabilidad:
```
├── README.md    <--- Usted esta aqui
├── dashboard    <--- Carpeta para la implementacion del dashboard (proximamente)
├── enviroment.yml   <--- Requerimientos para la replicacion (entorno conda/mamba)
├── notebooks        <--- Cuadernos de Jupyter generados 
│   ├── 01_kpi_Recalde-Cartagena.ipynb
│   ├── ELT.ipynb
│   └── graficas_y_dashboards.ipynb
├── src   <--- Codigo implementado
│   └── kpis
│       ├── __pycache__
│       │   └── kpis.cpython-312.pyc
│       └── kpis.py
└── tests
    └── test.py
```
