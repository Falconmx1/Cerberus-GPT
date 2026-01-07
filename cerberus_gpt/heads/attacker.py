# cerberus_gpt/heads/attacker.py
import re
import requests
from typing import Dict, Any, List
from urllib.parse import urljoin, urlparse, parse_qs

class Attacker:
    """Cabeza 2: El Agresor (The Attacker)."""
    
    def __init__(self, model: str, api_key: str):
        self.model = model
        self.api_key = api_key
        # self.client = OpenAI(api_key=api_key) if api_key else None # Para uso futuro con LLM
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Cerberus-GPT/1.0 (Security Testing Tool)'
        })
        print("  - Cabeza de Ataque (Attacker) inicializada.")

    def run(self, target: str, technique: str, **kwargs) -> Dict[str, Any]:
        """Punto de entrada principal para ejecutar una simulación de ataque."""
        print(f"  -> Simulando ataque con técnica: {technique}")
        
        attack_map = {
            "sql_injection": self._simulate_sql_injection,
            "xss": self._simulate_xss,
            "brute_force_ssh": self._simulate_brute_force_ssh, # Mantenemos el esqueleto
            "directory_traversal": self._simulate_directory_traversal, # Mantenemos el esqueleto
            "password_cracking": self._simulate_password_cracking, # Mantenemos el esqueleto
        }

        attack_function = attack_map.get(technique.lower())
        if attack_function:
            return attack_function(target, **kwargs)
        else:
            return {"status": "error", "message": f"Técnica de ataque '{technique}' no soportada."}

    def _simulate_sql_injection(self, target_url: str, payload: str = "' OR '1'='1") -> Dict[str, Any]:
        """
        Simula un ataque de inyección SQL probando el payload en parámetros GET.
        """
        print(f"    -> Probando payload SQLi: {payload}")
        try:
            # Parseamos la URL para encontrar los parámetros
            parsed_url = urlparse(target_url)
            query_params = parse_qs(parsed_url.query)

            if not query_params:
                return {"status": "info", "message": "No se encontraron parámetros GET para inyectar en la URL."}

            # Iteramos sobre cada parámetro para probar el payload
            for param in query_params:
                original_params = parsed_url.query
                # Creamos una nueva query con el payload inyectado en el parámetro actual
                injected_params = query_params.copy()
                injected_params[param] = [payload]
                
                # Reconstruimos la URL con el payload
                from urllib.parse import urlencode
                new_query = urlencode(injected_params, doseq=True)
                attack_url = parsed_url._replace(query=new_query).geturl()

                # Hacemos la petición
                response = self.session.get(attack_url, timeout=10)

                # Analizamos la respuesta en busca de errores SQL comunes
                sql_errors = [
                    "you have an error in your sql syntax",
                    "warning: mysql_fetch_assoc()",
                    "unclosed quotation mark",
                    "microsoft ole db provider for odbc drivers error"
                ]
                
                is_vulnerable = any(err in response.text.lower() for err in sql_errors)
                
                if is_vulnerable:
                    return {
                        "status": "completed",
                        "technique": "SQL Injection",
                        "target": target_url,
                        "payload_used": payload,
                        "vulnerable_parameter": param,
                        "is_vulnerable": True,
                        "evidence": f"La respuesta contenía un error de SQL común al inyectar en el parámetro '{param}'.",
                        "recommendation": "Use sentencias preparadas (prepared statements) o un ORM para sanitizar las entradas del usuario."
                    }

            # Si no se encontró vulnerabilidad en ningún parámetro
            return {
                "status": "completed",
                "technique": "SQL Injection",
                "target": target_url,
                "is_vulnerable": False,
                "message": "No se detectaron vulnerabilidades de SQL Injection con el payload proporcionado."
            }

        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"Error de red: {e}"}
        except Exception as e:
            return {"status": "error", "message": f"Error inesperado: {e}"}

    def _simulate_xss(self, target_url: str, payload: str = "<script>alert('XSS')</script>") -> Dict[str, Any]:
        """
        Simula un ataque de XSS reflejado probando el payload en parámetros GET.
        """
        print(f"    -> Probando payload XSS: {payload}")
        try:
            # La lógica es similar a la de SQLi, pero buscando el payload en la respuesta
            parsed_url = urlparse(target_url)
            query_params = parse_qs(parsed_url.query)

            if not query_params:
                return {"status": "info", "message": "No se encontraron parámetros GET para inyectar en la URL."}
            
            for param in query_params:
                injected_params = query_params.copy()
                injected_params[param] = [payload]
                
                from urllib.parse import urlencode
                new_query = urlencode(injected_params, doseq=True)
                attack_url = parsed_url._replace(query=new_query).geturl()
                
                response = self.session.get(attack_url, timeout=10)
                
                # Comprobamos si el payload se refleja SIN escapar en el HTML de la respuesta
                if payload in response.text:
                    return {
                        "status": "completed",
                        "technique": "Cross-Site Scripting (XSS)",
                        "target": target_url,
                        "payload_used": payload,
                        "vulnerable_parameter": param,
                        "is_vulnerable": True,
                        "evidence": f"El payload se reflejó sin escapar en la respuesta al inyectar en el parámetro '{param}'.",
                        "recommendation": "Escape todos los datos de entrada del usuario antes de renderizarlos en HTML. Utilice una librería de sanitización."
                    }
            
            return {
                "status": "completed",
                "technique": "Cross-Site Scripting (XSS)",
                "target": target_url,
                "is_vulnerable": False,
                "message": "No se detectaron vulnerabilidades de XSS reflejado con el payload proporcionado."
            }

        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"Error de red: {e}"}
        except Exception as e:
            return {"status": "error", "message": f"Error inesperado: {e}"}

    # --- Métodos de ataque que mantendremos como esqueletos por ahora ---
    def _simulate_brute_force_ssh(self, target_ip: str, usernames: List[str] = ["root", "admin"], password_list: List[str] = ["123456", "password", "admin"]) -> Dict[str, Any]:
        print("    -> (Simulación) La lógica real de fuerza bruta SSH requiere librerías como 'paramiko' y es más compleja.")
        return {
            "status": "simulated",
            "technique": "SSH Brute Force",
            "target": target_ip,
            "credentials_found": {"username": "admin", "password": "password"},
            "recommendation": "Deshabilite el login por contraseña y use únicamente claves SSH."
        }

    def _simulate_directory_traversal(self, target_url: str, payload: str = "../../../etc/passwd") -> Dict[str, Any]:
        print("    -> (Simulación) La lógica real es similar a SQLi/XSS, pero buscando contenido de archivos conocidos en la respuesta.")
        return {
            "status": "simulated",
            "technique": "Directory Traversal",
            "target": target_url,
            "is_vulnerable": True,
            "evidence": "La respuesta del servidor devolvió el contenido del archivo /etc/passwd.",
            "recommendation": "Nunca confíe en la entrada del usuario para construir rutas de archivo."
        }

    def _simulate_password_cracking(self, hash_to_crack: str, hash_type: str = "sha256", wordlist: str = "rockyou.txt") -> Dict[str, Any]:
        print("    -> (Simulación) La lógica real requiere 'hashcat' o un bucle de hashing lento.")
        return {
            "status": "simulated",
            "technique": "Password Cracking",
            "target": hash_to_crack,
            "cracked_password": "P@ssw0rd123",
            "recommendation": "Use hashes lentos y con sal (salt) como bcrypt, scrypt o Argon2 en lugar de algoritmos rápidos como SHA-256 o MD5."
        }
