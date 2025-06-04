
use ESCOOL
EXEC sp_rename 'Estudiante', 'usuarios'

CREATE TABLE Estudiante (
    NoControlE CHAR(8) PRIMARY KEY,
    semestre VARCHAR(8) NOT NULL,
    carrera VARCHAR(80) NOT NULL
	foreign key (NoControlE) references usuarios(NoControl)
);

create table Administrativo(
    NoControlA CHAR(8) PRIMARY KEY,
    telefonoA VARCHAR(50) NOT NULL,
    correoA   VARCHAR(50) NOT NULL,
	foreign key (NoControlA) references usuarios(NoControl)

);

create table 