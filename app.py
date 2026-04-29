import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash # Seguridad de las sesiones
from functools import wraps
import os # Para manejar rutas de carpetas
from werkzeug.utils import secure_filename # Para limpiar nombres de archivos
from datetime import date

# Configure application
app = Flask(__name__)

# Agrega esta línea:
app.secret_key = "una_clave_super_secreta_y_segura"

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "/tmp"
Session(app)

# Definimos dónde se guardarán las imágenes
UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ruta donde se guardará el CV
CV_UPLOAD_FOLDER = 'static/cv'
app.config['CV_UPLOAD_FOLDER'] = CV_UPLOAD_FOLDER

# --- Función nativa para conectarse a la base de datos --- #
def get_db_connection():
    db = sqlite3.connect('portfolio.db')
    
    # Esto hace que la base de datos te devuelva diccionarios en lugar de tuplas.
    db.row_factory = sqlite3.Row 
    return db


# --- Función para evitar que los usuarios ingresen a la vista de admin--- #
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Revisa si NO hay un user_id en la sesión
        if session.get("user_id") is None:
            flash("Debes iniciar sesión para acceder a esta página.", "warning")
            return redirect("/login")
        
        # Si todo está bien, te deja pasar a la función original (f)
        return f(*args, **kwargs)
    
    return decorated_function


# --- ERROR 404 --- #
@app.errorhandler(404)
def page_not_found(e):
    # El segundo valor (404) es importante para que el navegador sepa que es un error
    return render_template('404.html'), 404


# --- VISTA PRINCIPAL --- #
@app.route("/")
def index():
    
    db = get_db_connection()
    
    # Buscamos los proyectos 
    proyectos = db.execute("SELECT * FROM proyectos").fetchall()
    
    # Buscamos las habilidades ordenadas de mayor a menor 
    habilidades = db.execute("SELECT * FROM habilidades ORDER BY porcentaje DESC").fetchall()
    # Traemos la trayectoria:
    trayectorias = db.execute("SELECT * FROM trayectoria ORDER BY id DESC").fetchall()
    
    db.close()
    
    # Le pasamos ambas listas a index.html
    return render_template("index.html", proyectos=proyectos, habilidades=habilidades, trayectorias = trayectorias)
    

# --- VISTA DE REGISTRO --- #
@app.route("/register", methods=["GET", "POST"])
def register():
    """ register """
    # Si el usuario envió el formulario (POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validaciones básicas de seguridad
        if not username or not password or not confirmation:
            flash("Debes completar todos los campos.")
            return redirect("/register")
        
        if password != confirmation:
            flash("Las contraseñas no coinciden.")
            return redirect("/register")

        #   Conectar a la base de datos
        db = get_db_connection()

        # Verificar si el usuario ya existe
        usuario_existente = db.execute("SELECT * FROM usuarios WHERE username = ?", (username,)).fetchone()
        if usuario_existente:
            flash("Ese nombre de usuario ya está en uso.")
            db.close()
            return redirect("/register")

        # Hashear la contraseña por seguridad
        hash_pw = generate_password_hash(password)

        # Insertar el nuevo usuario en la base de datos
        db.execute("INSERT INTO usuarios (username, hash) VALUES (?, ?)", (username, hash_pw))
        db.commit()  
        db.close()

        flash("¡Administrador registrado con éxito!")
        return redirect("/") 
    
    else:
        return render_template("register.html")
   
  
# --- VISTA DE LOGIN --- #  
@app.route("/login", methods=["GET", "POST"])
def login():
    # Limpiar cualquier sesión previa por seguridad
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Debes ingresar usuario y contraseña.")
            return redirect("/login")

        # Conectar a la base de datos y buscar al usuario
        db = get_db_connection()
        usuario = db.execute("SELECT * FROM usuarios WHERE username = ?", (username,)).fetchone()
        db.close()

        # Verificar que el usuario exista y la contraseña sea correcta
        if usuario is None or not check_password_hash(usuario["hash"], password):
            flash("Usuario o contraseña incorrectos.")
            return redirect("/login")

        # ¡Login exitoso! Guardamos el ID del usuario en la sesión
        session["user_id"] = usuario["id"]
        
        flash("¡Bienvenido de vuelta, Administrador!")
        return redirect("/")

    else:
        return render_template("login.html")


# --- RUTA DE LOGOUT--- #  
@app.route("/logout")
def logout():
    # Olvidar al usuario y enviarlo al inicio
    session.clear()
    flash("Sesión cerrada exitosamente.")
    return redirect("/")


