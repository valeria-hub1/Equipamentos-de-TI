from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from datetime import datetime

from models.conexao import (
    engine,
    SessionLocal,
    Base
)

from models.equipamento_model import Equipamento
from models.suporte_model import Suporte


# ==========================================
# CRIAÇÃO DA APLICAÇÃO FLASK
# ==========================================

app = Flask(__name__)

app.secret_key = "chave-secreta-sistema-ti"


# ==========================================
# CRIA AS TABELAS DO BANCO
# ==========================================

Base.metadata.create_all(bind=engine)


# ==========================================
# PÁGINA INICIAL
# ==========================================

@app.route("/")
def home():

    db = SessionLocal()

    equipamentos = db.query(Equipamento).count()

    em_uso = db.query(Equipamento).filter(
        Equipamento.status == "Em Uso"
    ).count()

    manutencao = db.query(Equipamento).filter(
        Equipamento.status == "Em Manutenção"
    ).count()

    suportes = db.query(Suporte).count()

    db.close()

    return render_template(
        "index.html",
        equipamentos=equipamentos,
        em_uso=em_uso,
        manutencao=manutencao,
        suportes=suportes
    )


# ==========================================
# LISTAR EQUIPAMENTOS
# ==========================================

@app.route("/equipamentos")
def equipamentos():

    db = SessionLocal()

    lista = db.query(
        Equipamento
    ).order_by(
        Equipamento.id.desc()
    ).all()

    db.close()

    return render_template(
        "equipamentos.html",
        equipamentos=lista
    )


# ==========================================
# CADASTRAR EQUIPAMENTO
# ==========================================

@app.route(
    "/equipamentos/novo",
    methods=["GET", "POST"]
)
def novo_equipamento():

    if request.method == "POST":

        db = SessionLocal()

        try:

            data_aquisicao = datetime.strptime(
                request.form["data_aquisicao"],
                "%Y-%m-%d"
            ).date()

            equipamento = Equipamento(

                patrimonio=request.form["patrimonio"],

                tipo=request.form["tipo"],

                marca=request.form["marca"],

                modelo=request.form["modelo"],

                numero_serie=request.form["numero_serie"],

                data_aquisicao=data_aquisicao,

                localizacao=request.form["localizacao"],

                status=request.form["status"]

            )

            db.add(equipamento)

            db.commit()

            flash(
                "Equipamento cadastrado com sucesso!",
                "success"
            )

            return redirect(
                url_for("equipamentos")
            )

        except Exception as erro:

            db.rollback()

            flash(
                f"Erro ao cadastrar equipamento: {erro}",
                "error"
            )

        finally:

            db.close()

    return render_template(
        "equipamento_form.html",
        equipamento=None
    )


# ==========================================
# DETALHES DO EQUIPAMENTO
# ==========================================

@app.route("/equipamentos/<int:id>")
def detalhe_equipamento(id):

    db = SessionLocal()

    equipamento = db.query(
        Equipamento
    ).filter(
        Equipamento.id == id
    ).first()

    if equipamento is None:

        db.close()

        flash(
            "Equipamento não encontrado.",
            "error"
        )

        return redirect(
            url_for("equipamentos")
        )

    suportes = db.query(
        Suporte
    ).filter(
        Suporte.id_equipamento == id
    ).order_by(
        Suporte.id.desc()
    ).all()

    db.close()

    return render_template(
        "equipamento_detalhe.html",
        equipamento=equipamento,
        suportes=suportes
    )


# ==========================================
# EDITAR EQUIPAMENTO
# ==========================================

@app.route(
    "/equipamentos/<int:id>/editar",
    methods=["GET", "POST"]
)
def editar_equipamento(id):

    db = SessionLocal()

    equipamento = db.query(
        Equipamento
    ).filter(
        Equipamento.id == id
    ).first()

    if equipamento is None:

        db.close()

        flash(
            "Equipamento não encontrado.",
            "error"
        )

        return redirect(
            url_for("equipamentos")
        )

    if request.method == "POST":

        try:

            equipamento.patrimonio = request.form[
                "patrimonio"
            ]

            equipamento.tipo = request.form[
                "tipo"
            ]

            equipamento.marca = request.form[
                "marca"
            ]

            equipamento.modelo = request.form[
                "modelo"
            ]

            equipamento.numero_serie = request.form[
                "numero_serie"
            ]

            equipamento.data_aquisicao = datetime.strptime(
                request.form["data_aquisicao"],
                "%Y-%m-%d"
            ).date()

            equipamento.localizacao = request.form[
                "localizacao"
            ]

            equipamento.status = request.form[
                "status"
            ]

            db.commit()

            flash(
                "Equipamento atualizado com sucesso!",
                "success"
            )

            db.close()

            return redirect(
                url_for(
                    "detalhe_equipamento",
                    id=id
                )
            )

        except Exception as erro:

            db.rollback()

            flash(
                f"Erro ao atualizar: {erro}",
                "error"
            )

    db.close()

    return render_template(
        "equipamento_form.html",
        equipamento=equipamento
    )


