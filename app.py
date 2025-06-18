from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from io import BytesIO
from weasyprint import HTML
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Planilha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_tear = db.Column(db.Integer, nullable=False)
    artigo_tecido = db.Column(db.String(50), nullable=False)
    defeito = db.Column(db.String(100), nullable=False)
    data = db.Column(db.String(10), nullable=False)
    horario = db.Column(db.String(5), nullable=False)
    turno = db.Column(db.String(20), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/registros')
def registros():
    registros = Planilha.query.order_by(Planilha.data.desc()).all()
    return render_template('registros.html', registros=registros)


@app.route('/salvar', methods=['POST'])
def salvar():
    try:
        novo_registro = Planilha(
            numero_tear=request.form['numero_tear'],
            artigo_tecido=request.form['artigo_tecido'],
            defeito=request.form['defeito'],
            data=request.form['data'],
            horario=request.form['horario'],
            turno=request.form['turno']
        )
        db.session.add(novo_registro)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        return f"Erro ao salvar: {str(e)}", 500


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_registro(id):
    registro = Planilha.query.get_or_404(id)
    if request.method == 'POST':
        try:
            registro.numero_tear = request.form['numero_tear']
            registro.artigo_tecido = request.form['artigo_tecido']
            registro.defeito = request.form['defeito']
            registro.data = request.form['data']
            registro.horario = request.form['horario']
            registro.turno = request.form['turno']
            db.session.commit()
            return redirect(url_for('registros'))
        except Exception as e:
            return f"Erro ao editar: {str(e)}", 500
    return render_template('editar.html', registro=registro)


@app.route('/limpar-banco', methods=['GET'])
def limpar_banco():
    try:
        db.session.query(Planilha).delete()
        db.session.commit()
        return redirect(url_for('registros'))
    except Exception as e:
        db.session.rollback()
        return f"Erro ao limpar banco: {str(e)}", 500


@app.route('/exportar/excel')
def exportar_excel():
    try:
        registros = Planilha.query.all()
        dados = [{
            'Tear': r.numero_tear,
            'Artigo': r.artigo_tecido,
            'Defeito': r.defeito,
            'Data': r.data,
            'Hora': r.horario,
            'Turno': r.turno
        } for r in registros]

        df = pd.DataFrame(dados)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Registros')

        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response.headers['Content-Disposition'] = 'attachment; filename=registros_teares.xlsx'
        return response
    except Exception as e:
        return f"Erro ao exportar Excel: {str(e)}", 500


@app.route('/exportar/pdf')
def exportar_pdf():
    try:
        registros = Planilha.query.order_by(Planilha.data.desc()).all()
        html = render_template('exportar_pdf.html',
                               registros=registros,
                               data_geracao=datetime.now().strftime('%d/%m/%Y %H:%M'))
        pdf = HTML(string=html).write_pdf()
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=registros_teares.pdf'
        return response
    except Exception as e:
        return f"Erro ao gerar PDF: {str(e)}", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)