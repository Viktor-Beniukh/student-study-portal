from django.contrib.auth import get_user_model
from django.test import TestCase
from students.models import Note, Homework, Todo


class NoteModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create_user(
            email="test@user.com",
            username="TestUser",
            password="testpassword"
        )
        Note.objects.create(
            user=user,
            title="Test Note",
            description="This is a test note."
        )

    def test_notes_fields(self):
        note = Note.objects.get(id=1)

        self.assertEqual(note.title, "Test Note")
        self.assertEqual(note.description, "This is a test note.")

    def test_notes_string_representation(self):
        note = Note.objects.get(id=1)

        self.assertEqual(str(note), "Test Note")


class HomeworkModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create_user(
            email="test@user.com",
            username="TestUser",
            password="testpassword"
        )
        Homework.objects.create(
            user=user,
            subject="History",
            title="Test Homework",
            description="This is a test homework."
        )

    def test_homeworks_fields(self):
        homework = Homework.objects.get(id=1)

        self.assertEqual(homework.subject, "History")
        self.assertEqual(homework.title, "Test Homework")
        self.assertEqual(homework.description, "This is a test homework.")

    def test_homeworks_string_representation(self):
        homework = Homework.objects.get(id=1)

        self.assertEqual(str(homework), "Test Homework")


class TodoModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create_user(
            email="test@user.com",
            username="TestUser",
            password="testpassword"
        )
        Todo.objects.create(
            user=user,
            title="Test Todo",
        )

    def test_todos_fields(self):
        todo = Todo.objects.get(id=1)

        self.assertEqual(todo.title, "Test Todo")

    def test_todos_string_representation(self):
        todo = Todo.objects.get(id=1)

        self.assertEqual(str(todo), "Test Todo")
