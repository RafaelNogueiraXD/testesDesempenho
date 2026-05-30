# Testes de Desempenho — JMeter

## Pré-requisitos

- [Apache JMeter](https://jmeter.apache.org/download_jmeter.cgi) instalado
- Backend rodando: `cd backend && uv run python run.py`
- Base URL: `http://localhost:5000`

---

## Configuração base do Test Plan

1. Abra o JMeter e crie um novo **Test Plan**
2. Adicione um **Thread Group** (clique direito no Test Plan → Add → Threads → Thread Group)
3. Configure conforme o cenário desejado (ver tabela abaixo)
4. Adicione um **HTTP Request Defaults** (clique direito no Thread Group → Add → Config Element → HTTP Request Defaults):
   - **Server Name:** `localhost`
   - **Port:** `5000`
   - **Protocol:** `http`

---

## Configurações de Thread Group por cenário

| Cenário          | Threads (usuários) | Ramp-Up (s) | Loop Count |
|------------------|--------------------|-------------|------------|
| Carga leve       | 10                 | 5           | 10         |
| Carga moderada   | 50                 | 10          | 20         |
| Carga pesada     | 200                | 20          | 50         |
| Pico (spike)     | 500                | 1           | 5          |

---

## Rotas para testar

### 1. GET /api/produtos — Listar todos os produtos

| Campo       | Valor             |
|-------------|-------------------|
| Method      | GET               |
| Path        | `/api/produtos`   |
| Body        | —                 |

### 2. GET /api/produtos/{id} — Buscar produto por ID

| Campo       | Valor                  |
|-------------|------------------------|
| Method      | GET                    |
| Path        | `/api/produtos/1`      |
| Body        | —                      |

> Substitua `1` por um ID válido após cadastrar produtos.

### 3. POST /api/produtos — Cadastrar produto

| Campo        | Valor                    |
|--------------|--------------------------|
| Method       | POST                     |
| Path         | `/api/produtos`          |
| Content-Type | `application/json`       |

**Body (JSON):**
```json
{
  "nome": "Produto Teste",
  "descricao": "Criado pelo JMeter",
  "preco": 99.90,
  "quantidade": 10
}
```

> **Passos no JMeter:**
> 1. No HTTP Request, selecione a aba **Body Data** e cole o JSON acima
> 2. Clique com o botão direito no HTTP Request → **Add → Config Element → HTTP Header Manager**
> 3. Clique em **Add** e preencha:
>    - Name: `Content-Type`
>    - Value: `application/json`
>
> ⚠️ Sem esse header o servidor retorna **415 Unsupported Media Type**.

### 4. PUT /api/produtos/{id} — Editar produto

| Campo        | Valor                    |
|--------------|--------------------------|
| Method       | PUT                      |
| Path         | `/api/produtos/1`        |
| Content-Type | `application/json`       |

**Body (JSON):**
```json
{
  "nome": "Produto Editado",
  "preco": 149.90,
  "quantidade": 20
}
```

### 5. DELETE /api/produtos/{id} — Deletar produto

| Campo       | Valor                   |
|-------------|-------------------------|
| Method      | DELETE                  |
| Path        | `/api/produtos/1`       |
| Body        | —                       |

---

## Listeners recomendados

Adicione os listeners abaixo ao Thread Group (Add → Listener):

| Listener                    | Finalidade                                        |
|-----------------------------|---------------------------------------------------|
| **View Results Tree**       | Ver cada request/response individualmente         |
| **Summary Report**          | Média, min, max, throughput e % de erro           |
| **Aggregate Report**        | Percentis (90%, 95%, 99%) e desvio padrão         |
| **Response Time Graph**     | Visualizar latência ao longo do tempo             |
| **Active Threads Over Time**| Ver ramp-up dos usuários no gráfico               |

---

## Assertions (validações)

Adicione **Response Assertion** em cada HTTP Request para garantir respostas corretas:

| Rota             | Campo a verificar       | Valor esperado |
|------------------|-------------------------|----------------|
| GET /produtos    | Response Code           | 200            |
| GET /produtos/id | Response Code           | 200            |
| POST /produtos   | Response Code           | 201            |
| PUT /produtos/id | Response Code           | 200            |
| DELETE /id       | Response Code           | 200            |
| GET id inválido  | Response Body contém    | `erro`         |

---

## Dica: popular o banco antes do teste

Antes de rodar testes de leitura/edição/delete, cadastre produtos via POST em um **setUp Thread Group** (1 thread, 1 loop) com múltiplos HTTP Requests de cadastro, garantindo IDs disponíveis.

---

## Métricas a observar

- **Throughput** (req/s): capacidade do servidor
- **Average / 90th percentile** de tempo de resposta
- **Error %**: deve ser 0% em carga normal
- **Latência vs. número de threads**: identifica o ponto de saturação
