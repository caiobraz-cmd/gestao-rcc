-- Aplicar uma vez. Guarda autoria sem duplicar informações clínicas.
CREATE TABLE rcc_registro_servico (
 registro VARCHAR2(32 BYTE) PRIMARY KEY,
 servico_id NUMBER NOT NULL UNIQUE REFERENCES servico_prestado(id),
 autor VARCHAR2(120 BYTE),
 perfil VARCHAR2(10 BYTE) CHECK (perfil IN ('admin','operador')),
 criado_em TIMESTAMP WITH TIME ZONE DEFAULT SYSTIMESTAMP NOT NULL
);
