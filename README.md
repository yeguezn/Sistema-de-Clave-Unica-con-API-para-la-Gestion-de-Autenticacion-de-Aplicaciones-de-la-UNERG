


# Sistema de Clave Única con API para la Gestión de Autenticación de Aplicaciones de la UNERG

## Descripción General

### Acerca del Proyecto
El presente producto tecnológico formó parte de mi proyecto de grado en la **Universidad Nacional Experimental Rómulo Gallegos** (UNERG). Dicho producto tecnológico fue presentado en Julio del año 2023.

**Autor**: Nelson Yegüez.

**Calificación**: 9/10.

### introducción
Este proyecto consiste en una API que tiene las siguientes características:
- Proporcionar a un usuario administrador las funciones de registrar aplicaciones, registrar usuarios, autorizar y/o denegar el acceso a los usuarios a determinadas aplicaciones.
- Proporcionar al usuario la capacidad de autenticarse en distintas aplicaciones (registradas en la API) con un único par de credenciales, eliminando la necesidad de registrarse en cada una de las aplicaciones.
- Proporcionar al usuario la capacidad de autenticarse en las aplicaciones a través del servicio de Inicio de Sesión Único de Google.

## Principales Herramientas de Desarrollo
- Lenguaje de Programación Python **(versión 3.10.10)**.
- Gestor de Base de datos MongoDB **(versión 6.0.5)**.
- Framework Flask **(versión 2.2.3)**.
- Swagger para documentar y probar la API.
- JSON Web Token (JWT).

## Consideraciones previas a la instalación
Antes de avanzar a la instalación es necesario generar un archivo `.env` que contenga las siguientes variables de entorno:
- `SECRET_KEY`.
- `GOOGLE_CLIENT_ID` y `GOOGLE_CLIENT_SECRET`.
- `DB_NAME`.

**NOTA: Es importante que entre palabras haya un carácter underscore "_" de por medio y, una vez clonado este repositorio (que se explicará más adelante cómo hacerlo), colocar el archivo `.env` debe ir en la raiz del proyecto**.

La `SECRET_KEY` puede contener cualquier valor como por ejemplo: `123`. Sin embargo se sugiere un valor más complejo con el fin de hacer que el proyecto no sea fácilmente vulnerable.

Para generar las variables `GOOGLE_CLIENT_ID` y `GOOGLE_CLIENT_SECRET` debes seguir este [tutorial ](https://support.google.com/workspacemigrate/answer/9222992?hl=es-419). **EL CAMPO PARA LOS ORÍGENES DE JAVASCRIPT AUTORIZADOS SE DEJA VACÍO**. **EN EL CAMPO PARA LA URL DE REDIRECCIONAMIENTO AUTORIZADO COLOCAR EL SIGUIENTE VALOR EN MINÚSCULAS:** `https://sso.unerg.com:5000/google/callback`. 

La variable `DB_NAME` debe contener el valor: `auth_api`.

## Instalación
**NOTA: A partir del paso 2 se debe hacer uso de la terminal o cmd**.
1. Primeramente se necesita registrar el siguiente nombre de dominio `sso.unerg.com` en el archivo hosts del sistema operativo que se esté usando. Este paso es fundamental para poner en marcha el proyecto y usar el servicio de Google. A continuación se describirán los pasos a seguir para modificar el archivo host en lo sistemas operativos Linux y Windows.

[Pasos para modificar el archivo host en windows](./HOST_FILE_WINDOWS_TUTORIAL.md).

[Pasos para modificar el archivo host linux](./HOST_FILE_LINUX_TUTORIAL.md).

2.Clonar este repositorio
```bash
git clone https://github.com/yeguezn/Sistema-de-Clave-Unica-con-API-para-la-Gestion-de-Autenticacion-de-Aplicaciones-de-la-UNERG flask_app
cd flask_app
```
3. Una vez clonado el repositorio, se debe colocar en la raiz del mismo el archivo `.env` ya conteniendo las variables de entorno anteriormente mencionadas y explicadas.
4. Crear un entorno virtual con el siguiente comando
```bash
python3 -m venv venv
```
5. Activar el entorno virtual

Windows
```bash
cd venv/scripts
activate
cd..
cd.. 
```

Linux
```bash
cd venv/bin
source activate
cd .. 
cd .. 
```
6. Instalar las dependencias, se hace con el siguiente comando

Windows

```bash
pip install -r requirements.txt 
```

Linux

```bash
pip3 install -r requirements.txt 
```





