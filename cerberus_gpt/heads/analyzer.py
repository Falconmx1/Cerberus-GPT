# cerberus_gpt/heads/analyzer.py
import re
import os
from typing import Dict, Any, List
from openai import OpenAI

class Analyzer:
    """Cabeza 1: El Observador (The Watcher)."""
    
    def __init__(self, model: str, api_key: str):
        self.model = model
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key) if api_key else None
        print("  - Cabeza de Análisis (Analyzer) inicializada.")

    def run(self, target: str, target_type: str, use_llm: bool = True) -> Dict[str, Any]:
        """
        Ejecuta el análisis. Primero intenta un análisis con regex, y si se
        permite, refina los hallazgos con un LLM.
        """
        print(f"  -> Analizando objetivo de tipo: {target_type}")
        
        if target_type == "code":
            # 1. Análisis con RegEx
            initial_findings = self._analyze_code_with_regex(target)
            
            # 2. Análisis con LLM (si está disponible y se activa)
            llm_findings = []
            if use_llm and self.client:
                print("  -> Refinando análisis con LLM...")
                llm_findings = self._analyze_code_with_llm(target)
            
            # 3. Fusionar y priorizar resultados
            all_findings = initial_findings + llm_findings
            
            return {
                "status": "completed",
                "target": target,
                "vulnerabilities_found": all_findings,
                "summary": self._generate_summary(all_findings)
            }
        # ... (lógica para network y logs iría aquí) ...
        else:
            return {"status": "error", "message": f"Tipo de análisis '{target_type}' no soportado."}

    def _analyze_code_with_regex(self, file_path: str) -> List[Dict[str, Any]]:
        """Analiza el código usando patrones de expresiones regulares."""
        findings = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.splitlines()
        except FileNotFoundError:
            return [{"type": "File Error", "severity": "Error", "line": "N/A", "description": f"Archivo no encontrado: {file_path}"}]
        except Exception as e:
            return [{"type": "Read Error", "severity": "Error", "line": "N/A", "description": f"No se pudo leer el archivo: {e}"}]

        # Patrones de vulnerabilidades comunes
        patterns = {
            "Hardcoded Password": re.compile(r"(password\s*=\s*['\"][^^'\"]{8,}['\"])"),
            "SQL Injection (f-string)": re.compile(r"(cursor\.execute$$f\".*?\{.*?\}.*?\"))"),
            "SQL Injection (string format)": re.compile(r"(cursor\.execute$$\".*?%.*?\".*?%.*?$$)"),
            "Command Injection": re.compile(r"(os\.system$$|subprocess\.call$$.*shell=True)"),
            "Insecure Deserialization": re.compile(r"(pickle\.loads$$|cPickle\.loads$$)"),
            "Debug/Print Statement": re.compile(r"(print$$|console\.log$$)")
        }

        for line_num, line in enumerate(lines, 1):
            for vuln_type, pattern in patterns.items():
                if pattern.search(line):
                    severity = "Critical" if "Password" in vuln_type else ("High" if "SQL" in vuln_type or "Command" in vuln_type else "Low")
                    findings.append({
                        "type": vuln_type,
                        "severity": severity,
                        "line": line_num,
                        "description": f"Patón potencial para '{vuln_type}' detectado.",
                        "code_snippet": line.strip()
                    })
        return findings

    def _analyze_code_with_llm(self, file_path: str) -> List[Dict[str, Any]]:
        """Usa un LLM para un análisis más profundo y contextual."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()
        except Exception as e:
            return [{"type": "LLM Read Error", "severity": "Error", "line": "N/A", "description": f"No se pudo leer el archivo para el LLM: {e}"}]

        prompt = f"""
        Analiza el siguiente código fuente en busca de vulnerabilidades de seguridad.
        Clasifica cada hallazgo por tipo (ej. 'SQL Injection', 'XSS', 'Hardcoded Secret') y severidad ('Critical', 'High', 'Medium', 'Low').
        Proporciona la línea de código donde ocurre y una breve descripción.
        Responde ÚNICAMENTE en formato JSON, como una lista de objetos.

        Código a analizar:
        ```python
        {code_content}
        ```

        Respuesta JSON esperada:
        [
            {{"type": "Tipo de Vulnerabilidad", "severity": "Severidad", "line": 1, "description": "Descripción del problema."}},
            ...
        ]
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            
            # El LLM debería devolver una cadena JSON
            llm_output = response.choices[0].message.content
            
            # Intentar parsear el JSON
            import json
            findings = json.loads(llm_output)
            
            # Validar que la estructura sea correcta
            if not isinstance(findings, list):
                return []
                
            return findings

        except json.JSONDecodeError:
            return [{"type": "LLM Parsing Error", "severity": "Medium", "line": "N/A", "description": "El LLM no devolvió un JSON válido."}]
        except Exception as e:
            return [{"type": "LLM API Error", "severity": "Error", "line": "N/A", "description": f"Error en la llamada a la API del LLM: {e}"}]

    def _generate_summary(self, findings: List[Dict[str, Any]]) -> Dict[str, int]:
        """Genera un resumen de las vulnerabilidades encontradas."""
        summary = {"total_vulnerabilities": len(findings), "critical": 0, "high": 0, "medium": 0, "low": 0, "error": 0}
        for finding in findings:
            severity = finding.get("severity", "low").lower()
            if severity in summary:
                summary[severity] += 1
        return summary

    # --- Métodos de red y logs se mantienen igual por ahora ---
    def _analyze_network(self, target_ip: str) -> Dict[str, Any]:
        # (Lógica de análisis de red real iría aquí)
        return {"status": "not_implemented", "message": "Análisis de red no implementado aún."}

    def _analyze_logs(self, log_file_path: str) -> Dict[str, Any]:
        # (Lógica de análisis de logs real iría aquí)
        return {"status": "not_implemented", "message": "Análisis de logs no implementado aún."}
