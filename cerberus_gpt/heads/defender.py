# cerberus_gpt/heads/defender.py
from typing import Dict, Any, List

class Defender:
    """
    Cabeza 3: El Guardián (The Guardian).
    
    Encargada de sintetizar la información de las otras dos cabezas para
    generar estrategias de defensa proactivas, parches y planes de respuesta.
    """
    
    def __init__(self, model: str, api_key: str):
        """
        Inicializa la cabeza de defensa.
        
        Args:
            model (str): El nombre del modelo LLM a utilizar.
            api_key (str): La clave API para el servicio LLM.
        """
        self.model = model
        self.api_key = api_key
        # Aquí iría la inicialización del cliente LLM
        print("  - Cabeza de Defensa (Defender) inicializada.")

    def generate_plan(self, analysis_report: Dict[str, Any], attack_report: Dict[str, Any] = None) -> List[str]:
        """
        Genera un plan de defensa basado en los reportes de análisis y ataque.
        
        Lógica real a implementar:
        1. Extraer las vulnerabilidades y hallazgos clave del `analysis_report`.
        2. Si hay un `attack_report`, extraer las técnicas que tuvieron éxito.
        3. Construir un "prompt" para el LLM que incluya todo este contexto.
        4. Pedir al LLM que genere una lista de acciones concretas y priorizadas.
        5. Parsear la respuesta del LLM en una lista limpia.
        
        Args:
            analysis_report (Dict[str, Any]): El reporte de la cabeza de análisis.
            attack_report (Dict[str, Any], optional): El reporte de la cabeza de ataque.
        
        Returns:
            List[str]: Una lista de recomendaciones de defensa, ordenadas por prioridad.
        """
        print("  -> Generando plan de defensa a partir de la evidencia...")
        
        # --- LÓGICA DE SÍNTESIS REAL IRÍA AQUÍ ---
        # Por ahora, simularemos la creación de un plan basado en los datos de entrada.
        
        plan = []
        
        # 1. Analizar el reporte de análisis
        if analysis_report and analysis_report.get("status") == "completed":
            target = analysis_report.get("target", "Objetivo desconocido")
            vulnerabilities = analysis_report.get("vulnerabilities_found", [])
            
            if vulnerabilities:
                plan.append(f"ALTA PRIORIDAD - Corregir las {len(vulnerabilities)} vulnerabilidades encontradas en '{target}':")
                for vuln in vulnerabilities:
                    plan.append(f"  - Corregir '{vuln['type']}' (Severidad: {vuln['severity']}) en la línea {vuln.get('line', 'N/A')}. Detalle: {vuln.get('description', 'N/A')}")
                plan.append("") # Línea en blanco para separar

        # 2. Analizar el reporte de ataque
        if attack_report and attack_report.get("status") == "completed":
            technique = attack_report.get("technique", "Técnica desconocida")
            is_vulnerable = attack_report.get("is_vulnerable", False)
            
            if is_vulnerable:
                plan.append(f"CRÍTICA - Se confirmó una vulnerabilidad mediante un ataque de '{technique}'.")
                plan.append(f"  - Evidencia: {attack_report.get('evidence', 'No disponible')}")
                plan.append(f"  - Acción inmediata: {attack_report.get('recommendation', 'Revisar manualmente.')}")
                plan.append("")
            else:
                plan.append(f"INFORMATIVO - El sistema resistió la simulación de ataque de '{technique}'.")
                plan.append("")

        # 3. Recomendaciones generales (usando un LLM en el futuro)
        plan.append("RECOMENDACIONES GENERALES DE ENDURECIMIENTO:")
        plan.append("  - Implementar un Web Application Firewall (WAF) para filtrar tráfico malicioso.")
        plan.append("  - Asegurar que todos los servicios estén actualizados a sus últimas versiones estables.")
        plan.append("  - Revisar y minimizar los permisos de los usuarios y servicios (Principio de Menor Privilegio).")
        plan.append("  - Establecer un sistema de monitorización y alertas en tiempo real.")
        
        return plan

    def generate_patch(self, vulnerability: Dict[str, Any]) -> str:
        """
        Intenta generar un parche o un snippet de código para una vulnerabilidad específica.
        
        Lógica real a implementar:
        1. Tomar la descripción de la vulnerabilidad y el código afectado.
        2. Usar un LLM de código (como Codex o GPT-4) para generar una versión corregida del código.
        3. Incluir comentarios explicando el cambio.
        
        Args:
            vulnerability (Dict[str, Any]): Un diccionario con los detalles de una vulnerabilidad.
        
        Returns:
            str: Un string con el código parchado y una explicación.
        """
        print(f"  -> Generando parche para: {vulnerability.get('type', 'N/A')}")
        
        # --- LÓGICA DE GENERACIÓN DE PARCHES REAL IRÍA AQUÍ ---
        # Ejemplo simulado para una SQL Injection
        if vulnerability.get("type") == "SQL Injection":
            return """
# CÓDIGO VULNERABLE:
# cursor.execute(f"SELECT * FROM users WHERE name = '{user_name}' AND pass = '{password}'")

# CÓDIGO PARCHEADO (Usando sentencias preparadas):
# Este cambio previene la inyección SQL al separar el comando SQL de los datos.
query = "SELECT * FROM users WHERE name = ? AND pass = ?"
cursor.execute(query, (user_name, password))
"""
        return "No se pudo generar un parche automático para esta vulnerabilidad. Por favor, revise manualmente."

    def create_incident_response_plan(self, attack_report: Dict[str, Any]) -> List[str]:
        """
        Crea un plan de respuesta a incidentes basado en un ataque exitoso.
        
        Args:
            attack_report (Dict[str, Any]): El reporte de un ataque que tuvo éxito.
        
        Returns:
            List[str]: Pasos a seguir para contener, erradicar y recuperar del incidente.
        """
        print("  -> Creando plan de respuesta a incidentes...")
        
        # --- LÓGICA REAL IRÍA AQUÍ ---
        plan = [
            "PLAN DE RESPUESTA A INCIDENTES",
            "============================",
            "1. CONTENCIÓN (Inmediata):",
            f"   - Bloquear la IP atacante ({attack_report.get('target', 'N/A')}) en el firewall.",
            "   - Si el ataque afecta a una aplicación, ponerla en modo mantenimiento.",
            "",
            "2. INVESTIGACIÓN:",
            f"   - Analizar los logs del servidor para encontrar todas las actividades de la IP atacante.",
            f"   - Determinar el alcance exacto del compromiso (¿qué datos se vieron afectados?).",
            "",
            "3. ERRADICACIÓN:",
            f"   - Aplicar el parche recomendado: {attack_report.get('recommendation', 'N/A')}.",
            "   - Forzar el cambio de contraseña de todos los usuarios que pudieron haber sido comprometidos.",
            "",
            "4. RECUPERACIÓN:",
            "   - Restaurar los servicios a su operación normal una vez aplicadas las medidas correctivas.",
            "   - Monitorizar de cerca la actividad en busca de comportamientos anómalos.",
            "",
            "5. LECCIONES APRENDIDAS:",
            "   - Documentar el incidente y las acciones tomadas.",
            "   - Actualizar los procedimientos de seguridad para evitar futuros incidentes similares."
        ]
        return plan
