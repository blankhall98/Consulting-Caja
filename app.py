#libraries
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy


# instances
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///caja.db'
db = SQLAlchemy(app)

# database model
class Caja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(100), nullable=False)
    monto_1000 = db.Column(db.Integer, nullable=False)
    monto_500 = db.Column(db.Integer, nullable=False)
    monto_200 = db.Column(db.Integer, nullable=False)
    monto_100 = db.Column(db.Integer, nullable=False)


class Movimiento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(100), nullable=False)
    monto_1000 = db.Column(db.Integer, nullable=False)
    monto_500 = db.Column(db.Integer, nullable=False)
    monto_200 = db.Column(db.Integer, nullable=False)
    monto_100 = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(100), nullable=False)

# routes
@app.route('/')
def index():
    return render_template('index.html')

# acceder al cierre de la caja
@app.route('/cierre')
def cierre():
    caja = Caja.query.all()
    last = Caja.query.order_by(Caja.id.desc()).first()
    mov = Movimiento.query.all()
    return render_template('cierre.html',caja=caja,last=last,mov=mov)

# realizar un deposito a la caja
@app.route('/deposito', methods=['GET', 'POST'])
def deposito():
    if request.method == 'POST':
        fecha = request.form['fecha']
        monto_1000 = int(request.form['monto_1000'])
        monto_500 = int(request.form['monto_500'])
        monto_200 = int(request.form['monto_200'])
        monto_100 = int(request.form['monto_100'])

        movimiento = Movimiento(fecha=fecha, monto_1000=monto_1000, monto_500=monto_500, monto_200=monto_200, monto_100=monto_100, tipo='deposito')

        last = Caja.query.order_by(Caja.id.desc()).first()

        if last is not None:
            monto_1000 = monto_1000 + last.monto_1000
            monto_500 = monto_500 + last.monto_500
            monto_200 = monto_200 + last.monto_200
            monto_100 = monto_100 + last.monto_100

        caja = Caja(fecha=fecha, monto_1000=monto_1000, monto_500=monto_500, monto_200=monto_200, monto_100=monto_100)

        db.session.add(caja)
        db.session.commit()

        db.session.add(movimiento)
        db.session.commit()

        return redirect(url_for('index'))
    else:
        return render_template('deposito.html')

# realizar un retiro a la caja
@app.route('/retiro', methods=['GET', 'POST'])
def retiro():
    if request.method == 'POST':
        fecha = request.form['fecha']
        monto_1000 = int(request.form['monto_1000'])
        monto_500 = int(request.form['monto_500'])
        monto_200 = int(request.form['monto_200'])
        monto_100 = int(request.form['monto_100'])

        movimiento = Movimiento(fecha=fecha, monto_1000=monto_1000, monto_500=monto_500, monto_200=monto_200, monto_100=monto_100, tipo='retiro')

        last = Caja.query.order_by(Caja.id.desc()).first()

        if last is not None:
            monto_1000 = last.monto_1000 - monto_1000 
            monto_500 = last.monto_500 - monto_500 
            monto_200 = last.monto_200 - monto_200 
            monto_100 = last.monto_100 - monto_100 

        caja = Caja(fecha=fecha, monto_1000=monto_1000, monto_500=monto_500, monto_200=monto_200, monto_100=monto_100)

        db.session.add(caja)
        db.session.commit()

        db.session.add(movimiento)
        db.session.commit()

        return redirect(url_for('index'))
    else:
        return render_template('retiro.html')


# run app
if __name__ == '__main__':
    app.run(debug=True)
    #crear tablas y modelos en la base de datos
    with app.app_context():
        db.create_all()