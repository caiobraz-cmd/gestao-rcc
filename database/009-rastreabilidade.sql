-- Aplicar uma vez; não copia valores de campos pessoais ou clínicos.
CREATE TABLE rcc_registro_operacao (
 registro VARCHAR2(32 BYTE) PRIMARY KEY,
 pessoa_id NUMBER NOT NULL REFERENCES pessoa(id),
 entrega_id NUMBER UNIQUE REFERENCES entrega_cesta(id),
 operacao VARCHAR2(12 BYTE) NOT NULL CHECK (operacao IN ('cadastro','alteracao','entrega')),
 autor VARCHAR2(120 BYTE),
 perfil VARCHAR2(10 BYTE) CHECK (perfil IN ('admin','operador')),
 criado_em TIMESTAMP WITH TIME ZONE DEFAULT SYSTIMESTAMP NOT NULL
);
