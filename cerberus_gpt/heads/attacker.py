# test_guardian.py
# ... (el principio del archivo se mantiene igual) ...

def main():
    # ...
    # ... (la PRUEBA 1 de análisis se mantiene igual) ...

    print("\n" + "-"*40)
    print("PRUEBA 2: Ataques Web REALES contra testphp.vulnweb.com")
    print("-"*40)

    # --- Ataque de SQL Injection Real ---
    # ... (el código de la prueba de SQLi se mantiene igual) ...
    
    print("\n" + "-"*20 + "\n")

    # --- Ataque de Directory Traversal Real (NUEVO) ---
    print(">>> Lanzando ataque de Directory Traversal...")
    dt_target = "http://testphp.vulnweb.com/showimage.php?file=./pictures/1.jpg"
    dt_result = guardian.simulate_attack(
        target=dt_target,
        technique="directory_traversal"
    )
    print("⚔️ Reporte del Ataque (Directory Traversal):")
    print(f"  - Estado: {dt_result.get('status')}")
    print(f"  - ¿Vulnerable?: {'Sí' if dt_result.get('is_vulnerable') else 'No'}")
    if dt_result.get('is_vulnerable'):
        print(f"  - Evidencia: {dt_result.get('evidence')}")
    else:
        print(f"  - Mensaje: {dt_result.get('message')}")
    
    print("\n" + "-"*20 + "\n")

    # --- Ataque de XSS Real ---
    # ... (el código de la prueba de XSS se mantiene igual) ...

    print("\n" + "-"*40)
    print("PRUEBA 3: Generación de Plan de Defensa (Con datos reales)")
    print("-"*40)

    # Usamos los resultados del ataque de Directory Traversal para el plan de defensa
    defense_plan = guardian.get_defense_plan(
        analysis_report=analysis_full_result,
        attack_report=dt_result
    )
    print("🛡️ Plan de Defensa Generado:")
    for step in defense_plan:
        print(f"- {step}")

    print("\n" + "="*60)
    print("✅ PRUEBAS FINALIZADAS. ¡El ataque de Directory Traversal está funcionando!")
    print("="*60)

# ... (el resto del archivo se mantiene igual) ...
