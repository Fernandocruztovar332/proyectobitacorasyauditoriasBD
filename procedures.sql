-- PROCEDURE para listar NoControl de Estudiante
CREATE OR ALTER PROCEDURE sp_ListarNoControl
AS
BEGIN
    SELECT NoControl
    FROM Estudiante;
END;
GO

CREATE OR ALTER PROCEDURE sp_RegistrarCalificacion
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
GO


CREATE OR ALTER PROCEDURE sp_ActualizarEstudiante
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

        -- Actualizar datos del estudiante
        UPDATE Estudiante
        SET nombre = @nombre,
            apP = @apP,
            apM = @apM,
            semestre = @semestre,
            carrera = @carrera
        WHERE NoControl = @NoControl;

        -- Actualizar o insertar en cursan (según si existe o no)
        IF EXISTS (
            SELECT 1 FROM cursan
            WHERE NoControl = @NoControl AND idmateria = @idmateria
        )
        BEGIN
            -- Si ya existe, solo actualizar
            UPDATE cursan
            SET calif = @calif,
                oportunidad = @oportunidad
            WHERE NoControl = @NoControl AND idmateria = @idmateria;
        END
        ELSE
        BEGIN
            -- Si no existe, insertar
            INSERT INTO cursan (NoControl, calif, oportunidad, idmateria)
            VALUES (@NoControl, @calif, @oportunidad, @idmateria);
        END

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END