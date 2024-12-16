-- Crear la base de datos si no existe
CREATE DATABASE task_list;

-- Conectar a la base de datos
\c task_list

-- Tabla para las listas
CREATE TABLE list (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla para las tareas
CREATE TABLE task (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    list_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (list_id) REFERENCES list(id) ON DELETE CASCADE
);

-- Insertar datos de prueba en la tabla list
INSERT INTO list (name, description) VALUES
    ('Lista de Compras', 'Artículos para comprar esta semana'),
    ('Tareas del Hogar', 'Pendientes de la casa'),
    ('Proyecto Web', 'Tareas del desarrollo web');

-- Insertar datos de prueba en la tabla task
INSERT INTO task (title, description, completed, list_id) VALUES
    ('Comprar leche', 'Leche deslactosada 1L', false, 1),
    ('Comprar pan', 'Pan integral', false, 1),
    ('Limpiar cocina', 'Limpiar y ordenar la cocina', false, 2),
    ('Lavar ropa', 'Lavar ropa de color', true, 2),
    ('Crear API', 'Desarrollar endpoints REST', false, 3),
    ('Testing', 'Realizar pruebas unitarias', false, 3);
