# Guía para montarlo

### Instalar dependencias
pip install -r requirements.txt

### Variables de entorno
TOKEN="your token" (http://cursad.jovenclub.cu/login/token.php?username=TU_USUARIO&password=TU_CONTRASEÑA&service=moodle_mobile_app)

### Configurar correo
python3 main.py init "user@example.com" "Passw0rd"

### Cambiar nombre
python3 main.py config displayname "Personal Bot"

### Correr
python3 main.py serve