# calculator/views.py
from rest_framework import filters, viewsets, pagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import CustomUser, Operation, Record
from .serializers import CustomUserSerializer, OperationSerializer, RecordSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.http import JsonResponse
from .utils import get_random_string
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.decorators import api_view

class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class OperationViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type']
    search_fields = ['type']
    ordering_fields = ['id', 'type', 'cost']
    pagination_class = CustomPagination

class RecordViewSet(viewsets.ModelViewSet):
    serializer_class = RecordSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'operation']
    search_fields = ['user__username', 'operation__type']
    ordering_fields = ['id', 'user', 'operation', 'amount', 'user_balance', 'operation_response', 'date']
    pagination_class = CustomPagination

    def get_queryset(self):
        return Record.objects.filter(user=self.request.user, deleted=False)


    def destroy(self, request, *args, **kwargs):
        record = self.get_object()
        record.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class UserCreate(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = ()

@csrf_exempt
@api_view(['GET'])
def user_detail(request):
    user = request.user
    serializer = CustomUserSerializer(user)
    return Response(serializer.data)

@csrf_exempt
@api_view(['POST'])
def addition(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        value1 = data.get('value1')
        value2 = data.get('value2')
        result = float(value1) + float(value2)

        user = request.user
        operation = Operation.objects.get(type='addition')

        if user.credit - operation.cost < 0:
            return JsonResponse({"error": "Insufficient credit"}, status=400)

        record = Record(
            operation=operation,
            user=user,
            amount=operation.cost,
            user_balance=user.credit,
            operation_response=str(result),
        )
        record.save()

        return JsonResponse({"result": str(result)})
    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
@api_view(['POST'])
def subtraction(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        value1 = data.get('value1')
        value2 = data.get('value2')
        result = float(value1) - float(value2)

        user = request.user
        operation = Operation.objects.get(type='subtraction')

        if user.credit - operation.cost < 0:
            return JsonResponse({"error": "Insufficient credit"}, status=400)

        record = Record(
            operation=operation,
            user=user,
            amount=operation.cost,
            user_balance=user.credit,
            operation_response=str(result),
        )
        record.save()

        return JsonResponse({"result": str(result)})
    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
@api_view(['POST'])
def multiplication(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        value1 = data.get('value1')
        value2 = data.get('value2')
        result = float(value1) * float(value2)

        user = request.user
        operation = Operation.objects.get(type='multiplication')

        if user.credit - operation.cost < 0:
            return JsonResponse({"error": "Insufficient credit"}, status=400)

        record = Record(
            operation=operation,
            user=user,
            amount=operation.cost,
            user_balance=user.credit,
            operation_response=str(result),
        )
        record.save()

        return JsonResponse({"result": str(result)})
    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
@api_view(['POST'])
def division(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        value1 = data.get('value1')
        value2 = data.get('value2')
        if value2 == 0:
            return JsonResponse({"error": "Division by zero is not allowed"}, status=400)
        result = float(value1) / float(value2)
        user = request.user
        operation = Operation.objects.get(type='division')

        if user.credit - operation.cost < 0:
            return JsonResponse({"error": "Insufficient credit"}, status=400)

        record = Record(
            operation=operation,
            user=user,
            amount=operation.cost,
            user_balance=user.credit,
            operation_response=str(result),
        )
        record.save()

        return JsonResponse({"result": str(result)})
    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
@api_view(['POST'])
def square_root(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        value = data.get('value1')
        result = float(value) ** 0.5
        user = request.user
        operation = Operation.objects.get(type='square_root')

        if user.credit - operation.cost < 0:
            return JsonResponse({"error": "Insufficient credit"}, status=400)

        record = Record(
            operation=operation,
            user=user,
            amount=operation.cost,
            user_balance=user.credit,
            operation_response=str(result),
        )
        record.save()

        return JsonResponse({"result": str(result)})
    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
@api_view(['POST'])
def random_string(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        length = data.get('length', 10)
        result = get_random_string(length)
        user = request.user
        operation = Operation.objects.get(type='random_string')

        if user.credit - operation.cost < 0:
            return JsonResponse({"error": "Insufficient credit"}, status=400)

        record = Record(
            operation=operation,
            user=user,
            amount=operation.cost,
            user_balance=user.credit,
            operation_response=str(result),
        )
        record.save()

        return JsonResponse({"result": str(result)})
    return JsonResponse({"error": "Invalid request method"}, status=400)

@api_view(['POST'])
def delete_record(request, record_id):
    try:
        record = Record.objects.get(id=record_id)
        record.deleted = True
        record.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Record.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

