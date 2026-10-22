import os
import sys
import time
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Global state for demonstration
SOC_LOGS = []
BURST_COUNTER = 0

def add_log(component, level, message):
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
        "component": component,
        "level": level,
        "message": message
    }
    SOC_LOGS.append(entry)
    if len(SOC_LOGS) > 200:
        SOC_LOGS.pop(0)

# Pre-populate some realistic initial logs
add_log("KERNEL", "INFO", "Linux 5.15.0-generic Ubuntu Server 22.04 LTS inicializado.")
add_log("SSHD", "INFO", "Servicio OpenSSH escuchando en puerto 2222 (Forwarding nativo).")
add_log("PORTAL", "INFO", "Portal Institucional Banco Digital Seguro en línea.")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/simulador/calcular", methods=["POST"])
def calcular_simulador():
    data = request.get_json() or {}
    capacidad = int(data.get("capacidad", 100))
    legitimo = int(data.get("legitimo", 30))
    adicional = int(data.get("adicional", 0))
    mitigacion = bool(data.get("mitigacion", False))

    # Mitigacion educativa: reducción del 80% del tráfico adicional
    if mitigacion:
        adicional_efectivo = round(adicional * 0.2, 1)
        factor_mitigacion = "80% de reducción aplicada"
    else:
        adicional_efectivo = float(adicional)
        factor_mitigacion = "Desactivada (Tráfico sin filtrar)"

    demanda_total = round(legitimo + adicional_efectivo, 1)
    utilizacion_pct = round(min(100.0, (demanda_total / capacidad) * 100.0), 1)
    utilizacion_real = round((demanda_total / capacidad) * 100.0, 1)

    if demanda_total <= capacidad:
        legitimas_atendidas = float(legitimo)
        legitimas_perdidas = 0.0
        disponibilidad = 100.0
        admitidas_total = demanda_total
        no_atendidas_total = 0.0
        if utilizacion_pct <= 70.0:
            estado = "Operación Normal"
            estado_badge = "success"
        else:
            estado = "Congestión Moderada"
            estado_badge = "warning"
    else:
        # La capacidad se comparte proporcionalmente entre legítimos y adicionales
        ratio = capacidad / demanda_total
        legitimas_atendidas = round(legitimo * ratio, 1)
        legitimas_perdidas = round(legitimo - legitimas_atendidas, 1)
        disponibilidad = round((legitimas_atendidas / legitimo) * 100.0, 1)
        admitidas_total = float(capacidad)
        no_atendidas_total = round(demanda_total - capacidad, 1)
        if mitigacion:
            estado = "Sobrecarga Mitigada (Controles Activos)"
            estado_badge = "primary"
        else:
            estado = "Sobrecarga Crítica (Denegación de Servicio)"
            estado_badge = "danger"

    add_log("SIMULADOR", "INFO" if estado_badge in ["success", "primary"] else "WARN",
            f"Escenario evaluado: Capacidad={capacidad}, Legítimo={legitimo}, Adicional={adicional}, Mitigación={mitigacion} -> Disponibilidad={disponibilidad}%, Utilización={utilizacion_real}%")

    return jsonify({
        "capacidad": capacidad,
        "legitimo": legitimo,
        "adicional_solicitado": adicional,
        "adicional_efectivo": adicional_efectivo,
        "mitigacion": mitigacion,
        "factor_mitigacion": factor_mitigacion,
        "demanda_total": demanda_total,
        "utilizacion_pct": utilizacion_pct,
        "utilizacion_real": utilizacion_real,
        "legitimas_atendidas": legitimas_atendidas,
        "legitimas_perdidas": legitimas_perdidas,
        "disponibilidad": disponibilidad,
        "admitidas_total": admitidas_total,
        "no_atendidas_total": no_atendidas_total,
        "estado": estado,
        "estado_badge": estado_badge
    })

@app.route("/api/ping", methods=["GET", "POST"])
def ping():
    global BURST_COUNTER
    BURST_COUNTER += 1
    if BURST_COUNTER % 25 == 0:
        add_log("RATE_MONITOR", "WARN", f"Ráfaga de tráfico detectada: {BURST_COUNTER} peticiones recibidas en ventana de prueba.")
    return jsonify({
        "status": "OK",
        "timestamp": time.time(),
        "total_requests": BURST_COUNTER
    })

@app.route("/api/simular/whaling", methods=["GET"])
def simular_whaling():
    add_log("GOPHISH", "ALERT", "Detección de correo de Whaling dirigido a: director.finanzas@bancodigitalseguro.gob.cl")
    return jsonify({
        "origen": "notificaciones-hacienda@banco-digital-soporte.com (Spoofing)",
        "destinatario": "director.finanzas@bancodigitalseguro.gob.cl",
        "asunto": "URGENTE: Instrucción Extraordinaria de Transferencia y Validación de Firma Digital",
        "fecha": "2026-10-21 14:22:15 CLT",
        "tecnica_mitre": "T1566.002 - Spearphishing Link / Whaling",
        "cabeceras": {
            "Return-Path": "<bounce@servidor-desconocido-ru.net>",
            "SPF": "SoftFail (IP 185.220.101.5 no autorizada para bancodigitalseguro.gob.cl)",
            "DMARC": "Fail (p=none en dominio observado)",
            "X-Mailer": "GoPhish v0.12.1 Mailer Framework"
        },
        "contenido": "Estimado Director: Se ha generado una auditoría urgente en la plataforma financiera. Ingrese con sus credenciales de alto nivel en el siguiente enlace seguro para autorizar la contingencia: http://banco-digital-soporte.com/login?token=whaling_directivo",
        "vector_exito": "El directivo ingresó sus credenciales y fue víctima de robo de sesión VPN sin MFA reforzado."
    })

