from loguru import logger
from rinha.api import async_pool
from psycopg.rows import dict_row
from rinha.model import Client, Balance, Response, Statement, Transaction

async def fetch_client_async(client_number):
    await async_pool.open()
    async with async_pool.connection() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("""SELECT * FROM client WHERE number = %s""", (client_number,))
            rs = await cursor.fetchone()
            return Client(**dict(zip(("number", "name", "limit_amount"), rs)))

async def transact_async(transaction_type, client_number, amount, description):
    if transaction_type == 'c':
        await async_pool.open()
        async with async_pool.connection() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("""SELECT * FROM credit(%s, %s, %s)""", (client_number, amount, description))
                rs = await cursor.fetchone()
                return Response(**dict(zip(("balance", "success", "message"), rs)))

    if transaction_type == 'd':
        await async_pool.open()
        async with async_pool.connection() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("""SELECT * FROM debit(%s, %s, %s)""", (client_number, amount, description))
                rs = await cursor.fetchone()
                return Response(**dict(zip(("balance", "success", "message"), rs)))

    return None

async def fetch_statement_async(client_number):
    await async_pool.open()
    async with async_pool.connection() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("""SELECT balance.amount AS balance, NOW() AS done, client.limit_amount FROM client JOIN balance ON balance.client_number = client.number WHERE client.number = %s""", (client_number,))
            rs = await cursor.fetchone()
            statement = Statement(**dict(zip(("balance", "done", "limit_amount"), rs))) if rs else None

            if statement:
                await cursor.execute("""SELECT number, client_number, amount, type as transaction_type, description, done FROM transaction WHERE transaction.client_number = %s ORDER BY done DESC LIMIT 10""", (client_number,))
                res = await cursor.fetchall()
                statement.transactions = [Transaction(**dict(zip(("number", "client_number", "amount", "transaction_type", "description", "done"), t))) for t in res]
                return statement

    return None
