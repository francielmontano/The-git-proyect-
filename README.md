# 🚀 Mini-Git

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Linux](https://img.shields.io/badge/Linux-Terminal-black?logo=linux)
![Git](https://img.shields.io/badge/Git-Version_Control-orange?logo=git)
![Status](https://img.shields.io/badge/Status-In_Development-yellow)

> **Sistema de control de versiones local desarrollado en Python 3 y Linux.**

Mini-Git es un proyecto educativo cuyo objetivo es construir una versión simplificada de un sistema de control de versiones como Git.

El sistema permitirá:

- Inicializar repositorios locales.
- Agregar archivos a un área de preparación (*staging area*).
- Crear instantáneas históricas mediante commits.
- Consultar el historial de cambios.
- Utilizar hashes SHA-1 para verificar la integridad de los archivos.

---

## 📊 Estado del Proyecto

| Fase | Descripción | Estado |
|:---:|---|:---:|
| 1 | Setup y estructura inicial | 🔴 Pendiente |
| 2 | Comando `init` | 🔴 Pendiente |
| 3 | Comando `add` | 🔴 Pendiente |
| 4 | Comando `commit` | 🔴 Pendiente |
| 5 | Comando `log` | 🔴 Pendiente |

> **Regla de desarrollo:** No se avanzará a la siguiente fase hasta completar correctamente la fase actual.

---

# 🏗️ Arquitectura del Proyecto

## 📁 Estructura del repositorio

```text
Bit_proyect/
├── .gitignore
├── README.md
├── requirements.txt
├── .venv/
└── source/
    ├── __init__.py
    ├── main.py
    ├── storage.py
    ├── crypto.py
    └── history.py
```

### Responsabilidad de cada archivo

| Archivo | Responsabilidad |
|---|---|
| `.gitignore` | Excluir archivos innecesarios del repositorio |
| `README.md` | Documentación del proyecto |
| `requirements.txt` | Dependencias externas |
| `source/main.py` | Punto de entrada y gestión de comandos |
| `source/storage.py` | Gestión del sistema de archivos |
| `source/crypto.py` | Generación de hashes SHA-1 |
| `source/history.py` | Gestión de commits e historial |

---

# 🔒 Arquitectura interna de Mini-Git

Al ejecutar:

```bash
python source/main.py init
```

El programa creará:

```text
.minigit/
├── index/
└── commits/
```

### `index/`

Área de preparación (*staging area*).

Contiene copias temporales de los archivos que serán incluidos en el próximo commit.

### `commits/`

Almacena las instantáneas históricas del proyecto.

```text
.minigit/commits/
├── commit_1/
├── commit_2/
└── commit_3/
```

---

# 👥 División de Responsabilidades

## 🧑‍💻 Desarrollador A — Arquitectura e Integración

**Archivos asignados:**

```text
source/main.py
source/history.py
```

**Responsabilidades:**

- Gestionar los comandos del programa.
- Procesar los argumentos de la terminal.
- Controlar el flujo de ejecución.
- Crear y administrar el historial de commits.

**Conocimientos:**

- `sys.argv`
- Importación de módulos.
- Flujo de ejecución.
- Gestión de historial.
- Integración entre módulos.

---

## 🧑‍💻 Desarrollador B — Sistema de Archivos y DevOps

**Archivo asignado:**

```text
source/storage.py
```

**Responsabilidades:**

- Crear directorios.
- Verificar rutas.
- Copiar archivos.
- Copiar carpetas.
- Limpiar el área de staging.

**Conocimientos:**

- `os`
- `shutil`
- `pathlib`
- Manejo de rutas.
- Permisos de archivos.

---

## 🧑‍💻 Desarrollador C — Datos y Criptografía

**Archivo asignado:**

```text
source/crypto.py
```

**Responsabilidades:**

- Leer archivos como bytes.
- Generar hashes SHA-1.
- Detectar cambios en los archivos.
- Verificar la integridad de los datos.

**Conocimientos:**

- `hashlib`
- SHA-1.
- Lectura binaria.
- Integridad de datos.

---

# 🗺️ Roadmap de Desarrollo

## 1. 🎬 Setup y estructura inicial

### Objetivo

Preparar el proyecto y verificar que Python pueda recibir comandos desde la terminal.

### Tareas

- [ ] Crear el repositorio en GitHub.
- [ ] Crear el archivo `.gitignore`.
- [ ] Ignorar la carpeta `.venv/`.
- [ ] Clonar el repositorio.
- [ ] Crear la estructura inicial.
- [ ] Verificar el funcionamiento de `sys.argv`.

### Primera prueba

```bash
python source/main.py init
```

Salida esperada:

```text
Inicializando...
```

---

## 2. 📂 Comando `init`

### Objetivo

Crear automáticamente la estructura interna de Mini-Git.

### Estructura esperada

```text
.minigit/
├── index/
└── commits/
```

### Ejecución

```bash
python source/main.py init
```

### Verificación

```bash
ls -la
```

```bash
ls -R .minigit
```

---

## 3. 📑 Comando `add`

### Objetivo

Agregar un archivo al área de preparación.

### Ejemplo

```bash
python source/main.py add notas.txt
```

El archivo deberá copiarse a:

```text
.minigit/index/notas.txt
```

### Flujo

```text
Archivo modificado
        │
        ▼
       add
        │
        ▼
     index/
        │
        ▼
    Preparado
```

Durante esta fase, `crypto.py` calculará el hash SHA-1 del archivo.

```text
Archivo
   │
   ▼
Lectura en bytes
   │
   ▼
SHA-1
   │
   ▼
Hash de integridad
```

---

## 4. 📸 Comando `commit`

### Objetivo

Crear una instantánea permanente del contenido preparado en `index/`.

### Ejecución

```bash
python source/main.py commit
```

### Flujo

```text
.minigit/index/
        │
        ▼
      commit
        │
        ▼
.minigit/commits/commit_1/
```

Los commits deberán generarse automáticamente:

```text
commit_1
commit_2
commit_3
```

Después de crear el commit, el contenido de `index/` deberá limpiarse.

---

## 5. 📜 Comando `log`

### Objetivo

Mostrar el historial de commits.

### Ejecución

```bash
python source/main.py log
```

### Resultado esperado

```text
commit_1
commit_2
commit_3
```

---

# 🔄 Flujo completo de uso

```bash
# Inicializar el repositorio
python source/main.py init

# Agregar un archivo
python source/main.py add notas.txt

# Crear un commit
python source/main.py commit

# Consultar el historial
python source/main.py log
```

---

# 🐧 Reglas de trabajo en Linux

El equipo utilizará la terminal como herramienta principal para inspeccionar el proyecto.

### Ver archivos ocultos

```bash
ls -la
```

### Ver la ubicación actual

```bash
pwd
```

### Entrar al repositorio Mini-Git

```bash
cd .minigit
```

### Inspeccionar la estructura

```bash
ls -R .minigit
```

También puede utilizarse:

```bash
tree .minigit
```

> **Importante:** El explorador gráfico de archivos no se utilizará para verificar los cambios del repositorio.

---

# 🤝 Programación en Parejas

Durante las sesiones de trabajo se utilizará **Pair Programming**.

| Rol | Responsabilidad |
|---|---|
| 🚗 Conductor | Escribe el código y ejecuta los comandos |
| 🧭 Navegadores | Analizan la lógica y detectan errores |

Los roles se rotarán cada:

> ⏱️ **30 minutos**

El objetivo es que todos los integrantes comprendan la arquitectura completa del proyecto.

---

# 🔀 Flujo de trabajo con Git

Antes de comenzar a trabajar:

```bash
git pull
```

Después de terminar una función o módulo:

```bash
git status
```

```bash
git add .
```

```bash
git commit -m "Descripción breve del cambio"
```

```bash
git push
```

---

## 📝 Ejemplos de commits

### ❌ Evitar

```bash
git commit -m "cambios"
```

### ✅ Recomendado

```bash
git commit -m "Implementa creación del directorio .minigit"
```

```bash
git commit -m "Agrega función para copiar archivos al staging"
```

```bash
git commit -m "Implementa generación de hash SHA-1"
```

```bash
git commit -m "Agrega creación automática de commits"
```

---

# 🎯 Prioridades del Proyecto

## 🔴 Prioridad crítica

Estas funcionalidades forman el núcleo de Mini-Git:

- [ ] Estructura inicial.
- [ ] Comando `init`.
- [ ] Área de staging.
- [ ] Comando `add`.
- [ ] Comando `commit`.
- [ ] Comando `log`.

---

## 🟡 Prioridad secundaria

Una vez terminado el núcleo:

- [ ] Mejorar mensajes de error.
- [ ] Validar rutas inexistentes.
- [ ] Evitar inicializaciones duplicadas.
- [ ] Mejorar la organización del código.
- [ ] Añadir pruebas automatizadas.

---

## 🟢 Mejoras futuras

Estas funcionalidades no son necesarias para la primera versión:

- [ ] Comando `status`.
- [ ] Comando `diff`.
- [ ] Comando `restore`.
- [ ] Mensajes personalizados para commits.
- [ ] Metadatos de autor y fecha.
- [ ] Recuperación de archivos.
- [ ] Sistema avanzado de integridad.

> **Primero se debe construir un núcleo funcional. Las mejoras se implementarán después.**

---

# 🧠 Objetivo Educativo

| Área | Conocimientos |
|---|---|
| 🐍 Python | Módulos, funciones, argumentos y errores |
| 🐧 Linux | Terminal, rutas, archivos y permisos |
| 🔀 Git | Commits, ramas, `push` y `pull` |
| 🔐 Criptografía | Hashes, SHA-1 e integridad |
| 🏗️ Ingeniería | Modularidad y división de responsabilidades |

---

# 🎯 Filosofía del Proyecto

> ## Construir algo pequeño para comprender cómo funcionan los sistemas grandes.

El objetivo de Mini-Git no es reemplazar Git.

El objetivo es comprender sus conceptos fundamentales:

```text
Archivo
   ↓
Staging
   ↓
Commit
   ↓
Historial
   ↓
Integridad mediante Hash
```

---

# 🚀 Próximo Objetivo

## Completar la Fase 1

El primer objetivo del equipo es conseguir que funcione:

```bash
python source/main.py init
```

Y obtener:

```text
Inicializando...
```

Una vez completada esta fase, se comenzará con la creación real del directorio:

```text
.minigit/
```

---

# 👨‍💻 Equipo

| Rol | Responsable | Archivos |
|---|---|---|
| Desarrollador A | Por asignar | `main.py`, `history.py` |
| Desarrollador B | Por asignar | `storage.py` |
| Desarrollador C | Por asignar | `crypto.py` |

---

> **Mini-Git — Aprendiendo los fundamentos de Git construyendo nuestro propio sistema de control de versiones.**
