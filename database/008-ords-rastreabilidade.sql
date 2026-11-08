-- Substitui somente o POST de serviços; preserva o GET e os dados existentes.
-- A autoria é fornecida pelo backend autenticado, nunca pelo formulário.
BEGIN
 ORDS.DEFINE_HANDLER(p_module_name=>'gestao_rcc_v2',p_pattern=>'servicos/:id/',
 p_method=>'POST',p_source_type=>'plsql/block',p_source=>q'~
 DECLARE
  novo_id NUMBER;
  fk_invalida EXCEPTION;
  PRAGMA EXCEPTION_INIT(fk_invalida,-2291);
 BEGIN
  IF TRIM(:tipo_servico) IS NULL OR LENGTH(TRIM(:tipo_servico))<3
   OR LENGTHB(:tipo_servico)>100 OR LENGTHB(:descricao)>255
   OR (:registro IS NOT NULL AND NOT REGEXP_LIKE(:registro,'^[a-f0-9]{32}$','c'))
   OR (:registro IS NOT NULL AND (TRIM(:autor) IS NULL OR LENGTHB(:autor)>120 OR NVL(:perfil,'?') NOT IN ('admin','operador')))
   THEN :status_code:=422; RETURN; END IF;
  INSERT INTO servico_prestado(pessoa_id,tipo_servico,descricao,data_servico)
   VALUES(:id,TRIM(:tipo_servico),TRIM(:descricao),
          CAST(SYSTIMESTAMP AT TIME ZONE 'America/Sao_Paulo' AS DATE))
   RETURNING id INTO novo_id;
  INSERT INTO rcc_registro_servico(registro,servico_id,autor,perfil)
   VALUES(NVL(:registro,LOWER(RAWTOHEX(SYS_GUID()))),novo_id,
          CASE WHEN :registro IS NOT NULL THEN :autor END,
          CASE WHEN :registro IS NOT NULL THEN :perfil END);
  :status_code:=201;
 EXCEPTION
  WHEN fk_invalida THEN ROLLBACK; :status_code:=404;
  WHEN DUP_VAL_ON_INDEX THEN ROLLBACK; :status_code:=409;
  WHEN OTHERS THEN ROLLBACK; RAISE;
 END;~');
 ORDS.DEFINE_TEMPLATE(p_module_name=>'gestao_rcc_v2',p_pattern=>'registros-servicos/');
 ORDS.DEFINE_HANDLER(p_module_name=>'gestao_rcc_v2',p_pattern=>'registros-servicos/',
 p_method=>'GET',p_source_type=>'json/collection',p_source=>q'~
 SELECT s.id servico_id,s.pessoa_id,p.nome paciente,s.tipo_servico servico,r.autor,r.perfil,
  COALESCE(TO_CHAR(r.criado_em AT TIME ZONE 'America/Sao_Paulo','YYYY-MM-DD HH24:MI:SS'),
           TO_CHAR(s.data_servico,'YYYY-MM-DD HH24:MI:SS')) quando
 FROM servico_prestado s JOIN pessoa p ON p.id=s.pessoa_id
 LEFT JOIN rcc_registro_servico r ON r.servico_id=s.id
 WHERE :busca IS NULL OR INSTR(LOWER(p.nome),LOWER(:busca))>0
  OR INSTR(LOWER(s.tipo_servico),LOWER(:busca))>0 OR INSTR(LOWER(r.autor),LOWER(:busca))>0
 ORDER BY s.id DESC~');
 ORDS.DEFINE_TEMPLATE(p_module_name=>'gestao_rcc_v2',p_pattern=>'registros-servicos/:registro/');
 ORDS.DEFINE_HANDLER(p_module_name=>'gestao_rcc_v2',p_pattern=>'registros-servicos/:registro/',
 p_method=>'GET',p_source_type=>'json/item',p_source=>q'~
 SELECT r.registro,r.servico_id,r.autor,r.perfil,s.pessoa_id FROM rcc_registro_servico r
 JOIN servico_prestado s ON s.id=r.servico_id WHERE r.registro=:registro~');
 COMMIT;
EXCEPTION WHEN OTHERS THEN ROLLBACK; RAISE;
END;
/
