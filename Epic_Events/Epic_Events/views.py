from rest_framework import filters
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Client, Event, Contract
from .permissions import Permissions
from .serializer import ClientSerializer, ContractSerializer, EventSerializer


class ReadOnlyClient(generics.ListCreateAPIView):
    serializer_class = ClientSerializer
    permission_classes = (Permissions,)
    search_fields = ['first_name', 'email']
    filter_backends = (filters.SearchFilter,)
    queryset = Client.objects.all()


class ReadOnlyContract(generics.ListCreateAPIView):
    serializer_class = ContractSerializer
    permission_classes = (Permissions,)
    search_fields = ['client__first_name', 'client__email', 'created_date', 'amount']
    filter_backends = (filters.SearchFilter,)
    queryset = Contract.objects.all()


class ReadOnlyEvent(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = (Permissions,)
    search_fields = ['client__first_name', 'client__email', 'event_date']
    filter_backends = (filters.SearchFilter,)
    queryset = Event.objects.all()


class ClientView(APIView):
    serializer_class = ClientSerializer
    permission_classes = (Permissions,)

    @staticmethod
    def get(request):
        if request.user.role == "Support":
            event_queryset = Event.objects.filter(support_user=request.user).values_list('client')
            client_queryset = Client.objects.filter(pk__in=event_queryset)
            objects = ClientSerializer(client_queryset, many=True)
            return Response(objects.data, status=status.HTTP_200_OK)
        elif request.user.is_superuser:
            return getAdvice()
        else:
            client_queryset = Client.objects.filter(sales_user=request.user)
            objects = ClientSerializer(client_queryset, many=True)
            return Response(objects.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        if request.user.role == "Support":
            return Response("You are not allowed to create a client", status=status.HTTP_401_UNAUTHORIZED)
        elif request.user.is_superuser:
            return getAdvice()
        else:
            context = {'request': request}
            serializer = ClientSerializer(data=request.data, context=context)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "Message": "Client created successfully"}, status=status.HTTP_201_CREATED
                )

            return Response({"Errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request, client_id):
        if request.user.role == "Support":
            return Response("You are not allowed to update a client", status=status.HTTP_401_UNAUTHORIZED)
        elif request.user.is_superuser:
            return getAdvice()
        else:
            if Client.objects.filter(id=client_id).exists():
                if Client.objects.filter(id=client_id, sales_user=request.user).exists():
                    client = Client.objects.get(id=client_id, sales_user=request.user)
                    context = {'request': request}
                    serializer = ClientSerializer(client, data=request.data, context=context)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({
                            "Message": "Client updated successfully"}, status=status.HTTP_201_CREATED
                        )

                    return Response({"Errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"You cannot updated the informations of a client that is not assigned to you"},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"There are no client with this id"}, status=status.HTTP_400_BAD_REQUEST)


class ContractView(APIView):
    serializer_class = ContractSerializer
    permission_classes = (Permissions,)

    @staticmethod
    def get(request):
        if request.user.role == "Support":
            return Response("You are not allowed to view contracts", status=status.HTTP_401_UNAUTHORIZED)
        elif request.user.is_superuser:
            return getAdvice()
        else:
            contract_queryset = Contract.objects.filter(sales_user=request.user)
            objects = ContractSerializer(contract_queryset, many=True)
            return Response(objects.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        if request.user.role == "Support":
            return Response("You are not allowed to create a contract", status=status.HTTP_401_UNAUTHORIZED)
        elif request.user.is_superuser:
            return getAdvice()
        else:
            context = {'request': request}
            serializer = ContractSerializer(data=request.data, context=context)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "Message": "Contract created successfully"}, status=status.HTTP_201_CREATED
                )

            return Response({"Errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request, client_id, contract_id):
        if request.user.role == "Support":
            return Response("You are not allowed to update a contract", status=status.HTTP_401_UNAUTHORIZED)
        elif request.user.is_superuser:
            return getAdvice()
        else:
            if Client.objects.filter(id=client_id).exists():
                client = Client.objects.get(id=client_id)
                if Contract.objects.filter(id=contract_id).exists():
                    if Contract.objects.filter(id=contract_id, client=client, sales_user=request.user).exists():
                        contract = Contract.objects.get(id=contract_id, client=client, sales_user=request.user)
                        context = {'request': request}
                        serializer = ContractSerializer(contract, data=request.data, context=context)
                        if serializer.is_valid():
                            serializer.save()
                            return Response({
                                "Message": "Contract updated successfully"}, status=status.HTTP_201_CREATED
                            )

                        return Response({"Errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response(
                            {"You cannot updated the informations of a contract that is not assigned to you"},
                            status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"There are no contract with this id"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"There are no client with this id"}, status=status.HTTP_400_BAD_REQUEST)


class EventView(APIView):
    serializer_class = EventSerializer
    permission_classes = (Permissions,)

    @staticmethod
    def get(request):
        if request.user.role == "Support":
            event_queryset = Event.objects.filter(support_user=request.user)
            objects = EventSerializer(event_queryset, many=True)
            return Response(objects.data, status=status.HTTP_200_OK)
        elif request.user.is_superuser:
            return getAdvice()
        else:
            event_queryset = Event.objects.filter(sales_user=request.user)
            objects = EventSerializer(event_queryset, many=True)
            return Response(objects.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        if request.user.role == "Support":
            return Response("You are not allowed to create an event", status=status.HTTP_401_UNAUTHORIZED)
        elif request.user.is_superuser:
            return getAdvice()
        else:
            context = {'request': request}
            serializer = EventSerializer(data=request.data, context=context)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "Message": "Event created successfully"}, status=status.HTTP_201_CREATED
                )

            return Response({"Errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request, client_id, contract_id, event_id):
        if request.user.role == "Vente":
            return Response("You are not allowed to update an event", status=status.HTTP_401_UNAUTHORIZED)
        elif request.user.is_superuser:
            return getAdvice()
        else:
            if Client.objects.filter(id=client_id).exists():
                client = Client.objects.get(id=client_id)
                if Contract.objects.filter(id=contract_id).exists():
                    contract = Contract.objects.get(id=contract_id)
                    if Event.objects.filter(id=event_id).exists():
                        if Event.objects.filter(id=event_id, client=client, contract=contract,
                                                support_user=request.user).exists():
                            event = Event.objects.get(id=event_id, client=client, contract=contract,
                                                      support_user=request.user)
                            context = {'request': request}
                            serializer = EventSerializer(event, data=request.data, context=context)
                            if serializer.is_valid():
                                serializer.save()
                                return Response({
                                    "Message": "Event updated successfully"}, status=status.HTTP_201_CREATED
                                )

                            return Response({"Errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response(
                                {"You cannot updated the informations of an event that is not assigned to you"},
                                status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({"There are no event with this id"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"There are no contract with this id"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"There are no client with this id"}, status=status.HTTP_400_BAD_REQUEST)


def getAdvice():
    return Response("Since you are an admin you can login to the django admin website and manage the crm there",
                    status=status.HTTP_200_OK)
