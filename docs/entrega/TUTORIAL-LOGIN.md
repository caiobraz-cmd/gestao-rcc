# Como entrar no Gestão RCC

O acesso ao Gestão RCC é separado do painel Oracle APEX.

## Neste computador — acesso já configurado

1. Abra `instance/ACESSO-LOCAL.txt` dentro da pasta do projeto para consultar seu usuário e sua senha. Esse arquivo é privado: não envie ao GitHub ou ao professor.
2. Abra **INICIAR.cmd** e mantenha a janela aberta. Se o sistema já estiver rodando, não abra uma segunda cópia.
3. Acesse **http://127.0.0.1:5000** e use os dados do arquivo.
4. No menu, clique em **Administração**. A conta original desta instalação é o administrador, mesmo que o login se chame `operador`.

## Cadastrar uma pessoa da equipe

1. Em **Administração → Cadastrar operador**, informe nome, login e uma senha de pelo menos 12 caracteres. Clique em **Cadastrar operador**.
2. Entregue o login e a senha à pessoa por um canal privado. Ela entra pelo endereço da instalação com a própria conta; não precisa baixar arquivos, usar terminal nem acessar o Oracle APEX.
3. Em **Contas da equipe**, use **Desativar**, **Reativar** ou **Redefinir senha**. Desativar ou trocar a senha invalida as sessões anteriores na próxima requisição protegida. Operadores não podem administrar contas nem abrir o painel pela URL.

O cadastro acima dá acesso ao sistema. Para cadastrar alguém atendido pela rede, use **Novo paciente**. O endereço `127.0.0.1` funciona apenas no computador que está executando o sistema; esta revisão do painel não foi publicada no Render.

## Trocar a própria senha — operadores

No menu **Minha senha**, informe a senha atual, a nova senha e sua confirmação. Após salvar, entre novamente. As sessões antigas deixam de funcionar na próxima requisição protegida. Se esquecer a senha atual, peça ao administrador para redefini-la no painel. A conta administrativa inicial continua na configuração privada e não usa essa tela.

## Para o responsável técnico — primeira instalação em outro computador

1. Abra a pasta `C:\Users\osval\Desktop\gestao-rcc` no Explorador de Arquivos. Se estiver usando o ZIP, extraia primeiro e abra a pasta extraída.
2. Dê dois cliques em **INICIAR.cmd**. O Windows pode mostrar apenas **INICIAR**. Aguarde a preparação terminar e mantenha essa janela aberta.
3. Quando aparecer **URL base do Oracle ORDS**, pressione **Enter** para aceitar o endereço sugerido.
4. Em **Nome do operador**, digite o usuário que deseja criar, por exemplo `osvaldo`, e pressione **Enter**. Use um nome sem espaços.
5. Em **Crie uma senha de pelo menos 12 caracteres**, digite uma senha escolhida por você e pressione **Enter**. **Enquanto digita, não aparecem letras nem asteriscos: isso é normal.** Na confirmação, digite exatamente a mesma senha e pressione **Enter**.
6. Informe o **ID do cliente OAuth** e o **segredo do cliente** fornecidos pelo responsável pelo Oracle. Essas credenciais são diferentes do login do sistema e não acompanham a entrega. O segredo é digitado de forma oculta. Para o cadastro completo, não deixe as credenciais vazias.
7. Quando a janela informar que o sistema está rodando, abra **http://127.0.0.1:5000** no navegador do mesmo computador.
8. Na tela do Gestão RCC, entre com o usuário e a senha que acabou de criar. Clique em **Entrar**.

## Nas próximas vezes

Abra **INICIAR.cmd**, aguarde iniciar e acesse **http://127.0.0.1:5000**. A configuração já fica salva neste computador e não será solicitada novamente.

Mantenha a janela do sistema aberta enquanto estiver usando. Para encerrar, volte à janela e pressione **Ctrl+C**.

## Se algo não funcionar

- **Nada aparece ao digitar a senha na janela:** é o comportamento normal do campo oculto. Digite e pressione Enter.
- **Senha curta ou confirmação diferente:** abra INICIAR.cmd novamente e refaça o cadastro com pelo menos 12 caracteres e confirmação idêntica.
- **Usuário ou senha inválidos na página:** confira o nome escolhido e a tecla Caps Lock. Não há senha padrão; use os dados criados nesta instalação.
- **Não pediu para criar usuário:** essa pasta já tem uma configuração. Use o usuário e senha criados anteriormente nessa mesma pasta.
- **O navegador não abre o sistema:** confira se a janela do INICIAR.cmd continua aberta e se mostrou o endereço 127.0.0.1:5000.
- **Entrou, mas apareceu erro do Oracle:** o login funcionou; a mensagem se refere à conexão com o banco.

Se precisar de ajuda, copie a mensagem de erro. Não envie sua senha nem o conteúdo do arquivo `.env`.
