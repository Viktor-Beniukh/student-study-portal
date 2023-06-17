from django.urls import path

from students import views


app_name = "students"


urlpatterns = [
    path("", views.index, name="index"),

    path(
        "notes/",
        views.NoteListView.as_view(),
        name="notes"
    ),
    path(
        "notes/<int:pk>/",
        views.NoteDetailView.as_view(),
        name="note-detail"
    ),
    path(
        "notes/<int:pk>/delete/",
        views.NoteDeleteView.as_view(),
        name="note-delete"
    ),

    path(
        "homeworks/",
        views.HomeworkListView.as_view(),
        name="homeworks"
    ),
    path(
        "homeworks/<int:pk>/delete/",
        views.HomeworkDeleteView.as_view(),
        name="homework-delete"
    ),
    path(
        "homeworks/<int:pk>/update/",
        views.HomeworkUpdateView.as_view(),
        name="homework-update"
    ),

    path("youtube/", views.youtube_view, name="youtube"),

    path(
        "todos/",
        views.TodoListView.as_view(),
        name="todos"
    ),
    path(
        "todos/<int:pk>/delete/",
        views.TodoDeleteView.as_view(),
        name="todo-delete"
    ),
    path(
        "todos/<int:pk>/update/",
        views.TodoUpdateView.as_view(),
        name="todo-update"
    ),

    path("books/", views.books_view, name="books"),

    path("dictionary/", views.dictionary_view, name="dictionary"),

    path("wikipedia/", views.wikipedia_view, name="wikipedia"),

    path("conversion/", views.conversion_view, name="conversion"),
]
