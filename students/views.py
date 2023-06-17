import os
import requests
import wikipedia
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from wikipedia.exceptions import PageError, DisambiguationError
from urllib.parse import urljoin
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DeleteView, DetailView
from requests import RequestException
from youtubesearchpython import VideosSearch

from students.forms import (
    NoteForm,
    HomeworkForm,
    AppForm,
    TodoForm,
    ConversionForm,
    ConversionLengthForm,
    ConversionWeightForm,
)
from students.models import Note, Homework, Todo


def index(request):
    return render(request, "students/index.html")


class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = "students/notes.html"
    context_object_name = "notes"
    form_class = NoteForm

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(
                request, "Your note has been successfully created."
            )
            return redirect("students:notes")
        else:
            context = self.get_context_data()
            context["form"] = form
            return self.render_to_response(context)


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    success_url = reverse_lazy("students:notes")


class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note
    template_name = "students/notes_detail.html"


class HomeworkListView(LoginRequiredMixin, ListView):
    model = Homework
    template_name = "students/homework.html"
    form_class = HomeworkForm

    def get_queryset(self):
        return Homework.objects.filter(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        homeworks = self.get_queryset()
        all_completed = all(homework.is_completed for homework in homeworks)
        context["all_completed"] = all_completed
        context["form"] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            homework = form.save(commit=False)
            homework.user = request.user
            homework.save()
            messages.success(
                request, "Your homework has been successfully created."
            )
            return redirect("students:homeworks")
        else:
            context = self.get_context_data()
            context["form"] = form
            return self.render_to_response(context)


class HomeworkDeleteView(LoginRequiredMixin, DeleteView):
    model = Homework
    success_url = reverse_lazy("students:homeworks")


class HomeworkUpdateView(LoginRequiredMixin, View):

    @staticmethod
    def post(request, pk=None):
        homework = Homework.objects.get(id=pk)
        is_completed = request.POST.get("is_completed") == "true"
        homework.is_completed = is_completed
        homework.save()
        return JsonResponse({"status": "ok"})


class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = "students/todo.html"
    form_class = TodoForm

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        todos = self.get_queryset()
        all_completed = all(todo.is_completed for todo in todos)
        context["all_completed"] = all_completed
        context["form"] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(
                request, "Your task has been successfully created."
            )
            return redirect("students:todos")
        else:
            context = self.get_context_data()
            context["form"] = form
            return self.render_to_response(context)


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo
    success_url = reverse_lazy("students:todos")


class TodoUpdateView(LoginRequiredMixin, View):

    @staticmethod
    def post(request, pk=None):
        todo = Todo.objects.get(id=pk)
        is_completed = request.POST.get("is_completed") == "true"
        todo.is_completed = is_completed
        todo.save()
        return JsonResponse({"status": "ok"})


@login_required
def youtube_view(request):
    if request.method == "POST":
        form = AppForm(request.POST)
        text = request.POST["text"]
        videos = VideosSearch(text, limit=10)
        result_list = []
        for video in videos.result()["result"]:
            result_dict = {
                "input": text,
                "title": video["title"],
                "duration": video["duration"],
                "thumbnail": video["thumbnails"][0]["url"],
                "channel": video["channel"]["name"],
                "link": video["link"],
                "views": video["viewCount"]["short"],
                "published": video["publishedTime"],
            }
            desc = ""
            if video["descriptionSnippet"]:
                for element in video["descriptionSnippet"]:
                    desc += element["text"]
            result_dict["description"] = desc
            result_list.append(result_dict)
        context = {
            "form": form,
            "results": result_list
        }
        return render(request, "students/youtube.html", context=context)
    else:
        form = AppForm()

    context = {"form": form}

    return render(request, "students/youtube.html", context=context)


@login_required
def books_view(request):
    if request.method == "POST":
        form = AppForm(request.POST)
        text = request.POST["text"]
        url = os.path.join(settings.BOOK_SEARCH_URL, text)
        response = requests.get(url).json()
        result_list = []

        if len(response["items"]) >= 10:
            range_limit = 10
        else:
            range_limit = len(response["items"])

        for char in range(range_limit):
            result_dict = {
                "title": response["items"][char]["volumeInfo"]["title"],
                "subtitle": (
                    response["items"][char]["volumeInfo"]
                    .get("subtitle")
                ),
                "description": (
                    response["items"][char]["volumeInfo"]
                    .get("description")),
                "count": (
                    response["items"][char]["volumeInfo"]
                    .get("pageCount")),
                "categories": (
                    response["items"][char]["volumeInfo"]
                    .get("categories")),
                "rating": (
                    response["items"][char]["volumeInfo"]
                    .get("pageRating")),
                "thumbnail": (
                    response["items"][char]["volumeInfo"]
                    .get("imageLinks", {}).get("thumbnail")),
                "preview": (
                    response["items"][char]["volumeInfo"]
                    .get("previewLink")
                ),
            }

            result_list.append(result_dict)
        context = {
            "form": form,
            "results": result_list
        }
        return render(request, "students/books.html", context=context)
    else:
        form = AppForm()

    context = {"form": form}

    return render(request, "students/books.html", context=context)


@login_required
def dictionary_view(request):
    if request.method == "POST":
        form = AppForm(request.POST)
        text = request.POST.get("text", "")
        base_url = settings.DICTIONARY_SEARCH_URL
        url = urljoin(base_url, text)

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data and isinstance(data, list) and len(data) > 0:
                if (
                    "phonetics" in data[0]
                    and isinstance(data[0]["phonetics"], list)
                    and len(data[0]["phonetics"]) > 0
                ):
                    phonetics = data[0]["phonetics"][0]["text"]
                    if len(data[0]["phonetics"]) > 1:
                        audio = data[0]["phonetics"][1]["audio"]
                    else:
                        audio = ""
                else:
                    phonetics = ""
                    audio = ""

                if (
                    "meanings" in data[0]
                    and isinstance(data[0]["meanings"], list)
                    and len(data[0]["meanings"]) > 0
                ):
                    if (
                        "definitions" in data[0]["meanings"][0]
                        and isinstance(
                            data[0]["meanings"][0]["definitions"], list
                        )
                        and len(data[0]["meanings"][0]["definitions"]) > 0
                    ):
                        definition = (
                            data[0]["meanings"][0]["definitions"][0]
                            .get("definition", "")
                        )
                        example = (
                            data[0]["meanings"][0]["definitions"][0]
                            .get("example", "")
                        )
                        synonyms = data[0]["meanings"][0].get("synonyms", [])
                    else:
                        definition = ""
                        example = ""
                        synonyms = []
                else:
                    definition = ""
                    example = ""
                    synonyms = []
                context = {
                    "form": form,
                    "input": text,
                    "phonetics": phonetics,
                    "audio": audio,
                    "definition": definition,
                    "example": example,
                    "synonyms": synonyms
                }
            else:
                context = {
                    "form": form,
                    "input": ""
                }
        except (RequestException, ValueError, KeyError, IndexError) as e:
            print(f"An error occurred: {e}")
            context = {
                "form": form,
                "input": ""
            }
        return render(request, "students/dictionary.html", context=context)
    else:
        form = AppForm()
        context = {"form": form}
    return render(request, "students/dictionary.html", context=context)


@login_required
def wikipedia_view(request):
    if request.method == "POST":
        text = request.POST.get("text")
        form = AppForm(request.POST)

        try:
            search = wikipedia.page(text)
            context = {
                "form": form,
                "title": search.title,
                "link": search.url,
                "details": search.summary
            }
        except DisambiguationError as e:
            options = e.options
            context = {
                "form": form,
                "disambiguation_error": True,
                "options": options
            }
        except PageError:
            context = {
                "form": form,
                "error_message": "The requested page was not found."
            }

        return render(request, "students/wiki.html", context=context)

    else:
        form = AppForm()
        context = {"form": form}

    return render(request, "students/wiki.html", context=context)


miles_to_km = 1.60934
km_to_miles = 0.621371
pound_to_kg = 0.453592
kg_to_pound = 2.20462


@login_required
def conversion_view(request):
    if request.method == "POST":
        form = ConversionForm(request.POST)
        if request.POST["measurement"] == "length":
            measurement_form = ConversionLengthForm()
            context = {
                "form": form,
                "m_form": measurement_form,
                "input_conv": True
            }
            if "input_conv" in request.POST:
                first = request.POST["measure1"]
                second = request.POST["measure2"]
                input_conv = request.POST["input_conv"]
                answer = ""
                if input_conv and int(input_conv) >= 0:
                    if first == "miles" and second == "kilometers":
                        answer = (
                            f"{input_conv} miles = "
                            f"{int(input_conv) * miles_to_km} kilometers"
                        )
                    if first == "kilometers" and second == "miles":
                        answer = (
                            f"{input_conv} kilometers = "
                            f"{int(input_conv) * km_to_miles} miles"
                        )
                context = {
                    "form": form,
                    "m_form": measurement_form,
                    "input_conv": True,
                    "answer": answer
                }

        if request.POST["measurement"] == "weight":
            measurement_form = ConversionWeightForm()
            context = {
                "form": form,
                "m_form": measurement_form,
                "input_conv": True
            }
            if "input_conv" in request.POST:
                first = request.POST["measure1"]
                second = request.POST["measure2"]
                input_conv = request.POST["input_conv"]
                answer = ""
                if input_conv and int(input_conv) >= 0:
                    if first == "pound" and second == "kilogram":
                        answer = (
                            f"{input_conv} pound = "
                            f"{int(input_conv) * pound_to_kg} kilogram"
                        )
                    if first == "kilogram" and second == "pound":
                        answer = (
                            f"{input_conv} kilogram = "
                            f"{int(input_conv) * kg_to_pound} pound"
                        )
                context = {
                    "form": form,
                    "m_form": measurement_form,
                    "input_conv": True,
                    "answer": answer
                }
    else:
        form = ConversionForm()
        context = {
            "form": form,
            "input_conv": False
        }
    return render(request, "students/conversion.html", context=context)