@app.route("/api/simular/privesc", methods=["POST"])
def simular_privesc():
    add_log("SYSMON_LINUX", "CRITICAL", "Evento ID 1 (Process Creation): Proceso ejecutado con UID 0 (root) desde usuario no privilegiado (admin) vía exploit local.")
    add_log("AUDITD", "WARN", "SYSCALL=execve success=yes arch=c000003e uid=1000 euid=0 exe='/usr/bin/python3'")
    return jsonify({
        "status": "Explotación Exitosa",
        "tecnica_mitre": "T1068 - Exploitation for Privilege Escalation",
        "proceso": "/usr/bin/escalate_demo",
        "usuario_anterior": "admin (UID=1000, GID=1000)",
        "usuario_obtenido": "root (UID=0, GID=0)",
        "evidencia": "Captura en Auditd: SYSCALL execve con euid=0 detectada en Wireshark/Sysmon.",
        "mitigacion": "Parchar kernel/servicios vulnerables, remover permisos SUID innecesarios y segmentar privilegios con AppArmor/SELinux."
    })

@app.route("/api/simular/rootkit", methods=["GET"])
def simular_rootkit():
    add_log("VOLATILITY3", "NOTICE", "Análisis de volcado LiME: Detección de módulo de kernel oculto (stealth_hook_proc).")
    return jsonify({
        "tecnica_mitre": "T1014 - Rootkit",
        "espacio_usuario_ps": [
            {"pid": 1, "name": "systemd", "status": "Visible en ps aux"},
            {"pid": 754, "name": "sshd", "status": "Visible en ps aux"},
            {"pid": 8920, "name": "python3 (portal)", "status": "Visible en ps aux"},
            {"pid": 9411, "name": "[OCULTO POR ROOTKIT]", "status": "Infiltrado (No visible en ps)"}
        ],
        "espacio_memoria_volatility": [
            {"pid": 9411, "name": "kworker_bd_stealth", "estado": "DETECTADO por linux.psscan (inconsistencia en task_struct)", "offset": "0xffff888006b2a000"}
        ],
        "conclusion_forense": "El rootkit manipula las llamadas en /proc pero no puede burlar el análisis forense de memoria RAM física."
    })

@app.route("/api/simular/ransomware/status", methods=["GET"])
def ransomware_status():
    folder = "/home/lab/victima_files"
    files = []
    if os.path.exists(folder):
        for f in os.listdir(folder):
            path = os.path.join(folder, f)
            files.append({
                "nombre": f,
                "tamano": os.path.getsize(path),
                "cifrado": f.endswith(".locked") or f == "NOTA_DE_RESCATE.txt"
            })
    return jsonify({"archivos": files})

@app.route("/api/simular/ransomware/encrypt", methods=["POST"])
def ransomware_encrypt():
    folder = "/home/lab/victima_files"
    count = 0
    if os.path.exists(folder):
        for f in os.listdir(folder):
            if not f.endswith(".locked") and f != "NOTA_DE_RESCATE.txt":
                old_path = os.path.join(folder, f)
                new_path = os.path.join(folder, f + ".locked")
                try:
                    with open(old_path, "r", errors="ignore") as r:
                        content = r.read()
                    with open(new_path, "w") as w:
                        w.write("=== ARCHIVO CIFRADO POR RANSOMWARE (AES-256 SIMULADO) ===\n" + content[::-1])
                    os.remove(old_path)
                    count += 1
                except Exception as e:
                    pass

        # Crear nota de rescate
        with open(os.path.join(folder, "NOTA_DE_RESCATE.txt"), "w") as w:
            w.write("""===================================================================
¡ATENCIÓN! BANCO DIGITAL SEGURO - ARCHIVOS CIFRADOS
===================================================================
Todos sus archivos financieros y bases de datos han sido bloqueados
mediante un algoritmo de cifrado militar de doble llave.

Para obtener la clave de descifrado, debe enviar 5 BTC a la dirección:
bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh

Tiene 48 horas antes de que la clave sea destruida permanentemente.
ID de Víctima: LAB-CHILE-2026-OCT
===================================================================""")

    add_log("RANSOMWARE", "CRITICAL", f"Cifrado masivo detectado en {folder}: {count} archivos alterados. Generada NOTA_DE_RESCATE.txt")
    return jsonify({"status": "Cifrado completado", "archivos_cifrados": count})

@app.route("/api/simular/ransomware/restore", methods=["POST"])
def ransomware_restore():
    src = "/home/lab/backup_offline"
    dst = "/home/lab/victima_files"
    if os.path.exists(src):
        os.system(f"rm -rf {dst} && cp -r {src} {dst}")
        add_log("BLUE_TEAM", "INFO", "Procedimiento de Contingencia: Datos restaurados exitosamente desde Respaldo Offline Limpio.")
        return jsonify({"status": "Restauración completada desde backup limpio"})
    return jsonify({"status": "Error: no existe backup offline"}), 500

@app.route("/api/logs", methods=["GET"])
def get_logs():
    return jsonify({"logs": SOC_LOGS})

@app.route("/api/logs/clear", methods=["POST"])
def clear_logs():
    global SOC_LOGS
    SOC_LOGS = []
    add_log("SOC", "INFO", "Registro de auditoría reiniciado.")
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
