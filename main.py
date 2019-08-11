from flask import Flask, render_template, request,redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
#configurar la direccion donde esta la bbdd  las 3 barras son pra especificar 
#conexion con sqlite en el prompt
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/tareas.db'
db = SQLAlchemy(app)#ejecutanto e instanciado a la bbdd

#crear el modelo de la bbdd
#desde db.quiero crear un modelo de datos
#el id lo genera la misma bbdd|
class Tarea(db.Model):
	#colocar todos los datos que estan relacionados con una taea
	id = db.Column(db.Integer, primary_key=True)
	contenido = db.Column(db.String(200))
	done = db.Column(db.Boolean)


##rutas
@app.route('/')
def inicio():
	#consulta a la base de datos
	tareas = Tarea.query.all()
	#renderizar a index.html
	return render_template('index.html', tareas=tareas)


@app.route('/crear-tarea', methods=['POST'])
def crear():
	#se recive con el metodo request
	tarea = Tarea(contenido=request.form['contenido'], done=False)
	db.session.add(tarea)
	db.session.commit()
	return redirect(url_for('inicio'))

	
@app.route('/done/<id>')
def done(id):
	#convertirn el id en un entero
	tarea = Tarea.query.filter_by(id=int(id)).first()#ubicar la primera tarea con el id
	#covertir a false
	tarea.done = not(tarea.done)
	db.session.commit()
	return redirect(url_for('inicio'))

	
@app.route('/eliminar/<id>')
def eliminar(id):
	#convertirn el id en un entero
	tarea = Tarea.query.filter_by(id=int(id)).delete()#ubicar la primera tarea con el id
	db.session.commit()
	return redirect(url_for('inicio'))



if __name__=='__main__':
	app.run(debug=True)