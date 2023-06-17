from django.test import TestCase
from students.forms import (
    NoteForm,
    HomeworkForm,
    TodoForm,
    AppForm,
    ConversionForm,
    ConversionLengthForm,
    ConversionWeightForm,
)
from students.models import Note, Homework, Todo


class NoteFormTest(TestCase):

    def test_note_fields(self):
        form = NoteForm()
        self.assertEqual(
            form.Meta.model,
            Note
        )
        self.assertTupleEqual(
            form.Meta.fields,
            ("title", "description")
        )


class HomeworkFormTest(TestCase):

    def test_homework_fields(self):
        form = HomeworkForm()
        self.assertEqual(
            form.Meta.model,
            Homework
        )
        self.assertTupleEqual(
            form.Meta.fields,
            ("subject", "title", "description")
        )


class TodoFormTest(TestCase):

    def test_todo_fields(self):
        form = TodoForm()
        self.assertEqual(
            form.Meta.model,
            Todo
        )
        self.assertTupleEqual(
            form.Meta.fields,
            ("title",)
        )


class AppFormTest(TestCase):

    def test_text_label(self):
        form = AppForm()
        self.assertEqual(form.fields["text"].label, "Enter Your Search")

    def test_text_max_length(self):
        form = AppForm()
        self.assertEqual(form.fields["text"].max_length, 255)


class ConversionFormTest(TestCase):

    def test_measurement_choices(self):
        form = ConversionForm()
        self.assertListEqual(
            form.fields["measurement"].choices,
            [("length", "Length"), ("weight", "Weight")]
        )


class ConversionLengthFormTest(TestCase):

    def test_input_conv_widget(self):
        form = ConversionLengthForm()
        self.assertIsNone(form.fields["input_conv"].widget.attrs.get("type"))
        self.assertEqual(
            form.fields["input_conv"].widget.attrs.get("placeholder"),
            "Enter the Number"
        )

    def test_measure1_choices(self):
        form = ConversionLengthForm()
        self.assertListEqual(
            form.fields["measure1"].widget.choices,
            [("miles", "Miles"), ("kilometers", "Kilometers")]
        )

    def test_measure2_choices(self):
        form = ConversionLengthForm()
        self.assertListEqual(
            form.fields["measure2"].widget.choices,
            [("miles", "Miles"), ("kilometers", "Kilometers")]
        )


class ConversionWeightFormTest(TestCase):

    def test_input_conv_widget(self):
        form = ConversionWeightForm()
        self.assertIsNone(form.fields["input_conv"].widget.attrs.get("type"))
        self.assertEqual(
            form.fields["input_conv"].widget.attrs.get("placeholder"),
            "Enter the Number"
        )

    def test_measure1_choices(self):
        form = ConversionWeightForm()
        self.assertListEqual(
            form.fields["measure1"].widget.choices,
            [("pound", "Pound"), ("kilogram", "Kilogram")]
        )

    def test_measure2_choices(self):
        form = ConversionWeightForm()
        self.assertListEqual(
            form.fields["measure2"].widget.choices,
            [("pound", "Pound"), ("kilogram", "Kilogram")]
        )
