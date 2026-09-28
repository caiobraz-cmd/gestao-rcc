-- Executar APOS 005-cadastro-cestas.sql. Instala um modulo separado, NAO PUBLICADO.
-- Homologar e configurar cliente OAuth com papel gestao_rcc_v2_operador antes de publicar.
-- Nao substitui nem modifica os handlers de /rcc/.
DECLARE
  roles OWA.VC_ARR;
  patterns OWA.VC_ARR;
  modules OWA.VC_ARR;
  projection VARCHAR2(32767) := q'~SELECT p.id, p.nome, p.cpf,
    TO_CHAR(p.data_nascimento,'YYYY-MM-DD') data_nascimento,
    p.telefone, p.endereco, p.status, p.char_diagnostico, p.char_tratamento,
    p.char_medicamento, p.char_alergia, p.char_observacoes,
    TO_CHAR(p.data_obito,'YYYY-MM-DD') data_obito, p.num_frequencia_cesta,
    (SELECT TO_CHAR(MAX(c.data_entrega),'YYYY-MM-DD') FROM entrega_cesta c
     WHERE c.pessoa_id=p.id) dt_ultima_cesta FROM pessoa p~';
  validation VARCHAR2(32767) := q'~
    IF :nome IS NULL OR LENGTH(TRIM(:nome)) < 3 OR :cpf IS NULL
       OR NOT REGEXP_LIKE(:cpf, '^[0-9]{11}$')
       OR :data_nascimento IS NULL OR TO_DATE(:data_nascimento,'FXYYYY-MM-DD') >
          TRUNC(CAST(SYSTIMESTAMP AT TIME ZONE 'America/Sao_Paulo' AS DATE))
       OR NVL(:status,'?') NOT IN ('ATIVO','INATIVO')
       OR (:num_frequencia_cesta IS NOT NULL AND
           (:num_frequencia_cesta < 1 OR :num_frequencia_cesta > 365
            OR :num_frequencia_cesta <> TRUNC(:num_frequencia_cesta)))
       OR (:data_obito IS NOT NULL AND
           (TO_DATE(:data_obito,'FXYYYY-MM-DD') < TO_DATE(:data_nascimento,'FXYYYY-MM-DD')
            OR TO_DATE(:data_obito,'FXYYYY-MM-DD') > TRUNC(CAST(SYSTIMESTAMP AT TIME ZONE 'America/Sao_Paulo' AS DATE))
            OR :status <> 'INATIVO')) THEN
      :status_code := 422; RETURN;
    END IF;
  ~';
