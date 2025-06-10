use ESCOOL

CREATE TABLE Usuarios (
    idUsuario INT IDENTITY PRIMARY KEY,
    nombreUsuario VARCHAR(50) NOT NULL,
    contrasena VARCHAR(100) NOT NULL,
    tipoUsuario VARCHAR(20) NOT NULL CHECK (tipoUsuario IN ('admin', 'normal', 'auditor'))
);

CREATE OR ALTER PROCEDURE sp_InsertarEstudianteSolo
    @NoControl CHAR(8),
    @nombre VARCHAR(50),
    @apP VARCHAR(50),
    @apM VARCHAR(50),
    @semestre VARCHAR(8),
    @carrera VARCHAR(80)
AS
BEGIN
    INSERT INTO Estudiante VALUES (@NoControl, @nombre, @apP, @apM, @semestre, @carrera)
END;
GO

CREATE OR ALTER PROCEDURE sp_ActualizarEstudianteSolo
    @NoControl CHAR(8),
    @nombre VARCHAR(50) = NULL,
    @apP VARCHAR(50) = NULL,
    @apM VARCHAR(50) = NULL,
    @semestre VARCHAR(8) = NULL,
    @carrera VARCHAR(80) = NULL
AS
BEGIN
    UPDATE Estudiante
    SET 
        nombre   = COALESCE(NULLIF(@nombre, ''), nombre),
        apP      = COALESCE(NULLIF(@apP, ''), apP),
        apM      = COALESCE(NULLIF(@apM, ''), apM),
        semestre = COALESCE(NULLIF(@semestre, ''), semestre),
        carrera  = COALESCE(NULLIF(@carrera, ''), carrera)
    WHERE NoControl = @NoControl;
END;
GO

CREATE OR ALTER PROCEDURE sp_EliminarEstudianteSolo
    @NoControl CHAR(8)
AS
BEGIN
    DELETE FROM Estudiante WHERE NoControl=@NoControl;
END;
GO

CREATE OR ALTER PROCEDURE sp_InsertarMateria
    @nombreM VARCHAR(50),
    @horasP VARCHAR(10),
    @horasT VARCHAR(10),
    @creditos INT
AS
BEGIN
    INSERT INTO materia(nombreM, horasP, horasT, creditos)
    VALUES (@nombreM, @horasP, @horasT, @creditos);
END;
GO

CREATE OR ALTER PROCEDURE sp_ActualizarMateria
    @idmateria INT,
    @nombreM VARCHAR(50) = '',
    @horasP VARCHAR(10) = '',
    @horasT VARCHAR(10) = '',
    @creditos INT = 0
AS
BEGIN
    UPDATE materia
    SET 
        nombreM = COALESCE(NULLIF(@nombreM, ''), nombreM),
        horasP  = COALESCE(NULLIF(@horasP, ''), horasP),
        horasT  = COALESCE(NULLIF(@horasT, ''), horasT),
        creditos = CASE WHEN @creditos = 0 THEN creditos ELSE @creditos END
    WHERE idmateria = @idmateria;
END;
GO

CREATE OR ALTER PROCEDURE sp_EliminarMateria
    @idmateria INT
AS
BEGIN
    DELETE FROM materia WHERE idmateria=@idmateria;
END;
GO


CREATE OR ALTER PROCEDURE sp_InsertarCursan
    @NoControl CHAR(8),
    @idmateria INT,
    @calif INT,
    @oportunidad VARCHAR(20)
AS
BEGIN
    INSERT INTO cursan (NoControl, idmateria, calif, oportunidad)
    VALUES (@NoControl, @idmateria, @calif, @oportunidad);
END;
GO

CREATE OR ALTER PROCEDURE sp_ActualizarCursan
    @NoControl CHAR(8),
    @idmateria INT,
    @calif INT,
    @oportunidad VARCHAR(20)
