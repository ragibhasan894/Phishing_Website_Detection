from django import forms

class HomeForm(forms.Form):
	post = forms.CharField(widget=forms.URLInput(
		attrs={
			'class': 'form-control',
			'placeholder': 'http://www.example.com',
			'size': 110

		}
	))