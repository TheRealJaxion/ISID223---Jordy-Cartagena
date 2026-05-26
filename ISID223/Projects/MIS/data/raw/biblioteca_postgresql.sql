-- ============================================================
-- Base de datos: biblioteca
-- Motor: PostgreSQL (compatible con WSL2)
-- Convertido desde: MariaDB / phpMyAdmin dump
-- ============================================================

-- 1. Crear la base de datos (ejecutar como superusuario, fuera del script)
-- CREATE DATABASE biblioteca;
-- \c biblioteca

-- ============================================================
-- EXTENSIONES (opcional pero recomendado)
-- ============================================================
-- CREATE EXTENSION IF NOT EXISTS "pgcrypto"; -- Para hashing de contraseñas futuro

-- ============================================================
-- TABLA: libros
-- ============================================================
CREATE TABLE libros (
    id_libro        SERIAL          PRIMARY KEY,
    isbn            VARCHAR(20)     NOT NULL UNIQUE,
    titulo          VARCHAR(200)    NOT NULL,
    autor           VARCHAR(100)    NOT NULL,
    editorial       VARCHAR(100)    NOT NULL,
    anio            INTEGER         NOT NULL CHECK (anio > 0),
    categoria       VARCHAR(50)     NOT NULL,
    cantidad_total  INTEGER         NOT NULL CHECK (cantidad_total >= 0),
    cantidad_disponible INTEGER     NOT NULL CHECK (cantidad_disponible >= 0),
    ubicacion       VARCHAR(50)     NOT NULL,
    activo          BOOLEAN         NOT NULL DEFAULT TRUE,

    CONSTRAINT chk_cantidad CHECK (cantidad_disponible <= cantidad_total)
);

-- ============================================================
-- TABLA: personas
-- ============================================================
CREATE TABLE personas (
    id_persona  SERIAL          PRIMARY KEY,
    cedula      VARCHAR(10)     NOT NULL UNIQUE,
    nombre      VARCHAR(100)    NOT NULL,
    apellido    VARCHAR(100)    NOT NULL,
    email       VARCHAR(100)    NOT NULL UNIQUE,
    direccion   VARCHAR(200)    NOT NULL,
    tipo        VARCHAR(20)     NOT NULL CHECK (tipo IN ('estudiante', 'docente', 'bibliotecario', 'admin')),
    usuario     VARCHAR(50)     NOT NULL UNIQUE,
    contrasena  VARCHAR(255)    NOT NULL,   -- Aumentado a 255 para hashes bcrypt/argon2
    activo      BOOLEAN         NOT NULL DEFAULT TRUE
);

-- ============================================================
-- TABLA: prestamos
-- ============================================================
CREATE TABLE prestamos (
    id_prestamo                 SERIAL      PRIMARY KEY,
    fecha_prestamo              DATE        NOT NULL DEFAULT CURRENT_DATE,
    fecha_devolucion_esperada   DATE        NOT NULL,
    fecha_devolucion_real       DATE,                   -- NULL si aún no fue devuelto
    estado                      VARCHAR(20) NOT NULL DEFAULT 'activo'
                                    CHECK (estado IN ('activo', 'devuelto', 'vencido', 'renovado')),
    id_usuario                  INTEGER     NOT NULL,
    id_libro                    INTEGER     NOT NULL,

    CONSTRAINT fk_usuario FOREIGN KEY (id_usuario) REFERENCES personas (id_persona)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_libro   FOREIGN KEY (id_libro)   REFERENCES libros   (id_libro)
        ON DELETE RESTRICT ON UPDATE CASCADE,

    CONSTRAINT chk_fechas CHECK (fecha_devolucion_esperada > fecha_prestamo)
);

-- ============================================================
-- ÍNDICES adicionales para rendimiento
-- ============================================================
CREATE INDEX idx_prestamos_usuario ON prestamos (id_usuario);
CREATE INDEX idx_prestamos_libro   ON prestamos (id_libro);
CREATE INDEX idx_prestamos_estado  ON prestamos (estado);
CREATE INDEX idx_libros_categoria  ON libros    (categoria);
CREATE INDEX idx_personas_tipo     ON personas  (tipo);

