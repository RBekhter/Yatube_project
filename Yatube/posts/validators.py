from django import forms


def not_empty(value):
    if value == '':
        raise forms.ValidationError('Текст поста не может быть пустым',
                                    params={'value': value},)


def clean_text(self):
    value = self.cleaned_data['text']
    if value == '':
        raise forms.ValidationError('А кто поле будет заполнять, Пушкин?')
    return value
