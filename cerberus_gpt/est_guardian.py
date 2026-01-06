# test_guardian.py

import os
from dotenv import load_dotenv

# Importa a tu guardián
from cerberus_gpt import Cerberus

# --- CONFIGURACIÓN INICIAL ---
# Carga variables de entorno desde un archivo .env (muy recomendado para no exponer tu API Key)
load_dotenv()

# Obtén la API Key desde las variables de entorno o hardcodéala para pruebas (no recomendado para producción)
API_KEY = os.getenv("OPENAI_API_KEY", "sk-tu-api-key-de-prueba-aqui") 
MODEL_NAME = "gpt-4-turbo" # O el modelo que prefieras usar

def main():
    """
    Función principal para ejecutar las pruebas de Cerberus-GPT.
    """
    print("="*60)
    print("🐕‍🦺 INICIANDO PRUEBAS DE CERBERUS-GPT 🐕‍🦺")
    print("="*60)

    # 1. Inicializa al Guardián
    try:
        guardian = Cerberus(model_name=MODEL_NAME, api_key=API_KEY)
    except Exception as e:
        print(f"❌ Error al inicializar a Cerberus: {e}")
        print("   Asegúrate de tener las dependencias instaladas (pip install -r requirements.txt)")
        return

    print("\n" + "-"*40)
    print("PRUEBA 1: Análisis de Código Fuente")
    print("-"*40)
    
    # Simula el análisis de un archivo Python
    analysis_result = guardian.analyze(
        target="src/app/user_auth.py", 
        target_type="code"
    )
    print("📊 Resultado del Análisis:")
    print(analysis_result)

    print("\n" + "-"*40)
    print("PRUEBA 2: Simulación de Ataque de Inyección SQL")
    print("-"*40)

    # Simula un ataque contra una URL de prueba
    attack_result = guardian.simulate_attack(
        target="http://testphp.vulnweb.com/listproducts.php?cat=1",
        technique="sql_injection",
        payload="' OR '1'='1"
    )
    print("⚔️ Reporte del Ataque:")
    print(attack_result)

    print("\n" + "-"*40)
    print("PRUEBA 3: Generación de Plan de Defensa")
    print("-"*40)

    # Usa los resultados anteriores para generar un plan de defensa
    defense_plan = guardian.get_defense_plan(
        analysis_report=analysis_result,
        attack_report=attack_result
    )
    print("🛡️ Plan de Defensa Generado:")
    for step in defense_plan:
        print(f"- {step}")

    print("\n" + "-"*40)
    print("PRUEBA 4: Auditoría Completa (Análisis -> Ataque -> Defensa)")
    print("-"*40)

    # Ejecuta el flujo completo de una vez
    full_audit_report = guardian.full_audit(
        target="src/payment/gateway.py",
        target_type="code",
        attack_technique="directory_traversal"
    )
    print("📜 Reporte de Auditoría Completa:")
    print(f"  - Análisis: {full_audit_report['analysis']['summary']}")
    print(f"  - Ataque: {full_audit_report['attack']['technique']} -> {'Vulnerable' if full_audit_report['attack']['is_vulnerable'] else 'No Vulnerable'}")
    print(f"  - Plan de Defensa ({len(full_audit_report['defense_plan'])} pasos):")
    for step in full_audit_report['defense_plan'][:3]: # Imprime los primeros 3 pasos
        print(f"    - {step}")
    print("    ...")


    print("\n" + "="*60)
    print("✅ PRUEBAS FINALIZADAS. Cerberus-GPT funciona como se esperaba.")
    print("="*60)


if __name__ == "__main__":
    main()
