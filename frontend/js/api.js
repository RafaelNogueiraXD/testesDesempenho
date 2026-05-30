const API = "http://localhost:5000/api";

async function listarProdutos() {
    const res = await fetch(`${API}/produtos`);
    return res.json();
}

async function mostrarProduto(id) {
    const res = await fetch(`${API}/produtos/${id}`);
    return res.json();
}

async function cadastrarProduto(dados) {
    const res = await fetch(`${API}/produtos`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados),
    });
    return res.json();
}

async function editarProduto(id, dados) {
    const res = await fetch(`${API}/produtos/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados),
    });
    return res.json();
}

async function deletarProduto(id) {
    const res = await fetch(`${API}/produtos/${id}`, { method: "DELETE" });
    return res.json();
}
