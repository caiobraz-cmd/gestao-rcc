-- Atualização incremental: preserva validações da 005, GETs e serviços da 008.
BEGIN
ORDS.DEFINE_HANDLER(p_module_name=>'gestao_rcc_v2',p_pattern=>'pessoas/',p_method=>'POST',p_source_type=>'plsql/block',p_source=>q'~DECLARE novo_id NUMBER; BEGIN
 IF :registro IS NOT NULL AND (NOT REGEXP_LIKE(:registro,'^[a-f0-9]{32}$','c')
  OR TRIM(:autor) IS NULL OR LENGTHB(:autor)>120 OR NVL(:perfil,'?') NOT IN ('admin','operador'))
 THEN :status_code:=422; RETURN; END IF;

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

      INSERT INTO pessoa(nome, cpf, data_nascimento, telefone, endereco, status,
        char_diagnostico, char_tratamento, char_medicamento, char_alergia, char_observacoes,
        data_obito, num_frequencia_cesta)
      VALUES(:nome, :cpf, TO_DATE(:data_nascimento,'FXYYYY-MM-DD'), :telefone, :endereco, :status,
        :char_diagnostico, :char_tratamento, :char_medicamento, :char_alergia, :char_observacoes,
        TO_DATE(:data_obito,'FXYYYY-MM-DD'), :num_frequencia_cesta) RETURNING id INTO novo_id;
      INSERT INTO rcc_registro_operacao(registro,pessoa_id,entrega_id,operacao,autor,perfil)
 VALUES(NVL(:registro,LOWER(RAWTOHEX(SYS_GUID()))),novo_id,NULL,'cadastro',
 CASE WHEN :registro IS NOT NULL THEN :autor END,CASE WHEN :registro IS NOT NULL THEN :perfil END);
:status_code := 201;
    EXCEPTION
      WHEN DUP_VAL_ON_INDEX THEN ROLLBACK; :status_code := 409;
      WHEN OTHERS THEN ROLLBACK; :status_code := 400;
    END;~');
ORDS.DEFINE_HANDLER(p_module_name=>'gestao_rcc_v2',p_pattern=>'pessoas/:id',p_method=>'PUT',p_source_type=>'plsql/block',p_source=>q'~BEGIN
 IF :registro IS NOT NULL AND (NOT REGEXP_LIKE(:registro,'^[a-f0-9]{32}$','c')
  OR TRIM(:autor) IS NULL OR LENGTHB(:autor)>120 OR NVL(:perfil,'?') NOT IN ('admin','operador'))
 THEN :status_code:=422; RETURN; END IF;

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
      IF SQL%ROWCOUNT=0 THEN :status_code:=404; ELSE INSERT INTO rcc_registro_operacao(registro,pessoa_id,entrega_id,operacao,autor,perfil)
 VALUES(NVL(:registro,LOWER(RAWTOHEX(SYS_GUID()))),:id,NULL,'alteracao',
 CASE WHEN :registro IS NOT NULL THEN :autor END,CASE WHEN :registro IS NOT NULL THEN :perfil END); :status_code:=200; END IF;
    EXCEPTION
      WHEN DUP_VAL_ON_INDEX THEN ROLLBACK; :status_code:=409;
      WHEN OTHERS THEN ROLLBACK; :status_code:=400;
    END;~');
ORDS.DEFINE_HANDLER(p_module_name=>'gestao_rcc_v2',p_pattern=>'cestas/:id/',p_method=>'POST',p_source_type=>'plsql/block',p_source=>q'~
    DECLARE
      freq NUMBER;
 nova_entrega NUMBER;
      situacao VARCHAR2(20);
      obito DATE;
      ultima DATE;
      hoje DATE := TRUNC(CAST(SYSTIMESTAMP AT TIME ZONE 'America/Sao_Paulo' AS DATE));
    BEGIN

 IF :registro IS NOT NULL AND (NOT REGEXP_LIKE(:registro,'^[a-f0-9]{32}$','c')
  OR TRIM(:autor) IS NULL OR LENGTHB(:autor)>120 OR NVL(:perfil,'?') NOT IN ('admin','operador'))
 THEN :status_code:=422; RETURN; END IF;

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
      INSERT INTO entrega_cesta(pessoa_id,data_entrega,frequencia_dias) VALUES(:id,hoje,freq) RETURNING id INTO nova_entrega;
INSERT INTO rcc_registro_operacao(registro,pessoa_id,entrega_id,operacao,autor,perfil)
 VALUES(NVL(:registro,LOWER(RAWTOHEX(SYS_GUID()))),:id,nova_entrega,'entrega',
 CASE WHEN :registro IS NOT NULL THEN :autor END,CASE WHEN :registro IS NOT NULL THEN :perfil END);
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
