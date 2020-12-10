from django import forms
from solver.models import BoxValue, Parent


class BoxForm(forms.ModelForm):
    class Meta:
        model = BoxValue
        fields = ['box_value']

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['box_value'].help_text = None
        self.fields['box_value'].label = ""
        self.fields['box_value'].widget.attrs['size'] = 1
        self.fields['box_value'].widget.attrs['pattern'] = '[1-9]'


BoxFormSet = forms.formset_factory(BoxForm, extra=81)

BoxValueFormSet = forms.inlineformset_factory(Parent, BoxValue, fields=('box_value', 'id'), extra=0)


class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ['name']
