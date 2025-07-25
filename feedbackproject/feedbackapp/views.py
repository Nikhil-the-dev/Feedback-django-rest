from django.shortcuts import render
from rest_framework import viewsets
from .serializers import AdminSerializer, FeedbackSerializer, ManagerSerializer, CustomerSerializer, ReplySerializer
from .models import Admin,Feedback,Manager,Customer,Reply
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.contrib.auth import login
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# from rest_framework import status

# class AdminLoginViewset(APIView):
#     def post(self, request, format=None):
#         serializer = AdminSerializers(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data
#             login(request, user)
#             return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminViewset(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

class FeedbackViewset(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

class ManagerViewset(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer

class CustomerViewset(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

from rest_framework import viewsets
from .models import Reply
from .serializers import ReplySerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

class ReplyViewset(viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

    @action(detail=False, methods=['get'])
    def by_feedback(self, request):
        feedback_id = request.query_params.get('feedback', None)
        if feedback_id is not None:
            replies = Reply.objects.filter(feedback_id=feedback_id)
            serializer = self.get_serializer(replies, many=True)
            return Response(serializer.data)
        return Response([], status=status.HTTP_404_NOT_FOUND)


