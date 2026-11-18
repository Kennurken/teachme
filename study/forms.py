from django import forms


class SourceForm(forms.Form):
    title = forms.CharField(label='Атауы', max_length=120, required=True, strip=True)
    text = forms.CharField(
        label='Конспект мәтіні',
        min_length=80,
        max_length=12000,
        strip=True,
        widget=forms.Textarea(attrs={'rows': 10}),
    )

    def clean_text(self):
        text = self.cleaned_data['text']
        return text.replace('\r\n', '\n').replace('\r', '\n')
