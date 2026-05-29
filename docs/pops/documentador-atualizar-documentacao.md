# 📝 Procedimento Operacional Padrão (POP 01)
## Título: Atualização e Manutenção da Documentação do Projeto

* **Objetivo**: Normatizar o processo de edição, revisão e publicação de novos documentos técnicos e modificações no README do sistema, garantindo conformidade com os padrões de qualidade de informação[cite: 1, 2].
* **Responsável**: Documentador (Osvaldo Mazoni Neto)[cite: 1, 2].
* **Quando usar**: Sempre que houver mudanças no escopo do projeto, encerramento de sprints semanais, novos direcionamentos arquiteturais ou atualizações necessárias no manual do usuário[cite: 1, 2].
* **Pré-requisitos**: Branch de documentação isolada criada a partir da `main` e editores de texto compatíveis com sintaxe Markdown (.md)[cite: 1, 2].

### 📑 Passo a Passo Executivo
1. Abra a issue correspondente no GitHub Projects informando qual documento será criado ou alterado[cite: 1, 2].
2. Crie uma branch específica utilizando o prefixo padrão (ex: `sprint-01/sprint-pops-evidencias`)[cite: 1].
3. Abra o repositório local na sua IDE (VS Code) e navegue até a pasta correspondente (`/docs` ou raiz para o `README.md`)[cite: 1, 2].
4. Escreva ou atualize as informações necessárias respeitando a hierarquia de cabeçalhos markdown (`#`, `##`, `###`)[cite: 2].
5. Valide localmente se os hiperlinks internos e caminhos de imagens estão corretos.
6. Realize o commit utilizando o prefixo semântico apropriado: `docs: mensagem descritiva`[cite: 1, 2].
7. Envie as modificações para o servidor remoto e abra o Pull Request solicitando a validação técnica da equipe antes do merge final[cite: 1, 2].

* **Evidências Esperadas**: Histórico de commits semânticos com o marcador `docs:` e arquivos markdown atualizados no repositório[cite: 1, 2].
* **Critérios de Sucesso**: Renderização visual completa e limpa no GitHub, ausência de links quebrados e aprovação do revisor no Pull Request[cite: 2].
* **Referências Utilizadas**: Associação Brasileira de Normas Técnicas (ABNT) e diretrizes de Documentação de Processos baseadas na ISO 9001[cite: 2].