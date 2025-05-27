

EXEC sp_addrolemember 'db_owner', 'usuario_admin';

-- Permitir respaldo
GRANT BACKUP DATABASE TO usuario_admin;


USE master;
GO

CREATE USER usuario_admin FOR LOGIN usuario_admin;
GO

-- Permitir restauración
GRANT CREATE DATABASE TO usuario_admin;
