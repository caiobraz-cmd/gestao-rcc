# Atualização instalada — 0.5.0-rc1

## Situação real

**Instalada e ativada no Oracle em 27/09/2026.** Campos e histórico criados, módulo protegido publicado
e cliente OAuth configurado localmente, fora do Git. Passaram 28 testes locais e 23 verificações reais,
incluindo concorrência, autenticação, edição, óbito e persistência. A entrega pelo navegador também foi confirmada.
Os dois cadastros preexistentes foram preservados em `BKP_PESSOA_20260927_V05` antes da migração.
O ZIP original da 0.4.0-rc1 continua preservado. Não use evidências da 0.4 como validação da 0.5.

## O que foi recuperado

O código anterior possuía diagnóstico, tratamentos, medicamentos, alergias e observações,
além de óbito na edição. O controle de cestas usava uma lista fictícia; o botão de entrega
somente mostrava uma mensagem. A próxima versão inclui esses campos, validação e uma operação
de entrega que exige confirmação posterior no Oracle.

## Como funcionam as cestas

- O responsável informa a frequência em dias: 7, 15, 20, 30 ou qualquer inteiro de 1 a 365.
- Campo vazio significa que a pessoa não recebe cesta.
- Sem entrega anterior, a situação é **Primeira entrega pendente**.
- Próxima entrega = data da última entrega + frequência atual. Alterar a frequência recalcula a próxima data; não altera o histórico.
- Na data prevista, aparece **Entrega prevista hoje**. Atraso só começa no dia seguinte.
- **Registrar entrega de cesta hoje** fica disponível na primeira entrega ou a partir da data prevista.
- Entregas antecipadas, retroativas ou duplicadas no mesmo dia não são permitidas nesta versão.
- Inativos ou pessoas com óbito não recebem novas entregas. Informar óbito torna o cadastro inativo.
- Cada entrega preserva sua data e a frequência vigente. Não há edição ou exclusão de histórico na interface.
- O calendário de entrega usa UTC−03:00 no aplicativo e America/Sao_Paulo no Oracle. Revisar se as regras de fuso do Brasil mudarem.

Esse cálculo organiza datas. Não decide elegibilidade social ou clínica; a equipe define quem recebe e a frequência.

## Instalação em outra base Oracle

Estas etapas já foram executadas na base GESTAORCC. **Não repita os scripts de criação nessa base.**

1. Exportar os dados e os metadados atuais. Preferir uma base de homologação com dados fictícios.
2. Conferir se a tabela PESSOA corresponde a `database/schema.sql` e se os objetos da 0.5 ainda não existem.
3. Executar `database/005-cadastro-cestas.sql` uma única vez em SQL Scripts. Ele acrescenta campos e cria ENTREGA_CESTA, sem apagar cadastros.
4. Executar `database/005-ords-v2.sql`. Ele cria o módulo `gestao_rcc_v2`, caminho `/rcc-v2/`, inicialmente **NOT_PUBLISHED**, com privilégio `gestao_rcc_v2.acesso` e papel `gestao_rcc_v2_operador`.
5. Configurar um cliente OAuth autorizado somente para esse papel. Guardar suas credenciais fora do repositório e obter um token de acesso. A senha do operador local não é um token Oracle.
6. Publicar o módulo para homologação após revisar a proteção. Confirmar que uma consulta sem token é recusada e que o token autorizado permite os fluxos esperados. Não tornar o módulo público para contornar erros.
7. No `.env` local, configurar a URL base e as credenciais próprias do cliente; então ativar:

```dotenv
API_BASE_URL=https://oracleapex.com/ords/gestaorcc/rcc-v2/
API_TOKEN=
ORDS_CLIENT_ID=SUBSTITUIR_LOCALMENTE
ORDS_CLIENT_SECRET=SUBSTITUIR_LOCALMENTE
ORDS_DADOS_MEDICOS_HABILITADOS=true
ORDS_CESTAS_HABILITADAS=true
ORDS_SERVICOS_HABILITADOS=false
```

8. Reiniciar o aplicativo e executar a homologação abaixo. Nunca versionar o `.env`.

O aplicativo obtém e renova tokens automaticamente com o cliente OAuth, guardando o token somente em memória. Erros de autenticação não repetem automaticamente uma gravação. Nunca compartilhar credenciais em evidências ou repositórios.
O novo módulo não implementa serviços nem exclusão de pacientes. O módulo antigo `/rcc/` permanece intacto;
antes de qualquer uso com dados reais, revisar também o acesso público aos seus endpoints e bloquear alterações anônimas.
O login local sozinho não protege uma API pública.

**Cuidados na migração:** DDL Oracle faz commit implícito; ROLLBACK não desfaz a adição de colunas ou a criação da tabela.
Se um script falhar parcialmente, conferir o estado antes de repetir. O script de módulo redefine os seus próprios handlers se executado novamente.
Não remover colunas ou histórico para voltar à versão anterior: desligar as flags e usar a API antiga permite voltar ao cadastro básico,
mas registros com óbito continuam sujeitos à restrição de situação inativa no banco.

## Roteiro de homologação e limites da verificação

Cadastro completo, edição, limpeza de campo, primeira entrega, concorrência, duplicidade/inativo,
óbito e nova instância autenticada foram aprovados no Oracle. Datas-limite e atraso foram testados localmente;
não foram criadas entregas retroativas no Oracle. A API antiga foi preservada, e seus testes anteriores continuam identificados como 0.4.

| Fluxo | Resultado esperado |
|---|---|
| Cadastro fictício com todos os campos | Nova sessão e nova consulta mantêm os mesmos textos e frequência |
| Edição dos textos e limpeza de campo opcional | Alterações persistidas sem mexer no histórico |
| Datas inválidas, frequência 0/366 e texto acima do limite | Rejeição e formulário preservado |
| Primeira entrega | Um registro no histórico e última entrega atualizada |
| Duplo clique e duas sessões simultâneas | Apenas uma entrega; verificar diretamente a tabela |
| Entrega antes do intervalo, inativo ou óbito | Rejeição sem inserir registro |
| Paciente com entrega vencendo hoje e outro em atraso | Situações corretas, conforme datas fictícias preparadas em homologação |
| Alteração da frequência | Próxima data recalculada; frequência das entregas antigas preservada |
| Falha de rede durante a gravação | Consultar o histórico antes de repetir; não presumir sucesso ou falha de persistência |
| API sem autenticação | Nenhum dado clínico retornado; escrita também recusada |
| Entrega 0.4 / API antiga | Fluxos básicos continuam operando |

## Verificação local realizada

`python -m unittest discover -s tests -v`: **28 testes aprovados**.
Cobrem regressões do cadastro básico, campos clínicos, óbito, datas-limite, atraso, primeira entrega,
impedimento de repetição/antecipação, preservação do histórico e confirmação de gravação.
As verificações reais complementares estão em `docs/evidences/v05-oracle/`, separadas da prévia simulada.

## Referência técnica

[Referência oficial ORDS 26.2](https://docs.oracle.com/en/database/oracle/oracle-rest-data-services/26.2/orddg/ORDS-reference.html),
consultada em 27/09/2026: definição de módulos, handlers, papéis e privilégios. O módulo novo inicia sem publicação para permitir configurar e conferir seu acesso antes da ativação.
