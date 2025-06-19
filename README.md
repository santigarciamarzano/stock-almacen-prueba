# Proyecto de Gestión de Inventario

Aplicación web full-stack para la gestión de un inventario simple, parte de un desafío técnica. El proyecto permite visualizar, actualizar y auditar el stock de productos en un almacén.

## Características Principales

*   **Listado de Stock:** Visualización en tiempo real del stock de todos los ítems.
*   **Actualización de Stock:** Permite establecer una cantidad total de stock o ajustarla (sumar/restar) para cada ítem.
*   **Historial de Movimientos:** Registro detallado de cada entrada y salida de stock, con fecha y hora.
*   **Auditoría Completa:** Posibilidad de limpiar el historial de movimientos para mantenimiento.

## Tecnologías Utilizadas

*   **Frontend:** React (creado con Vite)
*   **Backend:** Python con FastAPI
*   **Base de Datos:** PostgreSQL (gestionada con Docker)
*   **ORM (Object-Relational Mapping):** SQLAlchemy

---

## Requisitos Previos

Asegúrate de tener instalados los siguientes programas en tu sistema:
*   [Docker](https://www.docker.com/products/docker-desktop/)
*   [Python 3.10+](https://www.python.org/downloads/)
*   [Node.js 16+](https://nodejs.org/) (incluye npm)

## Guía de Instalación y Ejecución

Sigue estos pasos en orden para levantar la aplicación completa.

### 1. Backend y Base de Datos

a. **Clona el repositorio** (si aún no lo has hecho):
```bash
git clone [URL de tu repositorio]
cd [nombre-de-la-carpeta-del-proyecto]
```
b. **Inicia la Base de Datos con Docker:**
Abre una terminal y ejecuta el siguiente comando. Esto creará y ejecutará un contenedor de PostgreSQL en segundo plano.
```bash
docker run --name inventory-postgres -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_USER=myuser -e POSTGRES_DB=inventorydb -p 5432:5432 -d postgres
```
Nota: Si el contenedor ya existe de una ejecución anterior, puedes simplemente iniciarlo con:

```bash
docker start inventory-postgres.
```
c. **Configura el Entorno Virtual con Conda:**
Desde la carpeta raíz del proyecto, crea y activa un entorno de Conda.
```bash
# Crea un nuevo entorno llamado 'almacen' con una versión de Python 3.10 o +
conda create --name almacen python=3.10

# Activa el entorno
conda activate almacen
```
d. **Instala las Dependencias del Backend:**
Asegúrate de que tu entorno `almacen` esté activado y luego ejecuta:
```bash
pip install -r requirements.txt
```
e. **Ejecuta el Servidor del Backend:**
El servidor de la API se iniciará y estará disponible en `http://localhost:8000`.
```bash
uvicorn backend.main:app --reload
```
Deja esta terminal abierta.

f. **(Opcional) Poblar la Base de Datos:**
Para tener datos iniciales, se pued usar una herramienta gráfica como [DBeaver](https://dbeaver.io/) para conectar a la base de datos e insertar filas en la tabla `items`.

*   **Host:** `localhost`
*   **Puerto:** `5432`
*   **Base de datos:** `inventorydb`
*   **Usuario:** `myuser`
*   **Contraseña:** `mysecretpassword`

### 2. Frontend

a. **Abre una SEGUNDA terminal.**

b. **Navega a la Carpeta del Frontend:**
Desde la carpeta raíz del proyecto, entra al directorio del frontend.

```bash
cd frontend
```
c. **Instala las Dependencias del Frontend:**

```bash
npm install
```
d. **Ejecuta el Servidor de Desarrollo del Frontend:**
La aplicación web estará disponible en tu navegador en http://localhost:5173.

```bash
npm run dev
```
Deja esta segunda terminal abierta.


