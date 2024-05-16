CREATE TABLE pensionados (
    id SERIAL PRIMARY KEY,
    ci VARCHAR(20) UNIQUE NOT NULL,
    nombre_apellido VARCHAR(100),
    departamento VARCHAR(100),
    distrito VARCHAR(100)
);

CREATE TABLE pensionados_regulares (
    id SERIAL PRIMARY KEY,
    pensionado_id INTEGER REFERENCES pensionados(id),
    sexo VARCHAR(10),
    estado VARCHAR(50),
    fecha_ingreso DATE,
    com_indigena BOOLEAN
);

CREATE TABLE pensionados_honorificos (
    id SERIAL PRIMARY KEY,
    pensionado_id INTEGER REFERENCES pensionados(id),
    concepto_pension VARCHAR(100),
    fecha_ingreso DATE,
    monto_pension DECIMAL(10, 2)
);

CREATE TABLE pensionados_en_proceso (
    id SERIAL PRIMARY KEY,
    pensionado_id INTEGER REFERENCES pensionados(id),
    documentacion_faltante BOOLEAN
);

CREATE TABLE pensionados_candidatos (
    id SERIAL PRIMARY KEY,
    pensionado_id INTEGER REFERENCES pensionados(id),
    año_censo INTEGER,
    institucion VARCHAR(100),
    situacion VARCHAR(50)
);
