"""Relatórios agregados, sem exportação de dados pessoais ou clínicos."""
import csv
from datetime import date, datetime, timezone, timedelta
from io import StringIO
from flask import Blueprint, Response, render_template, request
from app import ords
from app.cestas import hoje
from app.routes.auth_routes import admin_required

relatorios_bp = Blueprint('relatorios_bp', __name__)


def periodo():
    today = hoje()
    inicio = request.args.get('inicio', today.replace(day=1).isoformat())
    fim = request.args.get('fim', today.isoformat())
    try:
        first, last = date.fromisoformat(inicio), date.fromisoformat(fim)
        if first > last or last > today:
            raise ValueError
    except ValueError:
        raise ValueError('Informe datas válidas, com início anterior ou igual ao fim e sem datas futuras.') from None
    return first, last


def resumo(first, last):
    people = ords.collection('pessoas/')
    # Esta consulta inclui cestas e serviços legados, sem depender de autoria.
    operations = ords.collection('registros-operacoes/')
    active = sum(p.get('status') == 'ATIVO' for p in people)
    inactive = sum(p.get('status') == 'INATIVO' for p in people)
    days, ids = {}, set()
    for item in operations:
        kind = item.get('operacao')
        if kind not in ('entrega', 'servico'):
            continue
        try:
            day = date.fromisoformat(item['quando'][:10])
            identifier = int(item['referencia'])
            if identifier <= 0:
                raise ValueError
        except (ValueError, KeyError, TypeError):
            raise ords.APIError('Há um registro sem data ou referência válida. O relatório não foi gerado.') from None
        if not first <= day <= last or (kind, identifier) in ids:
            continue
        ids.add((kind, identifier))
        count = days.setdefault(day.isoformat(), {'entrega': 0, 'servico': 0})
        count[kind] += 1
    rows = [{'data': key, **days[key]} for key in sorted(days)]
    return {'total':len(people), 'ativos':active,'inativos':inactive,
            'outros':len(people)-active-inactive,'dias':rows,
            'cestas':sum(r['entrega'] for r in rows),'servicos':sum(r['servico'] for r in rows)}


@relatorios_bp.get('/')
@admin_required
def index():
    try:
        first, last = periodo()
    except ValueError as exc:
        return render_template('erro.html',titulo='Período inválido',mensagem=str(exc)),422
    try:
        data = resumo(first,last)
    except ords.APIError:
        return render_template('erro.html',titulo='Relatório indisponível',
            mensagem='Não foi possível obter todos os dados do Oracle. Tente novamente; nenhum total parcial foi apresentado.'),503
    if request.args.get('formato') == 'csv':
        output = StringIO(newline='')
        writer = csv.writer(output, delimiter=';')
        writer.writerow(['Resumo agregado','Inicio','Fim','Quantidade'])
        for label, value in [('Cestas entregues',data['cestas']),('Servicos registrados',data['servicos'])]:
            writer.writerow([label,first.isoformat(),last.isoformat(),value])
        writer.writerow([])
        writer.writerow(['Pacientes - situacao atual','Quantidade'])
        for key,label in [('total','Total'),('ativos','Ativos'),('inativos','Inativos'),('outros','Outras situacoes')]:
            writer.writerow([label,data[key]])
        writer.writerow([])
        writer.writerow(['Data','Cestas entregues','Servicos registrados'])
        for row in data['dias']:
            writer.writerow([row['data'],row['entrega'],row['servico']])
        return Response('\ufeff'+output.getvalue(),mimetype='text/csv',
            headers={'Content-Disposition':f'attachment; filename="relatorio-rcc-{first}-{last}.csv"'})
    return render_template('relatorios.html',titulo='Relatórios',dados=data,inicio=first.isoformat(),
        fim=last.isoformat(),gerado=datetime.now(timezone(timedelta(hours=-3))).strftime('%d/%m/%Y %H:%M'))
