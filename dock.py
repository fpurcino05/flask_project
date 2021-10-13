from datetime import date, datetime 
from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_,text

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.dock'  


db = SQLAlchemy(app)

db.init_app(app)
########CRIA TABELAS#############################

class Pessoas (db.Model):
    idPessoa = db.Column(db.Integer, primary_key=True)
    nome = db.Column (db.String(50))
    cpf =  db.Column (db.String(50))
    dataNascimento = db.Column(db.DateTime)


class Contas (db.Model):
    idConta = db.Column(db.Integer, primary_key=True)
    idPessoa = db.Column(db.Integer, db.ForeignKey ('pessoas.idPessoa'), unique =True)
    saldo =  db.Column (db.Float)
    limiteSaqueDiario =db.Column (db.Float)
    flagAtivo =  db.Column (db.Boolean)
    tipoConta = db.Column(db.Integer)
    dataCriacao = db.Column(db.DateTime, default =datetime.now)

class Transacoes (db.Model):
    idTransacao = db.Column(db.Integer, primary_key=True)
    idConta = db.Column (db.Integer, db.ForeignKey ('contas.idConta'))
    valor =  db.Column (db.Float)
    dataTransacao = db.Column(db.DateTime, default =datetime.now)


########CRIA TABELAS#############################


######## Cadastro de Clientes #############################
@app.route ('/pessoas/', methods =["GET"])
def params():
    nome = request.args['nome']  
    cpf = request.args['cpf']
    dataNascimento = datetime.strptime(request.args['dataNascimento'], '%d-%m-%Y')
    user = Pessoas(nome = nome, cpf=cpf, dataNascimento=dataNascimento)
    db.session.add(user)
    db.session.commit() 
    return '<h1> Cliente cadastrado! </h1> '

######## Criacao de Contas #############################

@app.route('/conta/', methods = ["GET"])
def conta():
    idPessoa =request.args['idPessoa']
    saldo =request.args['saldo']
    limiteSaqueDiario = request.args['limiteSaqueDiario']
    flagAtivo= bool(request.args ['flagAtivo'])
    tipoConta= request.args ['tipoConta']
    conta = Contas(idPessoa=idPessoa,saldo = saldo, limiteSaqueDiario=limiteSaqueDiario, flagAtivo=flagAtivo,tipoConta=tipoConta)
    db.session.add(conta)
    db.session.commit()
    return '<h1> Conta criada! </h1> '
    #return str(saldo) + ' '+str(limiteSaqueDiario)+ ' '+ str(flagAtivo)+ ' '+ str(tipoConta)


######## Deposito #############################

@app.route('/deposito/', methods = ["GET"])
def transacao():
    idConta =request.args['idConta']
    valor =float(request.args['valor'])

#Valida se o deposito será maior que 0    
    if valor >=0.01:
        tran = Transacoes(idConta=idConta,valor=valor)
        db.session.add(tran)
        db.session.commit()
        return 'Transacao efetuada'
    else:
        return 'Transacao nao efetuada'


######## Extrato #############################

@app.route('/extrato/')

def extrato():
    data_ini = datetime.strptime(request.args['data_ini'], '%d-%m-%Y')
    data_fim = datetime.strptime(request.args['data_fim'], '%d-%m-%Y')
    
    idConta = request.args['idConta']
    extrato = Transacoes.query.filter(text (" dataTransacao >= {} and dataTransacao <={} and idConta={}".format(data_ini,data_fim,idConta)))
    
    return extrato

######## Saldo #############################

@app.route('/saldo/', methods = ["GET"])

def get_saldo():
    idConta =request.args['idConta']    
    user = Contas.query.filter_by(idConta = idConta).first()
    
    return f'Seu saldo é: {user.saldo}'

######## Saque #############################

@app.route('/saque/', methods = ["GET"])

def get_saque():
    idConta =request.args['idConta'] 
    saque  = float(request.args['saque'])     
    user = Contas.query.filter_by(idConta = idConta).first()
    if float(user.saldo) < saque :
        return f'Seu saldo é insuficiente' #valida se tem saldo suficiente 
    else:
        saldo_final = float(user.saldo) -float(saque) 
        return f'Saque efetuado no valor de : {saque}, seu novo saldo é de {saldo_final}'

app.run (debug=True)
