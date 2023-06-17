from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from students.forms import AppForm, ConversionForm
from students.models import Note, Homework, Todo


INDEX_URL = reverse("students:index")
NOTE_URL = reverse("students:notes")
HOMEWORK_URL = reverse("students:homeworks")
TODO_URL = reverse("students:todos")
YOUTUBE_URL = reverse("students:youtube")
BOOKS_URL = reverse("students:books")
DICTIONARY_URL = reverse("students:dictionary")
WIKIPEDIA_URL = reverse("students:wikipedia")
CONVERSION_URL = reverse("students:conversion")


class PublicIndexTests(TestCase):

    def test_login_required(self):
        response = self.client.get(INDEX_URL)

        self.assertEqual(response.status_code, 200)


class PrivateIndexTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            email="test@user.com",
            username="user_name",
            password="user12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_index(self):
        response = self.client.get(INDEX_URL)

        self.assertEqual(response.status_code, 200)


def detail_url(note_id):
    return reverse("students:note-detail", args=[note_id])


class PublicNotesTests(TestCase):

    def test_login_required(self):
        response = self.client.get(NOTE_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateNotesTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            email="test@user.com",
            username="user_name",
            password="user12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_notes(self):
        Note.objects.create(
            user=self.user, title="Test1", description="Test1"
        )
        Note.objects.create(
            user=self.user, title="Test2", description="Test2"
        )

        response = self.client.get(NOTE_URL)
        note = Note.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["notes"]),
            list(note)
        )
        self.assertTemplateUsed(
            response,
            "students/notes.html"
        )

    def test_retrieve_note_detail(self):
        note = Note.objects.create(
            user=self.user, title="Test1", description="Test1"
        )

        url = detail_url(note.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "students/notes_detail.html"
        )

    def test_create_notes(self):
        form_data = {
            "user": self.user,
            "title": "Test",
            "description": "Test",
        }

        self.client.post(reverse("students:notes"), data=form_data)
        new_note = Note.objects.get(title=form_data["title"])

        self.assertEqual(new_note.title, form_data["title"])
        self.assertEqual(new_note.description, form_data["description"])


class PrivateNoteDeleteTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@user.com",
            username="testuser",
            password="testpassword"
        )
        self.note = Note.objects.create(
            user=self.user,
            title="Test1",
            description="Test1"
        )
        self.NOTE_DELETE_URL = reverse(
            "students:note-delete", args=[self.note.pk]
        )
        self.client.force_login(self.user)

    def test_delete_note(self):
        response = self.client.post(self.NOTE_DELETE_URL)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("students:notes"))
        self.assertFalse(Note.objects.filter(pk=self.note.pk).exists())


class PublicHomeworksTests(TestCase):

    def test_login_required(self):
        response = self.client.get(HOMEWORK_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateHomeworksTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            email="test@user.com",
            username="user_name",
            password="user12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_homeworks(self):
        Homework.objects.create(
            user=self.user, subject="Test1", title="Test1", description="Test1"
        )
        Homework.objects.create(
            user=self.user, subject="Test2", title="Test2", description="Test2"
        )

        response = self.client.get(HOMEWORK_URL)
        homework = Homework.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["homework_list"]),
            list(homework)
        )
        self.assertTemplateUsed(
            response,
            "students/homework.html"
        )

    def test_create_homeworks(self):
        form_data = {
            "user": self.user,
            "subject": "Test",
            "title": "Test",
            "description": "Test",
        }

        self.client.post(reverse("students:homeworks"), data=form_data)
        new_homework = Homework.objects.get(subject=form_data["subject"])

        self.assertEqual(new_homework.subject, form_data["subject"])
        self.assertEqual(new_homework.title, form_data["title"])
        self.assertEqual(new_homework.description, form_data["description"])


class PrivateHomeworkDeleteTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@user.com",
            username="testuser",
            password="testpassword"
        )
        self.homework = Homework.objects.create(
            user=self.user,
            subject="Test",
            title="Test1",
            description="Test1"
        )
        self.HOMEWORK_DELETE_URL = reverse(
            "students:homework-delete", args=[self.homework.pk]
        )
        self.client.force_login(self.user)

    def test_delete_homework(self):
        response = self.client.post(self.HOMEWORK_DELETE_URL)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("students:homeworks"))
        self.assertFalse(Note.objects.filter(pk=self.homework.pk).exists())


