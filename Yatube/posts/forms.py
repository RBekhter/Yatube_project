from django import forms
from .models import Post, Group


def validate_not_empty(value):
    if value == '':
        raise forms.ValidationError('Текст поста не может быть пустым',
                                    params={'value': value},)


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')

    #def clean_text(self):
     #   data = self.cleaned_data['text']
     #   if data == '':
     #       raise forms.ValidationError('А кто поле будет заполнять, Пушкин?')
      #  return data



#class PostCreateForm(forms.Form):
 #   text = forms.CharField(widget=forms.Textarea,
 #                          validators=[validate_not_empty])
    #group = forms.IntegerField()
 #   group = forms.ChoiceField(required=False, validators=[validate_not_empty])
    