AS
BEGIN
    IF EXISTS (
        SELECT 1 FROM cursan 
        WHERE NoControl = @NoControl AND idmateria = @idmateria
    )
    BEGIN
        UPDATE cursan
        SET 
            calif = @calif,
            oportunidad = @oportunidad
        WHERE NoControl = @NoControl AND idmateria = @idmateria;
    END
END;
GO

CREATE OR ALTER PROCEDURE sp_EliminarCursan
    @NoControl CHAR(8),
    @idmateria INT
AS
BEGIN
    DELETE FROM cursan
    WHERE NoControl=@NoControl AND idmateria=@idmateria;
END;
GO


EXEC sp_rename 'AuditoriaGeneral', 'Bitacora';

go
CREATE OR ALTER TRIGGER trg_Insertar_EstudianteB
ON Estudiante
AFTER INSERT
AS
BEGIN
    DECLARE @usuario VARCHAR(100) = CONVERT(VARCHAR(100), SESSION_CONTEXT(N'usuario_app'));

    INSERT INTO Bitacora(nombre_tabla, tipo_accion, usuario, detalle)
    SELECT 
        'Estudiante',
        'INSERT',
        ISNULL(@usuario, 'desconocido'),
        CONCAT('Insertado estudiante NoControl: ', NoControl, ', nombre: ', nombre, ' ', apP, ' ', apM)
    FROM inserted;
END;
GO

CREATE OR ALTER TRIGGER trg_Actualizar_Cursan
ON cursan
AFTER UPDATE
AS
BEGIN
    DECLARE @usuario VARCHAR(100) = CONVERT(VARCHAR(100), SESSION_CONTEXT(N'usuario_app'));

    INSERT INTO Bitacora(nombre_tabla, tipo_accion, usuario, detalle)
    SELECT 
        'cursan',
        'UPDATE',
        ISNULL(@usuario, 'desconocido'),
        CONCAT(
            'Actualización - NoControl: ', i.NoControl, ', materia: ', i.idmateria,
            CASE 
                WHEN i.calif <> d.calif THEN CONCAT(', calif antes: ', d.calif, ', ahora: ', i.calif)
                ELSE ''
            END,
            CASE 
                WHEN i.oportunidad <> d.oportunidad THEN CONCAT(', oportunidad antes: ', d.oportunidad, ', ahora: ', i.oportunidad)
                ELSE ''
            END
        )
    FROM inserted i
    INNER JOIN deleted d ON i.NoControl = d.NoControl AND i.idmateria = d.idmateria
    WHERE 
        i.calif <> d.calif OR
        i.oportunidad <> d.oportunidad;
END;
GO


CREATE OR ALTER TRIGGER trg_Eliminar_EstudianteB
ON Estudiante
AFTER DELETE
AS
BEGIN
    DECLARE @usuario VARCHAR(100) = CONVERT(VARCHAR(100), SESSION_CONTEXT(N'usuario_app'));

    INSERT INTO Bitacora(nombre_tabla, tipo_accion, usuario, detalle)
    SELECT 
        'Estudiante',
        'DELETE',
        ISNULL(@usuario, 'desconocido'),
        CONCAT('Eliminado estudiante NoControl: ', NoControl, ', nombre: ', nombre, ' ', apP, ' ', apM)
    FROM deleted;
END;
GO

CREATE OR ALTER TRIGGER trg_Insertar_Materia
ON materia
AFTER INSERT
AS
BEGIN
    DECLARE @usuario VARCHAR(100) = CONVERT(VARCHAR(100), SESSION_CONTEXT(N'usuario_app'));

    INSERT INTO Bitacora(nombre_tabla, tipo_accion, usuario, detalle)
    SELECT 
        'materia',
        'INSERT',
        ISNULL(@usuario, 'desconocido'),
        CONCAT('Insertada materia ID: ', idmateria, ', nombre: ', nombreM)
    FROM inserted;
END;
GO

