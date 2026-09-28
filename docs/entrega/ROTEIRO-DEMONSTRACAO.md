# Demonstração ao cliente — Gestão RCC 0.5.0-rc1

## Preparação

Confirmar base de teste e consentimento para criar registros fictícios. Seguir o README, iniciar a aplicação e verificar que a versão aparece no rodapé. Não usar cadastros reais em prints.

## Roteiro de apresentação

1. Explicar o objetivo e o escopo desta versão: cadastro e consulta de pacientes. Explicar os recursos que permanecem pendentes.
2. Fazer login com o operador configurado. Mostrar que acesso sem login é redirecionado.
3. Abrir Novo Cadastro e informar um nome começando por `TESTE DEMONSTRACAO RCC`, CPF de teste aprovado para a base, nascimento fictício, telefone e endereço fictícios.
4. Salvar, localizar pelo nome e abrir os detalhes. Recarregar a página para demonstrar que o registro foi consultado novamente no Oracle.
5. Editar o nome acrescentando `EDITADO`, salvar e consultar novamente. Sair e entrar para confirmar que os dados não dependem da sessão.
6. Tentar cadastrar um CPF com 11 dígitos iguais. Mostrar a mensagem de validação e confirmar que não surgiu novo paciente.
7. Marcar o registro fictício como Inativo, salvar e conferir a mudança na lista. Não excluir registros existentes do cliente.
8. Mostrar os campos clínicos fictícios, definir uma frequência de cesta, registrar a primeira entrega e mostrar histórico e próxima data. Explicar o bloqueio de entrega antecipada e a suspensão por inatividade/óbito. Serviços continuam pendentes.

## Evidências a guardar

Lista principal; detalhe do registro de teste persistido; edição confirmada; rejeição do CPF inválido; versão visível. Cada captura deve ter legenda com data, operação e resultado. Os resultados devem ser registrados em `docs/evidences/produto/README.md`.

## Confirmação da apresentação

Preencher somente após a demonstração efetiva:

- Data e forma da apresentação: **pendente**.
- Papel do participante (evitar dados pessoais desnecessários): **pendente**.
- Versão apresentada: **pendente**.
- Fluxos vistos e aceitos: **pendente**.
- Dificuldades relatadas: **pendente**.
- Itens acordados para depois: **pendente**.

Uma confirmação do professor só substitui a do cliente se ele autorizar esse formato de demonstração.
