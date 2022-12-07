from django.utils import timezone

from .models import AcademicSession


class SiteWideConfigs:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            current_session = AcademicSession.objects.get(current=True)
        except:
            year = timezone.localtime(timezone.now()).year
            current_session = AcademicSession.objects.create(year=year)

        request.current_session = current_session

        response = self.get_response(request)

        return response