# --- RUTA PARA RECIBIR EL MENSAJE DEL PÚBLICO ---
@app.route("/enviar_mensaje", methods=["POST","GET"])
def enviar_mensaje():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        email = request.form.get("email")
        mensaje = request.form.get("mensaje")

        if not nombre or not email or not mensaje:
            flash("Todos los campos son obligatorios.", "danger")
            return redirect("/#contacto")

        db = get_db_connection()
        db.execute("INSERT INTO mensajes (nombre, email, mensaje) VALUES (?, ?, ?)", 
                (nombre, email, mensaje))
        db.commit()
        db.close()

        flash("¡Mensaje enviado con éxito! Te responderé muy pronto.", "success")
        return redirect("/")
    return render_template("enviar_mensaje.html")

# --- RUTA PARA DESCARGAR EL MENSAJE DEL PÚBLICO ---
@app.route("/upload_cv", methods=["POST"])
@login_required
def upload_cv():
    if 'cv_file' not in request.files:
        flash("No se seleccionó ningún archivo", "danger")
        return redirect("/admin")
    
    file = request.files['cv_file']
    
    if file.filename == '':
        flash("Nombre de archivo vacío", "danger")
        return redirect("/admin")

    if file and file.filename.lower().endswith('.pdf'):
        # Siempre lo guardamos con el mismo nombre para que el enlace sea permanente
        path = os.path.join(app.config['CV_UPLOAD_FOLDER'], "curriculum.pdf")
        file.save(path)
        flash("¡Curriculum actualizado correctamente!", "success")
    else:
        flash("Solo se permiten archivos PDF", "danger")
        
    return redirect("/admin")


# --- RUTA DE ADMIN --- #
@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        url_github = request.form.get("git_hub")
        tecnologias = request.form.get("tecnologias")
        
        # --- LÓGICA DE IMAGEN ---
        file = request.files.get("imagen")
        filename = None # Por si no suben nada
        
        if file and file.filename != '':
            # Limpiamos el nombre para evitar problemas de seguridad
            filename = secure_filename(file.filename)
            # Guardamos el archivo físicamente en static/img/
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # ------------------------

        if not title or not description:
            flash("Título y descripción obligatorios")
            return redirect("/admin")

        db = get_db_connection()
        
        db.execute("INSERT INTO proyectos (titulo, descripcion, url_github, url_imagen, tecnologias) VALUES (?, ?, ?, ?, ?)",
            (title, description, url_github, filename, tecnologias))
        db.commit()
        db.close()
        
        flash("¡Proyecto guardado!")
        return redirect("/")
        
    # LÓGICA PARA EL GET
    db = get_db_connection()
    proyectos = db.execute("SELECT * FROM proyectos").fetchall()
    habilidades = db.execute("SELECT * FROM habilidades ORDER BY porcentaje DESC").fetchall()
    
    # Traemos los mensajes ordenados del más reciente al más antiguo
    mensajes = db.execute("SELECT * FROM mensajes ORDER BY fecha DESC").fetchall()
    
    # Traemos las trayectorias:
    trayectorias = db.execute("SELECT * FROM trayectoria ORDER BY fecha_fin DESC").fetchall() 
    
    
    db.close()
    

    return render_template("admin.html", 
                           proyectos=proyectos, 
                           habilidades=habilidades, 
                           mensajes=mensajes,
                           trayectorias=trayectorias)


# --- RUTA PARA BORRAR MENSAJES DESDE EL PANEL ---
@app.route("/delete_mensaje/<int:id>", methods=["POST"])
@login_required
def delete_mensaje(id):
    db = get_db_connection()
    db.execute("DELETE FROM mensajes WHERE id = ?", (id,))
    db.commit()
    db.close()
    
    flash("Mensaje eliminado de la bandeja.", "success")
    return redirect("/admin")


# --- RUTA PARA BORRAR PROYECTOS DESDE EL PANEL --- #
@app.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):
    # Conectamos a la base de datos
    db = get_db_connection()
    
    # Ejecutamos el borrado filtrando por el ID exacto
    db.execute("DELETE FROM proyectos WHERE id = ?", (id,))
    
    # Guardamos los cambios y cerramos
    db.commit()
    db.close()
    
    # Mensaje de éxito y recargamos el panel
    flash("Proyecto eliminado correctamente.")
    return redirect("/admin")


