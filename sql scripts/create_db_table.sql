create database eaud;

use eaud;

create table monitoramento (
	idTrefa int not null primary key,
	dataRealizadaInicio	date,
    dataRealizadaFim date,
    estado varchar (100),
    titulo varchar (240),
    siglaUnidadeAuditada varchar(15),
    unidadesDeAuditoria varchar(15),
    dtLimite date,
    listaTiposUltimaManifestacao varchar (240),
    listaTiposUltimoPosicionamento varchar (240)
)