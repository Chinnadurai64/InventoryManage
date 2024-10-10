import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Item
from .serializers import ItemSerializer
from django.core.cache import cache
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework import serializers

logger = logging.getLogger('inventory')  

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]  

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.info(f"User registered: {serializer.data['username']}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning(f"User registration failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemView(APIView):
    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Item created: {serializer.data}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning(f"Item creation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, item_id):
        cached_item = cache.get(f'item_{item_id}')
        if cached_item:
            logger.info(f"Retrieved cached item: {item_id}")
            return Response(cached_item)

        try:
            item = Item.objects.get(id=item_id)
            serializer = ItemSerializer(item)
            cache.set(f'item_{item_id}', serializer.data)
            logger.info(f"Retrieved item: {item_id}")
            return Response(serializer.data)
        except Item.DoesNotExist:
            logger.error(f"Item not found: {item_id}")
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
            serializer = ItemSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                cache.set(f'item_{item_id}', serializer.data)
                logger.info(f"Updated item: {item_id}")
                return Response(serializer.data)
            logger.warning(f"Item update failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Item.DoesNotExist:
            logger.error(f"Item not found for update: {item_id}")
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
            item.delete()
            cache.delete(f'item_{item_id}')
            logger.info(f"Deleted item: {item_id}")
            return Response({"message": "Item deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Item.DoesNotExist:
            logger.error(f"Item not found for deletion: {item_id}")
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
