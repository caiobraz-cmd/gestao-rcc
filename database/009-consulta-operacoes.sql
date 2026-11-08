BEGIN
 ORDS.DEFINE_TEMPLATE(p_module_name=>'gestao_rcc_v2',p_pattern=>'registros-operacoes/');
 ORDS.DEFINE_HANDLER(p_module_name=>'gestao_rcc_v2',p_pattern=>'registros-operacoes/',
 p_method=>'GET',p_source_type=>'json/collection',p_source=>q'~
 SELECT e.registro,e.pessoa_id,p.nome paciente,e.operacao,e.autor,e.perfil,e.referencia,
  TO_CHAR(e.quando,'YYYY-MM-DD HH24:MI:SS') quando FROM (
 SELECT registro,pessoa_id,operacao,autor,perfil,entrega_id referencia,
  CAST(criado_em AT TIME ZONE 'America/Sao_Paulo' AS TIMESTAMP) quando FROM rcc_registro_operacao
 UNION ALL
 SELECT r.registro,s.pessoa_id,'servico',r.autor,r.perfil,s.id,
  COALESCE(CAST(r.criado_em AT TIME ZONE 'America/Sao_Paulo' AS TIMESTAMP),CAST(s.data_servico AS TIMESTAMP))
 FROM servico_prestado s LEFT JOIN rcc_registro_servico r ON r.servico_id=s.id
 UNION ALL
 SELECT NULL,c.pessoa_id,'entrega',NULL,NULL,c.id,CAST(c.data_entrega AS TIMESTAMP)
 FROM entrega_cesta c WHERE NOT EXISTS(SELECT 1 FROM rcc_registro_operacao r WHERE r.entrega_id=c.id)
 ) e JOIN pessoa p ON p.id=e.pessoa_id
 WHERE (:tipo IS NULL OR e.operacao=:tipo) AND
 (:busca IS NULL OR INSTR(LOWER(p.nome),LOWER(:busca))>0 OR INSTR(LOWER(e.autor),LOWER(:busca))>0)
 ORDER BY e.quando DESC,e.registro DESC NULLS LAST,e.operacao,e.referencia DESC~');
 ORDS.DEFINE_TEMPLATE(p_module_name=>'gestao_rcc_v2',p_pattern=>'registros-operacoes/:registro/');
 ORDS.DEFINE_HANDLER(p_module_name=>'gestao_rcc_v2',p_pattern=>'registros-operacoes/:registro/',
 p_method=>'GET',p_source_type=>'json/item',p_source=>q'~
 SELECT registro,pessoa_id,entrega_id,operacao,autor,perfil FROM rcc_registro_operacao WHERE registro=:registro~');
 COMMIT;
EXCEPTION WHEN OTHERS THEN ROLLBACK; RAISE;
END;
/
