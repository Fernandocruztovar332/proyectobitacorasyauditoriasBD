--bdescolv2.sql
CREATE DATABASE ESCOOL		;

USE ESCOOL

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
    idmateria INT PRIMARY KEY identity not null,
    nombreM VARCHAR(50) NOT NULL,
    horasP VARCHAR(10) NOT NULL,
    horasT VARCHAR(10) NOT NULL,
    creditos INT NOT NULL
);


use ESCOOL



CREATE TABLE cursan (
    calif INT NOT NULL,
    oportunidad VARCHAR(20) NOT NULL,
    NoControl CHAR(8) NOT NULL REFERENCES Estudiante(NoControl),
    idmateria INT NOT NULL REFERENCES materia(idmateria),
    PRIMARY KEY (NoControl, idmateria) -- Clave primaria compuesta
);


CREATE TABLE Historial (
    idHistorial int PRIMARY KEY identity not null,
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



-- Insertar datos en la tabla Estudiante
INSERT INTO Estudiante VALUES ('22660256', 'Juan', 'P�rez', 'G�mez', '1', 'Ingenieria en Sistemas');
INSERT INTO Estudiante VALUES ('22660277', 'Mar�a', 'L�pez', 'Hern�ndez', '3', 'Ingenieria Industrial');
INSERT INTO Estudiante VALUES ('22660137', 'Pedro', 'Mart�nez', 'Torres', '7', 'Gestion Empresarial');
INSERT INTO Estudiante VALUES ('22660198', 'Laura', 'Gonz�lez', 'Ram�rez', '5', 'Contador Publico');
INSERT INTO Estudiante VALUES ('22660145', 'Ana', 'Hern�ndez', 'Mora', '1', 'Ingenier�a Civil');

-- Insertar datos en la tabla datosPA
INSERT INTO datosPA VALUES ('O+', '4881234567', 'juan@gmail.com', 'Las Flores', 'Encino', '101', '22660256');
INSERT INTO datosPA VALUES ('A-', '4887766555', 'maria@gmail.com', 'Los Pinos', 'Cedro', '202', '22660277');
INSERT INTO datosPA VALUES ('B+', '4882345678', 'pedro@gmail.com', 'La Esperanza', 'Roble', '303', '22660137');
INSERT INTO datosPA VALUES ('AB-', '4889876543', 'laura@gmail.com', 'El Sol', 'Olmo', '404', '22660198');
INSERT INTO datosPA VALUES ('O-', '4886543210', 'ana@gmail.com', 'San Pedro', 'Fresno', '505', '22660145');

-- Insertar datos en la tabla materia
INSERT INTO materia VALUES ( 'Programacion Orientada a Objetos', '4', '3', 7);
INSERT INTO materia VALUES ( 'Sistemas Operativos', '3', '2', 5);
INSERT INTO materia VALUES ( 'Taller de Bases de Datos', '4', '3', 6);
INSERT INTO materia VALUES ( 'Redes de Computadoras', '3', '2', 5);
INSERT INTO materia VALUES ( 'Calculo Diferencial', '4', '3', 6);

-- Insertar datos en la tabla cursa
INSERT INTO cursan VALUES (90, 'Primera', '22660256',1);
INSERT INTO cursan VALUES (85, 'Primera', '22660277',2);
INSERT INTO cursan VALUES (88, 'Segunda', '22660137',3 );
INSERT INTO cursan VALUES (92, 'Primera', '22660198',4);
INSERT INTO cursan VALUES (75, 'Primera', '22660145',2);

-- Insertar datos en la tabla Historial
INSERT INTO Historial VALUES ( '22660256', 'Juan', 'P�rez', 'G�mez', 'Ingenier�a en Sistemas', '1', '4', '3', 90, 'Primera');
INSERT INTO Historial VALUES ( '22660277', 'Mar�a', 'L�pez', 'Hern�ndez', 'Ingenieria Industrial', '3', '3', '2', 85, 'Primera');
INSERT INTO Historial VALUES ( '22660137', 'Pedro', 'Mart�nez', 'Torres', 'Gestion Empresarial', '2', '4', '2', 88, 'Segunda');
INSERT INTO Historial VALUES ( '22660198', 'Laura', 'Gonz�lez', 'Ram�rez', 'Contador Publico', '4', '2', '2', 92, 'Primera');
INSERT INTO Historial VALUES ('22660198', 'Ana', 'Hern�ndez', 'Mora', 'Ingenier�a Civil', '1', '3', '1', 75, 'Primera');
GO
CREATE TRIGGER Trigger_VerificarCrearEstudiante
ON Estudiante
INSTEAD OF INSERT
AS
BEGIN
    IF EXISTS (SELECT 1 FROM Estudiante WHERE NoControl = (SELECT NoControl FROM inserted))
    BEGIN
        PRINT 'El estudiante ya existe. Operaci�n cancelada.';
    END
    ELSE
    BEGIN
        INSERT INTO Estudiante (NoControl, nombre, apP, apM, semestre, carrera)
        SELECT NoControl, nombre, apP, apM, semestre, carrera FROM inserted;
        PRINT 'Estudiante creado exitosamente.';
    END
END;
GO

CREATE TRIGGER Trigger_EliminarCursaMateria
ON materia
AFTER DELETE
AS
BEGIN
    DELETE FROM cursan WHERE idmateria IN (SELECT idmateria FROM deleted);
    PRINT 'Registros de cursa asociados a las materias eliminadas han sido borrados.';
END;
GO

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
LEFT JOIN cursan c
ON e.NoControl = c.NoControl;
GO

CREATE TRIGGER trg_InsertarEstudiante
ON Estudiante
AFTER INSERT
AS
BEGIN
    -- Aseguramos que solo se ejecuta si hay datos nuevos en la tabla 'inserted'
    INSERT INTO cursan(NoControl, calif, oportunidad, idmateria)
    SELECT NoControl, 0, 'Primera', NULL
    FROM inserted; -- inserted contiene los datos del registro reci�n insertado
END;
GO

CREATE TRIGGER trg_ActualizarEstudiante
ON Estudiante
AFTER UPDATE
AS
BEGIN
    UPDATE cursan
    SET idmateria = cursan.idmateria  -- Puedes ajustar las columnas que quieres sincronizar
    FROM cursan
    INNER JOIN inserted ON cursan.NoControl = inserted.NoControl;
END;
GO

CREATE TRIGGER trg_EliminarEstudiante
ON Estudiante
AFTER DELETE
AS
BEGIN
    DELETE FROM cursan
    WHERE NoControl IN (SELECT NoControl FROM deleted); -- deleted contiene las filas eliminadas
END;
GO

CREATE OR ALTER TRIGGER trg_InsertarEstudiante
ON Estudiante
AFTER INSERT
AS
BEGIN
    -- Inserta un registro en 'cursan' con una materia predeterminada
    DECLARE @idmateria INT = (SELECT TOP 1 idmateria FROM materia ORDER BY idmateria);

    IF @idmateria IS NOT NULL
    BEGIN
        INSERT INTO cursan (NoControl, calif, oportunidad, idmateria)
        SELECT NoControl, 0, 'Primera', @idmateria
        FROM inserted;
    END
    ELSE
    BEGIN
        PRINT 'No se encontr� ninguna materia predeterminada.';
    END
END;
GO


CREATE OR ALTER TRIGGER trg_ActualizarEstudiante
ON Estudiante
AFTER UPDATE
AS
BEGIN
    -- Actualiza la informaci�n en la tabla 'cursan' basada en el NoControl
    UPDATE c
    SET 
        c.calif = c.calif,  -- Puedes agregar m�s l�gica si es necesario
        c.oportunidad = c.oportunidad
    FROM cursan c
    INNER JOIN inserted i ON c.NoControl = i.NoControl;
END;
GO


CREATE OR ALTER TRIGGER trg_EliminarEstudiante
ON Estudiante
AFTER DELETE
AS
BEGIN
    -- Borra los registros relacionados en la tabla 'cursan'
    DELETE FROM cursan
    WHERE NoControl IN (SELECT NoControl FROM deleted);
END;
GO

ALTER TABLE datosPA
DROP CONSTRAINT FK_datosPA_NoControl;

ALTER TABLE datosPA
ADD CONSTRAINT FK_datosPA_NoControl
FOREIGN KEY (NoControl) REFERENCES Estudiante(NoControl)
ON DELETE CASCADE;
 
GO

CREATE OR ALTER TRIGGER trg_EliminarEstudiante
ON Estudiante
AFTER DELETE
AS
BEGIN
    BEGIN TRY
        BEGIN TRANSACTION;

        -- Eliminar registros relacionados en la tabla datosPA
        DELETE FROM datosPA
        WHERE NoControl IN (SELECT NoControl FROM deleted);

        -- Inserta en la tabla Historial los datos del estudiante eliminado junto con las materias cursadas
        INSERT INTO Historial (NoControl, nombre, apP, apM, carrera, semestre, horasP, horasT, calif, oportunidad)
        SELECT 
            d.NoControl, 
            d.nombre, 
            d.apP, 
            d.apM, 
            d.carrera, 
            d.semestre, 
            m.horasP, 
            m.horasT, 
            c.calif, 
            c.oportunidad
        FROM deleted d
        LEFT JOIN cursan c ON d.NoControl = c.NoControl
        LEFT JOIN materia m ON c.idmateria = m.idmateria;

        -- Eliminar registros relacionados en la tabla cursan
        DELETE FROM cursan
        WHERE NoControl IN (SELECT NoControl FROM deleted);

        -- Confirmar la transacci�n
        COMMIT TRANSACTION;

        PRINT 'Datos eliminados correctamente e insertados en Historial.';
    END TRY
    BEGIN CATCH
        -- Revertir la transacci�n en caso de error
        ROLLBACK TRANSACTION;

        -- Lanzar el error para depuraci�n
        THROW;
    END CATCH
END;



GO



use ESCOOL

CREATE PROCEDURE sp_InsertarEstudiante
    @NoControl CHAR(8),
    @nombre VARCHAR(50),
    @apP VARCHAR(50),
    @apM VARCHAR(50),
    @semestre VARCHAR(8),
    @carrera VARCHAR(80)
AS
BEGIN
    BEGIN TRY
        INSERT INTO Estudiante (NoControl, nombre, apP, apM, semestre, carrera)
        VALUES (@NoControl, @nombre, @apP, @apM, @semestre, @carrera);
    END TRY
    BEGIN CATCH
        THROW;
    END CATCH
END;

EXEC sp_help 'sp_InsertarEstudiante';

CREATE PROCEDURE sp_ConsultarEstudiante
    @NoControl CHAR(8)
AS
BEGIN
    SELECT *
    FROM vw_EstudianteCompleto
    WHERE NoControl = @NoControl;
END;



CREATe PROCEDURE sp_RegistrarCalificacion
    @calif INT,
    @oportunidad VARCHAR(20),
    @NoControl CHAR(8),
    @idmateria INT
AS
BEGIN
    BEGIN TRY
        INSERT INTO cursan (calif, oportunidad, NoControl, idmateria)
        VALUES (@calif, @oportunidad, @NoControl, @idmateria);
    END TRY
    BEGIN CATCH
        THROW;
    END CATCH
END;


CREATE PROCEDURE sp_ActualizarEstudiante
    @NoControl CHAR(8),
    @nombre VARCHAR(50),
    @apP VARCHAR(50),
    @apM VARCHAR(50),
    @semestre VARCHAR(8),
    @carrera VARCHAR(80),
    @calif INT,
    @oportunidad VARCHAR(20),
    @idmateria INT
AS
BEGIN
    BEGIN TRY
        -- Actualizar informaci�n del estudiante
        UPDATE Estudiante
        SET nombre = @nombre,
            apP = @apP,
            apM = @apM,
            semestre = @semestre,
            carrera = @carrera
        WHERE NoControl = @NoControl;

        -- Actualizar la tabla cursan
        UPDATE cursan
        SET calif = @calif,
            oportunidad = @oportunidad,
            idmateria = @idmateria
        WHERE NoControl = @NoControl;
    END TRY
    BEGIN CATCH
        THROW;
    END CATCH
END;



CREATE PROCEDURE sp_EliminarEstudiante
    @NoControl CHAR(8)
AS
BEGIN
    BEGIN TRY
        -- Eliminar registros relacionados en la tabla cursan
        DELETE FROM cursan
        WHERE NoControl = @NoControl;

        -- Eliminar el estudiante
        DELETE FROM Estudiante
        WHERE NoControl = @NoControl;
    END TRY
    BEGIN CATCH
        THROW;
    END CATCH
END;



CREATE PROCEDURE sp_EliminarMateriasRelacionadas
    @idmateria INT
AS
BEGIN
    BEGIN TRY
        DELETE FROM cursan
        WHERE idmateria = @idmateria;

        DELETE FROM materia
        WHERE idmateria = @idmateria;
    END TRY
    BEGIN CATCH
        THROW;
    END CATCH
END;


CREATE PROCEDURE sp_ListarMateriasEstudiantes
AS
BEGIN
    SELECT 
        m.idmateria,
        m.nombreM AS Materia,
        e.NoControl,
        e.nombre AS Estudiante,
        c.calif,
        c.oportunidad
    FROM materia m
    INNER JOIN cursan c ON m.idmateria = c.idmateria
    INNER JOIN Estudiante e ON c.NoControl = e.NoControl;
END;


CREATE or alter PROCEDURE sp_InsertarEstudiante
    @NoControl CHAR(8),
    @nombre VARCHAR(50),
    @apP VARCHAR(50),
    @apM VARCHAR(50),
    @semestre VARCHAR(8),
    @carrera VARCHAR(80),
    @calif INT,                  -- Nueva entrada: calificaci�n
    @oportunidad VARCHAR(20),  -- Nueva entrada: oportunidad (por ejemplo, "Primera", "Segunda")
    @idmateria INT          -- Nueva entrada: id de la materia
AS
BEGIN
    BEGIN TRY
        -- Inicia una transacci�n para asegurar consistencia
        BEGIN TRANSACTION;

        -- Insertar el estudiante en la tabla Estudiante
        INSERT INTO Estudiante (NoControl, nombre, apP, apM, semestre, carrera)
        VALUES (@NoControl, @nombre, @apP, @apM, @semestre, @carrera);

        -- Insertar el registro en la tabla cursan
        INSERT INTO cursan (calif, oportunidad, NoControl, idmateria)
        VALUES (@calif, @oportunidad, @NoControl,@idmateria);

        -- Confirma la transacci�n si ambas operaciones son exitosas
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        -- En caso de error, deshacer la transacci�n
        ROLLBACK TRANSACTION;

        -- Lanzar el error para manejo externo
        THROW;
    END CATCH
END;
use ESCOOL
DROP TRIGGER trg_InsertarEstudiante;

CREATE OR ALTER PROCEDURE sp_InsertarEstudiante
    @NoControl CHAR(8),
    @nombre VARCHAR(50),
    @apP VARCHAR(50),
    @apM VARCHAR(50),
    @semestre VARCHAR(8),
    @carrera VARCHAR(80),
    @calif INT,
    @oportunidad VARCHAR(20),
    @idmateria INT
AS
BEGIN
    BEGIN TRY
        BEGIN TRANSACTION;

        -- Insertar en la tabla Estudiante
        INSERT INTO Estudiante (NoControl, nombre, apP, apM, semestre, carrera)
        VALUES (@NoControl, @nombre, @apP, @apM, @semestre, @carrera);

        -- Insertar en la tabla cursan
        INSERT INTO cursan (NoControl, calif, oportunidad, idmateria)
        VALUES (@NoControl, @calif, @oportunidad, @idmateria);

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;


CREATE OR ALTER PROCEDURE sp_ListarMateriasEstudiantes
    @NoControl CHAR(8)
AS
BEGIN
    SELECT 
        m.idmateria,
        m.nombreM AS Materia,
        c.oportunidad,
        c.calif
    FROM materia m
    INNER JOIN cursan c ON m.idmateria = c.idmateria
    WHERE c.NoControl = @NoControl;
END;

SELECT 
    OBJECT_NAME(fk.constraint_object_id) AS ConstraintName,
    t.name AS TableName,
    c.name AS ColumnName,
    ref.name AS ReferencedTableName
FROM 
    sys.foreign_key_columns fk
INNER JOIN sys.tables t ON fk.parent_object_id = t.object_id
INNER JOIN sys.columns c ON fk.parent_object_id = c.object_id AND fk.parent_column_id = c.column_id
INNER JOIN sys.tables ref ON fk.referenced_object_id = ref.object_id
WHERE t.name = 'datosPA';

ALTER TABLE datosPA
DROP CONSTRAINT FK__datosPA__NoContr__4AB81AF0;

ALTER TABLE datosPA
ADD CONSTRAINT FK_datosPA_NoControl
FOREIGN KEY (NoControl) REFERENCES Estudiante(NoControl)
ON DELETE CASCADE;

DELETE FROM Estudiante WHERE NoControl = '22660277';

SELECT 
    OBJECT_NAME(fk.constraint_object_id) AS ConstraintName,
    t.name AS TableName,
    c.name AS ColumnName,
    ref.name AS ReferencedTableName
FROM 
    sys.foreign_key_columns fk
INNER JOIN sys.tables t ON fk.parent_object_id = t.object_id
INNER JOIN sys.columns c ON fk.parent_object_id = c.object_id AND fk.parent_column_id = c.column_id
INNER JOIN sys.tables ref ON fk.referenced_object_id = ref.object_id
WHERE t.name = 'cursan';


DECLARE @sql NVARCHAR(MAX) = '';

SELECT @sql += 'ALTER TABLE ' + QUOTENAME(OBJECT_NAME(parent_object_id)) +
               ' DROP CONSTRAINT ' + QUOTENAME(name) + ';'
FROM sys.foreign_keys
WHERE parent_object_id = OBJECT_ID('cursan');

EXEC sp_executesql @sql;

ALTER TABLE cursan
ADD CONSTRAINT FK_cursan_NoControl
FOREIGN KEY (NoControl) REFERENCES Estudiante(NoControl)
ON DELETE CASCADE;

DELETE FROM Estudiante WHERE NoControl = '22660277';


ALTER TABLE cursan
DROP CONSTRAINT FK__cursan__NoControl__6198B048;

ALTER TABLE cursan
ADD CONSTRAINT FK_cursan_Estudiante
FOREIGN KEY (NoControl) REFERENCES Estudiante(NoControl)
ON DELETE NO ACTION;

SELECT 
    OBJECT_NAME(fk.constraint_object_id) AS ConstraintName,
    t.name AS TableName,
    c.name AS ColumnName,
    ref.name AS ReferencedTableName
FROM 
    sys.foreign_key_columns fk
INNER JOIN sys.tables t ON fk.parent_object_id = t.object_id
INNER JOIN sys.columns c ON fk.parent_object_id = c.object_id AND fk.parent_column_id = c.column_id
INNER JOIN sys.tables ref ON fk.referenced_object_id = ref.object_id
WHERE t.name = 'cursan';

ALTER TABLE cursan
DROP CONSTRAINT FK_cursan_Estudiante;

ALTER TABLE cursan
DROP CONSTRAINT FK_cursan_NoControl;


ALTER TABLE cursan
ADD CONSTRAINT FK_cursan_NoControl
FOREIGN KEY (NoControl) REFERENCES Estudiante(NoControl)
ON DELETE CASCADE;


ALTER TABLE cursan
ADD CONSTRAINT FK_cursan_Materia
FOREIGN KEY (idmateria) REFERENCES materia(idmateria)
ON DELETE CASCADE;

SELECT 
    OBJECT_NAME(fk.constraint_object_id) AS ConstraintName,
    t.name AS TableName,
    c.name AS ColumnName,
    ref.name AS ReferencedTableName
FROM 
    sys.foreign_key_columns fk
INNER JOIN sys.tables t ON fk.parent_object_id = t.object_id
INNER JOIN sys.columns c ON fk.parent_object_id = c.object_id AND fk.parent_column_id = c.column_id
INNER JOIN sys.tables ref ON fk.referenced_object_id = ref.object_id
WHERE t.name = 'cursan';


DELETE FROM Estudiante WHERE NoControl = '22660277';

GO

CREATE OR ALTER TRIGGER trg_EliminarEstudiante
ON Estudiante
AFTER DELETE
AS
BEGIN
    BEGIN TRY
        BEGIN TRANSACTION;

        -- Eliminar registros relacionados en la tabla cursan
        DELETE FROM cursan
        WHERE NoControl IN (SELECT NoControl FROM deleted);

        -- Eliminar registros relacionados en la tabla datosPA
        DELETE FROM datosPA
        WHERE NoControl IN (SELECT NoControl FROM deleted);

        -- Insertar en la tabla Historial
        INSERT INTO Historial (NoControl, nombre, apP, apM, carrera, semestre, horasP, horasT, calif, oportunidad)
        SELECT 
            d.NoControl, 
            d.nombre, 
            d.apP, 
            d.apM, 
            d.carrera, 
            d.semestre, 
            ISNULL(m.horasP, 0), -- Asignar 0 si horasP es NULL
            ISNULL(m.horasT, 0), -- Asignar 0 si horasT es NULL
            ISNULL(c.calif, 0),  -- Asignar 0 si calif es NULL
            ISNULL(c.oportunidad, 'No Aplica') -- Asignar 'No Aplica' si oportunidad es NULL
        FROM deleted d
        LEFT JOIN cursan c ON d.NoControl = c.NoControl
        LEFT JOIN materia m ON c.idmateria = m.idmateria;

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;


DELETE FROM Estudiante WHERE NoControl = '22660277';

SELECT * FROM Historial WHERE NoControl = '22660277';