CREATE OR ALTER TRIGGER trg_Actualizar_Materia
ON materia
AFTER UPDATE
AS
BEGIN
    DECLARE @usuario VARCHAR(100) = CONVERT(VARCHAR(100), SESSION_CONTEXT(N'usuario_app'));

    INSERT INTO Bitacora(nombre_tabla, tipo_accion, usuario, detalle)
    SELECT 
        'materia',
        'UPDATE',
        ISNULL(@usuario, 'desconocido'),
        CONCAT(
            'Actualizada materia ID: ', i.idmateria,
            CASE WHEN i.nombreM <> d.nombreM THEN CONCAT(', nombre antes: ', d.nombreM, ', ahora: ', i.nombreM) ELSE '' END,
            CASE WHEN i.horasP <> d.horasP THEN CONCAT(', horasP antes: ', d.horasP, ', ahora: ', i.horasP) ELSE '' END,
            CASE WHEN i.horasT <> d.horasT THEN CONCAT(', horasT antes: ', d.horasT, ', ahora: ', i.horasT) ELSE '' END,
            CASE WHEN i.creditos <> d.creditos THEN CONCAT(', creditos antes: ', d.creditos, ', ahora: ', i.creditos) ELSE '' END
        )
    FROM inserted i
    INNER JOIN deleted d ON i.idmateria = d.idmateria
    WHERE
        i.nombreM <> d.nombreM OR
        i.horasP <> d.horasP OR
        i.horasT <> d.horasT OR
        i.creditos <> d.creditos;
END;
GO

CREATE OR ALTER TRIGGER trg_Eliminar_Materia
ON materia
AFTER DELETE
AS
BEGIN
    DECLARE @usuario VARCHAR(100) = CONVERT(VARCHAR(100), SESSION_CONTEXT(N'usuario_app'));

    INSERT INTO Bitacora(nombre_tabla, tipo_accion, usuario, detalle)
    SELECT 
        'materia',
        'DELETE',
        ISNULL(@usuario, 'desconocido'),
        CONCAT('Eliminada materia ID: ', idmateria, ', nombre: ', nombreM)
    FROM deleted;
END;
GO

CREATE OR ALTER TRIGGER trg_Insertar_Cursan
ON cursan
AFTER INSERT
AS
BEGIN
    DECLARE @usuario VARCHAR(100) = CONVERT(VARCHAR(100), SESSION_CONTEXT(N'usuario_app'));

    INSERT INTO Bitacora(nombre_tabla, tipo_accion, usuario, detalle)
    SELECT 
        'cursan',
        'INSERT',
        ISNULL(@usuario, 'desconocido'),
        CONCAT('Inscripción - NoControl: ', NoControl, ', materia: ', idmateria, ', calificación: ', calif)
    FROM inserted;
END;
GO

CREATE OR ALTER TRIGGER trg_Actualizar_Cursan
ON cursan
AFTER UPDATE
AS
BEGIN
    DECLARE @usuario VARCHAR(100) = CONVERT(VARCHAR(100), SESSION_CONTEXT(N'usuario_app'));

    INSERT INTO Bitacora(nombre_tabla, tipo_accion, usuario, detalle)
    SELECT 
        'cursan',
        'UPDATE',
        ISNULL(@usuario, 'desconocido'),
        CONCAT('Actualización - NoControl: ', i.NoControl, ', materia: ', i.idmateria,
               ', calif antes: ', d.calif, ', ahora: ', i.calif,
               ', oportunidad antes: ', d.oportunidad, ', ahora: ', i.oportunidad)
    FROM inserted i
    INNER JOIN deleted d ON i.NoControl = d.NoControl AND i.idmateria = d.idmateria;
END;

go

