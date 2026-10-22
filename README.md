# Operación Escudo Digital: Simulación y Respuesta ante DoS/DDoS
**Laboratorio de Ciberseguridad Ofensiva y Defensiva**

Este proyecto contiene el entorno de laboratorio desarrollado para evaluar la resiliencia de la plataforma financiera ficticia **Banco Digital Seguro** frente a escenarios de saturación y degradación de disponibilidad (inspirado en el incidente de Banco Santander Chile de Octubre 2024), integrando la auditoría de cinco vectores de ataque simulados y la evaluación de controles Blue Team.

---

## 👥 Integrantes del Equipo
* **Felipe Vásquez**
* **Diego Parra**
* **Marcelo Mancilla**

---

## 🏗️ Arquitectura y Componentes del Laboratorio

La plataforma está desarrollada en **Python 3 / Flask** con una interfaz interactiva basada en Bootstrap 5 y estructura modular:

1. **🏛️ Portal Financiero Institucional:**  
   Simulación del portal web del banco con diseño sobrio y ministerial (Gobierno de Chile / Banco Digital Seguro), interfaz de consulta ciudadana y avisos de contingencia.
2. **📊 Simulador DoS/DDoS (Fases II y III del Desafío):**  
   Implementación del modelo matemático educativo para calcular métricas de rendimiento y degradación en 4 escenarios oficiales:
   * **Escenario A (Operación Normal):** Capacidad 100, Legítimo 30, Adicional 0, Mitigación OFF.
   * **Escenario B (Incremento Moderado):** Capacidad 100, Legítimo 30, Adicional 100, Mitigación OFF.
   * **Escenario C (Sobrecarga Crítica):** Capacidad 100, Legítimo 30, Adicional 400, Mitigación OFF.
   * **Escenario D (Sobrecarga Mitigada):** Capacidad 100, Legítimo 30, Adicional 400, Mitigación ON (80% de reducción del tráfico adicional).
   * **Ráfaga Ligera en Bucle:** Botón para generar 100 solicitudes HTTP asíncronas para evaluar respuesta en tiempo real.
3. **🎯 Laboratorio de 5 Vectores de Ataque (MITRE ATT&CK):**
   * **Vector 1 - Whaling / Ingeniería Social (`T1566.002`):** Visor de correo malicioso capturado con GoPhish dirigido al directivo, cabeceras falsificadas (`SPF SoftFail`) y enlace de phishing.
   * **Vector 2 - Escalamiento de Privilegios (`T1068`):** Explotación local simulada con cambio de contexto `admin` (UID 1000) a `root` (UID 0) y telemetría en `Auditd` / `Sysmon`.
   * **Vector 3 - Persistencia / Rootkit (`T1014`):** Demostración comparativa de ocultamiento de procesos en espacio de usuario (`ps aux`) vs detección en volcado de memoria física RAM mediante `LiME` y `Volatility 3` (`linux.psscan`).
   * **Vector 4 - DDoS como Cortina de Humo (`T1498`):** Generación de saturación de red simultánea para dispersar la atención del SOC.
   * **Vector 5 - Ransomware + Forense (`T1486`):** Script seguro que cifra archivos de prueba en `victima_files/` a extensión `.locked`, genera la nota de rescate `NOTA_DE_RESCATE.txt` y permite la restauración limpia desde `backup_offline/`.
4. **📟 Consola SOC / Telemetría en Vivo:**  
   Terminal interactiva que registra logs de eventos del kernel, Nginx/Flask, Sysmon y alertas de saturación en tiempo real.

---

## 🚀 Despliegue y Ejecución

### Opción 1: Ejecución directa con Python
```bash
# 1. Clonar el repositorio
git clone https://github.com/DamagedGhost/ciber-lab.git
cd ciber-lab

# 2. Instalar dependencias
pip install flask

# 3. Iniciar la aplicación
python3 app.py
```
Acceder en el navegador a: `http://127.0.0.1:5000`

### Opción 2: Ejecución con Docker Compose
```bash
docker-compose up -d --build
```

---

## 📐 Modelo Matemático del Simulador DoS

* **Demanda Total:**  
  $$D_{total} = \text{Tráfico Legítimo} + \text{Tráfico Adicional Efectivo}$$  
  *(Con mitigación activada, el tráfico adicional se reduce en un 80%, es decir, $\text{Adicional} \times 0.2$)*.
* **Porcentaje de Utilización:**  
  $$\text{Utilización} = \left(\frac{D_{total}}{\text{Capacidad}}\right) \times 100\%$$
* **Disponibilidad:**  
  $$\text{Disponibilidad} = \left(\frac{\text{Solicitudes Legítimas Atendidas}}{\text{Solicitudes Legítimas Recibidas}}\right) \times 100\%$$

---

## 📂 Estructura del Repositorio
```
├── app.py                # Servidor principal Flask y API de simulación
├── templates/
│   └── index.html        # Dashboard web institucional y módulos interactivos
├── victima_files/        # Archivos de prueba utilizados en la simulación de ransomware
├── backup_offline/       # Respaldo seguro utilizado por el Blue Team para restauración
├── dockerfile            # Configuración para contenedor Docker
├── docker-compose.yml    # Orquestación de servicios en puerto 5000
└── README.md             # Documentación técnica del laboratorio
```
