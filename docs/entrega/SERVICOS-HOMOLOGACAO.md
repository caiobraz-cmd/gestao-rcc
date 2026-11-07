# Serviços por paciente: roteiro de homologação

Revisão de 06/11/2026. O contrato foi instalado em GESTAORCC e homologado com o Oracle real usando a aplicação local. O Render ainda precisa receber a revisão antes de ativar serviços.

## Resultado da homologação

- Antes da instalação: tabela e módulo presentes; nenhum template de serviços existente. Após o script, o catálogo confirmou GET e POST em `servicos/:id/`.
- Sem credenciais, GET e POST retornaram 401. O Oracle rejeitou um nome de dois caracteres com 422; o formulário também rejeitou a entrada e a contagem de registros permaneceu igual.
- Pelo formulário Flask, foi gravado o serviço fictício de ID 1 no paciente de teste 41. A consulta ao Oracle confirmou nome, descrição, data e vínculo. Após logout e novo login, o histórico do paciente 41 exibiu o serviço e o do paciente de teste 42 não o exibiu.
- A flag foi habilitada apenas no processo de teste. Esta verificação não comprova a publicação do recurso no Render.

## Pré-requisitos

Usar uma base de homologação com dados fictícios, tabela `SERVICO_PRESTADO` e módulo `gestao_rcc_v2` protegido pelo privilégio da 0.5. Verificar se o caminho `servicos/:id/` está livre; se já existir, exportar e revisar os handlers antes de substituir. Não executar novamente os scripts da 0.5.

1. No SQL Workshop, aplicar `database/006-ords-servicos.sql` como script no schema de homologação. Ele define GET e POST em `servicos/:id/`; o paciente vem da URL e o banco atribui a data.
2. Sem token, confirmar que o módulo recusa GET e POST. Com o cliente OAuth de homologação, confirmar que GET para um paciente fictício devolve uma coleção JSON.
3. Habilitar `ORDS_SERVICOS_HABILITADOS=true` **somente na aplicação de homologação com esta revisão** e reiniciar. Entrar, abrir o paciente A e registrar um serviço identificado como TESTE. Depois de sair e entrar, conferir nome, descrição e data no histórico de A. Confirmar que o serviço não aparece no paciente B.
4. Tentar um nome com dois caracteres e verificar que a linha não foi criada. Registrar versão, resultado, ambiente e qualquer falha sem incluir credenciais ou dados pessoais.
5. Se a homologação falhar, manter a flag desativada no ambiente publicado. Desativar a flag remove a função da interface, mas não desinstala o endpoint Oracle.

## Verificações já realizadas em 06/11

O cliente OAuth local recebeu token e conseguiu ler a coleção protegida no Oracle. O Render respondeu em `/ping` com versão `0.5.0-rc1`; sem sessão, a raiz redirecionou para login e a tela de login respondeu 200. Esses testes são distintos: a consulta local não comprova a conexão a partir do Render.

Em seguida, o teste no próprio Render com o operador autorizado confirmou login (302 para a raiz), consulta da listagem protegida (200, rota que lê o ORDS) e saída (302). Nenhum cadastro foi criado ou alterado. A suíte local passou nos 28 testes, incluindo o fluxo simulado de serviço e o filtro do histórico por paciente.
