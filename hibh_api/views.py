from django.http import HttpResponse
from .models import Tracker, Alert
from .utils import createRandomUUID, get_location_data, send_alert_email, send_verification_email
from .serializers import TrackerSerializer,AlertSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from hibh.settings import BACKEND_URL

class TrackerView(APIView):

    def get(self, request):
        trackers = Tracker.objects.all()
        serializer = TrackerSerializer(trackers, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        data['private_key'] = createRandomUUID()
        data['public_key'] = createRandomUUID()
        data['email_token'] = createRandomUUID()
        serializer = TrackerSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            send_verification_email(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def verifyTracker(request, email_token):
    try:
        tracker = Tracker.objects.get(email_token=email_token)
        tracker.is_email_verified = True
        tracker.save()
        return Response(status = 200)
    except Tracker.DoesNotExist:
        return Response(
            {
            'message': 'Tracker Not Found',
            },
            status = status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
def getTrackerStats(request, private_key):
    try:
        tracker = Tracker.objects.get(private_key=private_key)
        alerts = Alert.objects.filter(tracker_id=tracker.id)
        trackerSerializer = TrackerSerializer(tracker)
        alertSerializer = AlertSerializer(alerts, many = True)
        data = {
            "info"  : trackerSerializer.data,
            "alerts" : alertSerializer.data
        }
        return Response(data)
    except Tracker.DoesNotExist:
        return Response(
            {
            'message': 'Tracker Not Found',
            },
            status = status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
def createAlert(request, public_key):
    try:
        tracker = Tracker.objects.get(public_key=public_key)
        ip = request.META.get('HTTP_X_FORWARDED_FOR').split(',')[0] if request.META.get('HTTP_X_FORWARDED_FOR') else request.META.get('REMOTE_ADDR', '')
        useragent = request.META.get('HTTP_USER_AGENT', '')
        locationData = get_location_data(ip)
        country = locationData["country_name"]
        country_flag = locationData["country_flag"]
        region = locationData["state_prov"]
        city = locationData["city"]
        coordinates = locationData["latitude"] + "," + locationData["longitude"]
        zip_code = locationData["zipcode"]
        isp = locationData["isp"]
        newAlert = Alert(tracker_id = tracker, ip_address = ip, country_flag = country_flag , useragent = useragent, country = country, region =  region, city = city, coordinates = coordinates, zip_code = zip_code, isp = isp)
        newAlert.save()
        
        if tracker.is_email_verified:
            send_alert_email(tracker, newAlert) # todo : Run Async in Background

    except Tracker.DoesNotExist:
        return Response(
            {},
            status = status.HTTP_404_NOT_FOUND
        )
    
    return Response(status = 200)

@api_view(['GET'])
def getTrackerHTMLFile(request, private_key):
    try:
        tracker = Tracker.objects.get(private_key=private_key)
        url = BACKEND_URL + "/api/alert/" + tracker.public_key
        html_content = f"""
        <!DOCTYPE html>
         <html>
            <head>
                <title>Loading...</title>
            </head>
            <body>
                <img src="{url}"/>
            </body>
         </html>
        """

        # Set the content type as text/html
        response = HttpResponse(html_content, content_type='text/html')

        # Set the content-disposition header to specify the filename
        response['Content-Disposition'] = 'attachment; filename="secret file.html"'
        return response
    
    except Tracker.DoesNotExist:
        return Response(
            {
            'message': 'Tracker Not Found',
            },
            status = status.HTTP_404_NOT_FOUND
        )