# 🗳️ Sistema Electoral SENA
Plataforma web diseñada para gestionar elecciones estudiantiles de forma transparente, segura y participativa. Este software permite a los estudiantes postularse, presentar sus propuestas, y votar por sus representantes de manera digital.

## 📌 Características principales
🔐 Autenticación segura para votantes, candidatos y administradores

🧑‍🎓 Panel de candidatos con perfiles, propuestas y multimedia

📊 Sistema de votación en tiempo real con control de duplicidad

📅 Cuenta regresiva automática para cierre de postulaciones

🎥 Soporte para videos de campaña y propuestas visuales

📄 Panel administrativo para gestión de usuarios, vacantes y resultados.

## 🧠 Tecnologías utilizadas
Backend:	
Django 

Base de datos:
mysql

Estilos:
CSS
Tailwind

Front:
HTML
JS


## 🚀 Cómo iniciar el proyecto


## Clona el repositorio
bash
git clone https://github.com/krigeer/Votaciones.git

## Entra al directorio
bash
cd sistema-electoral-sena

## Instala dependencias
bash
pip install -r requirements.txt

## Ejecuta migraciones
bash
python manage.py migrate

## IMPORTANTE
antes de iniciar el servidor debes de incorporar datos en la base de datos para poder que funcione el servidor los datos son: 
Fecha_votacion: se debe adjuntar una fecha de inicio de votación para permitir que se inicie el conteo de las eleciones y ya con esto funciona,
Al momento de iniciar el sistema se deben de registrar 3 roles en la tabla de roles y este debe ser el orden:
         - gestor
         -candidato
         -votante
         
preferiblemente es mejor añadir datos en todas las tablas que son heredadas.

## Inicia el servidor
python manage.py runserver



## 🎯 Objetivo del proyecto
Este sistema busca fortalecer la democracia estudiantil facilitando procesos electorales modernos, accesibles y confiables. Está diseñado para adaptarse a diferentes sedes, fichas y cargos representativos.


## 🤝 Contribuciones
¡Tu ayuda es bienvenida! Si deseas mejorar el sistema, corregir errores o proponer nuevas funcionalidades, abre un issue o haz un pull request.

## 📄 Licencia
Este proyecto está bajo la licencia MIT. Puedes usarlo, modificarlo y distribuirlo libremente.



# 📄 NOTA
1). El sistema cuenta con una plantilla para cargar los votantes al sistema, para poder que la plantilla funcione correctamente los campos que estan en la plantilla deben conicidir con los datos registrados en la base de datos y los campos de las tablas

2). Al momento de iniciar el sistema se deben de registrar 3 roles en la tabla de roles y este debe ser el orden:

         - gestor
         -candidato
         -votante
