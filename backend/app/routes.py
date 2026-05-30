from flask import Blueprint, jsonify, request
from .database import SessionLocal
from .models import Produto

bp = Blueprint("produtos", __name__, url_prefix="/api")


def get_db():
    return SessionLocal()


# GET /api/produtos — listar todos os produtos
@bp.get("/produtos")
def listar_produtos():
    db = get_db()
    produtos = db.query(Produto).all()
    db.close()
    return jsonify([
        {"id": p.id, "nome": p.nome, "descricao": p.descricao, "preco": p.preco, "quantidade": p.quantidade}
        for p in produtos
    ])


# GET /api/produtos/<id> — mostrar produto específico
@bp.get("/produtos/<int:produto_id>")
def mostrar_produto(produto_id):
    db = get_db()
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    db.close()
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404
    return jsonify({"id": produto.id, "nome": produto.nome, "descricao": produto.descricao, "preco": produto.preco, "quantidade": produto.quantidade})


# POST /api/produtos — cadastrar produto
@bp.post("/produtos")
def cadastrar_produto():
    data = request.get_json()
    if not data or not data.get("nome") or data.get("preco") is None:
        return jsonify({"erro": "nome e preco são obrigatórios"}), 400

    db = get_db()
    produto = Produto(
        nome=data["nome"],
        descricao=data.get("descricao", ""),
        preco=float(data["preco"]),
        quantidade=int(data.get("quantidade", 0)),
    )
    db.add(produto)
    db.commit()
    db.refresh(produto)
    db.close()
    return jsonify({"id": produto.id, "nome": produto.nome, "descricao": produto.descricao, "preco": produto.preco, "quantidade": produto.quantidade}), 201


# PUT /api/produtos/<id> — editar produto
@bp.put("/produtos/<int:produto_id>")
def editar_produto(produto_id):
    db = get_db()
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        db.close()
        return jsonify({"erro": "Produto não encontrado"}), 404

    data = request.get_json()
    if "nome" in data:
        produto.nome = data["nome"]
    if "descricao" in data:
        produto.descricao = data["descricao"]
    if "preco" in data:
        produto.preco = float(data["preco"])
    if "quantidade" in data:
        produto.quantidade = int(data["quantidade"])

    db.commit()
    db.refresh(produto)
    db.close()
    return jsonify({"id": produto.id, "nome": produto.nome, "descricao": produto.descricao, "preco": produto.preco, "quantidade": produto.quantidade})


# DELETE /api/produtos/<id> — deletar produto
@bp.delete("/produtos/<int:produto_id>")
def deletar_produto(produto_id):
    db = get_db()
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        db.close()
        return jsonify({"erro": "Produto não encontrado"}), 404

    db.delete(produto)
    db.commit()
    db.close()
    return jsonify({"mensagem": "Produto deletado com sucesso"})
