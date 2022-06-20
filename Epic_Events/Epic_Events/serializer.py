from datetime import datetime

from rest_framework import serializers

from .models import Client, Contract, Event


class ClientSerializer(serializers.ModelSerializer):
    is_confirmed_client = serializers.BooleanField(allow_null=True, default=False, required=False)

    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ('id', 'sales_user', 'created_date', 'updated_date')

    def create(self, validated_data):
        sales_user = self.context['request'].user
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        email = validated_data['email']
        phone = validated_data['phone']
        mobile = validated_data['mobile']
        company_name = validated_data['company_name']
        is_confirmed_client = validated_data['is_confirmed_client']
        client_obj = Client(sales_user=sales_user,
                            first_name=first_name,
                            last_name=last_name,
                            email=email,
                            phone=phone,
                            mobile=mobile,
                            company_name=company_name,
                            is_confirmed_client=is_confirmed_client)
        client_obj.save()
        return validated_data


class ContractSerializer(serializers.ModelSerializer):
    client = serializers.CharField(required=False)
    is_signed = serializers.BooleanField(allow_null=True, default=False, required=False)

    class Meta:
        model = Contract
        fields = '__all__'
        read_only_fields = ('id', 'created_date', 'updated_date')

    def create(self, validated_data):
        client = Client.objects.get(first_name=validated_data['client'])
        sales_user = self.context['request'].user
        name = validated_data['name']
        description = validated_data['description']
        amount = validated_data['amount']
        is_signed = validated_data['is_signed']
        contract_obj = Contract(client=client,
                                sales_user=sales_user,
                                name=name,
                                description=description,
                                amount=amount,
                                is_signed=is_signed)
        contract_obj.save()
        return validated_data

    def validate(self, attrs):
        if self.context['request'].method == "POST":
            if Client.objects.filter(first_name=attrs['client']).exists():
                client = Client.objects.get(first_name=attrs['client'])
            else:
                raise serializers.ValidationError("There are no client with the first name : " + str(attrs['client']))

            if client.is_confirmed_client:
                pass
            else:
                raise serializers.ValidationError('This client is not a confirmed client yet')
        else:
            pass

        return attrs


class EventSerializer(serializers.ModelSerializer):
    client = serializers.CharField(required=False)
    contract = serializers.CharField(required=False)
    event_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", default=datetime.now, allow_null=True,
                                           required=False)
    is_finished = serializers.BooleanField(allow_null=True, default=False, required=False)

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('id', 'created_date', 'updated_date')

    def create(self, validated_data):
        client = Client.objects.get(first_name=validated_data['client'])
        sales_user = None
        support_user = None
        if self.context['request'].user.role == "Vente":
            sales_user = self.context['request'].user
        else:
            support_user = self.context['request'].user
        contract = Contract.objects.get(name=validated_data['contract'])
        name = validated_data['name']
        description = validated_data['description']
        guests_number = validated_data['guests_number']
        event_date = validated_data['event_date']
        is_finished = validated_data['is_finished']
        event_obj = Event(client=client,
                          sales_user=sales_user,
                          support_user=support_user,
                          contract=contract,
                          name=name,
                          description=description,
                          guests_number=guests_number,
                          event_date=event_date,
                          is_finished=is_finished,
                          )
        event_obj.save()
        return validated_data

    def validate(self, attrs):
        if self.context['request'].method == "POST":
            if Client.objects.filter(first_name=attrs['client']).exists():
                pass
            else:
                raise serializers.ValidationError("There are no client with the first name : " + str(attrs['client']))

            if Contract.objects.filter(name=attrs['contract']).exists():
                contract = Contract.objects.get(name=attrs['contract'])
            else:
                raise serializers.ValidationError("There are no contract with the name : " + str(attrs['contract']))

            if contract.is_signed:
                pass
            else:
                raise serializers.ValidationError('The event cannot be created until it\'s contract is signed')

        else:
            pass

        return attrs
