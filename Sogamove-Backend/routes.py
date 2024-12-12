# main_routes.py
from flask import Blueprint, jsonify, request, redirect, url_for, session, render_template
from models import db, User,Comment
from werkzeug.security import generate_password_hash, check_password_hash 
import sqlite3
from datetime import datetime
import traceback

main_routes = Blueprint('main', __name__)

@main_routes.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        new_user = User(
            document_type=data['document_type'],
            number_Id=data['number_Id'],
            birth_date=data['birth_date'],
            expedition_date=data['expedition_date'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=data['password']
        )
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id

        return jsonify({"message": "Usuario registrado exitosamente", "redirect": url_for('main.usuarioRegistrado')})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@main_routes.route('/usuarioRegistrado', methods=['GET'])
def usuarioRegistrado():
    return render_template('usuarioRegistrado.html')

    
@main_routes.route('/logout') 
def logout(): 
    session.pop('user_id', None)  
    return redirect(url_for('main'))


@main_routes.route('/ingresoUsuarios', methods=['GET', 'POST'])
def ingreso_Usuarios():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Busca al usuario en la base de datos
        user = User.query.filter_by(email=email).first()
        
        # Compara las contraseñas directamente (no recomendado para producción)
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('main.usuarioRegistrado'))
        else:
            return render_template('ingresoUsuarios.html', error="Correo o contraseña incorrectos")
    
    return render_template('ingresoUsuarios.html')



@main_routes.route('/profile', methods=['GET'])
def perfil():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('main.ingreso_Usuarios'))

    try:
        user = User.query.get(user_id)
        if user:
            return render_template('perfil.html', user=user)
        else:
            return redirect(url_for('main.ingreso_Usuarios'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main_routes.route('/comment', methods=['POST'])
def post_comment():
    try:
        # Asegúrate de que el usuario esté logueado
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Usuario no autenticado'}), 403
        
        
        # Obtener los datos del comentario
        data = request.get_json()
        comment_content = data.get('content')
        
        if not comment_content:
            return jsonify({'error': 'Contenido del comentario vacío'}), 400

        # Crear un nuevo comentario
        user = User.query.get(user_id)
        if user:
            new_comment = Comment(user_Id=user.id, username=user.first_name + ' ' + user.last_name, content=comment_content)
            db.session.add(new_comment)
            db.session.commit()

            # Devuelve el comentario recién creado
            return jsonify({'message': 'Comentario publicado con éxito'}), 200
            
            #return jsonify({'comment': new_comment.to_dict()}), 200
        else:
            return jsonify({'error': 'Usuario no encontrado'}), 404

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500