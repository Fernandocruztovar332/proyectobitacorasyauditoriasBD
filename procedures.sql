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