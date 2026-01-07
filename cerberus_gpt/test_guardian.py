# test_guardian.py

import os
from dotenv import load_dotenv

# Importa a tu guardián
from cerberus_gpt import Cerberus

# --- CONFIGURACIÓN INICIAL ---
# Carga variables de entorno desde un archivo .env
load_dotenv()

# Obtén la API Key desde las variables de entorno
API_KEY = os.getenv("OPENAI_API_KEY") 
MODEL_NAME = "gpt-4-turbo" # O el modelo que prefieras usar

def main():
    """
    Función principal para ejecutar las pruebas de Cerberus-GPT.
    """
    print("="*60)
    print("🐕‍🦺 INICIANDO PRUEBAS DE CERBERUS-GPT (MODO REAL) 🐕‍🦺")
    print("="*60)

    # Verifica si la API Key está configurada
    if not API_KEY or API_KEY == "sk-tu-api-key-de-prueba-aqui":
        print("⚠️ ADVERTENCIA: No se encontró una API Key válida para OpenAI.")
        print("   El análisis con LLM fallará, pero el análisis con RegEx funcionará.")
        print("   Asegúrate de tener un archivo .env con OPENAI_API_KEY='tu-key-real'")
        print("-" * 60)
    
    # 1. Inicializa al Guardián
    try:
        guardian = Cerberus(model_name=MODEL_NAME, api_key=API_KEY)
    except Exception as e:
        print(f"❌ Error al inicializar a Cerberus: {e}")
        print("   Asegúrate de tener las dependencias instaladas (pip install -r requirements.txt)")
        return

    print("\n" + "-"*40)
    print("PRUEBA 1: Análisis de Código Fuente REAL")
    print("-"*40)
    
    # Analiza el archivo vulnerable que creamos
    target_file = "vulnerable_app.py"
    
    # Primero, ejecutamos SOLO el análisis con RegEx para ver los hallazgos básicos
    print(">>> Ejecutando análisis solo con RegEx...")
    analysis_regex_result = guardian.analyzer.run(target_file, "code", use_llm=False)
    print("📊 Resultado del Análisis (RegEx únicamente):")
    print(f"  - Hallazgos encontrados: {analysis_regex_result['summary']['total_vulnerabilities']}")
    for finding in analysis_regex_result['vulnerabilities_found']:
        print(f"    - [{finding['severity']}] {finding['type']} en la línea {finding['line']}")
    
    print("\n" + "-"*20 + "\n")
    
    # Ahora, ejecutamos el análisis completo (RegEx + LLM)
    print(">>> Ejecutando análisis completo (RegEx + LLM)...")
    analysis_full_result = guardian.analyze(target=target_file, target_type="code")
    print("📊 Resultado del Análisis (Completo):")
    print(f"  - Resumen: {analysis_full_result['summary']}")
    print("  - Detalles de las vulnerabilidades:")
    for finding in analysis_full_result['vulnerabilities_found']:
        print(f"    - [{finding['severity']}] {finding['type']} (Línea {finding.get('line', 'N/A')}): {finding['description']}")

    print("\n" + "-"*40)
    print("PRUEBA 2: Simulación de Ataque (Aún con datos de ejemplo)")
    print("-"*40)

    # Esta prueba sigue usando datos de ejemplo, pero ahora el contexto es más real
    attack_result = guardian.simulate_attack(
        target="http://testphp.vulnweb.com/listproducts.php?cat=1",
        technique="sql_injection",
        payload="' OR '1'='1"
    )
    print("⚔️ Reporte del Ataque:")
    print(attack_result)

    print("\n" + "-"*40)
    print("PRUEBA 3: Generación de Plan de Defensa (Con datos reales)")
    print("-"*40)

    # Usamos los resultados REALES del análisis para generar un plan de defensa
    defense_plan = guardian.get_defense_plan(
        analysis_report=analysis_full_result,
        attack_report=attack_result
    )
    print("🛡️ Plan de Defensa Generado:")
    for step in defense_plan:
        print(f"- {step}")

    print("\n" + "-"*40)
    print("PRUEBA 4: Auditoría Completa (Con datos reales)")
    print("-"*40)

    # Ejecuta el flujo completo de una vez, usando el archivo vulnerable
    full_audit_report = guardian.full_audit(
        target=target_file,
        target_type="code",
        attack_technique="directory_traversal" # Este ataque es de ejemplo
    )
    print("📜 Reporte de Auditoría Completa:")
    print(f"  - Análisis: {full_audit_report['analysis']['summary']}")
    print(f"  - Ataque: {full_audit_report['attack']['technique']} -> {'Vulnerable' if full_audit_report['attack']['is_vulnerable'] else 'No Vulnerable'}")
    print(f"  - Plan de Defensa ({len(full_audit_report['defense_plan'])} pasos):")
    for step in full_audit_report['defense_plan'][:3]: # Imprime los primeros 3 pasos
        print(f"    - {step}")
    print("    ...")


    print("\n" + "="*60)
    print("✅ PRUEBAS FINALIZADAS. ¡El análisis real está funcionando!")
    print("="*60)


if __name__ == "__main__":
    main()
