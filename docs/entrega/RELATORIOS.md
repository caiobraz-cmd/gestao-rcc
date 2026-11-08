# Relatórios — 0.7.0-rc1

Acesso exclusivo do administrador pelo menu Relatórios.

- Pacientes: total, ativos, inativos e outras situações; fotografia do cadastro atual, não reconstrução histórica.
- Cestas entregues e serviços registrados: contagem no período inclusive, por data registrada no Oracle em horário de Brasília.
- Movimentação diária: mostra apenas dias com entregas ou serviços.
- CSV: resumo agregado e tabela diária, separados por ponto e vírgula, UTF-8 com BOM. Não exporta CPF, diagnóstico, nomes nem contatos.

São usadas as coleções pessoas/ e registros-operacoes/, já disponíveis após a migração 009. Não há migração adicional.

Registros antigos de cestas e serviços entram nos totais, mesmo sem autoria. Alterações de pacientes não contam como serviços. A referência de cada cesta/serviço é contada uma vez.

Se a API falhar, retornar referência/data inválida ou exceder o limite de paginação do cliente (10.000 registros), nenhum total parcial é exibido. O relatório não é uma transação de snapshot: gravações simultâneas podem alterar o resultado entre a tela e uma exportação posterior. Para volume maior, implementar agregações por período diretamente no banco.

O relatório não substitui um backup: não contém os dados necessários para restaurar os cadastros.
