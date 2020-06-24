from django.urls import path

from demo.views import question_controller

question_patterns = [
    path('<int:question_id>', question_controller.get_question_by_id, name="get_question_by_id"),
]
