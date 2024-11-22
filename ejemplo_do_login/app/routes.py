from flask import Blueprint, request, redirect, url_for, flash, session
from .models import User
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return "Esto es una prueba de mierda de sistema de login."

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        new_user = User(username=username, email=email, password=password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Usuario registrado exitosamente.")
            return redirect(url_for('main.login'))
        except:
            flash("El usuario o email ya están registrados.")
            return redirect(url_for('main.register'))

    return '''
    <form method="POST">
        <input type="text" name="username" placeholder="Nombre de Usuario" required>
        <input type="email" name="email" placeholder="Email" required>
        <input type="password" name="password" placeholder="Contraseña" required>
        <button type="submit">Registrarse</button>
    </form>
    '''

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form['username_or_email']
        password = request.form['password']

        user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()

        if user and user.password == password:
            session['user_id'] = user.id
            session['username'] = user.username
            flash("Inicio de sesión exitoso.")
            return redirect(url_for('main.dashboard'))
        else:
            flash("Usuario o contraseña incorrectos.")
            return redirect(url_for('main.login'))

    return '''
    <form method="POST">
        <input type="text" name="username_or_email" placeholder="Nombre de Usuario o Email" required>
        <input type="password" name="password" placeholder="Contraseña" required>
        <button type="submit">Iniciar Sesión</button>
    </form>
    '''

@main.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return f"Bienvenido, {session['username']}! <a href='/logout'>Cerrar Sesión</a>"
    else:
        flash("Por favor, inicia sesión primero.")
        return redirect(url_for('main.login'))

@main.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash("Sesión cerrada exitosamente.")
    return redirect(url_for('main.home'))