BEGIN
  ORDS.DEFINE_MODULE(p_module_name=>'gestao_rcc_v2', p_base_path=>'/rcc-v2/',
    p_items_per_page=>100, p_status=>'NOT_PUBLISHED');
  ORDS.CREATE_ROLE(p_role_name=>'gestao_rcc_v2_operador');
  roles(1) := 'gestao_rcc_v2_operador';
  patterns(1) := '/rcc-v2/*';
  modules(1) := 'gestao_rcc_v2';
  ORDS.DEFINE_PRIVILEGE(p_privilege_name=>'gestao_rcc_v2.acesso', p_roles=>roles,
    p_patterns=>patterns, p_modules=>modules, p_label=>'Cadastro completo e cestas');

  ORDS.DEFINE_TEMPLATE(p_module_name=>'gestao_rcc_v2', p_pattern=>'pessoas/');
  ORDS.DEFINE_HANDLER(p_module_name=>'gestao_rcc_v2', p_pattern=>'pessoas/',
    p_method=>'GET', p_source_type=>'json/collection',
    p_source=>projection || ' ORDER BY p.nome, p.id');
  ORDS.DEFINE_HANDLER(p_module_name=>'gestao_rcc_v2', p_pattern=>'pessoas/',
    p_method=>'POST', p_source_type=>'plsql/block', p_source=>'BEGIN ' || validation || q'~
      INSERT INTO pessoa(nome, cpf, data_nascimento, telefone, endereco, status,
        char_diagnostico, char_tratamento, char_medicamento, char_alergia, char_observacoes,
        data_obito, num_frequencia_cesta)
      VALUES(:nome, :cpf, TO_DATE(:data_nascimento,'FXYYYY-MM-DD'), :telefone, :endereco, :status,
        :char_diagnostico, :char_tratamento, :char_medicamento, :char_alergia, :char_observacoes,
        TO_DATE(:data_obito,'FXYYYY-MM-DD'), :num_frequencia_cesta);
      :status_code := 201;
    EXCEPTION
      WHEN DUP_VAL_ON_INDEX THEN ROLLBACK; :status_code := 409;
      WHEN OTHERS THEN ROLLBACK; :status_code := 400;
    END;~');
  ORDS.DEFINE_TEMPLATE(p_module_name=>'gestao_rcc_v2', p_pattern=>'pessoas/:id');
  ORDS.DEFINE_HANDLER(p_module_name=>'gestao_rcc_v2', p_pattern=>'pessoas/:id',
    p_method=>'GET', p_source_type=>'json/item', p_source=>projection || ' WHERE p.id=:id');
  ORDS.DEFINE_HANDLER(p_module_name=>'gestao_rcc_v2', p_pattern=>'pessoas/:id',
    p_method=>'PUT', p_source_type=>'plsql/block', p_source=>'BEGIN ' || validation || q'~
      UPDATE pessoa SET nome=:nome, cpf=:cpf,
        data_nascimento=TO_DATE(:data_nascimento,'FXYYYY-MM-DD'), telefone=:telefone,
        endereco=:endereco, status=:status,
        char_diagnostico=CASE WHEN :atualizar_clinico=1 THEN :char_diagnostico ELSE char_diagnostico END,
        char_tratamento=CASE WHEN :atualizar_clinico=1 THEN :char_tratamento ELSE char_tratamento END,
        char_medicamento=CASE WHEN :atualizar_clinico=1 THEN :char_medicamento ELSE char_medicamento END,
        char_alergia=CASE WHEN :atualizar_clinico=1 THEN :char_alergia ELSE char_alergia END,
        char_observacoes=CASE WHEN :atualizar_clinico=1 THEN :char_observacoes ELSE char_observacoes END,
        data_obito=CASE WHEN :atualizar_clinico=1 OR :atualizar_cestas=1
          THEN TO_DATE(:data_obito,'FXYYYY-MM-DD') ELSE data_obito END,
        num_frequencia_cesta=CASE WHEN :atualizar_cestas=1 THEN :num_frequencia_cesta ELSE num_frequencia_cesta END
      WHERE id=:id;
      IF SQL%ROWCOUNT=0 THEN :status_code:=404; ELSE :status_code:=200; END IF;
    EXCEPTION
      WHEN DUP_VAL_ON_INDEX THEN ROLLBACK; :status_code:=409;
      WHEN OTHERS THEN ROLLBACK; :status_code:=400;
    END;~');

  ORDS.DEFINE_TEMPLATE(p_module_name=>'gestao_rcc_v2', p_pattern=>'cestas/:id/');
  ORDS.DEFINE_HANDLER(p_module_name=>'gestao_rcc_v2', p_pattern=>'cestas/:id/',
    p_method=>'GET', p_source_type=>'json/collection', p_source=>q'~
      SELECT id, pessoa_id, TO_CHAR(data_entrega,'YYYY-MM-DD') data_entrega,
        frequencia_dias FROM entrega_cesta WHERE pessoa_id=:id ORDER BY data_entrega DESC, id DESC~');
  ORDS.DEFINE_HANDLER(p_module_name=>'gestao_rcc_v2', p_pattern=>'cestas/:id/',
    p_method=>'POST', p_source_type=>'plsql/block', p_source=>q'~
    DECLARE
      freq NUMBER;
      situacao VARCHAR2(20);
      obito DATE;
      ultima DATE;
      hoje DATE := TRUNC(CAST(SYSTIMESTAMP AT TIME ZONE 'America/Sao_Paulo' AS DATE));
    BEGIN
      -- Serializa entregas e edicoes para o mesmo paciente.
      SELECT num_frequencia_cesta,status,data_obito INTO freq,situacao,obito
        FROM pessoa WHERE id=:id FOR UPDATE;
      IF NVL(situacao,'?') <> 'ATIVO' OR obito IS NOT NULL OR freq IS NULL THEN
        ROLLBACK; :status_code:=409; RETURN;
      END IF;
      IF :data_entrega IS NULL OR TO_DATE(:data_entrega,'FXYYYY-MM-DD') <> hoje THEN
        ROLLBACK; :status_code:=422; RETURN;
      END IF;
      SELECT MAX(data_entrega) INTO ultima FROM entrega_cesta WHERE pessoa_id=:id;
      IF ultima IS NOT NULL AND ultima+freq > hoje THEN
        ROLLBACK; :status_code:=409; RETURN;
      END IF;
      INSERT INTO entrega_cesta(pessoa_id,data_entrega,frequencia_dias) VALUES(:id,hoje,freq);
      :status_code:=201;
    EXCEPTION
      WHEN NO_DATA_FOUND THEN ROLLBACK; :status_code:=404;
      WHEN DUP_VAL_ON_INDEX THEN ROLLBACK; :status_code:=409;
      WHEN OTHERS THEN ROLLBACK; :status_code:=400;
    END;~');
  COMMIT;
EXCEPTION WHEN OTHERS THEN ROLLBACK; RAISE;
END;
/
