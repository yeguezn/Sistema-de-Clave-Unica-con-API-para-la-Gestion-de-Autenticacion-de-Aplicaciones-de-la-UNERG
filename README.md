# Sistema-de-Clave-Unica-con-API-para-la-Gestion-de-Autenticacion-de-Aplicaciones-de-la-UNERG
****************Requisitos******************

1)Tener el lenguaje de programación Python instalado.

2)Tener mongodb y mongodb compass instalado. Además de tener creada
una base de datos "users" y en ella tener creadas las siguientes colecciones: 
admin, users_accounts, cellphone, developers. Los schemas de las colecciones
ya dichas figuran en la carpeta db del proyecto.

NOTA: Se usó la versión 3.10.10 de python, mongodb compass 1.36.1 y
la versión 6.0.5 de mongodb.


**************Pasos de instalación****************

1) Acceder a esta ruta: C:\Windows\System32\drivers\etc y modificar el archivo "hosts", agregando
el siguiente host: "127.0.0.1       sso.unerg.com" (sin comillas).

2)Descomprimir el archivo flask_app.rar.

3)Acceder por terminal a la carpeta flask_app crear un entorno virtual con el comando: 
"python -m venv venv" (sin comillas), ejemplo: 
"C:\Users\USUARIO\Desktop\grado II\flask_app>python -m venv venv" (sin comillas).

4)Una vez creado el entorno virtual se debe acceder a la carpeta "venv", luego a la carpeta 
"scripts" y una vez dentro de esa carpeta ejecutar el archivo "activate" (todo esto hecho en
la terminal), ejemplo: "C:\Users\USUARIO\Desktop\grado II\flask_app\venv\Scripts>activate" 
(sin comillas).

5)Volver a la raíz de la carpeta flask_app y ejecutar el comando 
"pip install -r requirements.txt" para instalar las dependencias necesarias para ejecutar el
proyecto, ejemplo: 
"C:\Users\USUARIO\Desktop\grado II\flask_app>pip install -r requirements.txt" (sin comillas).

6)Ejecutar el comando "python app.py", ejemplo:
"C:\Users\USUARIO\Desktop\grado II\flask_app>python app.py" (sin comillas).

7)Acceder a: https://sso.unerg.com:5000/swagger/
