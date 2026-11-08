-- Instalar somente no módulo gestao_rcc_v2 protegido por OAuth.
DECLARE
 m CONSTANT VARCHAR2(30) := 'gestao_rcc_v2';
BEGIN
 ORDS.DEFINE_TEMPLATE(p_module_name=>m,p_pattern=>'contas/');
 ORDS.DEFINE_HANDLER(p_module_name=>m,p_pattern=>'contas/',p_method=>'GET',p_source_type=>'json/collection',
 p_source=>'SELECT login,nome,ativo,versao FROM rcc_conta_operador ORDER BY nome,login');
 ORDS.DEFINE_HANDLER(p_module_name=>m,p_pattern=>'contas/',p_method=>'POST',p_source_type=>'plsql/block',p_source=>q'~
 BEGIN
 IF :nome IS NULL OR LENGTH(TRIM(:nome))<2 OR LENGTHB(:nome)>120 OR :login IS NULL OR
 NOT REGEXP_LIKE(:login,'^[a-z0-9][a-z0-9._-]{2,39}$','c') OR :senha_hash IS NULL OR
 :senha_hash NOT LIKE 'scrypt:%' OR LENGTHB(:senha_hash)>512 THEN :status_code:=422; RETURN; END IF;
 INSERT INTO rcc_conta_operador(login,nome,senha_hash) VALUES(:login,TRIM(:nome),:senha_hash);
 :status_code:=201;
 EXCEPTION WHEN DUP_VAL_ON_INDEX THEN ROLLBACK; :status_code:=409;
 END;~');
 ORDS.DEFINE_TEMPLATE(p_module_name=>m,p_pattern=>'contas/:usuario/');
 ORDS.DEFINE_HANDLER(p_module_name=>m,p_pattern=>'contas/:usuario/',p_method=>'GET',p_source_type=>'json/collection',
 p_source=>'SELECT login,ativo,versao FROM rcc_conta_operador WHERE login=:usuario');
 ORDS.DEFINE_HANDLER(p_module_name=>m,p_pattern=>'contas/:usuario/',p_method=>'PUT',p_source_type=>'plsql/block',p_source=>q'~
 BEGIN
 IF :acao IN ('ativar','desativar') THEN
 UPDATE rcc_conta_operador SET ativo=CASE :acao WHEN 'ativar' THEN 1 ELSE 0 END,versao=versao+1 WHERE login=:usuario;
 ELSIF :acao='senha' AND :senha_hash LIKE 'scrypt:%' AND LENGTHB(:senha_hash)<=512 THEN
 UPDATE rcc_conta_operador SET senha_hash=:senha_hash,versao=versao+1 WHERE login=:usuario;
 ELSE :status_code:=422; RETURN;
 END IF;
 IF SQL%ROWCOUNT=0 THEN :status_code:=404; ELSE :status_code:=200; END IF;
 END;~');
 ORDS.DEFINE_TEMPLATE(p_module_name=>m,p_pattern=>'conta-login/:usuario/');
 ORDS.DEFINE_HANDLER(p_module_name=>m,p_pattern=>'conta-login/:usuario/',p_method=>'GET',p_source_type=>'json/collection',
 p_source=>'SELECT login,ativo,versao,senha_hash FROM rcc_conta_operador WHERE login=:usuario');
 COMMIT;
EXCEPTION WHEN OTHERS THEN ROLLBACK; RAISE;
END;
/
