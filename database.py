import pymysql

config = {
    "host": "localhost",
    "user": "USUARIO MYSQL",
    "password": "CONTRASEÑA MYSQL",
    "database": "gas_alerta",
    "port": 3307,#CAMBIAR AL PUERTO CORRESPONDIENTE
    "cursorclass": pymysql.cursors.DictCursor
}

# ============================================================
# OBTENER TODOS LOS USUARIOS
# ============================================================
def obtener_todos_usuarios():
    conn = pymysql.connect(**config)
    cursor = conn.cursor()

    cursor.execute("SELECT correo, enviados FROM usuarios_alerta")
    datos = cursor.fetchall()

    conn.close()
    return datos


# ============================================================
# REGISTRAR USUARIO O SUMAR ENVÍO SI YA EXISTE
# ============================================================
def registrar_usuario(correo):
    conn = pymysql.connect(**config)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO usuarios_alerta (correo, enviados)
        VALUES (%s, 1)
        ON DUPLICATE KEY UPDATE enviados = enviados + 1;
    """, (correo,))

    conn.commit()
    conn.close()


# ============================================================
# SUMAR UN ENVÍO MANUALMENTE (para mailer)
# ============================================================
def sumar_envio(correo):
    conn = pymysql.connect(**config)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE usuarios_alerta
        SET enviados = enviados + 1
        WHERE correo = %s
    """, (correo,))

    conn.commit()
    conn.close()
