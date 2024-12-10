from flask import Blueprint, request, jsonify, abort
from .models import Movie
from . import db
import uuid
from datetime import datetime, timedelta

from flask_jwt_extended import (
    create_access_token, 
    jwt_required, 
    get_jwt_identity
)
import secrets

main = Blueprint('main', __name__)

# Generación de tokens
@main.route('/token', methods=['POST'])
def generate_token():
    try:
        # Generar un identificador único para el token
        token_identity = str(uuid.uuid4())

        # Crear un token con una expiración de 1 hora
        access_token = create_access_token(
            identity=token_identity,
            expires_delta=timedelta(hours=1)  # Corregido
        )

        return jsonify({
            'access_token': access_token,
            'token_type': 'Bearer',
            'expires_in': 3600  # Expiración en segundos
        }), 200
    except Exception as e:
        # Agregar logs de error para ayudar con la depuración
        return jsonify({'error': f"Error generando token: {str(e)}"}), 500


# Ruta para obtener películas protegida por JWT
@main.route('/movies', methods=['GET'])
@jwt_required()  # Requiere token válido
def get_movies():
    try:
        # Obtener la identidad actual del token
        current_user = get_jwt_identity()

        # Consultar todas las películas
        movies = Movie.query.all()
        movies_data = [movie.to_dict() for movie in movies]

        return jsonify({
            'user': current_user,  # Información del usuario actual
            'movies': movies_data
        }), 200
    except Exception as e:
        return jsonify({'error': f"Error obteniendo películas: {str(e)}"}), 500


@main.route('/movies/<id>', methods=['GET'])
@jwt_required()  # Requiere un token válido
def get_movie(id):
    """Obtener una película específica por su ID."""
    try:
        # Obtener la identidad del usuario desde el token
        current_user = get_jwt_identity()
        # Puedes usar `current_user` para auditoría o lógica personalizada
        
        movie = Movie.query.get(id)
        if movie:
            return jsonify(movie.to_dict()), 200
        
        return jsonify({'message': 'Movie not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@main.route('/movies', methods=['POST'])
@jwt_required()  # Requiere un token válido
def add_movie():
    """Agregar una nueva película."""
    try:
        # Obtener la identidad del usuario desde el token
        current_user = get_jwt_identity()
        # Puedes usar `current_user` para registrar quién agregó la película

        data = request.get_json()
        id = str(uuid.uuid4())
        title = data.get('title', '').strip()
        duration = int(data.get('duration', 0))
        release = datetime.strptime(data.get('release', ''), '%Y-%m-%d').date()

        # Validaciones
        if not title or len(title) > 50:
            return jsonify({'message': 'Invalid title'}), 400
        if duration <= 0 or duration > 200:
            return jsonify({'message': 'Invalid duration'}), 400

        # Crear la película y guardar en la base de datos
        movie = Movie(id=id, title=title, duration=duration, release=release)
        db.session.add(movie)
        db.session.commit()

        return jsonify(movie.to_dict()), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500



@main.route('/movies/<id>', methods=['PUT'])
@jwt_required()  # Requiere un token válido
def update_movie(id):
    """Actualizar una película existente."""
    try:
        # Obtener la identidad del usuario desde el token
        current_user = get_jwt_identity()
        # Puedes usar `current_user` para registros o auditoría

        movie = Movie.query.get(id)
        if not movie:
            return jsonify({'message': 'Movie not found'}), 404

        data = request.get_json()
        movie.title = data.get('title', movie.title).strip()
        movie.duration = int(data.get('duration', movie.duration))
        movie.release = datetime.strptime(data.get('release', movie.release.isoformat()), '%Y-%m-%d').date()

        # Validaciones
        if not movie.title or len(movie.title) > 50:
            return jsonify({'message': 'Invalid title'}), 400
        if movie.duration <= 0 or movie.duration > 200:
            return jsonify({'message': 'Invalid duration'}), 400

        # Guardar los cambios en la base de datos
        db.session.commit()
        return jsonify(movie.to_dict()), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500



@main.route('/movies/<id>', methods=['DELETE'])
@jwt_required()  # Requiere un token válido
def delete_movie(id):
    """Eliminar una película existente."""
    try:
        # Obtener la identidad del usuario desde el token
        current_user = get_jwt_identity()
        # Puedes usar `current_user` para registro o auditoría

        movie = Movie.query.get(id)
        if not movie:
            return jsonify({'message': 'Movie not found'}), 404

        # Eliminar la película
        db.session.delete(movie)
        db.session.commit()

        return jsonify({'message': 'Movie deleted'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500



# Manejadores de errores
@main.errorhandler(401)
def unauthorized(error):
    return jsonify({'error': 'Token inválido o expirado'}), 401
