from django import forms

from students.models import Note, Homework, Todo


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ("title", "description")


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ("subject", "title", "description")


class AppForm(forms.Form):
    text = forms.CharField(max_length=255, label="Enter Your Search")


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ("title",)


class ConversionForm(forms.Form):
    CHOICES = [("length", "Length"), ("weight", "Weight")]
    measurement = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)


class ConversionLengthForm(forms.Form):
    CHOICES = [("miles", "Miles"), ("kilometers", "Kilometers")]
    input_conv = forms.CharField(
        required=False,
        label=False,
        widget=forms.TextInput(
            attrs={"type": "number", "placeholder": "Enter the Number"}
        )
    )
    measure1 = forms.CharField(
        label="", widget=forms.Select(choices=CHOICES)
    )
    measure2 = forms.CharField(
        label="", widget=forms.Select(choices=CHOICES)
    )


class ConversionWeightForm(forms.Form):
    CHOICES = [("pound", "Pound"), ("kilogram", "Kilogram")]
    input_conv = forms.CharField(
        required=False,
        label=False,
        widget=forms.TextInput(
            attrs={"type": "number", "placeholder": "Enter the Number"}
        )
    )
    measure1 = forms.CharField(
        label="", widget=forms.Select(choices=CHOICES)
    )
    measure2 = forms.CharField(
        label="", widget=forms.Select(choices=CHOICES)
    )
