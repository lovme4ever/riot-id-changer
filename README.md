readme.md
# RIOT ID CHANGER

> Cambiador de Riot ID en Python para **League of Legends** y **Valorant**.

## Descripción

**RIOT ID CHANGER** es un programa en Python que permite cambiar tu Riot ID de manera rápida usando la API local del cliente de Riot (LCU). No requiere abrir el navegador y funciona directamente desde la línea de comandos.

> Funciona únicamente si el Riot Client está abierto y tu cuenta está iniciada.

---

## Características

* Cambia el Riot ID sin usar la web de Riot.


## Tecnologías y librerías

* Python 3.8+
* Librerías usadas:

  * `requests`
  * `base64`
  * `os`
  * `json`
  * `urllib3`

---

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/lovme4ever/riot-id-changer.git
cd riot-id-changer-main
```

2. Crear y activar un entorno virtual:

* Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

* macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Instala las dependencias:

```bash
pip install requests urllib3
---

## Uso

1. Asegúrate de que el **Riot Client** esté abierto y la cuenta iniciada.
2. Ejecuta el script:

```bash
python main.py
```

3. Sigue las instrucciones en pantalla:

   * Ingresa el nuevo Riot ID antes del `#`.
   * Ingresa el tag (4 dígitos después del `#`, opcional).
   * Confirma el cambio.

### Ejemplo

![Example Screenshot](https://github.com/lovme4ever/riot-id-changer/blob/main/ejemplo.png?raw=true)
```
Introduce el nuevo nombre: MiNick
Introduce el nuevo tag (opcional): 1234
Comprobando disponibilidad...
¡El nombre está disponible!
¿Deseas cambiar tu Riot ID a 'MiNick#1234'? (s/n): s
¡Nombre cambiado con éxito!
Tu nuevo Riot ID es: MiNick#1234
```