# --- RUTA PARA EDITAR PROYECTOS DESDE EL PANEL --- #
@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    if request.method == "POST":
        # Capturar datos del texto
        title = request.form.get("title")
        description = request.form.get("description")
        url_github = request.form.get("git_hub")
        
        # Traemos las tecnologias:
        tecnologias = request.form.get("tecnologias")
        
        # Validaciones básicas de texto
        if not title or not description:
            flash("El título y la descripción son obligatorios.", "danger")
            return redirect(f"/edit/{id}")

        # Abrimos conexión temprano para saber qué había antes
        db = get_db_connection()
        proyecto_actual = db.execute("SELECT url_imagen FROM proyectos WHERE id = ?", (id,)).fetchone()
        
        # --- LÓGICA DE IMAGEN MEJORADA ---
        file = request.files.get("imagen")
        
        # Si el usuario seleccionó un archivo nuevo
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            # Si no subió nada, mantenemos el nombre de la imagen anterior
            filename = proyecto_actual['url_imagen']
        
        
        #  Hacemos el UPDATE con el 'filename' correcto (sea el nuevo o el viejo)
        db.execute("""
            UPDATE proyectos 
            SET titulo = ?, descripcion = ?, url_imagen = ?, url_github = ?, tecnologias = ? 
            WHERE id = ?
        """, (title, description, filename, url_github,tecnologias, id))
        
        # Guardamos y cerramos
        db.commit()
        db.close()
        
        flash("¡Proyecto actualizado con éxito!", "success")
        return redirect("/admin")

    # --- LÓGICA PARA EL GET ---
    db = get_db_connection()
    proyecto = db.execute("SELECT * FROM proyectos WHERE id = ?", (id,)).fetchone()
    db.close()
    
    if proyecto is None:
        flash("El proyecto no existe.", "danger")
        return redirect("/admin")
        
    return render_template("edit.html", proyecto=proyecto)


# --- RUTA PARA AÑADIR HABILIDADES DESDE EL PANEL --- #
@app.route("/add_skill", methods=["POST"])
@login_required
def add_skill():
    # Capturar los datos del formulario
    nombre = request.form.get("nombre")
    porcentaje = request.form.get("porcentaje")
    
    # Validaciones básicas
    if not nombre or not porcentaje:
        flash("Debes ingresar el nombre y el porcentaje.", "danger")
        return redirect("/admin")
        
    # Validación de seguridad extra: número entre 0 y 100
    try:
        porcentaje = int(porcentaje)
        if porcentaje < 0 or porcentaje > 100:
            flash("El porcentaje debe ser un número entre 0 y 100.", "danger")
            return redirect("/admin")
    except ValueError:
        flash("El porcentaje ingresado no es válido.", "danger")
        return redirect("/admin")
        
    db = get_db_connection()
    
    # Convertimos ambos a minúsculas (LOWER) para una comparación exacta
    habilidad_existente = db.execute("SELECT * FROM habilidades WHERE LOWER(nombre) = LOWER(?)", (nombre,)).fetchone()
    
    if habilidad_existente:
        # Si encuentra algo, cerramos conexión, enviamos error y cortamos la función
        db.close()
        flash(f"La tecnología '{nombre}' ya se encuentra en tu lista de habilidades.", "danger")
        return redirect("/admin")
    
    # Si no existe, guardamos normalmente
    db.execute("INSERT INTO habilidades (nombre, porcentaje) VALUES (?, ?)", (nombre, porcentaje))
    db.commit()
    db.close()
    
    # Feedback y redirección
    flash(f"¡Habilidad '{nombre}' agregada con éxito!", "success")
    return redirect("/admin")


# --- RUTA PARA EDITAR HABILIDADES DESDE EL PANEL --- #
@app.route("/edit_skill/<int:id>", methods=["GET", "POST"])
@login_required
def edit_skill(id):
    db = get_db_connection()
    
    if request.method == "POST":
        nombre = request.form.get("nombre")
        porcentaje = request.form.get("porcentaje")
        
        # Actualización simple
        db.execute("UPDATE habilidades SET nombre = ?, porcentaje = ? WHERE id = ?", 
                   (nombre, porcentaje, id))
        db.commit()
        db.close()
        
        flash("Habilidad actualizada correctamente", "success")
        return redirect("/admin")

    # GET: Buscamos la habilidad para cargarla en el formulario
    habilidad = db.execute("SELECT * FROM habilidades WHERE id = ?", (id,)).fetchone()
    db.close()
    
    if not habilidad:
        flash("Habilidad no encontrada", "danger")
        return redirect("/admin")
        
    return render_template("edit_skill.html", habilidad=habilidad)
    
    
