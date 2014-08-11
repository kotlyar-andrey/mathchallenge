# -*- coding: utf-8 -*-

from django.contrib.auth.forms import UserChangeForm, UserCreationForm, PasswordResetForm as AuthPasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.utils.http import int_to_base36
from django import forms
from yacaptcha.fields import YaCaptchaField

from .models import User
from src.mail import send_templated_email


class AdminUserAddForm(UserCreationForm):

    class Meta:
        model = User

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


class AdminUserChangeForm(UserChangeForm):

    class Meta:
        model = User


class CreateUserForm(forms.ModelForm):
    error_messages = {
        'duplicate_email': u"Пользователь с таким адресом электронной почты уже существует",
        'duplicate_username': u"Пользователь с таким логином уже существует",
        'password_mismatch': u"Введенные пароли не совпадают",
    }

    password1 = forms.CharField(label="Пароль",
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повторите пароль",
                                widget=forms.PasswordInput,
                                help_text="Введите пароль еще раз, чтобы не ошибиться")
    captcha = YaCaptchaField(label=u'Введите символы с картинки')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')

    def clean_email(self):
        email = self.cleaned_data["email"]
        if email:
            try:
                User._default_manager.get(email=email)
            except User.DoesNotExist:
                return email
            raise forms.ValidationError(self.error_messages['duplicate_email'])

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserEditForm(forms.ModelForm):
    current_password = forms.CharField(label=u'Текущий пароль', widget=forms.PasswordInput, required=False,
                                       help_text=u'Введите Ваш текущий пароль, чтобы его изменить')
    current_password.widget.attrs.update({'autocomplit': 'off'})
    new_password = forms.CharField(label=u'Новый пароль', widget=forms.PasswordInput, required=False)
    new_password_verify = forms.CharField(label=u'Повторите новый пароль', widget=forms.PasswordInput,
                                          required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)

    def clean(self):
        current, new, verify = map(self.cleaned_data.get,
                                   ('current_password', 'new_password', 'new_password_verify'))
        if current and self.instance.has_usable_password() and not self.instance.check_password(current):
            raise forms.ValidationError(u'Неправильный пароль')
        if new and new != verify:
            raise forms.ValidationError(u'Пароли не совпадают')
        return self.cleaned_data

    def clean_email(self):
        value = self.cleaned_data['email']
        if value:
            try:
                User.objects.exclude(pk=self.instance.pk).get(email=value)
                raise forms.ValidationError(u'Этот адрес электронной почты уже используется')
            except User.DoesNotExist:
                pass
        return value

    def save(self, commit=True):
        password = self.cleaned_data.get('new_password')
        if password:
            self.instance.set_password(password)
        return super(UserEditForm, self).save(commit)


class PasswordResetForm(AuthPasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data["email"]
        self.users_cache = User.objects.filter(
            email__iexact=email,
            is_active=True,
            is_valid_email=True
        )
        if len(self.users_cache) == 0:
            raise forms.ValidationError(u"Указанный электронный адрес не найден. Вы уверены, что зарегистрировались и подтвердили электронный адрес?")
        return email

    def save(self, domain_override=None, email_template_name='accounts/password_reset_email.html',
             use_https=False, token_generator=default_token_generator, from_email=None, request=None, **kwargs):
        """
        Generates a one-use only link for resetting password and sends to the user
        """
        for user in self.users_cache:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override

            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': int_to_base36(user.id),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': use_https and 'https' or 'http',
                }
            subject = u"Смена пароля для %s" % site_name
            send_templated_email([user.email], subject, email_template_name, c, from_email)