-- Aplicar uma vez em GESTAORCC. Não altera USUARIO nem dados de pacientes.
CREATE TABLE rcc_conta_operador (
 login VARCHAR2(40 BYTE) PRIMARY KEY,
 nome VARCHAR2(120 BYTE) NOT NULL,
 senha_hash VARCHAR2(512 BYTE) NOT NULL,
 ativo NUMBER(1) DEFAULT 1 NOT NULL CHECK (ativo IN (0,1)),
 versao NUMBER DEFAULT 1 NOT NULL,
 CONSTRAINT ck_rcc_conta_login CHECK (REGEXP_LIKE(login,'^[a-z0-9][a-z0-9._-]{2,39}$','c'))
);
