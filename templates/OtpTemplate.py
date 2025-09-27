def render_login_otp_email(otp_code):
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Excuses 404 - Código de verificación</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; color: #333; }}
            .container {{ max-width: 600px; margin: 40px auto; background-color: #fff; border-radius: 8px;
                         box-shadow: 0 2px 8px rgba(0,0,0,0.1); overflow: hidden; }}
            .header {{ background-color: #1e1e1e; color: #fff; text-align: center; padding: 30px 20px; }}
            .header h1 {{ margin: 0; font-size: 28px; text-transform: uppercase; letter-spacing: 2px; }}
            .body {{ padding: 30px 40px; font-size: 16px; line-height: 1.6; }}
            .otp {{ font-size: 36px; font-weight: bold; color: #ff4c4c; text-align: center; margin: 30px 0; letter-spacing: 6px; }}
            .footer {{ background-color: #f1f1f1; color: #777; text-align: center; padding: 20px; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Excuses 404</h1>
            </div>
            <div class="body">
                <p>Se detectó un intento de inicio de sesión en tu cuenta.</p>
                <p>Si fuiste vos, ingresá el siguiente código para continuar:</p>
                <div class="otp">{otp_code}</div>
                <p>Si <strong>no</strong> fuiste vos, te recomendamos cambiar tu contraseña inmediatamente para proteger tu cuenta.</p>
                <p>Atentamente,<br>El equipo de <strong>Excuses 404</strong></p>
            </div>
            <div class="footer">
                © 2025 Excuses 404 | Este es un mensaje automático, no respondas a este correo.
            </div>
        </div>
    </body>
    </html>
    """

def render_recover_otp_email(first_name, last_name, otp_code):
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Excuses 404 - Recuperación de cuenta</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; color: #333; }}
            .container {{ max-width: 600px; margin: 40px auto; background-color: #fff; border-radius: 8px;
                         box-shadow: 0 2px 8px rgba(0,0,0,0.1); overflow: hidden; }}
            .header {{ background-color: #1e1e1e; color: #fff; text-align: center; padding: 30px 20px; }}
            .header h1 {{ margin: 0; font-size: 28px; text-transform: uppercase; letter-spacing: 2px; }}
            .body {{ padding: 30px 40px; font-size: 16px; line-height: 1.6; }}
            .otp {{ font-size: 36px; font-weight: bold; color: #ff4c4c; text-align: center; margin: 30px 0; letter-spacing: 6px; }}
            .footer {{ background-color: #f1f1f1; color: #777; text-align: center; padding: 20px; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Excuses 404</h1>
            </div>
            <div class="body">
                <h2>¡Hola {first_name} {last_name}!</h2>
                <p>Recibimos una solicitud para <strong>recuperar el acceso</strong> a tu cuenta.</p>
                <p>Ingresá el siguiente código para continuar con el proceso de recuperación:</p>
                <div class="otp">{otp_code}</div>
                <p>Si <strong>no</strong> realizaste esta solicitud, ignorá este mensaje. Tu cuenta permanecerá segura.</p>
                <p>Atentamente,<br>El equipo de <strong>Excuses 404</strong></p>
            </div>
            <div class="footer">
                © 2025 Excuses 404 | Este es un mensaje automático, no respondas a este correo.
            </div>
        </div>
    </body>
    </html>
    """
def render_registration_verification_email(first_name, last_name, username, otp_code):
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Excuses 404 - Verifica tu cuenta</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; color: #333; }}
            .container {{ max-width: 600px; margin: 40px auto; background-color: #fff; border-radius: 8px;
                         box-shadow: 0 2px 8px rgba(0,0,0,0.1); overflow: hidden; }}
            .header {{ background-color: #28a745; color: #fff; text-align: center; padding: 30px 20px; }}
            .header h1 {{ margin: 0; font-size: 28px; text-transform: uppercase; letter-spacing: 2px; }}
            .body {{ padding: 30px 40px; font-size: 16px; line-height: 1.6; }}
            .otp {{ font-size: 36px; font-weight: bold; color: #28a745; text-align: center; margin: 30px 0; 
                    letter-spacing: 6px; background-color: #f8f9fa; padding: 20px; border-radius: 8px; }}
            .footer {{ background-color: #f1f1f1; color: #777; text-align: center; padding: 20px; font-size: 12px; }}
            .welcome {{ background-color: #e8f5e8; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>¡Bienvenido/a a Excuses 404!</h1>
            </div>
            <div class="body">
                <div class="welcome">
                    <h2>¡Hola {first_name} {last_name}!</h2>
                    <p>Gracias por registrarte en <strong>Excuses 404</strong> con el usuario: <strong>{username}</strong></p>
                </div>
                
                <p>Para completar tu registro y activar tu cuenta, necesitamos verificar tu dirección de email.</p>
                <p>Por favor, ingresa el siguiente código de verificación en la pantalla de registro:</p>
                
                <div class="otp">{otp_code}</div>
                
                <p><strong>Importante:</strong></p>
                <ul>
                    <li>Este código expira en <strong>15 minutos</strong></li>
                    <li>Solo puedes usarlo una vez</li>
                    <li>Si no completaste el registro, ignora este mensaje</li>
                </ul>
                
                <p>Una vez verificada tu cuenta, podrás acceder a todas las funcionalidades de nuestra plataforma.</p>
                
                <p>¡Esperamos que disfrutes la experiencia!</p>
                <p>Atentamente,<br>El equipo de <strong>Excuses 404</strong></p>
            </div>
            <div class="footer">
                © 2025 Excuses 404 | Este es un mensaje automático, no respondas a este correo.
            </div>
        </div>
    </body>
    </html>
    """
