"""Agenda de entregas; a frequência é definida pelo responsável pelo cadastro."""
from datetime import date, datetime, timedelta, timezone


def hoje():
    # Mesmo calendário civil usado pelo handler Oracle (America/Sao_Paulo).
    return datetime.now(timezone(timedelta(hours=-3))).date()


def agenda(pessoa, dia=None):
    dia = dia or hoje()
    result = {'situacao': 'Não recebe', 'pode_entregar': False, 'proxima': None, 'atraso': 0}
    if pessoa.get('data_obito') or pessoa.get('status') != 'ATIVO':
        return {**result, 'situacao': 'Suspenso'}
    value = pessoa.get('num_frequencia_cesta')
    if value in (None, ''):
        return result
    try:
        frequency = int(value)
        if str(frequency) != str(value) or not 1 <= frequency <= 365:
            raise ValueError
        raw = pessoa.get('dt_ultima_cesta')
        if not raw:
            return {**result, 'situacao': 'Primeira entrega pendente', 'pode_entregar': True}
        last = date.fromisoformat(str(raw)[:10])
        if last > dia:
            raise ValueError
        due = last + timedelta(days=frequency)
    except (ValueError, TypeError, OverflowError):
        return {**result, 'situacao': 'Revisar cadastro'}
    if last == dia:
        label = 'Entregue hoje'
    elif due < dia:
        label = 'Em atraso'
    elif due == dia:
        label = 'Entrega prevista hoje'
    else:
        label = 'Agendada'
    return {**result, 'situacao': label, 'proxima': due.isoformat(),
            'atraso': max(0, (dia - due).days), 'pode_entregar': due <= dia}
