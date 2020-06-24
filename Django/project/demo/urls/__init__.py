from django.urls import path, include

from demo.urls.api_question import question_patterns

api_urls = [
    path('question/', include(question_patterns)),
]
