CREATE DATABASE SCHOOL;

USE SCHOOL

CREATE TABLE Estudiante (
    NoControl CHAR(8) PRIMARY KEY CLUSTERED,
    nombre VARCHAR(50) NOT NULL,
    apP VARCHAR(50) NOT NULL,
    apM VARCHAR(50) NOT NULL,
    semestre VARCHAR(8) NOT NULL,
    carrera VARCHAR(80) NOT NULL
);

CREATE TABLE datosPA (
    tipoS VARCHAR(8) NOT NULL,
    numeroT VARCHAR(15) NOT NULL,
    correoE VARCHAR(15) NOT NULL,
    colonia VARCHAR(30) NOT NULL,
    calle VARCHAR(20) NOT NULL,
    numero VARCHAR(6) NOT NULL,
    NoControl CHAR(8) NOT NULL REFERENCES Estudiante(NoControl)
);

CREATE TABLE materia (
    idmateria CHAR(3) PRIMARY KEY CLUSTERED,
    nombreM VARCHAR(50) NOT NULL,
    horasP VARCHAR(10) NOT NULL,
    horasT VARCHAR(10) NOT NULL,
    creditos INT NOT NULL
);
USE master

drop database SCHOOL

CREATE TABLE cursa (
    calif INT NOT NULL,
    oportunidad VARCHAR(20) NOT NULL,
    NoControl CHAR(8) NOT NULL REFERENCES Estudiante(NoControl),
    idmateria CHAR(3) NOT NULL REFERENCES materia(idmateria)
);

CREATE TABLE Historial (
    idHistorial CHAR(3) PRIMARY KEY CLUSTERED,
    NoControl CHAR(8) NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    apP VARCHAR(50) NOT NULL,
    apM VARCHAR(50) NOT NULL,
    carrera VARCHAR(80) NOT NULL,
    semestre VARCHAR(8) NOT NULL,
    horasP VARCHAR(10) NOT NULL,
    horasT VARCHAR(10) NOT NULL,
    calif INT NOT NULL,
    oportunidad VARCHAR(20) NOT NULL
);

use SCHOOL

-- Insertar datos en la tabla Estudiante
INSERT INTO Estudiante VALUES ('22660256', 'Juan', 'Pérez', 'Gómez', '1', 'Ingenieria en Sistemas');
INSERT INTO Estudiante VALUES ('22660277', 'María', 'López', 'Hernández', '3', 'Ingenieria Industrial');
INSERT INTO Estudiante VALUES ('22660137', 'Pedro', 'Martínez', 'Torres', '7', 'Gestion Empresarial');
INSERT INTO Estudiante VALUES ('22660198', 'Laura', 'González', 'Ramírez', '5', 'Contador Publico');
INSERT INTO Estudiante VALUES ('22660145', 'Ana', 'Hernández', 'Mora', '1', 'Ingeniería Civil');

-- Insertar datos en la tabla datosPA
INSERT INTO datosPA VALUES ('O+', '4881234567', 'juan@gmail.com', 'Las Flores', 'Encino', '101', '22660256');
INSERT INTO datosPA VALUES ('A-', '4887766555', 'maria@gmail.com', 'Los Pinos', 'Cedro', '202', '22660277');
INSERT INTO datosPA VALUES ('B+', '4882345678', 'pedro@gmail.com', 'La Esperanza', 'Roble', '303', '22660137');
INSERT INTO datosPA VALUES ('AB-', '4889876543', 'laura@gmail.com', 'El Sol', 'Olmo', '404', '22660198');
INSERT INTO datosPA VALUES ('O-', '4886543210', 'ana@gmail.com', 'San Pedro', 'Fresno', '505', '22660145');

-- Insertar datos en la tabla materia
INSERT INTO materia VALUES ('POO', 'Programacion Orientada a Objetos', '4', '3', 7);
INSERT INTO materia VALUES ('SO', 'Sistemas Operativos', '3', '2', 5);
INSERT INTO materia VALUES ('TBD', 'Taller de Bases de Datos', '4', '3', 6);
INSERT INTO materia VALUES ('RDC', 'Redes de Computadoras', '3', '2', 5);
INSERT INTO materia VALUES ('CDL', 'Calculo Diferencial', '4', '3', 6);

