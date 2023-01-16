from django.http import JsonResponse
from django.views import View
from netnegar.models import HealthDetail


class NewRecord(View):
    @staticmethod
    def get(request):
        data = request.GET
        print(data)
        result = HealthDetail.add_record(data)
        if result:
            return JsonResponse({"status": True}, status=200)
        else:
            return JsonResponse({"status": False}, status=400)

    @staticmethod
    def post(request):
        data = request.POST
        print(data)
        result = HealthDetail.add_record(data)
        if result:
            return JsonResponse({"status": True}, status=200)
        else:
            return JsonResponse({"status": False}, status=400)


class GetData(View):
    def get(self, request):
        return self.retrieve_data(

        )

    def post(self, request):
        return self.retrieve_data(

        )

    @staticmethod
    def retrieve_data(**filters):
        if filters is None:
            filters = {}
        result = HealthDetail.get_data(**filters)
        if result is False:
            return JsonResponse(
                data={"status": False},
                status=400
            )
        else:
            return JsonResponse(
                data={"status": False, "data": result},
                status=200,
                safe=False
            )
