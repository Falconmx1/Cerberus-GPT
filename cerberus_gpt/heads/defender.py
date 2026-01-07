# cerberus_gpt/heads/defender.py
from typing import Dict, Any, List
from openai import OpenAI

class Defender:
    """Cabeza 3: El Guardián (The Guardian)."""
    
    def __init__(self, model: str, api_key: str):
        self.model = model
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key) if api_key else None
        print("  - Cabeza de Defensa (Defender) inicializada.")

    def generate_plan(self, analysis_report: Dict[str, Any], attack_report: Dict[str, Any] = None) -> List[str]:
        """
        Genera un plan de defensa inteligente usando un LLM para sintetizar la evidencia.
        """
        print("  -> Generando plan de defensa inteligente con LLM...")
        
        if not self.client:
            print("  -> [AVISO] No se encontró API Key. Generando plan básico sin LLM.")
            return self._generate_basic_plan(analysis_report, attack_report)

        # 1. Construir el contexto para el LLM
        context = self._build_context(analysis_report, attack_report)

        # 2. Crear el prompt para el LLM
        prompt = f"""
        Eres un experto en ciberseguridad de élite (CISSP, OSCP). Tu tarea es analizar los siguientes reportes de un análisis de seguridad y un ataque simulado, y generar un plan de acción claro, priorizado y conciso.

        El plan debe ser una lista de pasos numerados. Cada paso debe ser una acción directa y ejecutable. Prioriza las acciones que abordan las vulnerabilidades más críticas.

        CONTEXTO:
        {context}

        INSTRUCCIONES:
        - Responde ÚNICAMENTE con la lista de pasos del plan de defensa.
        - No incluyas introducciones, conclusiones ni explicaciones fuera de la lista.
        - El formato debe ser: 1. [Acción], 2. [Acción], etc.
        - Si no hay vulnerabilidades críticas, enfócate en el endurecimiento general.

        PLAN DE DEFENSA:
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3 # Un poco de creatividad, pero enfocada
            )
            
            llm_output = response.choices[0].message.content.strip()
            
            # 3. Parsear la respuesta del LLM en una lista limpia
            plan = [line.strip() for line in llm_output.split('\n') if line.strip()]
            
            return plan

        except Exception as e:
            print(f"  -> [ERROR] Falló la generación del plan con LLM: {e}")
            print("  -> Reintentando con el plan básico...")
            return self._generate_basic_plan(analysis_report, attack_report)

    def _build_context(self, analysis_report: Dict[str, Any], attack_report: Dict[str, Any] = None) -> str:
        """Construye una cadena de texto formateada con la evidencia para el LLM."""
        context_parts = []
        
        # Contexto del Análisis
        if analysis_report and analysis_report.get("status") == "completed":
            context_parts.append("--- REPORTE DE ANÁLISIS ---")
            summary = analysis_report.get("summary", {})
            context_parts.append(f"Vulnerabilidades totales: {summary.get('total_vulnerabilities', 0)}")
            context_parts.append(f"Críticas: {summary.get('critical', 0)}, Altas: {summary.get('high', 0)}, Medias: {summary.get('medium', 0)}")
            
            vulnerabilities = analysis_report.get("vulnerabilities_found", [])
            if vulnerabilities:
                context_parts.append("\nDetalles de Vulnerabilidades:")
                for vuln in vulnerabilities[:5]: # Limitar para no sobrepasar el contexto del LLM
                    context_parts.append(f"- Tipo: {vuln.get('type')}, Severidad: {vuln.get('severity')}, Línea: {vuln.get('line')}, Descripción: {vuln.get('description')}")

        # Contexto del Ataque
        if attack_report and attack_report.get("is_vulnerable"):
            context_parts.append("\n--- REPORTE DE ATAQUE ---")
            context_parts.append(f"Se confirmó una vulnerabilidad de '{attack_report.get('technique')}'.")
            context_parts.append(f"Evidencia: {attack_report.get('evidence')}")
            context_parts.append(f"Recomendación inicial: {attack_report.get('recommendation')}")

        return "\n".join(context_parts)

    def _generate_basic_plan(self, analysis_report: Dict[str, Any], attack_report: Dict[str, Any] = None) -> List[str]:
        """Generador de planes simple (fallback) si no hay LLM."""
        plan = []
        if analysis_report and analysis_report.get("status") == "completed":
            vulnerabilities = analysis_report.get("vulnerabilities_found", [])
            if vulnerabilities:
                plan.append("ALTA PRIORIDAD - Corregir las siguientes vulnerabilidades:")
                for vuln in vulnerabilities:
                    plan.append(f"  - Corregir '{vuln['type']}' (Severidad: {vuln['severity']}).")
        
        if not plan:
            plan.append("No se encontraron vulnerabilidades críticas, pero se recomienda:")
        plan.append("  - Revisar y actualizar todos los componentes del sistema.")
        plan.append("  - Implementar un WAF y un sistema de monitorización.")
        return plan

    # --- Métodos de parcheo y respuesta a incidentes se mantienen como esqueletos ---
    def generate_patch(self, vulnerability: Dict[str, Any]) -> str:
        print("    -> (Simulación) La generación de parches con LLM es una excelente extensión.")
        return "No se pudo generar un parche automático. Por favor, revise manualmente."

    def create_incident_response_plan(self, attack_report: Dict[str, Any]) -> List[str]:
        print("    -> (Simulación) La generación de planes de respuesta a incidentes con LLM es otra gran extensión.")
        return ["Plan de respuesta a incidentes no implementado aún."]
