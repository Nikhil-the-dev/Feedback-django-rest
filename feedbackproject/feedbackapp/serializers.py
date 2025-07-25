# serializers.py
from rest_framework import serializers
from .models import Customer, Manager, Feedback, Admin, Reply

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'custid', 'password', 'email', 'mobileno', 'regdate']


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = ['id', 'managerid', 'password', 'deptname', 'fullname', 'email', 'mobile','regdate']


class FeedbackSerializer(serializers.ModelSerializer):
    # Instead of CustomerSerializer, just use the ID for `custid`
    custid = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    customer_details = CustomerSerializer(source='custid', read_only=True)
    class Meta:
        model = Feedback
        fields = ['id', 'custid','customer_details', 'feeddesc', 'feedrate', 'feeddate']


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id', 'adminid', 'fullname', 'email', 'password']



class ReplySerializer(serializers.ModelSerializer):
    # Only use the ID for customer, feedback, and manager
    custid = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())  # Only Customer ID
    feedback = serializers.PrimaryKeyRelatedField(queryset=Feedback.objects.all())  # Only Feedback ID
    managerid = serializers.PrimaryKeyRelatedField(queryset=Manager.objects.all())  # Only Manager ID
    customer_details = CustomerSerializer(source='custid', read_only=True)  # Include full customer data in the serialized output
    feedback_details = FeedbackSerializer(source='feedback', read_only=True)
    manager_details = ManagerSerializer(source='managerid', read_only=True)
    class Meta:
        model = Reply
        fields = ['id', 'custid', 'customer_details', 'feedback','feedback_details', 'managerid','manager_details','replymessage', 'replydate']
        


    




