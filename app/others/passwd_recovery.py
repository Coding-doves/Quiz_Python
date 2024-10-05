import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import render_template, redirect, url_for
import datetime
import random
import string
from others.db import connect_to_database
'''Route for handling password reset'''

db = connect_to_database()
cursor = db.cursor()


def password_recovery_token():
    '''generate random token'''
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


def forgot_password_func(request):
    ''' generate token for password resent '''
    if request.method == 'POST':
        email = request.form.get('email')
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            token = password_recovery_token()
            cursor.execute("INSERT INTO password_reset_tokens (user_id, reset_token, token_expiry) VALUES ((SELECT id FROM users WHERE email = %s), %s, %s)", (email, token, datetime.datetime.now() + datetime.timedelta(minutes=35)))
            db.commit()

            # Send reset link to user's mail
            send_email(email, token)

            # Confirm link has been sent
            return render_template('login.html', message='A reset link has been sent to your mail.')
        else:
            return render_template('forgot_password.html', error='Email not found')
    return render_template('forgot_password.html')


def reset_password_func(request):
    ''' reset password '''
    token = request.args.get('token')
    if token:
        cursor.execute("SELECT users.* FROM users INNER JOIN password_reset_tokens ON users.id = password_reset_tokens.user_id WHERE password_reset_tokens.reset_token = %s AND password_reset_tokens.token_expiry > %s", (token, datetime.datetime.now()))
        user = cursor.fetchone()
        if user:
            if request.method == 'POST':
                new_passwd = request.form.get('new_password')
                cursor.execute("UPDATE users SET password = %s WHERE id = (SELECT user_id FROM password_reset_tokens WHERE reset_token = %s)", (new_passwd, token))
                cursor.execute("DELETE FROM password_reset_tokens WHERE reset_token = %s", (token,))
                db.commit()
                # Redirect to login page or any other page confirming password reset
                return redirect(url_for('login'))
            return render_template('reset_password.html', token=token)
        else:
            return render_template('login.html', message='The password reset link is invalid or has expired.')
    else:
        return redirect(url_for('forgot_password'))            


def send_email(receiver_email, token):
    try:
        # Email configuration
        sender_email = "dovedrops4@gmail.com"
        sender_passwd = "Benedicta.070"
        smtp_server = "smtp.gmail.com"
        smtp_port = 587 # Gmail SMTP port

        # Create message container
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "Password Reset Link"

        # Email body
        body = f"Click the link below to reset your password:\n\nhttp://http://127.0.0.1:5000/reset-password?token={token}"
        msg.attach(MIMEText(body, 'plain'))

        # Create SMTP session
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Enable TLS
            server.login(sender_email, sender_passwd)  # Login to SMTP server

            # Send email
            server.sendmail(sender_email, receiver_email, msg.as_string())

        # Send email
        server.sendmail(sender_email, receiver_email, msg.as_string())

        # Close SMTP session
        server.quit()
    except Exception as e:
        print(f"An error occurred while sending email: {e}")
        # Handle the exception here
