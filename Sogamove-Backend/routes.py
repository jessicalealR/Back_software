from flask import Blueprint, jsonify, request, redirect, url_for, session, render_template
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash 
import sqlite3
import traceback

main_routes = Blueprint('main', __name__)

@main_routes.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        print(f"Datos recibidos: {data}")
        new_user = User(
            document_type=data['document_type'],
            number_Id=data['number_Id'],
            birth_date=data['birth_date'],
            expedition_date=data['expedition_date'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=data['password']
            #password=generate_password_hash(data['password'])  # Encriptar la contraseña
        )
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id  # Almacenar el ID del usuario en la sesión

        print("Redirigiendo a la página de usuario registrado...")
        return jsonify({"message": "Usuario registrado exitosamente", "redirect": url_for('main.usuarioRegistrado')})
    except Exception as e:
        db.session.rollback()
        print(f"Error al registrar usuario: {str(e)}")
        traceback.print_exc()  # Imprime el traceback completo para obtener más información
        return jsonify({"error": str(e)}), 500

@main_routes.route('/usuarioRegistrado', methods=['GET'])
def usuarioRegistrado():
    return render_template('usuarioRegistrado.html')

@main_routes.route('/login', methods=['GET', 'POST']) 
def login(): 
    if request.method == 'POST': 
        email = request.form['email'] 
        password = request.form['password'] 
        with sqlite3.connect('database.db') as con: 
            cur = con.cursor() 
            cur.execute("SELECT * FROM users WHERE email = ?", (email,)) 
            user = cur.fetchone() 
        if user and check_password_hash(user[2], password): 
            session['user_id'] = user[0] 
            return redirect(url_for('main')) 
        else: return "Inicio de sesión fallido. Verifica tus credenciales." 
        return render_template('login.html')