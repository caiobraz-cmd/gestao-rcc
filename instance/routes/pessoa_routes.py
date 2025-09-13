# =====================================================================================
# ARQUIVO DE ROTAS PARA A GESTÃO DE PESSOAS (BACK-END)
#
# Olá, colega do Front-end!
#
# Este arquivo contém toda a lógica do servidor para gerenciar as pessoas.
# Cada função abaixo corresponde a uma URL específica que você pode usar
# para listar, criar, editar ou deletar uma pessoa.
#
# O "contrato" é o seguinte: você monta o HTML e os formulários,
# e eu cuido de salvar e buscar os dados no banco.
#
# Qualquer dúvida, fale com seu parceiro de back-end! :)
# =====================================================================================

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from instance.models.pessoa import Pessoa

# O 'Blueprint' organiza nossas rotas.
# O 'url_prefix' significa que TODAS as URLs deste arquivo começarão com '/pessoas'.
# Exemplo: a rota '/' na verdade será '/pessoas/', a rota '/novo' será '/pessoas/novo', e assim por diante.
pessoa_bp = Blueprint(
    'pessoa_bp',
    __name__,
    template_folder='../templates',
    url_prefix='/pessoas'
)

# --- ROTA PARA LISTAR TODAS AS PESSOAS (READ) ---
@pessoa_bp.route('/')
def listar():
    """
    URL: GET /pessoas/
    FUNÇÃO: Busca todas as pessoas cadastradas no banco de dados.
    FRONT-END: Envia uma lista de objetos 'pessoa' para o template 'listar.html'.
               Você deve usar essa lista para criar a tabela ou a listagem na tela.
    """
    # 1. Busca todos os registros da tabela 'Pessoa' no banco de dados.
    pessoas = Pessoa.query.all()
    # 2. Renderiza o arquivo 'listar.html' e envia a lista 'pessoas' para ele.
    return render_template('listar.html', pessoas=pessoas)


# --- ROTA PARA CADASTRAR UMA NOVA PESSOA (CREATE) ---
@pessoa_bp.route('/novo', methods=['GET', 'POST'])
def novo():
    """
    URL: GET /pessoas/novo  -> Para exibir o formulário de cadastro.
         POST /pessoas/novo -> Para receber os dados do formulário e salvar.
    FUNÇÃO: Controla a criação de uma nova pessoa.
    FRONT-END: No seu formulário em 'novo.html', use method="POST".
               Cada <input> deve ter um atributo 'name' correspondente
               (ex: <input name="nome">, <input name="cpf">, etc.).
    """
    # Verifica se o formulário foi enviado (método POST).
    if request.method == 'POST':
        # 1. Coleta todos os dados enviados pelo formulário.
        nome = request.form.get('nome')
        cpf = request.form.get('cpf')
        idade = request.form.get('idade')
        telefone = request.form.get('telefone')
        endereco = request.form.get('endereco')
        diagnostico = request.form.get('diagnostico')
        tratamentos = request.form.get('tratamentos')
        medicamentos = request.form.get('medicamentos')
        alergias = request.form.get('alergias')
        historico_medico = request.form.get('historico_medico')
        observacoes = request.form.get('observacoes')

        # 2. Validação simples para campos obrigatórios.
        if not nome or not cpf or not idade:
            flash('Nome, CPF e Idade são campos obrigatórios.', 'warning')
            # Devolve o usuário para o formulário, mantendo os dados que ele já digitou.
            return render_template('novo.html', form_data=request.form)

        # 3. Cria um novo objeto 'Pessoa' em memória com os dados coletados.
        nova_pessoa = Pessoa(
            nome=nome,
            cpf=cpf,
            idade=idade,
            telefone=telefone,
            endereco=endereco,
            diagnostico=diagnostico,
            tratamentos=tratamentos,
            medicamentos=medicamentos,
            alergias=alergias,
            historico_medico=historico_medico,
            observacoes=observacoes
        )

        try:
            # 4. Tenta salvar o novo objeto no banco de dados.
            db.session.add(nova_pessoa)
            db.session.commit()
            flash('Pessoa cadastrada com sucesso!', 'success')
            # 5. Se tudo der certo, redireciona para a página de listagem.
            return redirect(url_for('pessoa_bp.listar'))
        except Exception as e:
            # Em caso de erro (ex: CPF duplicado), desfaz a operação e mostra uma mensagem.
            db.session.rollback()
            flash(f'Erro ao cadastrar pessoa: Dados inválidos ou CPF já cadastrado.', 'danger')

    # Se a requisição for GET, apenas mostra a página com o formulário em branco.
    return render_template('novo.html')


# --- ROTA PARA ATUALIZAR UMA PESSOA EXISTENTE (UPDATE) ---
@pessoa_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    """
    URL: GET /pessoas/editar/<id>  -> Para exibir o formulário com os dados da pessoa.
         POST /pessoas/editar/<id> -> Para salvar as alterações.
    FUNÇÃO: Controla a edição de uma pessoa específica, identificada pelo 'id' na URL.
    FRONT-END: No template 'editar.html', você receberá um objeto 'pessoa'.
               Use os dados desse objeto para preencher os 'value' dos campos do formulário.
               Ex: <input name="nome" value="{{ pessoa.nome }}">.
    """
    # 1. Busca a pessoa pelo 'id' fornecido na URL. Se não encontrar, retorna erro 404.
    pessoa = Pessoa.query.get_or_404(id)

    # 2. Se o formulário de edição for enviado (POST), atualiza os dados.
    if request.method == 'POST':
        pessoa.nome = request.form.get('nome')
        pessoa.cpf = request.form.get('cpf')
        pessoa.idade = request.form.get('idade')
        pessoa.telefone = request.form.get('telefone')
        pessoa.endereco = request.form.get('endereco')
        pessoa.diagnostico = request.form.get('diagnostico')
        pessoa.tratamentos = request.form.get('tratamentos')
        pessoa.medicamentos = request.form.get('medicamentos')
        pessoa.alergias = request.form.get('alergias')
        pessoa.historico_medico = request.form.get('historico_medico')
        pessoa.observacoes = request.form.get('observacoes')

        try:
            # 3. Salva as alterações no banco de dados.
            db.session.commit()
            flash('Pessoa atualizada com sucesso!', 'success')
            # 4. Redireciona para a página de listagem.
            return redirect(url_for('pessoa_bp.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar pessoa.', 'danger')

    # 5. Se for GET, mostra o 'editar.html' com os campos já preenchidos.
    return render_template('editar.html', pessoa=pessoa)


# --- ROTA PARA DELETAR UMA PESSOA (DELETE) ---
@pessoa_bp.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    """
    URL: POST /pessoas/deletar/<id>
    FUNÇÃO: Deleta uma pessoa do banco de dados com base no 'id'.
    FRONT-END: Na página de listagem, o botão "Deletar" de cada pessoa deve
               estar dentro de um <form> que envia um POST para esta URL.
               Ex: <form action="/pessoas/deletar/{{ pessoa.id }}" method="POST">
                       <button type="submit">Deletar</button>
                   </form>
    """
    # 1. Busca a pessoa a ser deletada. Se não existir, retorna erro 404.
    pessoa = Pessoa.query.get_or_404(id)
    try:
        # 2. Remove a pessoa do banco de dados.
        db.session.delete(pessoa)
        db.session.commit()
        flash('Pessoa deletada com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao deletar pessoa.', 'danger')

    # 3. Após deletar, redireciona de volta para a página de listagem.
    return redirect(url_for('pessoa_bp.listar'))