-- ============================================================
-- DATOS INICIALES: libros
-- ============================================================
INSERT INTO libros (isbn, titulo, autor, editorial, anio, categoria, cantidad_total, cantidad_disponible, ubicacion, activo) VALUES
('978000000001', 'Introducción a la Programación',   'Juan Pérez',      'Editorial Alfa',  2018, 'Informática',    10, 7,  'Estante A1', TRUE),
('978000000002', 'Estructuras de Datos',             'María Gómez',     'Editorial Beta',  2019, 'Informática',    8,  5,  'Estante A2', TRUE),
('978000000003', 'Bases de Datos Relacionales',      'Carlos López',    'Editorial Gamma', 2020, 'Bases de Datos', 12, 10, 'Estante B1', TRUE),
('978000000004', 'Ingeniería de Software',           'Ana Torres',      'Editorial Delta', 2017, 'Software',       6,  4,  'Estante B2', TRUE),
('978000000005', 'Redes de Computadoras',            'Luis Martínez',   'Editorial Omega', 2016, 'Redes',          9,  6,  'Estante C1', TRUE),
('978000000006', 'Sistemas Operativos',              'Pedro Ramírez',   'Editorial Alfa',  2019, 'Informática',    7,  3,  'Estante C2', TRUE),
('978000000007', 'Programación en Java',             'Laura Sánchez',   'Editorial Beta',  2021, 'Programación',   15, 12, 'Estante D1', TRUE),
('978000000008', 'Programación en Python',           'Miguel Herrera',  'Editorial Gamma', 2022, 'Programación',   14, 11, 'Estante D2', TRUE),
('978000000009', 'Algoritmos y Complejidad',         'Sofía Castro',    'Editorial Delta', 2018, 'Algoritmos',     5,  2,  'Estante E1', TRUE),
('978000000010', 'Matemáticas Discretas',            'Andrés Vega',     'Editorial Omega', 2017, 'Matemática',     10, 8,  'Estante E2', TRUE),
('978000000011', 'Inteligencia Artificial Básica',   'Daniel Ruiz',     'Editorial Alfa',  2020, 'IA',             6,  6,  'Estante F1', TRUE),
('978000000012', 'Introducción al Machine Learning', 'Paula Moreno',    'Editorial Beta',  2021, 'IA',             4,  3,  'Estante F2', TRUE),
('978000000013', 'Seguridad Informática',            'Ricardo León',    'Editorial Gamma', 2019, 'Seguridad',      8,  5,  'Estante G1', TRUE),
('978000000014', 'Criptografía Aplicada',            'Valentina Cruz',  'Editorial Delta', 2020, 'Seguridad',      3,  2,  'Estante G2', TRUE),
('978000000015', 'Desarrollo Web HTML y CSS',        'Fernando Díaz',   'Editorial Omega', 2018, 'Web',            12, 9,  'Estante H1', TRUE),
('978000000016', 'JavaScript Moderno',               'Camila Ortiz',    'Editorial Alfa',  2021, 'Web',            11, 7,  'Estante H2', TRUE),
('978000000017', 'Frameworks Backend',               'Jorge Silva',     'Editorial Beta',  2022, 'Software',       6,  6,  'Estante I1', TRUE),
('978000000018', 'Bases de Datos NoSQL',             'Natalia Flores',  'Editorial Gamma', 2020, 'Bases de Datos', 5,  4,  'Estante I2', TRUE),
('978000000019', 'Análisis de Sistemas',             'Héctor Molina',   'Editorial Delta', 2017, 'Software',       9,  5,  'Estante J1', TRUE),
('978000000020', 'Metodologías Ágiles',              'Patricia Ríos',   'Editorial Omega', 2019, 'Gestión',        7,  6,  'Estante J2', TRUE);
