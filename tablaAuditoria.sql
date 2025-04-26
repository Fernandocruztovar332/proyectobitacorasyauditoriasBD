use	ESCOOL

CREATE TABLE AuditoriaGeneral (
    id_auditoria INT PRIMARY KEY IDENTITY(1,1),
    nombre_tabla VARCHAR(50),
    tipo_accion VARCHAR(10), -- INSERT, UPDATE, DELETE
    usuario VARCHAR(100),
    fecha DATETIME DEFAULT GETDATE(),
    detalle NVARCHAR(MAX)
);

CREATE OR ALTER TRIGGER trg_Auditoria_Insert_Estudiante
ON Estudiante
AFTER INSERT
AS
BEGIN
    INSERT INTO AuditoriaGeneral (nombre_tabla, tipo_accion, usuario, detalle)
    SELECT 
        'Estudiante',
        'INSERT',
        SYSTEM_USER,
        CONCAT('Se insertó el estudiante ', NoControl, ' - ', nombre, ' ', apP, ' ', apM)
    FROM inserted;
END;


CREATE OR ALTER TRIGGER trg_Auditoria_Update_Estudiante
ON Estudiante
AFTER UPDATE
AS
BEGIN
    INSERT INTO AuditoriaGeneral (nombre_tabla, tipo_accion, usuario, detalle)
    SELECT 
        'Estudiante',
        'UPDATE',
        SYSTEM_USER,
        CONCAT('Se actualizó el estudiante ', i.NoControl, '. Cambios en nombre/apellidos/carrera/etc.')
    FROM inserted i;
END;


CREATE OR ALTER TRIGGER trg_Auditoria_Delete_Estudiante
ON Estudiante
AFTER DELETE
AS
BEGIN
    INSERT INTO AuditoriaGeneral (nombre_tabla, tipo_accion, usuario, detalle)
    SELECT 
        'Estudiante',
        'DELETE',
        SYSTEM_USER,
        CONCAT('Se eliminó el estudiante ', NoControl, ' - ', nombre, ' ', apP, ' ', apM)
    FROM deleted;
END;