CREATE OR ALTER TRIGGER trg_Eliminar_Cursan
ON cursan
AFTER DELETE
AS
BEGIN
    DECLARE @usuario VARCHAR(100) = CONVERT(VARCHAR(100), SESSION_CONTEXT(N'usuario_app'));

    INSERT INTO Bitacora(nombre_tabla, tipo_accion, usuario, detalle)
    SELECT 
        'cursan',
        'DELETE',
        ISNULL(@usuario, 'desconocido'),
        CONCAT('Eliminación - NoControl: ', NoControl, ', materia: ', idmateria)
    FROM deleted;
END;
GO

CREATE OR ALTER PROCEDURE sp_ConsultarEstudianteSolo
    @NoControl CHAR(8)
AS
BEGIN
    SELECT nombre, apP, apM, semestre, carrera
    FROM Estudiante
    WHERE NoControl = @NoControl;
END;
GO

INSERT INTO Usuarios (nombreUsuario, contrasena, tipoUsuario)
VALUES ('auditor1', '1234', 'auditor');

INSERT INTO Usuarios (nombreUsuario, contrasena, tipoUsuario)
VALUES ('usuario_admin', 'chestermaster323', 'admin');

INSERT INTO Usuarios (nombreUsuario, contrasena, tipoUsuario)
VALUES ('usuario_normal', 'chester323', 'normal');



CREATE LOGIN auditor_user WITH PASSWORD = 'michiauditor323';


CREATE USER auditor_user FOR LOGIN auditor_user;

GRANT SELECT ON dbo.Bitacora TO auditor_user;
GRANT SELECT ON dbo.Historial TO auditor_user; 

go
CREATE OR ALTER PROCEDURE sp_ConsultarAuditoriaGeneral
AS
BEGIN
    SELECT 
        fecha, 
        nombre_tabla, 
        tipo_accion, 
        usuario, 
        detalle
    FROM Bitacora
    ORDER BY fecha DESC;
END;

GRANT EXECUTE ON OBJECT::sp_ConsultarAuditoriaGeneral TO auditor_user;

DROP TRIGGER trg_Actualizar_Estudiante;

go

CREATE OR ALTER TRIGGER trg_Actualizar_EstudianteB
ON Estudiante
AFTER UPDATE
AS
BEGIN
    DECLARE @usuario VARCHAR(100) = CONVERT(VARCHAR(100), SESSION_CONTEXT(N'usuario_app'));

    INSERT INTO Bitacora(nombre_tabla, tipo_accion, usuario, detalle)
    SELECT 
        'Estudiante',
        'UPDATE',
        ISNULL(@usuario, 'desconocido'),
        CONCAT(
            'Actualizado estudiante NoControl: ', i.NoControl, 
            CASE WHEN i.nombre <> d.nombre THEN CONCAT(', nombre antes: ', d.nombre, ', ahora: ', i.nombre) ELSE '' END,
            CASE WHEN i.apP <> d.apP THEN CONCAT(', apP antes: ', d.apP, ', ahora: ', i.apP) ELSE '' END,
            CASE WHEN i.apM <> d.apM THEN CONCAT(', apM antes: ', d.apM, ', ahora: ', i.apM) ELSE '' END,
            CASE WHEN i.semestre <> d.semestre THEN CONCAT(', semestre antes: ', d.semestre, ', ahora: ', i.semestre) ELSE '' END,
            CASE WHEN i.carrera <> d.carrera THEN CONCAT(', carrera antes: ', d.carrera, ', ahora: ', i.carrera) ELSE '' END
        )
    FROM inserted i
    INNER JOIN deleted d ON i.NoControl = d.NoControl
    WHERE 
        i.nombre   <> d.nombre OR
        i.apP      <> d.apP OR
        i.apM      <> d.apM OR
        i.semestre <> d.semestre OR
        i.carrera  <> d.carrera;
END;
GO