class PublicTodosTests(TestCase):

    def test_login_required(self):
        response = self.client.get(TODO_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateTodoTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            email="test@user.com",
            username="user_name",
            password="user12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_todos(self):
        Todo.objects.create(
            user=self.user, title="Test1"
        )
        Todo.objects.create(
            user=self.user, title="Test2"
        )

        response = self.client.get(TODO_URL)
        todo = Todo.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["todo_list"]),
            list(todo)
        )
        self.assertTemplateUsed(
            response,
            "students/todo.html"
        )

    def test_create_todos(self):
        form_data = {
            "user": self.user,
            "title": "Test",
        }

        self.client.post(reverse("students:todos"), data=form_data)
        new_todo = Todo.objects.get(title=form_data["title"])

        self.assertEqual(new_todo.title, form_data["title"])


class PrivateTodoDeleteTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@user.com",
            username="testuser",
            password="testpassword"
        )
        self.todo = Todo.objects.create(
            user=self.user,
            title="Test1",
        )
        self.TODO_DELETE_URL = reverse(
            "students:todo-delete", args=[self.todo.pk]
        )
        self.client.force_login(self.user)

    def test_delete_todo(self):
        response = self.client.post(self.TODO_DELETE_URL)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("students:todos"))
        self.assertFalse(Note.objects.filter(pk=self.todo.pk).exists())


class PrivateYoutubeTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@user.com",
            username="testuser",
            password="testpassword"
        )
        self.client.force_login(self.user)

    def test_youtube_view(self):

        response = self.client.get(YOUTUBE_URL)
        self.assertEqual(response.status_code, 200)

        form = response.context["form"]
        self.assertIsInstance(form, AppForm)
        self.assertEqual(form.initial, {})

        self.assertTemplateUsed(response, "students/youtube.html")

    def test_youtube_view_post(self):
        data = {
            "text": "your_search_query",
        }

        response = self.client.post(YOUTUBE_URL, data)
        self.assertEqual(response.status_code, 200)

        self.assertIn("form", response.context)
        self.assertIn("results", response.context)

        results = response.context["results"]
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 10)


class PrivateBooksTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@user.com",
            username="testuser",
            password="testpassword"
        )
        self.client.force_login(self.user)

    def test_books_view_authentication(self):
        response = self.client.get(BOOKS_URL)
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "students/books.html")

    def test_books_view_search(self):
        response = self.client.post(BOOKS_URL, {"text": "Harry Potter"})
        self.assertEqual(response.status_code, 200)

        self.assertIn("form", response.context)
        self.assertIn("results", response.context)

        form = response.context["form"]
        self.assertIsInstance(form, AppForm)

        results = response.context["results"]
        self.assertIsInstance(results, list)
        self.assertGreaterEqual(len(results), 0)


class PrivateDictionaryTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@user.com",
            username="testuser",
            password="testpassword"
        )
        self.client.force_login(self.user)

    def test_dictionary_view_authentication(self):
        response = self.client.get(DICTIONARY_URL)
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "students/dictionary.html")

    def test_dictionary_view_search(self):
        response = self.client.post(DICTIONARY_URL, {"text": "apple"})
        self.assertEqual(response.status_code, 200)

        self.assertIn("form", response.context)
        self.assertIn("input", response.context)
        self.assertIn("phonetics", response.context)
        self.assertIn("audio", response.context)
        self.assertIn("definition", response.context)
        self.assertIn("example", response.context)
        self.assertIn("synonyms", response.context)

        form = response.context["form"]
        self.assertIsInstance(form, AppForm)

        input_text = response.context["input"]
        self.assertEqual(input_text, "apple")

        example_text = response.context["example"]
        self.assertEqual(example_text, "")

        synonyms_text = response.context["synonyms"]
        self.assertEqual(synonyms_text, [])


class PrivateWikipediaTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@user.com",
            username="testuser",
            password="testpassword"
        )
        self.client.force_login(self.user)

    def test_wikipedia_view_authentication(self):
        response = self.client.get(WIKIPEDIA_URL)
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "students/wiki.html")

    def test_wikipedia_view_search(self):
        response = self.client.post(
            WIKIPEDIA_URL, {"text": "Python programming language"}
        )
        self.assertEqual(response.status_code, 200)

        self.assertIn("form", response.context)

        form = response.context["form"]
        self.assertIsInstance(form, AppForm)

        if "disambiguation_error" in response.context:
            self.assertIn("options", response.context)
        elif "error_message" in response.context:
            self.assertIn("error_message", response.context)
        else:
            self.assertIn("title", response.context)
            self.assertIn("link", response.context)
            self.assertIn("details", response.context)


class PrivateConversionTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@user.com",
            username="testuser",
            password="testpassword"
        )
        self.client.force_login(self.user)

    def test_conversion_view_authentication(self):
        response = self.client.get(CONVERSION_URL)
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "students/conversion.html")

    def test_conversion_view_conversion(self):
        response = self.client.post(CONVERSION_URL, {"measurement": "length"})
        self.assertEqual(response.status_code, 200)

        self.assertIn("form", response.context)

        form = response.context["form"]
        self.assertIsInstance(form, ConversionForm)
