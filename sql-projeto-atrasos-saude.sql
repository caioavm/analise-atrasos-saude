create database clinica;

USE clinica;

Create table pacientes (
paciente_id int PRIMARY key auto_increment,
nome varchar(100),
idade int,
sexo varchar(10)
);

create table agendamentos (
	id_agendamento int primary key auto_increment,
    paciente_id int,
    especialidade varchar(100),
    data_agendamento DATE,
    hora_agendada time,
    hora_atendimento time,
    local varchar(50),
    motivo_atraso varchar(100),
    FOREIGN KEY(paciente_id) references pacientes(paciente_id)
);

ALTER TABLE pacientes add column nome varchar(100);

ALTER TABLE pacientes MODIFY COLUMN sexo VARCHAR(25);

describe pacientes;

select * from pacientes;

delete from agendamentos;
delete from pacientes;

alter table pacientes auto_increment = 1;

select * from agendamentos
