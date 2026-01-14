import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from database import obtener_todos_usuarios, sumar_envio
from datetime import datetime

# ============================================
# CONFIGURACIÓN DEL SERVIDOR DE CORREO
# ============================================
EMAIL_SENDER = "CORREO"
EMAIL_PASSWORD = "CONTRASEÑA"  # IMPORTANTE: Usa una contraseña de aplicación de Gmail

# Para obtener tu contraseña de aplicación:
# 1. Ve a myaccount.google.com
# 2. Seguridad → Verificación en 2 pasos (debe estar activada)
# 3. Contraseñas de aplicaciones → Generar nueva
# 4. Selecciona "Correo" y "Otro (nombre personalizado)"
# 5. Copia la contraseña de 16 caracteres


def enviar_correo(ao, do):
    """
    Envía alertas de gas a todos los usuarios registrados en la base de datos.
    Función principal compatible con ws_client.py
    
    Args:
        ao: Valor de sensor analógico
        do: Valor de sensor digital
    
    Returns:
        str: Mensaje de resultado
    """
    
    # Obtener todos los usuarios
    try:
        usuarios = obtener_todos_usuarios()
    except Exception as e:
        return f"Error al obtener usuarios de la BD: {e}"
    
    if not usuarios:
        return "No hay usuarios registrados en el sistema"
    
    # Validar configuración
    if not EMAIL_PASSWORD:
        return "EMAIL_PASSWORD no configurada. Agrega tu contraseña de aplicación."
    
    # Contadores
    exitosos = 0
    fallidos = 0
    errores = []
    
    # Timestamp de la alerta
    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # Conectar al servidor SMTP una sola vez
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10)
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        
        # Enviar a cada usuario
        for usuario in usuarios:
            correo_destino = usuario.get("correo", "")
            
            if not correo_destino:
                continue
            
            try:
                # Crear mensaje individual
                msg = MIMEMultipart("alternative")
                msg["Subject"] = "ALERTA CRÍTICA: Detección de Gas - GasAlert D.A.T"
                msg["From"] = f"GasAlert System <{EMAIL_SENDER}>"
                msg["To"] = correo_destino
                
                # Contenido HTML profesional y moderno
                mensaje_html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <style>
                        * {{
                            margin: 0;
                            padding: 0;
                            box-sizing: border-box;
                        }}
                        body {{
                            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            padding: 40px 20px;
                            line-height: 1.6;
                        }}
                        .email-wrapper {{
                            max-width: 650px;
                            margin: 0 auto;
                            background-color: #ffffff;
                            border-radius: 16px;
                            overflow: hidden;
                            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                        }}
                        
                        /* HEADER */
                        .header {{
                            background: linear-gradient(135deg, #ff4757 0%, #d63031 100%);
                            padding: 50px 40px;
                            text-align: center;
                            position: relative;
                            overflow: hidden;
                        }}
                        .header::before {{
                            content: '';
                            position: absolute;
                            top: 0;
                            left: 0;
                            right: 0;
                            height: 4px;
                            background: linear-gradient(90deg, #ff6b6b, #feca57, #48dbfb, #ff6b6b);
                        }}
                        .alert-icon {{
                            width: 80px;
                            height: 80px;
                            background-color: rgba(255, 255, 255, 0.2);
                            border: 4px solid #ffffff;
                            border-radius: 50%;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            margin: 0 auto 20px;
                            font-size: 40px;
                            font-weight: bold;
                            color: #ffffff;
                            animation: pulse 2s infinite;
                        }}
                        @keyframes pulse {{
                            0%, 100% {{ transform: scale(1); }}
                            50% {{ transform: scale(1.05); }}
                        }}
                        .header h1 {{
                            color: #ffffff;
                            font-size: 32px;
                            font-weight: 700;
                            margin-bottom: 10px;
                            letter-spacing: -0.5px;
                        }}
                        .header p {{
                            color: rgba(255, 255, 255, 0.95);
                            font-size: 16px;
                            font-weight: 500;
                        }}
                        
                        /* CONTENT */
                        .content {{
                            padding: 45px 40px;
                        }}
                        .alert-badge {{
                            display: inline-block;
                            background: linear-gradient(135deg, #ff4757, #d63031);
                            color: #ffffff;
                            padding: 10px 20px;
                            border-radius: 25px;
                            font-size: 13px;
                            font-weight: 700;
                            text-transform: uppercase;
                            letter-spacing: 1px;
                            margin-bottom: 25px;
                        }}
                        .main-message {{
                            background: linear-gradient(135deg, #fff5f5 0%, #ffe5e5 100%);
                            border-left: 5px solid #ff4757;
                            padding: 25px;
                            border-radius: 10px;
                            margin-bottom: 30px;
                        }}
                        .main-message h2 {{
                            color: #2d3436;
                            font-size: 22px;
                            margin-bottom: 12px;
                            font-weight: 700;
                        }}
                        .main-message p {{
                            color: #636e72;
                            font-size: 15px;
                            line-height: 1.7;
                        }}
                        .timestamp {{
                            display: inline-flex;
                            align-items: center;
                            background-color: #f8f9fa;
                            padding: 8px 16px;
                            border-radius: 6px;
                            font-size: 14px;
                            color: #495057;
                            margin-top: 12px;
                        }}
                        .timestamp::before {{
                            content: '●';
                            color: #ff4757;
                            margin-right: 8px;
                            font-size: 18px;
                        }}
                        
                        /* SENSOR DATA */
                        .section-title {{
                            color: #2d3436;
                            font-size: 18px;
                            font-weight: 700;
                            margin: 35px 0 20px;
                            padding-bottom: 10px;
                            border-bottom: 2px solid #f1f3f5;
                        }}
                        .sensor-grid {{
                            display: grid;
                            grid-template-columns: 1fr 1fr;
                            gap: 15px;
                            margin-bottom: 30px;
                        }}
                        .sensor-card {{
                            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                            padding: 20px;
                            border-radius: 12px;
                            border: 1px solid #dee2e6;
                            transition: transform 0.2s;
                        }}
                        .sensor-card:hover {{
                            transform: translateY(-2px);
                        }}
                        .sensor-label {{
                            color: #6c757d;
                            font-size: 13px;
                            font-weight: 600;
                            text-transform: uppercase;
                            letter-spacing: 0.5px;
                            margin-bottom: 8px;
                        }}
                        .sensor-value {{
                            color: #ff4757;
                            font-size: 28px;
                            font-weight: 700;
                            letter-spacing: -0.5px;
                        }}
                        .sensor-unit {{
                            color: #adb5bd;
                            font-size: 14px;
                            font-weight: 600;
                            margin-left: 5px;
                        }}
                        
                        /* SAFETY INSTRUCTIONS */
                        .safety-box {{
                            background: linear-gradient(135deg, #fff3cd 0%, #ffe5a0 100%);
                            border: 2px solid #ffc107;
                            border-radius: 12px;
                            padding: 25px;
                            margin-top: 25px;
                        }}
                        .safety-box h3 {{
                            color: #856404;
                            font-size: 18px;
                            margin-bottom: 18px;
                            font-weight: 700;
                        }}
                        .safety-list {{
                            list-style: none;
                            padding: 0;
                        }}
                        .safety-list li {{
                            color: #856404;
                            font-size: 15px;
                            padding: 12px 0 12px 35px;
                            position: relative;
                            line-height: 1.6;
                        }}
                        .safety-list li::before {{
                            content: '▸';
                            position: absolute;
                            left: 10px;
                            color: #ffc107;
                            font-size: 20px;
                            font-weight: bold;
                        }}
                        
                        /* EMERGENCY CONTACT */
                        .emergency-box {{
                            background: linear-gradient(135deg, #2d3436 0%, #000000 100%);
                            color: #ffffff;
                            padding: 25px;
                            border-radius: 12px;
                            margin-top: 25px;
                            text-align: center;
                        }}
                        .emergency-box h4 {{
                            font-size: 16px;
                            margin-bottom: 12px;
                            font-weight: 700;
                            color: #ffc107;
                        }}
                        .emergency-box p {{
                            font-size: 14px;
                            color: rgba(255, 255, 255, 0.9);
                            line-height: 1.6;
                        }}
                        .emergency-number {{
                            display: inline-block;
                            background-color: #ff4757;
                            color: #ffffff;
                            padding: 12px 30px;
                            border-radius: 8px;
                            font-size: 22px;
                            font-weight: 700;
                            margin-top: 15px;
                            letter-spacing: 1px;
                        }}
                        
                        /* FOOTER */
                        .footer {{
                            background-color: #f8f9fa;
                            padding: 30px 40px;
                            text-align: center;
                            border-top: 1px solid #dee2e6;
                        }}
                        .footer-logo {{
                            color: #495057;
                            font-size: 18px;
                            font-weight: 700;
                            margin-bottom: 10px;
                        }}
                        .footer-text {{
                            color: #6c757d;
                            font-size: 13px;
                            line-height: 1.6;
                        }}
                        .footer-divider {{
                            width: 50px;
                            height: 3px;
                            background: linear-gradient(90deg, #ff4757, #d63031);
                            margin: 15px auto;
                            border-radius: 3px;
                        }}
                        
                        /* RESPONSIVE */
                        @media only screen and (max-width: 600px) {{
                            .email-wrapper {{
                                border-radius: 0;
                            }}
                            .header, .content, .footer {{
                                padding: 30px 25px;
                            }}
                            .sensor-grid {{
                                grid-template-columns: 1fr;
                            }}
                            .header h1 {{
                                font-size: 26px;
                            }}
                        }}
                    </style>
                </head>
                <body>
                    <div class="email-wrapper">
                        <!-- HEADER -->
                        <div class="header">
                            <div class="alert-icon">!</div>
                            <h1>ALERTA CRÍTICA DE GAS</h1>
                            <p>Sistema de Detección GasAlert D.A.T</p>
                        </div>
                        
                        <!-- CONTENT -->
                        <div class="content">
                            <span class="alert-badge">Detección Inmediata</span>
                            
                            <div class="main-message">
                                <h2>Concentración de Gas Detectada</h2>
                                <p>
                                    El sistema de monitoreo ha identificado niveles anormales de gas en el área vigilada. 
                                    Se requiere atención inmediata para evaluar la situación y tomar las medidas de seguridad necesarias.
                                </p>
                                <div class="timestamp">Fecha y hora: {fecha_hora}</div>
                            </div>
                            
                            <h3 class="section-title">Lecturas de Sensores</h3>
                            
                            <div class="sensor-grid">
                                <div class="sensor-card">
                                    <div class="sensor-label">Sensor Analógico</div>
                                    <div class="sensor-value">{ao}<span class="sensor-unit">PPM</span></div>
                                </div>
                                
                                <div class="sensor-card">
                                    <div class="sensor-label">Sensor Digital</div>
                                    <div class="sensor-value">{do}<span class="sensor-unit">Estado</span></div>
                                </div>
                            </div>
                            
                            <div class="safety-box">
                                <h3>Protocolo de Seguridad Inmediata</h3>
                                <ul class="safety-list">
                                    <li>Evacue el área de manera ordenada y rápida</li>
                                    <li>No active interruptores eléctricos ni aparatos</li>
                                    <li>Ventile el espacio abriendo puertas y ventanas de forma segura</li>
                                    <li>Manténgase alejado del área hasta que sea declarada segura</li>
                                    <li>Notifique a personal capacitado o servicios de emergencia</li>
                                </ul>
                            </div>
                            
                            <div class="emergency-box">
                                <h4>EN CASO DE EMERGENCIA</h4>
                                <p>Contacte inmediatamente a los servicios de emergencia</p>
                                <div class="emergency-number">911</div>
                            </div>
                        </div>
                        
                        <!-- FOOTER -->
                        <div class="footer">
                            <div class="footer-logo">GasAlert D.A.T</div>
                            <div class="footer-divider"></div>
                            <p class="footer-text">
                                Sistema de Monitoreo Inteligente de Gas<br>
                                Este es un mensaje automático generado por el sistema.<br>
                                Por favor, no responda a este correo electrónico.
                            </p>
                            <p class="footer-text" style="margin-top: 15px; font-size: 12px;">
                                © 2024 GasAlert D.A.T. Todos los derechos reservados.
                            </p>
                        </div>
                    </div>
                </body>
                </html>
                """
                
                # Adjuntar HTML
                parte_html = MIMEText(mensaje_html, "html")
                msg.attach(parte_html)
                
                # Enviar correo
                server.sendmail(EMAIL_SENDER, correo_destino, msg.as_string())
                
                # Incrementar contador en la BD
                sumar_envio(correo_destino)
                
                exitosos += 1
                print(f"Correo enviado a: {correo_destino}")
                
            except Exception as e:
                fallidos += 1
                errores.append(f"{correo_destino}: {str(e)}")
                print(f"Error enviando a {correo_destino}: {e}")
        
        # Cerrar conexión
        server.quit()
        
        # Retornar mensaje de resumen
        mensaje_resultado = f"Alertas enviadas: {exitosos}/{len(usuarios)} usuarios"
        if fallidos > 0:
            mensaje_resultado += f" |  Fallidos: {fallidos}"
        
        return mensaje_resultado
        
    except smtplib.SMTPAuthenticationError:
        return "❌ Error de autenticación. Verifica EMAIL_PASSWORD (usa contraseña de aplicación)"
    except Exception as e:
        return f"❌ Error al conectar con el servidor SMTP: {e}"
