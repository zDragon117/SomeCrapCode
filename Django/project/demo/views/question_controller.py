from django.http import JsonResponse
from rest_framework.decorators import api_view

from demo.models import Question


@api_view(['GET'])
def get_all_question(request):
    err = 0
    msg = 'Get all question successfully!'
    dt = list()

    try:
        questions = Question.objects.all().values()
        dt = list(questions)
    except Exception as exc:
        err = 1
        msg = f'Get all question failed: {exc}'
    finally:
        return JsonResponse({
            'err': err,
            'msg': msg,
            'dt': dt,
        }, safe=False)


@api_view(['GET'])
def get_question_by_id(request, question_id):
    err = 0
    msg = 'Get question by id successfully!'
    dt = None

    check = request.META.get('HTTP_AI_SERVICES')
    if check == 'ai-services':
        question = Question.objects.filter(question_id=question_id).values()
        if len(question) == 0:
            return JsonResponse(status=404, data={'msg': f'Question with id {question_id} not found!'})
        return JsonResponse({
            'err': err,
            'msg': msg,
            'dt': question[0],
        })
    else:
        err = 1
        msg = 'Get question by id failed: Do not have authorization!'
        return JsonResponse({
            'err': err,
            'msg': msg,
            'dt': dt,
        })