CREATE OR ALTER TRIGGER trg_Actualizar_EstudianteB
ON Estudiante
AFTER UPDATE
AS
BEGIN
    DECLARE @usuario VARCHAR(100) = CONVERT(VARCHAR(100), SESSION_CONTEXT(N'usuario_app'));

    INSERT INTO Bitacora(nombre_tabla, tipo_accion, usuario, detalle)
    SELECT 
        'Estudiante',
        'UPDATE',
        ISNULL(@usuario, 'desconocido'),
        CONCAT(
            'Actualizado estudiante NoControl: ', i.NoControl,
            CASE WHEN i.nombre   <> d.nombre   THEN CONCAT(', nombre antes: ', d.nombre, ', ahora: ', i.nombre) ELSE '' END,
            CASE WHEN i.apP      <> d.apP      THEN CONCAT(', apP antes: ', d.apP, ', ahora: ', i.apP) ELSE '' END,
            CASE WHEN i.apM      <> d.apM      THEN CONCAT(', apM antes: ', d.apM, ', ahora: ', i.apM) ELSE '' END,
            CASE WHEN i.semestre <> d.semestre THEN CONCAT(', semestre antes: ', d.semestre, ', ahora: ', i.semestre) ELSE '' END,
            CASE WHEN i.carrera  <> d.carrera  THEN CONCAT(', carrera antes: ', d.carrera, ', ahora: ', i.carrera) ELSE '' END
        )
    FROM inserted i
    INNER JOIN deleted d ON i.NoControl = d.NoControl
    WHERE 
        (ISNULL(i.nombre, '')   <> ISNULL(d.nombre, '') OR
         ISNULL(i.apP, '')      <> ISNULL(d.apP, '') OR
         ISNULL(i.apM, '')      <> ISNULL(d.apM, '') OR
         ISNULL(i.semestre, '') <> ISNULL(d.semestre, '') OR
         ISNULL(i.carrera, '')  <> ISNULL(d.carrera, ''));
END;
GO

DROP TRIGGER trg_ActualizarEstudiante;


go

CREATE OR ALTER PROCEDURE sp_ListarMateriasDetalles
AS
BEGIN
    SELECT 
        idmateria, 
        nombreM, 
        horasP, 
        horasT, 
        creditos 
    FROM materia;
END;
GO

SELECT * 
FROM cursan 
WHERE NoControl = '22334455' AND idmateria = 2;

go

CREATE OR ALTER PROCEDURE sp_ActualizarCursan
    @NoControl CHAR(8),
    @idmateria INT,
    @calif INT,
    @oportunidad VARCHAR(20)
AS
BEGIN
    UPDATE cursan
    SET 
        calif = @calif,
        oportunidad = @oportunidad
    WHERE NoControl = @NoControl AND idmateria = @idmateria
      AND (calif <> @calif OR oportunidad <> @oportunidad);
END;

CREATE OR ALTER TRIGGER trg_Actualizar_Cursan
ON cursan
AFTER UPDATE
AS
BEGIN
    DECLARE @usuario VARCHAR(100) = CONVERT(VARCHAR(100), SESSION_CONTEXT(N'usuario_app'));

    INSERT INTO Bitacora(nombre_tabla, tipo_accion, usuario, detalle)
    SELECT 
        'cursan',
        'UPDATE',
        ISNULL(@usuario, 'desconocido'),
        CONCAT(
            'Actualización - NoControl: ', i.NoControl,
            ', materia: ', i.idmateria,
            CASE 
                WHEN i.calif <> d.calif 
                    THEN CONCAT(', calif antes: ', d.calif, ', ahora: ', i.calif) 
                ELSE '' 
            END,
            CASE 
                WHEN i.oportunidad <> d.oportunidad 
                    THEN CONCAT(', oportunidad antes: ', d.oportunidad, ', ahora: ', i.oportunidad) 
                ELSE '' 
            END
        )
    FROM inserted i
    INNER JOIN deleted d 
        ON i.NoControl = d.NoControl AND i.idmateria = d.idmateria
    WHERE 
        i.calif <> d.calif OR
        i.oportunidad <> d.oportunidad;
END;
GO

