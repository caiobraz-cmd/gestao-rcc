"""Validação antes de enviar dados ao Oracle."""
import re
from datetime import date

PATIENT_FIELDS = ('ds_nome', 'num_cpf', 'dt_nascimento', 'num_telefone', 'char_endereco',
                  'char_diagnostico', 'char_tratamento', 'char_medicamento', 'char_alergia', 'char_observacoes')


def valid_cpf(value):
    if len(value) != 11 or len(set(value)) == 1:
        return False
    for length in (9, 10):
        digit = (sum(int(value[i]) * (length + 1 - i) for i in range(length)) * 10) % 11
        if digit % 10 != int(value[length]):
            return False
    return True


def patient(form, baskets=False, editing=False):
    basic_fields = ('ds_nome', 'num_cpf', 'dt_nascimento', 'num_telefone', 'char_endereco')
    data = {field: form.get(field, '').strip() or None for field in basic_fields}
    errors = []
    if not data['ds_nome'] or len(data['ds_nome']) < 3 or len(data['ds_nome']) > 150:
        errors.append('Informe um nome entre 3 e 150 caracteres.')
    cpf = re.sub(r'[.\-\s]', '', data['num_cpf'] or '')
    if not cpf.isascii() or not cpf.isdigit() or not valid_cpf(cpf):
        errors.append('Informe um CPF válido com 11 dígitos.')
    data['num_cpf'] = cpf
    try:
        birth = date.fromisoformat(data['dt_nascimento'] or '')
        if birth > date.today():
            raise ValueError
    except ValueError:
        errors.append('Informe uma data de nascimento válida, que não esteja no futuro.')
    for field in basic_fields:
        if data[field] and len(data[field]) > 2000:
            errors.append('Um dos campos ultrapassou o limite de 2000 caracteres.')
    for field, maximum in [('num_telefone', 20), ('char_endereco', 255)]:
        if len((data[field] or '').encode('utf-8')) > maximum:
            errors.append(f'O campo {"telefone" if field == "num_telefone" else "endereço"} excede o tamanho permitido pelo Oracle.')
    if len((data['ds_nome'] or '').encode('utf-8')) > 150:
        errors.append('O nome excede o tamanho permitido pelo Oracle.')
    data['status'] = form.get('status', 'ATIVO')
    if data['status'] not in ('ATIVO', 'INATIVO'):
        errors.append('Selecione uma situação válida: ativo ou inativo.')
    if baskets:
        frequency = form.get('frequencia_cesta', '').strip()
        try:
            data['num_frequencia_cesta'] = int(frequency) if frequency else None
            if frequency and not 1 <= data['num_frequencia_cesta'] <= 365:
                raise ValueError
        except ValueError:
            errors.append('A frequência da cesta deve ser de 1 a 365 dias, ou ficar vazia.')
    return data, errors
