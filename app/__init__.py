from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from decouple import config
from flask_jwt_extended import JWTManager, create_access_token

# Inicializar extensiones
db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    # Configuración desde el archivo .env
    app.config['SECRET_KEY'] = config('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{config('PGSQL_USER')}:{config('PGSQL_PASSWORD')}@"
        f"{config('PGSQL_HOST')}/{config('PGSQL_DATABASE')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configuración de JWT    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = config('JWT_SECRET_KEY', default=config('SECRET_KEY'))
        
    
    # Habilitar el manejo de Refresh Token
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Duración del access token
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)  # Duración del refresh token
       
        
    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)

    # Importar y registrar las rutas
    #from .routes import main
    #app.register_blueprint(main)
    
    # Importar y registrar el Blueprint
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
