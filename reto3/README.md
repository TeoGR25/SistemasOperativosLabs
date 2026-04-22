# Laboratorio: Administración de Usuarios en Linux con Docker y Python

## Descripción

Este proyecto implementa un sistema de administración de usuarios en Linux utilizando Python dentro de un contenedor Docker.

Permite realizar operaciones de crear, eliminar, bloquear, activar y gestión de permisos de usuarios desde consola.

---

## Requisitos

* Docker Desktop instalado
* Sistema operativo Windows / Linux / Mac

---

## Construcción del contenedor

```bash
docker build -t reto3 .
```

---

## Ejecución del contenedor

```bash
docker run -it reto3
```

---

## Ejecución del programa

Dentro del contenedor:

```bash
python3 main.py
```

---

## Configuración de seguridad (IMPORTANTE)

### 1. Políticas de contraseña (PAM)

Editar el archivo:

```bash
nano /etc/pam.d/common-password
```

Agregar o modificar la línea:

```bash
password requisite pam_pwquality.so retry=3 minlen=8 ucredit=-1 ocredit=-1
```

Eso garantiza:

* Mínimo 8 caracteres
* Al menos una mayúscula
* Al menos un carácter especial
* Sin espacios

---

### 2. Mensaje de advertencia personalizado

Editar:

```bash
nano /etc/motd
```

Agregar:

```
Su contraseña está próxima a vencer. Cámbiela pronto.
```

---

## Funcionalidades implementadas

* Crear usuario con contraseña por defecto
* Forzar cambio de contraseña en primer login
* Listar usuarios del sistema
* Bloquear usuario
* Activar usuario
* Eliminar usuario
* Asignar permisos sudo limitados al programa
* Configuración de expiración de contraseña
* Advertencia de vencimiento

---

## Control de acceso

El sistema solo puede ser ejecutado por el usuario root:

```bash
sudo python3 main.py
```

---

## Tecnologías utilizadas

* Python 3
* Docker
* Linux (Ubuntu)
* Comandos de administración de usuarios (useradd, usermod, chage, etc.)

---

## Notas

* La expiración de contraseñas se gestiona mediante `chage`
* El bloqueo automático ocurre cuando la contraseña expira
* Las políticas de seguridad son aplicadas mediante PAM