-- Insertar datos en la tabla cursa
INSERT INTO cursa VALUES (90, 'Primera', '22660256', 'POO');
INSERT INTO cursa VALUES (85, 'Primera', '22660277', 'SO');
INSERT INTO cursa VALUES (88, 'Segunda', '22660137', 'TBD');
INSERT INTO cursa VALUES (92, 'Primera', '22660198', 'RDC');
INSERT INTO cursa VALUES (75, 'Primera', '22660145', 'CDL');

-- Insertar datos en la tabla Historial
INSERT INTO Historial VALUES ('H01', '22660256', 'Juan', 'Pérez', 'Gómez', 'Ingeniería en Sistemas', '1', '4', '3', 90, 'Primera');
INSERT INTO Historial VALUES ('H02', '22660277', 'María', 'López', 'Hernández', 'Ingenieria Industrial', '3', '3', '2', 85, 'Primera');
INSERT INTO Historial VALUES ('H03', '22660137', 'Pedro', 'Martínez', 'Torres', 'Gestion Empresarial', '2', '4', '2', 88, 'Segunda');
INSERT INTO Historial VALUES ('H04', '22660198', 'Laura', 'González', 'Ramírez', 'Contador Publico', '4', '2', '2', 92, 'Primera');
INSERT INTO Historial VALUES ('H05', '22660198', 'Ana', 'Hernández', 'Mora', 'Ingeniería Civil', '1', '3', '1', 75, 'Primera');


CREATE TRIGGER Trigger_VerificarCrearEstudiante
ON Estudiante
INSTEAD OF INSERT
AS
BEGIN
    IF EXISTS (SELECT 1 FROM Estudiante WHERE NoControl = (SELECT NoControl FROM inserted))
    BEGIN
        PRINT 'El estudiante ya existe. Operación cancelada.';
    END
    ELSE
    BEGIN
        INSERT INTO Estudiante (NoControl, nombre, apP, apM, semestre, carrera)
        SELECT NoControl, nombre, apP, apM, semestre, carrera FROM inserted;
        PRINT 'Estudiante creado exitosamente.';
    END
END;
CREATE TRIGGER Trigger_EliminarCursaMateria
ON materia
AFTER DELETE
AS
BEGIN
    DELETE FROM cursa WHERE idmateria IN (SELECT idmateria FROM deleted);
    PRINT 'Registros de cursa asociados a las materias eliminadas han sido borrados.';
END;


CREATE VIEW vw_EstudianteCompleto AS
SELECT 
    e.NoControl,
    e.nombre,
    e.apP,
    e.apM,
    e.semestre,
    e.carrera,
    c.calif,
    c.oportunidad,
    c.idmateria
FROM Estudiante e
LEFT JOIN cursa c
ON e.NoControl = c.NoControl;





CREATE TRIGGER trg_InsertarEstudiante
ON Estudiante
AFTER INSERT
AS
BEGIN
    -- Aseguramos que solo se ejecuta si hay datos nuevos en la tabla 'inserted'
    INSERT INTO cursa (NoControl, calif, oportunidad, idmateria)
    SELECT NoControl, 0, 'Primera', NULL
    FROM inserted; -- inserted contiene los datos del registro recién insertado
END;


CREATE TRIGGER trg_ActualizarEstudiante
ON Estudiante
AFTER UPDATE
AS
BEGIN
    UPDATE cursa
    SET idmateria = cursa.idmateria  -- Puedes ajustar las columnas que quieres sincronizar
    FROM cursa
    INNER JOIN inserted ON cursa.NoControl = inserted.NoControl;
END;


CREATE TRIGGER trg_EliminarEstudiante
ON Estudiante
AFTER DELETE
AS
BEGIN
    DELETE FROM cursa
    WHERE NoControl IN (SELECT NoControl FROM deleted); -- deleted contiene las filas eliminadas
END;
