from flask import render_template
import random
import string
# from others.db import connect_to_database
'''Route for handling password reset'''


def password_recovery_token():
    '''generate random token'''
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


def forgot_password_func(request):
    ''' generate token for password resent '''
    return render_template('forgot_password.html', error='Not Avaliable yet.')


def reset_password_func(request):
    ''' reset password '''
    return render_template('login.html', message='Not Avaliable yet.')         


def send_email(receiver_email, token):
    pass
