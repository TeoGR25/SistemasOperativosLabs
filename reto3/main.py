import subprocess
import re
import sys

def run_command(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()

# -----------------------------
# VALIDACIÓN DE CONTRASEÑA
# -----------------------------
def validar_password(password):
    if " " in password:
        return False, "No puede tener espacios"
    if not re.search(r"[A-Z]", password):
        return False, "Debe tener una mayúscula"
    if not re.search(r"[^A-Za-z0-9]", password):
        return False, "Debe tener un carácter especial"
    if len(password) < 8:
        return False, "Debe tener al menos 8 caracteres"
    return True, ""

# -----------------------------
# VERIFICAR USUARIO
# -----------------------------
def usuario_existe(nombre):
    code, _, _ = run_command(["id", nombre])
    return code == 0

# -----------------------------
# CREAR USUARIO
# -----------------------------
def crear_usuario():
    nombre = input("Nombre de usuario: ")

    if usuario_existe(nombre):
        print("⚠️ El usuario ya existe.")
        return

    password = "Default123!"

    run_command(["useradd", "-m", nombre])
    run_command(["bash", "-c", f"echo '{nombre}:{password}' | chpasswd"])

    run_command(["chage", "-d", "0", nombre])
    run_command(["chage", "-M", "30", "-W", "10", nombre])

    print(f"Usuario {nombre} creado con contraseña por defecto.")

# -----------------------------
# LISTAR USUARIOS
# -----------------------------
def listar_usuarios():
    _, out, _ = run_command(["cut", "-d:", "-f1", "/etc/passwd"])
    print(out)

# -----------------------------
# BLOQUEAR USUARIO
# -----------------------------
def bloquear_usuario():
    nombre = input("Usuario a bloquear: ")

    if not usuario_existe(nombre):
        print("⚠️ Usuario no existe.")
        return

    run_command(["usermod", "-L", nombre])
    print("Usuario bloqueado.")

# -----------------------------
# ACTIVAR USUARIO
# -----------------------------
def activar_usuario():
    nombre = input("Usuario a activar: ")

    if not usuario_existe(nombre):
        print("⚠️ Usuario no existe.")
        return

    run_command(["usermod", "-U", nombre])
    print("Usuario activado.")

# -----------------------------
# ELIMINAR USUARIO
# -----------------------------
def eliminar_usuario():
    nombre = input("Usuario a eliminar: ")

    if not usuario_existe(nombre):
        print("⚠️ Usuario no existe.")
        return

    run_command(["userdel", "-r", nombre])
    print("Usuario eliminado.")

# -----------------------------
# SUDOERS
# -----------------------------
def agregar_sudo():
    nombre = input("Usuario: ")

    if not usuario_existe(nombre):
        print("⚠️ Usuario no existe.")
        return

    try:
        with open("/etc/sudoers.d/lab", "a") as f:
            f.write(f"{nombre} ALL=(ALL) NOPASSWD: /usr/bin/python3 /app/app.py\n")
        print("Usuario agregado a sudoers.")
    except Exception as e:
        print(f"Error: {e}")

# -----------------------------
# MENU
# -----------------------------
def menu():
    while True:
        print("""
1. Crear usuario
2. Listar usuarios
3. Bloquear usuario
4. Activar usuario
5. Eliminar usuario
6. Agregar a sudoers
7. Salir
""")
        opcion = input("Seleccione opción: ")

        if opcion == "1":
            crear_usuario()
        elif opcion == "2":
            listar_usuarios()
        elif opcion == "3":
            bloquear_usuario()
        elif opcion == "4":
            activar_usuario()
        elif opcion == "5":
            eliminar_usuario()
        elif opcion == "6":
            agregar_sudo()
        elif opcion == "7":
            sys.exit()
        else:
            print("Opción inválida")

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    if subprocess.run(["id", "-u"], capture_output=True, text=True).stdout.strip() != "0":
        print("Debe ejecutar como root.")
        sys.exit()

    menu()