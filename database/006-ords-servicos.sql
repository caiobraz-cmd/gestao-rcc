-- Aplicar em homologação, no módulo existente protegido gestao_rcc_v2.
-- Não recria tabelas, módulo, privilégios nem handlers de pacientes ou cestas.
BEGIN
  ORDS.DEFINE_TEMPLATE(p_module_name=>'gestao_rcc_v2', p_pattern=>'servicos/:id/');
  ORDS.DEFINE_HANDLER(p_module_name=>'gestao_rcc_v2', p_pattern=>'servicos/:id/',
    p_method=>'GET', p_source_type=>'json/collection', p_source=>q'~
      SELECT id, pessoa_id, tipo_servico, descricao,
        TO_CHAR(data_servico,'YYYY-MM-DD HH24:MI') data_servico
      FROM servico_prestado WHERE pessoa_id=:id ORDER BY data_servico DESC, id DESC~');
  ORDS.DEFINE_HANDLER(p_module_name=>'gestao_rcc_v2', p_pattern=>'servicos/:id/',
    p_method=>'POST', p_source_type=>'plsql/block', p_source=>q'~
    DECLARE
      fk_invalida EXCEPTION;
      PRAGMA EXCEPTION_INIT(fk_invalida, -2291);
    BEGIN
      IF TRIM(:tipo_servico) IS NULL OR LENGTH(TRIM(:tipo_servico)) < 3
        OR LENGTHB(:tipo_servico) > 100 OR LENGTHB(:descricao) > 255 THEN
        :status_code:=422; RETURN;
      END IF;
      INSERT INTO servico_prestado(pessoa_id,tipo_servico,descricao,data_servico)
        VALUES(:id,TRIM(:tipo_servico),TRIM(:descricao),
          CAST(SYSTIMESTAMP AT TIME ZONE 'America/Sao_Paulo' AS DATE));
      :status_code:=201;
    EXCEPTION
      WHEN fk_invalida THEN ROLLBACK; :status_code:=404;
    END;~');
  COMMIT;
EXCEPTION WHEN OTHERS THEN ROLLBACK; RAISE;
END;
/
