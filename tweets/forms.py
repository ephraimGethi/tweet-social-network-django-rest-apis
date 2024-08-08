from .models import Tweet
from django import forms

class TweetForm(forms.ModelForm):
   class Meta:
        model = Tweet
        fields = ('__all__')

        def clean_content(self):
            content = self.cleaned_data.get('content')
            if len(content) > 240:
                raise forms.validationError('this teet is too long')
            return content