# --- RUTA PARA ELIMINAR HABILIDADES DESDE EL PANEL --- #
@app.route("/delete_skill/<int:id>", methods=["POST"])
@login_required
def delete_skill(id):
    db = get_db_connection()
    db.execute("DELETE FROM habilidades WHERE id = ?", (id,))
    db.commit()
    db.close()
    
    flash("Habilidad eliminada correctamente.", "success")
    return redirect("/admin")


# --- RUTA PARA AÑADIR TRAYECTORIA DESDE EL PANEL --- #
@app.route("/add_trayectoria", methods=["POST"])
@login_required
def add_trayectoria():
    # Calculamos la fecha de hoy en el formato que usa el HTML (YYYY-MM-DD)
    hoy = date.today().strftime("%Y-%m-%d")
    
    titulo = request.form.get("titulo")
    lugar = request.form.get("lugar")
    descripcion = request.form.get("descripcion")
    fecha_inicio = request.form.get("fecha_inicio")
    tipo = request.form.get("tipo")
    
    # Lógica inteligente para la fecha de fin
    fecha_fin = request.form.get("fecha_fin") or "Actualidad"
    if fecha_fin == hoy or not fecha_fin:
        fecha_fin = "Actualidad"

    # Aseguramos que el tipo se guarde en minusculas
    if tipo:
        tipo = tipo.lower()
    else:
        flash("El tipo es obligatorio", "danger")
        return redirect("/admin")

    db = get_db_connection()
    db.execute("INSERT INTO trayectoria (titulo, lugar, descripcion, fecha_inicio, fecha_fin, tipo) VALUES (?, ?, ?, ?, ?, ?)",
               (titulo, lugar, descripcion, fecha_inicio, fecha_fin, tipo))
    db.commit()
    db.close()
    flash("Trayectoria agregada.", "success")
    return redirect("/admin")


# --- RUTA PARA EDITAR TRAYECTORIA DESDE EL PANEL --- #
@app.route("/edit_trayectoria/<int:id>", methods=["GET", "POST"])
@login_required
def edit_trayectoria(id):
    db = get_db_connection()
    
    # Calculamos la fecha de hoy en el formato que usa el HTML (YYYY-MM-DD)
    hoy = date.today().strftime("%Y-%m-%d")
    
    if request.method == "POST":
        titulo = request.form.get("titulo")
        lugar = request.form.get("lugar")
        descripcion = request.form.get("descripcion")
        fecha_inicio = request.form.get("fecha_inicio")
        tipo = request.form.get("tipo")
        
        # Lógica inteligente para la fecha de fin
        fecha_fin = request.form.get("fecha_fin")
        if fecha_fin == hoy or not fecha_fin:
            fecha_fin = "Actualidad"
            
        if tipo:
            tipo = tipo.lower()
        else:
            flash("El tipo es obligatorio", "danger")
            return redirect("/admin")
            
        db.execute("UPDATE trayectoria SET titulo = ?, lugar = ?, descripcion = ?, fecha_inicio = ?, fecha_fin = ?, tipo = ? WHERE id = ?",
                   (titulo, lugar, descripcion, fecha_inicio, fecha_fin, tipo, id))
        
        db.commit()
        db.close()
        
        flash("¡Trayectoria actualizada exitosamente!", "success")
        return redirect("/admin")

    # --- LÓGICA PARA EL GET ---
    trayectoria = db.execute("SELECT * FROM trayectoria WHERE id = ?", (id,)).fetchone()
    db.close()
    
    if not trayectoria:
        flash("Trayectoria no encontrada", "danger")
        return redirect("/admin")
        
    # Le pasamos la variable 'hoy' a la plantilla también
    return render_template("edit_trayectoria.html", trayectoria=trayectoria, hoy=hoy)
    
    
# --- RUTA PARA ELIMINAR TRAYECTORIA DESDE EL PANEL --- #    
@app.route("/delete_trayectoria/<int:id>", methods=["POST"])
@login_required
def delete_trayectoria(id):
    db = get_db_connection()
    db.execute("DELETE FROM trayectoria WHERE id = ?", (id,))
    db.commit()
    db.close()

    flash("Trayectoria eliminada correctamente.", "success")
    return redirect("/admin")


if __name__ == "__main__":
    app.run(debug=True)