# ==========================================
# LISTAR SUPORTES
# ==========================================

@app.route("/suportes")
def suportes():

    db = SessionLocal()

    lista = db.query(
        Suporte
    ).order_by(
        Suporte.id.desc()
    ).all()

    db.close()

    return render_template(
        "suportes.html",
        suportes=lista
    )


# ==========================================
# CADASTRAR SUPORTE
# ==========================================

@app.route(
    "/suportes/novo",
    methods=["GET", "POST"]
)
def novo_suporte():

    db = SessionLocal()

    equipamentos = db.query(
        Equipamento
    ).order_by(
        Equipamento.patrimonio
    ).all()

    if request.method == "POST":

        try:

            data_suporte = datetime.strptime(
                request.form["data_suporte"],
                "%Y-%m-%d"
            ).date()

            custo = request.form["custo"]

            if custo == "":
                custo = 0
            else:
                custo = float(custo)

            suporte = Suporte(

                id_equipamento=int(
                    request.form["id_equipamento"]
                ),

                data_suporte=data_suporte,

                tipo_suporte=request.form[
                    "tipo_suporte"
                ],

                descricao=request.form[
                    "descricao"
                ],

                responsavel=request.form[
                    "responsavel"
                ],

                custo=custo
            )

            db.add(suporte)

            db.commit()

            flash(
                "Registro de suporte cadastrado!",
                "success"
            )

            db.close()

            return redirect(
                url_for("suportes")
            )

        except Exception as erro:

            db.rollback()

            flash(
                f"Erro ao cadastrar suporte: {erro}",
                "error"
            )

    db.close()

    return render_template(
        "suporte_form.html",
        equipamentos=equipamentos,
        suporte=None
    )


# ==========================================
# EDITAR SUPORTE
# ==========================================

@app.route(
    "/suportes/<int:id>/editar",
    methods=["GET", "POST"]
)
def editar_suporte(id):

    db = SessionLocal()

    suporte = db.query(
        Suporte
    ).filter(
        Suporte.id == id
    ).first()

    if suporte is None:

        db.close()

        flash(
            "Registro não encontrado.",
            "error"
        )

        return redirect(
            url_for("suportes")
        )

    equipamentos = db.query(
        Equipamento
    ).all()

    if request.method == "POST":

        try:

            suporte.id_equipamento = int(
                request.form["id_equipamento"]
            )

            suporte.data_suporte = datetime.strptime(
                request.form["data_suporte"],
                "%Y-%m-%d"
            ).date()

            suporte.tipo_suporte = request.form[
                "tipo_suporte"
            ]

            suporte.descricao = request.form[
                "descricao"
            ]

            suporte.responsavel = request.form[
                "responsavel"
            ]

            custo = request.form["custo"]

            suporte.custo = (
                float(custo)
                if custo
                else 0
            )

            db.commit()

            flash(
                "Registro atualizado com sucesso!",
                "success"
            )

            db.close()

            return redirect(
                url_for("suportes")
            )

        except Exception as erro:

            db.rollback()

            flash(
                f"Erro ao atualizar: {erro}",
                "error"
            )

    db.close()

    return render_template(
        "suporte_form.html",
        equipamentos=equipamentos,
        suporte=suporte
    )


# ==========================================
# EXCLUIR SUPORTE
# ==========================================

@app.route(
    "/suportes/<int:id>/excluir",
    methods=["POST"]
)
def excluir_suporte(id):

    db = SessionLocal()

    suporte = db.query(
        Suporte
    ).filter(
        Suporte.id == id
    ).first()

    if suporte:

        db.delete(suporte)

        db.commit()

        flash(
            "Registro de suporte excluído.",
            "success"
        )

    else:

        flash(
            "Registro não encontrado.",
            "error"
        )

    db.close()

    return redirect(
        url_for("suportes")
    )


# ==========================================
# RELATÓRIOS
# ==========================================

@app.route("/relatorios")
def relatorios():

    db = SessionLocal()

    equipamentos = db.query(
        Equipamento
    ).order_by(
        Equipamento.tipo
    ).all()

    db.close()

    return render_template(
        "relatorios.html",
        equipamentos=equipamentos
    )


# ==========================================
# SOBRE
# ==========================================

@app.route("/sobre")
def sobre():

    return render_template(
        "sobre.html"
    )


# ==========================================
# EXECUTAR SERVIDOR
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
