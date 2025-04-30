use ESCOOL

-- Crear usuario normal
CREATE USER usuario_normal FOR LOGIN usuario_normal;

-- Crear usuario administrador
CREATE USER usuario_admin FOR LOGIN usuario_admin;


-- Permisos de solo operación básica
GRANT SELECT, INSERT, UPDATE, DELETE ON Estudiante TO usuario_normal;
GRANT SELECT, INSERT, UPDATE, DELETE ON materia TO usuario_normal;
GRANT SELECT, INSERT, UPDATE, DELETE ON cursan TO usuario_normal;
GRANT SELECT, INSERT, UPDATE, DELETE ON datosPA TO usuario_normal;

GRANT EXECUTE ON dbo.sp_ListarNoControl TO usuario_normal;
GRANT EXECUTE ON dbo.sp_InsertarEstudiante TO usuario_normal;
GRANT EXECUTE ON dbo.sp_ActualizarEstudiante TO usuario_normal;
GRANT EXECUTE ON dbo.sp_RegistrarCalificacion TO usuario_normal;
GRANT EXECUTE ON dbo.sp_EliminarEstudiante TO usuario_normal;
GRANT EXECUTE ON dbo.sp_ListarMateriasEstudiantes TO usuario_normal;

GRANT SELECT ON dbo.vw_EstudianteCompleto TO usuario_normal;


-- (NO DAR ACCESO a AuditoriaGeneral, Historial, etc.)


ALTER ROLE db_owner ADD MEMBER usuario_admin;

