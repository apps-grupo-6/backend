def render_alert_email(subject, description, endpoint, method, request_id, response_code):
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Excuses 404 - {subject}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; color: #333; }}
            .container {{ max-width: 600px; margin: 40px auto; background-color: #fff; border-radius: 8px;
                         box-shadow: 0 2px 8px rgba(0,0,0,0.1); overflow: hidden; }}
            .header {{ background-color: #b71c1c; color: #fff; text-align: center; padding: 30px 20px; }}
            .header h1 {{ margin: 0; font-size: 26px; text-transform: uppercase; letter-spacing: 2px; }}
            .body {{ padding: 30px 40px; font-size: 15px; line-height: 1.6; }}
            .highlight {{ font-size: 18px; font-weight: bold; color: #d32f2f; text-align: center; margin: 20px 0; }}
            .info {{ background-color: #f9f9f9; border-left: 4px solid #d32f2f; padding: 12px; margin: 15px 0; font-family: monospace; font-size: 14px; }}
            .footer {{ background-color: #f1f1f1; color: #777; text-align: center; padding: 20px; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>{subject}</h1>
            </div>
            <div class="body">
                <p>Se detectó una posible violación de seguridad en el sistema:</p>
                <div class="highlight">{description}</div>
                <div class="info">
                    <p><strong>Endpoint:</strong> {endpoint}</p>
                    <p><strong>Método:</strong> {method}</p>
                    <p><strong>Request ID:</strong> {request_id}</p>
                    <p><strong>Response Code:</strong> {response_code}</p>
                </div>
                <p>Por favor, investigá este incidente lo antes posible.</p>
                <p>Atentamente,<br>El backend de <strong>Excuses 404</strong></p>
            </div>
            <div class="footer">
                © 2025 Excuses 404 | Este mensaje es interno, no reenviar fuera del equipo de desarrollo.
            </div>
        </div>
    </body>
    </html>
    """
