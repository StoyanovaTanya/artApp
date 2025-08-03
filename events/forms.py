from django import forms
from events.models import Event
from artwork.models import Artwork


class EventForm(forms.ModelForm):
    # artworks = forms.ModelMultipleChoiceField(
    #     queryset=Artwork.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=False,
    # )

    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'image', 'artworks']
        widgets = {
            'date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                },
                format='%Y-%m-%dT%H:%M',
            ),
            'artworks': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['date'].input_formats = ['%Y-%m-%dT%H:%M']

        if user:
            self.fields['artworks'].queryset = Artwork.objects.filter(owner=user)

        if isinstance(self.fields['artworks'].widget, forms.CheckboxSelectMultiple):
            self.fields['artworks'].widget.attrs.pop('class', None)