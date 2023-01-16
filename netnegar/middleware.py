import json
import traceback

from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from datetime import datetime

from status.models import ErrorLog


class JSONMiddleware(MiddlewareMixin):
    """
    Process application/json requests data from GET and POST requests.
    """
    def process_request(self, request):

        if 'application/json' in request.META['CONTENT_TYPE']:
            # load the json data
            body_unicode = request.body.decode('utf-8')
            try:
                data = json.loads(body_unicode)
            except:
                data = body_unicode

            if request.method == 'POST':
                request.POST = data

        return None


class ExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        print(traceback.format_exc())
        try:
            ErrorLog(
                time=datetime.now(), place=request.path,
                data=str(request.user.username) + "\n" + str(request) + "\n" + str(request.body),
                error=traceback.format_exc()
            ).save()
            return JsonResponse(
                {'message': 'خطای داخلی سرور، زیبال این خطا را بررسی و برطرف خواهد کرد', 'status': False, 'result': -1},
                status=500, safe=False)
        except:
            print(traceback.format_exc())
            response = JsonResponse(
                {'message': 'خطای داخلی سرور، زیبال این خطا را بررسی و برطرف خواهد کرد', 'status': False, 'result': -1},
                status=500, safe=False)
            return response
