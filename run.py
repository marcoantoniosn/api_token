from app import create_app, db
#from app import create_app, db
#from app.authTK import auth 

app = create_app()

# Registrar el blueprint
#app.register_blueprint(auth)

if __name__ == '__main__':
    with app.app_context():
        # Crear las tablas en la base de datos si no existen
        db.create_all()
        app.run(debug=True)
    # En produccion cambiar: app.run(debug=False)