# Evidências do produto — 0.4.0-rc1

**Revisão validada em 27/09/2026:** integração Flask/Oracle real, com dados fictícios autorizados. Esta pasta não contém conversas de IA, credenciais ou sessões do painel Oracle.

## Resultados atuais

| Arquivo | O que comprova |
|---|---|
| `testes-locais.txt` | 15 testes da aplicação com API simulada; não substituem o teste real abaixo. |
| `oracle-real-20260927T050620.json` | 11 verificações concluídas com Oracle real: login, listagem, entrada inválida sem criação, cadastro, detalhes, edição, inativação, saída, proteção, nova sessão e persistência. Registro fictício ID 21. |
| `diagnostico-httpx-aprovado.json` | Consulta real retornando JSON pelo cliente corrigido; somente metadados, sem conteúdo dos pacientes. |
| `01-login-versao.png` | Login e versão identificada. |
| `02-cpf-invalido.png` | Rejeição de CPF inválido no navegador, preservando os campos. |
| `04-saida.png` | Retorno ao login depois de sair. |
| `05-listagem-oracle.png` | Tela principal com busca pelo registro fictício gravado no Oracle. |
| `06-detalhes-oracle.png` | Leitura do registro de teste persistido, incluindo situação inativa. |
| `07-edicao-confirmada.png` | Edição realizada pela interface e confirmação por nova consulta ao Oracle. |

Os horários dos arquivos JSON estão em UTC. As capturas de login usam um operador temporário; não existe senha padrão distribuída. O registro fictício permanece inativo para não confundir a demonstração. O histórico da API pode ser consultado novamente após a sessão, como verificado no relatório.

As capturas 05 a 07 foram conferidas visualmente em 27/09/2026. Depois do teste integrado, o endereço do registro ID 21 foi editado novamente pelo navegador para `Endereco ficticio - edicao confirmada pelo navegador`, com confirmação de persistência. O relatório integrado descreve a execução anterior a essa última edição. O processo de verificação foi encerrado; `INICIAR.cmd` inicia a instalação com o operador escolhido pelo usuário.

## Registros anteriores — falha resolvida na revisão atual

`oracle-real-20260927T000041.json`, `diagnostico-conexao.json` e `03-falha-conexao-oracle.png` documentam a falha inicial, antes da adoção do HTTPX. Não representam o resultado aprovado mais recente. Foram preservados para não apagar o resultado dos testes anteriores.

## O que ainda falta

A apresentação ao cliente/usuário final e sua confirmação não foram realizadas por estes testes. Use [o roteiro](../../entrega/ROTEIRO-DEMONSTRACAO.md). Serviços, cestas e campos médicos continuam fora do escopo habilitado; veja [limitações](../../entrega/LIMITACOES.md).
