use ESCOOL


CREATE TABLE Usuarios (
    idUsuario INT IDENTITY PRIMARY KEY,
    nombreUsuario VARCHAR(50) UNIQUE NOT NULL,
    contrasena VARCHAR(100) NOT NULL,
    tipoUsuario VARCHAR(20) NOT NULL CHECK (tipoUsuario IN ('admin', 'normal', 'auditor'))
);
go

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
    @nombre VARCHAR(50),
    @apP VARCHAR(50),
    @apM VARCHAR(50),
    @semestre VARCHAR(8),
    @carrera VARCHAR(80)
AS
BEGIN
    UPDATE Estudiante
    SET nombre=@nombre, apP=@apP, apM=@apM, semestre=@semestre, carrera=@carrera
    WHERE NoControl=@NoControl;
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
    @nombreM VARCHAR(50),
    @horasP VARCHAR(10),
    @horasT VARCHAR(10),
    @creditos INT
AS
BEGIN
    UPDATE materia
    SET nombreM=@nombreM, horasP=@horasP, horasT=@horasT, creditos=@creditos
    WHERE idmateria=@idmateria;
END;
GO

CREATE OR ALTER PROCEDURE sp_EliminarMateria
    @idmateria INT
AS
BEGIN
    DELETE FROM materia WHERE idmateria=@idmateria;
END;

go

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
    UPDATE cursan
    SET calif=@calif, oportunidad=@oportunidad
    WHERE NoControl=@NoControl AND idmateria=@idmateria;
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

-- Solo lectura
GRANT SELECT ON Estudiante TO usuario_normal;
GRANT SELECT ON materia TO usuario_normal;
GRANT SELECT ON cursan TO usuario_normal;

-- Admin tiene todos los permisos
ALTER ROLE db_owner ADD MEMBER usuario_admin;