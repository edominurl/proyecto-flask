from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__); app.secret_key='dev'

def get_conn():
    c = sqlite3.connect('demo.db'); 
    c.row_factory = sqlite3.Row; 
    return c

def init_db():
    with get_conn() as c:
        c.execute('''CREATE TABLE IF NOT EXISTS est (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT, 
            grado TEXT, 
            promedio REAL
        )''')
        
@app.route('/')
def home():
    with get_conn() as c:
        data = c.execute('SELECT id,nombre,grado,promedio FROM est').fetchall()
    return render_template('index.html', est=data)

# CREATE
@app.route('/crear', methods=['POST', 'GET'])
def crear():
    if request.method == 'POST':
        n = request.form['nombre']; 
        g = request.form['grado']; 
        p = float(request.form['promedio'])
        with get_conn() as c:
            c.execute('INSERT INTO est(nombre,grado,promedio) VALUES(?,?,?)',(n,g,p))
        flash('Creado','success'); 
        return render_template('index.html')
    return render_template('crear.html')

@app.route('/editar/<int:id>', methods=['POST', 'GET'])
def editar(id):
    with get_conn() as c:
        est = c.execute('SELECT id,nombre,grado,promedio FROM est WHERE id=?',(id,)).fetchone()
    if request.method == 'POST':
        n = request.form['nombre']; 
        g = request.form['grado']; 
        p = float(request.form['promedio'])
        with get_conn() as c:
            c.execute('UPDATE est SET nombre=?, grado=?, promedio=? WHERE id=?',(n,g,p,id))
        flash('Actualizado','info'); 
        return redirect(url_for('home'))
    return render_template('editar.html', est=est)

@app.route('/eliminar/<int:id>', methods=['POST', 'GET'])
def eliminar(id):
    if request.method == 'POST':
        with get_conn() as c:
            c.execute('DELETE FROM est WHERE id=?',(id,))
        flash('Eliminado','danger'); 
        return redirect(url_for('home'))
    with get_conn() as c:
        est = c.execute('SELECT id,nombre,grado,promedio FROM est WHERE id=?',(id,)).fetchone()
    return render_template('eliminar.html', est=est)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
    