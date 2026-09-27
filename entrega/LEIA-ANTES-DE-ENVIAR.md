# Pacote atualizado — revisão HTTPX

Versão candidata: 0.4.0-rc1, revisão de 27/09/2026.

O ZIP contém código-fonte, iniciador Windows, instruções, configuração de exemplo, definições Oracle, testes e evidências. Não contém ambiente virtual, .env, histórico Git ou banco local de pacientes.

O bloqueio de conexão anterior foi resolvido nas verificações com HTTPX. Passaram 15 testes locais e 11 verificações com Oracle real, incluindo cadastro, edição, inativação e persistência após nova sessão. O cadastro fictício ID 21 ficou inativo. A pasta de evidências preserva também a tentativa anterior que falhou, identificada como histórica.

Use este ZIP atualizado. Após extrair, abra INICIAR.cmd e crie seu usuário e senha na primeira execução. O arquivo .sha256.txt e MANIFESTO-SHA256.json identificam o conteúdo exato deste pacote, mesmo mantendo o número da versão candidata.

Para finalizar a avaliação, ainda é necessário apresentar o produto ao cliente/usuário final e registrar a confirmação. Serviços, cestas e campos médicos continuam pendentes, conforme a documentação. O pacote não deve ser apresentado como versão 1.0 com todo o roadmap concluído.

Para reconstruir o ZIP: .\.venv\Scripts\python.exe tools/empacotar.py.
