from .models import AcademicSession


class SiteWideConfigs:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_session = AcademicSession.objects.get(current=True)

        request.current_session = current_session

        response = self.get_response(request)

        return response
