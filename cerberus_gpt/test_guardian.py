# test_guardian.py

import os
from dotenv import load_dotenv

# Importa a tu guardián
from cerberus_gpt import Cerberus

# --- CONFIGURACIÓN INICIAL ---
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY") 
MODEL_NAME = "gpt-4-turbo"

def main():
    print("="*60)
    print("🐕‍🦺 INICIANDO PRUEBAS DE CERBERUS-GPT (MODO REAL) 🐕‍🦺")
    print("="*60)

    if not API_KEY or API_KEY == "sk-tu-api-key-de-prueba-aqui":
        print("⚠️ ADVERTENCIA: No se encontró una API Key válida para OpenAI.")
        print("   El análisis con LLM fallará, pero el análisis con RegEx y los ataques funcionarán.")
        print("-" * 60)
    
    try:
        guardian = Cerberus(model_name=MODEL_NAME, api_key=API_KEY)
    except Exception as e:
        print(f"❌ Error al inicializar a Cerberus: {e}")
        return

    print("\n" + "-"*40)
    print("PRUEBA 1: Análisis de Código Fuente REAL")
    print("-"*40)
    
    target_file = "vulnerable_app.py"
    analysis_full_result = guardian.analyze(target=target_file, target_type="code")
    print("📊 Resultado del Análisis (Completo):")
    print(f"  - Resumen: {analysis_full_result['summary']}")
    print("  - Detalles de las vulnerabilidades:")
    for finding in analysis_full_result['vulnerabilities_found']:
        print(f"    - [{finding['severity']}] {finding['type']} (Línea {finding.get('line', 'N/A')}): {finding['description']}")

    print("\n" + "-"*40)
    print("PRUEBA 2: Ataques Web REALES contra testphp.vulnweb.com")
    print("-"*40)

    # --- Ataque de SQL Injection Real ---
    print(">>> Lanzando ataque de SQL Injection...")
    sqli_target = "http://testphp.vulnweb.com/listproducts.php?cat=1"
    sqli_result = guardian.simulate_attack(
        target=sqli_target,
        technique="sql_injection",
        payload="' OR '1'='1"
    )
    print("⚔️ Reporte del Ataque (SQLi):")
    print(f"  - Estado: {sqli_result.get('status')}")
    print(f"  - ¿Vulnerable?: {'Sí' if sqli_result.get('is_vulnerable') else 'No'}")
    if sqli_result.get('is_vulnerable'):
        print(f"  - Evidencia: {sqli_result.get('evidence')}")
    else:
        print(f"  - Mensaje: {sqli_result.get('message')}")
    
    print("\n" + "-"*20 + "\n")

    # --- Ataque de XSS Real ---
    print(">>> Lanzando ataque de XSS Reflejado...")
    xss_target = "http://testphp.vulnweb.com/search.php?test=query"
    xss_result = guardian.simulate_attack(
        target=xss_target,
        technique="xss",
        payload="<script>alert('XSS')</script>"
    )
    print("⚔️ Reporte del Ataque (XSS):")
    print(f"  - Estado: {xss_result.get('status')}")
    print(f"  - ¿Vulnerable?: {'Sí' if xss_result.get('is_vulnerable') else 'No'}")
    if xss_result.get('is_vulnerable'):
        print(f"  - Evidencia: {xss_result.get('evidence')}")
    else:
        print(f"  - Mensaje: {xss_result.get('message')}")

    print("\n" + "-"*40)
    print("PRUEBA 3: Generación de Plan de Defensa (Con datos reales)")
    print("-"*40)

    # Usamos los resultados REALES de ambos análisis y ataque
    defense_plan = guardian.get_defense_plan(
        analysis_report=analysis_full_result,
        attack_report=sqli_result # Priorizamos el plan de defensa basado en el ataque que tuvo éxito
    )
    print("🛡️ Plan de Defensa Generado:")
    for step in defense_plan:
        print(f"- {step}")

    print("\n" + "="*60)
    print("✅ PRUEBAS FINALIZADAS. ¡El ataque real está funcionando!")
    print("="*60)


if __name__ == "__main__":
    main()
