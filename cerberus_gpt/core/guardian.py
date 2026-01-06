# cerberus_gpt/core/guardian.py
from typing import Dict, Any, List
from ..heads.analyzer import Analyzer
from ..heads.attacker import Attacker
from ..heads.defender import Defender

class Cerberus:
    """
    El guardián de tres cabezas que une las capacidades de análisis,
    ataque y defensa.
    """
    def __init__(self, model_name: str = "gpt-4-turbo", api_key: str = None):
        """
        Inicializa a Cerberus y sus tres cabezas.
        
        Args:
            model_name (str): El nombre del modelo LLM a usar.
            api_key (str): La clave API para el servicio LLM.
        """
        print("🐕‍🦺 Inicializando a Cerberus-GPT...")
        self.analyzer = Analyzer(model=model_name, api_key=api_key)
        self.attacker = Attacker(model=model_name, api_key=api_key)
        self.defender = Defender(model=model_name, api_key=api_key)
        print("✅ Las tres cabezas están listas.")

    # --- Interfaz con la Cabeza de Análisis ---
    def analyze(self, target: str, target_type: str = "code") -> Dict[str, Any]:
        """
        Delega el análisis a la cabeza del Analizador.
        
        Args:
            target (str): El objetivo a analizar (código, IP, etc.).
            target_type (str): El tipo de objetivo ('code', 'network', 'logs').
        
        Returns:
            Dict[str, Any]: Un diccionario con los hallazgos del análisis.
        """
        print(f"🔍 [Cabeza 1: Análisis] Analizando {target_type}: {target}")
        return self.analyzer.run(target, target_type)

    # --- Interfaz con la Cabeza de Ataque ---
    def simulate_attack(self, target: str, technique: str) -> Dict[str, Any]:
        """
        Delega la simulación de ataque a la cabeza del Atacante.
        
        Args:
            target (str): El objetivo del ataque.
            technique (str): La técnica de ataque a simular.
        
        Returns:
            Dict[str, Any]: Un reporte del ataque simulado.
        """
        print(f"⚔️ [Cabeza 2: Ataque] Simulando ataque '{technique}' contra: {target}")
        return self.attacker.run(target, technique)

    # --- Interfaz con la Cabeza de Defensa ---
    def get_defense_plan(self, analysis_report: Dict[str, Any], attack_report: Dict[str, Any] = None) -> List[str]:
        """
        Delega la generación de un plan de defensa a la cabeza del Defensor.
        
        Args:
            analysis_report (Dict[str, Any]): El reporte del análisis.
            attack_report (Dict[str, Any], optional): El reporte del ataque simulado.
        
        Returns:
            List[str]: Una lista de recomendaciones de defensa.
        """
        print("🛡️ [Cabeza 3: Defensa] Generando plan de defensa...")
        return self.defender.generate_plan(analysis_report, attack_report)

    # --- Flujo Completo ---
    def full_audit(self, target: str, target_type: str = "code", attack_technique: str = None) -> Dict[str, Any]:
        """
        Ejecuta el flujo completo: Análisis -> Ataque -> Defensa.
        
        Args:
            target (str): El objetivo a auditar.
            target_type (str): El tipo de objetivo.
            attack_technique (str, optional): La técnica a simular.
        
        Returns:
            Dict[str, Any]: Un resumen completo de la auditoría.
        """
        print("\n--- INICIANDO AUDITORÍA COMPLETA DE CERBERUS ---")
        
        # 1. Análisis
        analysis = self.analyze(target, target_type)
        
        # 2. Ataque (si se especifica)
        attack = None
        if attack_technique:
            attack = self.simulate_attack(target, attack_technique)
        
        # 3. Defensa
        defense_plan = self.get_defense_plan(analysis, attack)
        
        print("--- AUDITORÍA COMPLETA FINALIZADA ---\n")
        
        return {
            "analysis": analysis,
            "attack": attack,
            "defense_plan": defense_plan
        }
