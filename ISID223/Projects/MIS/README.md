# Proyecto Primer Bimestre 

## Diseño de una Solución de MIS a partir de un TPS

### FASE 1

### Modelo de negocio

Kinetix, empresa ecuatoriana enfocada a brindar  servicios para empresas que buscan la correcta gestion de datos a gran escala, analitica predictiva y optimizacion de flujo de datos en tiempo real. Su nombre un derivado Kinetic, relativo al movimiento, pues toma los datos como un activo dinámico, vivo, y en constante evolución, que impulsa el crecimiento de un necogio.

**Misión:** Promover y difundir el conomiento relacionado a la ciencia de datos, mediante el trabajo cooperativo junto diferentes empresas, con estrategias como analsis predictivo, para evidenciar como un correcto manejo de la informacion puede ayudar a crecer un negocio.

**Visión:** Ser la empresa número uno en gestion de datos del ecuador, reconocida por un trabajo eeficiente,  y la capacidad de innovación en la optimizacion de datos.

**Objetivos Especificos:**
- Desarroolar e implementar arquitecturas de datos que reduzacan la velocidad para el tiempo de procesamiento de datos
- Alcanzar indices de 95% o superiores en saisfaccion a clientes en los proyectos.
- Asegurar que el 100% de las soluciones de gestión de información diseñadas cumplan estrictamente con las normativas internacionales de protección de datos y gobernanza vigentes.

### Identificaión de Stackholders

| Stackholder | Visualizacion|
| :--- | :--- |
| Bibliotecario | Usarios morosos, vencimientos, renovaciones |
| jwfe de bilbioteca | Vision general, prestamos, stocks de libros |
| Coordinador Academico | Categorias más solicitadas, libros mas demandados |
---

### Análisis de Requerimeintos

Las Preguntas seleccionadas que el MIS resolvera son:

- ¿Cuáles son los 5 libros más prestados?
- ¿Qué categoría de libros tiene mayor demanda?
- ¿Cuántos préstamos se han vencido y devueltos a tiempo?
- ¿Cuál es la tendencia mensual de préstamos en el año?
- ¿Qué libros tiene un menor Stock?
- ¿Qué usarios tienen más prestamos?
- ¿Cuál es la tasa de renovación de préstamos?
- ¿Qué libros nunca han sido prestados?

### FASE 2
### Definición de KIPs

| # | KPI | Cómo se calcula |
| :--- | :--- | :--- |
|1|Total de préstamos registrados|COUNT de tabla préstamos
|2|Tasa de devolución a tiempo |DEVUELTOS / TOTAL × 100|
|3|Tasa de vencimiento|VENCIDOS / TOTAL × 100|
|4|Top 5 libros más prestados|COUNT por id_libro|
|5|Top 5 categorías más demandadas|COUNT por categoría|
|6|Préstamos por mes (tendencia)|COUNT agrupado por mes|
|7|Libros con stock crítico|disponible / total < 20%|
|8|Tasa de renovaciones|RENOVADOS / TOTAL × 100|
