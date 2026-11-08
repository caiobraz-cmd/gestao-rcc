# Revisão de dependências — 07/11/2026

Escopo: dependências de execução declaradas em requirements.txt, incluindo as dependências indiretas resolvidas pela ferramenta. A auditoria foi feita com pip-audit 2.10.1, em ambiente separado do aplicativo, usando a base pública do PyPI.

| Biblioteca | Antes | Depois |
|---|---|---|
| Flask | 3.0.0 | 3.1.3 |
| Werkzeug | 3.0.1 | 3.1.9 |
| python-dotenv | 1.0.0 | 1.2.2 |

- Antes: 19 pacotes resolvidos, 17 ocorrências reportadas em três pacotes, correspondentes a 10 identificadores distintos (há identificadores repetidos no retorno).
- Depois: 19 pacotes resolvidos e nenhum alerta conhecido nessa consulta.
- Os 43 testes locais passaram com as três versões atualizadas; pip check não encontrou dependências incompatíveis. Login e consultas de pacientes, contas e rastreabilidade passaram com o Oracle real, sem alteração de cadastros.
- requirements-antes.txt preserva a entrada original; antes.json e depois.json preservam as saídas da ferramenta.
- A versão de Gunicorn foi mantida. Esta revisão foi executada no Windows; não testa o processo Gunicorn no Linux.

## Reprodução

Instalar pip-audit em um ambiente separado e executar:

```powershell
python -m pip_audit -r requirements.txt --progress-spinner off --desc off -f json -o resultado.json
```

Uma consulta sem alertas não garante ausência de falhas: a ferramenta identifica vulnerabilidades conhecidas nos pacotes, não audita o código da aplicação, as permissões Oracle, o sistema operacional ou as configurações da nuvem. Dependências indiretas não estão travadas em arquivo de lock; uma instalação futura pode resolver versões diferentes.

Referências primárias consultadas: [pip-audit](https://github.com/pypa/pip-audit), [Flask](https://flask.palletsprojects.com/en/stable/changes/), [Werkzeug](https://werkzeug.palletsprojects.com/en/stable/changes/), [python-dotenv](https://github.com/theskumar/python-dotenv/blob/main/CHANGELOG.md).
