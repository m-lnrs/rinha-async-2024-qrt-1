# curl --header "Content-Type: application/json" --request POST --data '{"valor": 1000, "tipo": "c", "descricao": "descricao"}' http://127.0.0.1:5000/clientes/1/transacoes

from rinha.api import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_not_numeric_url_parameter():
    response = client.post("/clientes/1a/transacoes", json={"valor": 1000, "tipo": "c", "descricao": "descricao"})
    assert response.status_code == 404


