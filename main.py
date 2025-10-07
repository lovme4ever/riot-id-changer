
import requests
import base64
import os
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def find_riot_client_info():
    posibles_rutas = [
        os.path.expandvars(r"%LOCALAPPDATA%\Riot Games\Riot Client\Config\lockfile"),
        os.path.expanduser("~/Library/Application Support/Riot Games/Riot Client/Config/lockfile"),
        os.path.expanduser("~/.local/share/Riot Games/Riot Client/Config/lockfile")
    ]
    for lockfile_path in posibles_rutas:
        if os.path.exists(lockfile_path):
            try:
                with open(lockfile_path, 'r') as f:
                    contenido = f.read().strip()
                    partes = contenido.split(':')
                    if len(partes) >= 4:
                        return {
                            'port': partes[2],
                            'password': partes[3],
                            'protocol': partes[4] if len(partes) > 4 else 'https'
                        }
            except (OSError, IOError):
                continue
    return None

def make_riot_request(endpoint, method='GET', data=None):
    client_info = find_riot_client_info()
    if not client_info:
        raise Exception("El cliente de Riot no está abierto o no se encontró el lockfile")
    port = client_info['port']
    password = client_info['password']
    auth_string = f"riot:{password}"
    auth_bytes = base64.b64encode(auth_string.encode()).decode()
    headers = {
        'Authorization': f'Basic {auth_bytes}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    url = f"https://127.0.0.1:{port}{endpoint}"
    try:
        if method.upper() == 'POST':
            response = requests.post(url, headers=headers, json=data, verify=False)
        else:
            response = requests.get(url, headers=headers, verify=False)
        return response
    except requests.exceptions.RequestException as e:
        raise Exception(f"No se pudo conectar al cliente de Riot: {e}")

def extract_game_name(result):
    game_name = result.get("gameName") or result.get("game_name") or result.get("displayName")
    tag_line = result.get("tagLine") or result.get("tag_line") or result.get("tag")
    if not game_name:
        for key in ["account", "userInfo", "user", "summoner", "player"]:
            nested = result.get(key)
            if isinstance(nested, dict):
                game_name = nested.get("gameName") or nested.get("game_name") or nested.get("displayName")
                tag_line = nested.get("tagLine") or nested.get("tag_line") or nested.get("tag")
                if game_name:
                    break
    return game_name, tag_line

def get_current_riot_id():
    endpoint = "/player-account/aliases/v1/active"
    try:
        response = make_riot_request(endpoint)
        if response.status_code != 200:
            print(f"Depuración: error en el endpoint {endpoint} - código {response.status_code}")
            return None
        result = response.json()
        game_name, tag_line = extract_game_name(result)
        if game_name:
            return f"{game_name}#{tag_line if tag_line else '[desconocido]'}"
    except Exception as e:
        print(f"Depuración: error en {endpoint} - {e}")
    return None

def validate_name(game_name, tag_line=""):
    data = {"gameName": game_name, "tagLine": tag_line}
    response = make_riot_request("/player-account/aliases/v2/validity", "POST", data)
    result = response.json()
    return result.get("isValid", False), result.get("invalidReason", "Error desconocido")

def change_name(game_name, tag_line=""):
    data = {"gameName": game_name, "tagLine": tag_line}
    response = make_riot_request("/player-account/aliases/v1/aliases", "POST", data)
    result = response.json()
    success = result.get("isSuccess", False)
    if success:
        return True, "¡Nombre cambiado con éxito!"
    return False, f"{result.get('errorCode','')} {result.get('errorMessage','Error desconocido')}"

def prompt_for_name():
    game_name = input("Introduce el nuevo nombre: ").strip()
    if not game_name:
        print("El nombre no puede estar vacío.")
        return None, None
    tag_line = input("Introduce el nuevo tag (opcional): ").strip()
    return game_name, tag_line

def restart():
    print("\nReiniciando...\n")
    main()

def main():
    print("=== Cambiador de Riot ID ===")
    print("Asegúrate de que el cliente de Riot esté abierto y hayas iniciado sesión.")
    try:
        client_info = find_riot_client_info()
        if not client_info:
            print("No se encontró el cliente de Riot o no está en ejecución.")
            input("Presiona Enter para salir...")
            return

        print("Conectado al cliente de Riot.")
        current_id = get_current_riot_id()
        if current_id:
            print(f"Tu Riot ID actual es: {current_id}")
        else:
            print("No se pudo obtener el Riot ID actual (el cambio de nombre aún funcionará).")

        print("\nInstrucciones:")
        print("1. Escribe tu nuevo Riot ID (antes del #)")
        print("2. Escribe tu tag (4 dígitos después del #, opcional)")

        game_name, tag_line = prompt_for_name()
        if not game_name:
            choice = input("Presiona [R] para reiniciar o Enter para salir: ").lower()
            if choice == "r":
                restart()
            return

        new_riot_id = f"{game_name}#{tag_line if tag_line else 'auto-generado'}"
        print(f"\nComprobando disponibilidad de '{new_riot_id}'...")
        is_valid, reason = validate_name(game_name, tag_line)
        if not is_valid:
            print(f"Nombre no disponible: {reason}")
            choice = input("Presiona [R] para reiniciar o Enter para salir: ").lower()
            if choice == "r":
                restart()
            return

        print("¡El nombre está disponible!")
        confirm = input(f"¿Deseas cambiar tu Riot ID a '{new_riot_id}'? (s/n): ").lower()
        if confirm not in ['s', 'si', 'sí', 'y', 'yes']:
            print("Operación cancelada.")
            choice = input("Presiona [R] para reiniciar o Enter para salir: ").lower()
            if choice == "r":
                restart()
            return

        print("\nCambiando nombre...")
        success, message = change_name(game_name, tag_line)
        if success:
            print(message)
            print(f"Tu nuevo Riot ID es: {new_riot_id}")
        else:
            print(f"No se pudo cambiar el nombre: {message}")

    except Exception as e:
        print(f"Error: {e}")

    print()
    input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()
