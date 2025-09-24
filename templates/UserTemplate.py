def render_register_email(first_name, last_name, username):
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Excuses 404 - Registro exitoso</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; color: #333; }}
            .container {{ max-width: 600px; margin: 40px auto; background-color: #fff; border-radius: 8px;
                         box-shadow: 0 2px 8px rgba(0,0,0,0.1); overflow: hidden; }}
            .header {{ background-color: #1e1e1e; color: #fff; text-align: center; padding: 30px 20px; }}
            .header h1 {{ margin: 0; font-size: 28px; text-transform: uppercase; letter-spacing: 2px; }}
            .body {{ padding: 30px 40px; font-size: 16px; line-height: 1.6; }}
            .highlight {{ font-size: 20px; font-weight: bold; color: #ff4c4c; text-align: center; margin: 20px 0; }}
            .footer {{ background-color: #f1f1f1; color: #777; text-align: center; padding: 20px; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Excuses 404</h1>
            </div>
            <div class="body">
                <p>¡Bienvenido/a <strong>{first_name} {last_name}</strong>!</p>
                <p>Tu registro en <strong>Excuses 404</strong> se realizó con éxito.</p>
                <div class="highlight">Usuario: {username}</div>
                <p>Ya podés iniciar sesión con tus credenciales y empezar a disfrutar de nuestros servicios.</p>
                <p>Si no fuiste vos quien realizó este registro, por favor contactá a nuestro soporte.</p>
                <p>Atentamente,<br>El equipo de <strong>Excuses 404</strong></p>
            </div>
            <div class="footer">
                © 2025 Excuses 404 | Este es un mensaje automático, no respondas a este correo.
            </div>
        </div>
    </body>
    </html>
    """

def render_banned_account_email(first_name, last_name, username):
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Excuses 404 - Cuenta restringida</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; color: #333; }}
            .container {{ max-width: 600px; margin: 40px auto; background-color: #fff; border-radius: 8px;
                         box-shadow: 0 2px 8px rgba(0,0,0,0.1); overflow: hidden; }}
            .header {{ background-color: #1e1e1e; color: #fff; text-align: center; padding: 30px 20px; }}
            .header h1 {{ margin: 0; font-size: 28px; text-transform: uppercase; letter-spacing: 2px; }}
            .body {{ padding: 30px 40px; font-size: 16px; line-height: 1.6; }}
            .highlight {{ font-size: 20px; font-weight: bold; color: #ff4c4c; text-align: center; margin: 20px 0; }}
            .footer {{ background-color: #f1f1f1; color: #777; text-align: center; padding: 20px; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Excuses 404</h1>
            </div>
            <div class="body">
                <p>Hola <strong>{first_name} {last_name}</strong>,</p>
                <p>Lamentamos informarte que tu cuenta en <strong>Excuses 404</strong> ha sido <span style="color:#ff4c4c;"><strong>bloqueada</strong></span>.</p>
                <div class="highlight">Usuario: {username}</div>
                <p>Esto puede deberse a un incumplimiento de nuestras políticas de uso o términos de servicio.</p>
                <p>Si creés que se trata de un error, te pedimos que te pongas en contacto con nuestro equipo de soporte para revisar tu caso.</p>
                <p>Atentamente,<br>El equipo de <strong>Excuses 404</strong></p>
            </div>
            <div class="footer">
                © 2025 Excuses 404 | Este es un mensaje automático, no respondas a este correo.
            </div>
        </div>
    </body>
    </html>
    """

def render_password_changed_email(first_name, last_name, username):
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Excuses 404 - Contraseña actualizada</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; color: #333; }}
            .container {{ max-width: 600px; margin: 40px auto; background-color: #fff; border-radius: 8px;
                         box-shadow: 0 2px 8px rgba(0,0,0,0.1); overflow: hidden; }}
            .header {{ background-color: #1e1e1e; color: #fff; text-align: center; padding: 30px 20px; }}
            .header h1 {{ margin: 0; font-size: 28px; text-transform: uppercase; letter-spacing: 2px; }}
            .body {{ padding: 30px 40px; font-size: 16px; line-height: 1.6; }}
            .highlight {{ font-size: 20px; font-weight: bold; color: #28a745; text-align: center; margin: 20px 0; }}
            .footer {{ background-color: #f1f1f1; color: #777; text-align: center; padding: 20px; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Excuses 404</h1>
            </div>
            <div class="body">
                <p>Hola <strong>{first_name} {last_name}</strong>,</p>
                <p>Te confirmamos que tu contraseña en <strong>Excuses 404</strong> ha sido <span style="color:#28a745;"><strong>actualizada exitosamente</strong></span>.</p>
                <div class="highlight">Usuario: {username}</div>
                <p>Si no fuiste vos quien realizó este cambio, te recomendamos que te pongas en contacto con nuestro equipo de soporte inmediatamente.</p>
                <p>Por tu seguridad, recordá mantener tu contraseña en secreto y no compartirla con nadie.</p>
                <p>Atentamente,<br>El equipo de <strong>Excuses 404</strong></p>
            </div>
            <div class="footer">
                © 2025 Excuses 404 | Este es un mensaje automático, no respondas a este correo.
            </div>
        </div>
    </body>
    </html>
    """
