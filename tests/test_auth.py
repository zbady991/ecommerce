from auth import LoginForm, RegistrationForm
from wtforms import StringField, PasswordField, BooleanField, validators

def test_login_form_validation():
    form = LoginForm(
        username='testuser',
        password='password',
        remember=True
    )
    assert form.validate() is True

    empty_form = LoginForm(
        username='',
        password='',
        remember=False
    )
    assert empty_form.validate() is False

def test_registration_form_validation():
    form = RegistrationForm(
        username='newuser',
        email='new@example.com',
        password='password123',
        confirm_password='password123'
    )
    assert form.validate() is True

    mismatch_form = RegistrationForm(
        username='newuser',
        email='new@example.com',
        password='password123',
        confirm_password='different'
    )
    assert mismatch_form.validate() is False