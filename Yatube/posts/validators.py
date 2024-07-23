from django import forms


def not_empty(value):
    if value == '':
        raise forms.ValidationError('Текст поста не может быть пустым',
                                    params={'value': value},)


def clean_text(self):
        data = self.cleaned_data['text']
        if data == '':
            raise forms.ValidationError('А кто поле будет заполнять, Пушкин?')
        return data
