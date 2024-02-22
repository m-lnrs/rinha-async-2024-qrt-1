from rinha.api import app
from rinha.persistence import dao
from rinha.model import Transaction
from fastapi import Request, Response

@app.post("/clientes/{client_number}/transacoes", status_code=200)
async def transaction(client_number: int | None, request: Request, response: Response):
    if not request.json:
        response.status_code = 422
        return "BAD REQUEST"

    client = await dao.fetch_client_async(client_number)
    if not client:
        response.status_code = 404
        return "CLIENT NOT FOUND"

    transaction = await request.json()

    try:
        transaction_type = transaction["tipo"]
        transaction_amount = transaction["valor"]
        transaction_description = transaction["descricao"]

        if not transaction_amount or not isinstance(transaction_amount, int) or transaction_amount <= 0 or not transaction_type or transaction_type not in ['c', 'd'] or not transaction_description or len(transaction_description) > 10:
            response.status_code = 422
            return "BAD REQUEST"

        res = await dao.transact_async(transaction_type, client_number, transaction_amount, transaction_description)
        if not res.success:
            response.status_code = 422
            return "NON-SUFFICIENT FUNDS"
    except KeyError:
        response.status_code = 422
        return "BAD REQUEST"

    return { "limite" : client.limit_amount, "saldo" : res.balance }

@app.get("/clientes/{client_number}/extrato", status_code=200)
async def statement(client_number: int | None, response: Response):
    res = await dao.fetch_statement_async(client_number)
    if not res:
        response.status_code = 404
        return "CLIENT NOT FOUND"

    balance = {
        "total": res.balance,
        "data_extrato": res.done.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "limite": res.limit_amount,
    }

    trs = [{
        "valor": transaction.amount,
        "tipo": transaction.transaction_type,
        "descricao": transaction.description,
        "realizada_em": transaction.done.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
    } for transaction in res.transactions ]

    return { "saldo": balance, "ultimas_transacoes": trs }
