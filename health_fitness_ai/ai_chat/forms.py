from django import forms

class ChatForm(forms.Form):
    message = forms.CharField(max_length=500, widget=forms.TextInput(attrs={
        'placeholder': 'Ask me anything about your fitness...',
        'class': 'chat-input'
    }))
