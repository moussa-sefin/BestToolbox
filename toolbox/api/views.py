from django.http import JsonResponse
from rest_framework import generics,permissions,status
from rest_framework.generics import RetrieveAPIView
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import render, HttpResponse
from .models import Tool,Rating,Review,SharedTool,SharedTool,User,Favorite,Category,Tag
from .serializers import (ToolSerializer,
                          ToolDetailSerializer,
                          ToolRatingsAndReviewsSerializer,
                          RatingSerializer,
                          CreateToolSerializer,
                          ToolUpdateSerializer,
                          AverageRatingsAndReviewsSerializer,
                          UserRegistrationSerializer,
                          CategorySerializer,
                          TagSerializer
                          )
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny

from django.db.models import Avg, Value,CharField
from django.db.models.functions import Cast
from django.db import models


def home(request):
    
    # return render(request, "<IPI its work", {})
    return render(request,"api/index.html",{})



from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .serializers import CreateToolSerializer
from .models import Tool


from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # Use the TokenObtainPairSerializer to validate credentials and obtain the token
        serializer = TokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            # Customize the response payload with additional data
            user = serializer.user
            response = super().post(request, *args, **kwargs)
            if response.status_code == 200:
                response.data['user_id'] = user.id
                # Add any additional data you want to include in the response
                return response
        return Response(serializer.errors, status=400)



class ToolListWithAverageRatings(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 
    
    serializer_class = ToolSerializer
    pagination_class = PageNumberPagination 
    def get_queryset(self):
        # Calculate the average ratings for each tool
        queryset = Tool.objects.annotate(avg_ratings=Avg('ratings__value'))
        return queryset

class ToolList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer
    
    
from django.core.exceptions import PermissionDenied

class ToolListCreateView(generics.ListCreateAPIView):
    queryset = Tool.objects.all()
    permission_classes = [AllowAny] 
    serializer_class = CreateToolSerializer
    
    def tool_exists(self, name):
        return Tool.objects.filter(name=name).exists()

    def perform_create(self, serializer, ownerId):
        serializer.validated_data["owner"] = ownerId
        serializer.save()
        
    def post(self, request, *args, **kwargs):
        tool_name = request.data.get('name')
        
        if self.tool_exists(tool_name):
            return Response({'error': 'Tool with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)

        try:
            if serializer.is_valid():
                self.perform_create(serializer,request.data['owner'])
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                # The data is not valid, identify the fields with errors
                field_errors = {}
                for field, errors in serializer.errors.items():
                    if errors:
                        field_errors[field] = errors

                return Response({'field_errors': field_errors}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            # Catch the PermissionDenied exception and return its message
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)








    
    
    
    
class ToolViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'tags__name', 'categories__name', 'owner__username']



class ToolDetailAPIView(RetrieveAPIView):
    # You can adjust permissions as needed
    # By default, RetrieveAPIView handles retrieving a single object based on the URL parameter 'pk' (primary key)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  
    queryset = Tool.objects.all()
    serializer_class = ToolDetailSerializer
   


class ToolRatingsAndReviewsView(APIView):
    def get(self, request, pk):
        try:
            tool = Tool.objects.get(pk=pk)
        except Tool.DoesNotExist:
            return Response({"message": "Tool not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ToolRatingsAndReviewsSerializer(tool)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class SubmitRatingView(APIView):
    # authentication_classes = [YourAuthenticationClassHere]
    # permission_classes = [YourPermissionClassHere]
    @permission_classes([IsAuthenticated])
    def post(self, request, tool_id):
        try:
            tool = Tool.objects.get(pk=tool_id)
        except Tool.DoesNotExist:
            return Response({"detail": "Tool not found"}, status=status.HTTP_404_NOT_FOUND)

        # Extract the rating value from the request data
        rating_value = request.data.get('rating', None)

        if rating_value is None:
            return Response({"detail": "Rating value is missing"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new Rating instance and associate it with the tool
        Rating.objects.create(tool=tool, user=request.user, value=rating_value)

        return Response({"detail": "Rating submitted successfully"}, status=status.HTTP_201_CREATED)


class SubmitReviewView(APIView):
    # Define the required permission class
    @permission_classes([IsAuthenticated])
    def post(self, request, tool_id):
        try:
            tool = Tool.objects.get(pk=tool_id)
        except Tool.DoesNotExist:
            return Response({"detail": "Tool not found"}, status=status.HTTP_404_NOT_FOUND)

        # Extract the review content from the request data
        review_content = request.data.get('content', None)

        if review_content is None:
            return Response({"detail": "Review content is missing"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new Review instance and associate it with the tool and user
        Review.objects.create(tool=tool, user=request.user, content=review_content)

        return Response({"detail": "Review submitted successfully"}, status=status.HTTP_201_CREATED)
    


class ShareToolView(APIView):

    @permission_classes([IsAuthenticated])
    def post(self, request, tool_id):
        try:
            tool = Tool.objects.get(pk=tool_id)
        except Tool.DoesNotExist:
            return Response({"detail": "Tool not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the tool is already shared with the requesting user
        if SharedTool.objects.filter(tool=tool, shared_with=request.user).exists():
            return Response({"detail": "Tool is already shared with you"}, status=status.HTTP_400_BAD_REQUEST)

 
        # Extract the list of users to share the tool with from the request data
        shared_with_users = request.data.get('shared_with', [])

        if not shared_with_users:
            return Response({"detail": "Please specify users to share the tool with"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new SharedTool instance and share it with the specified users
        shared_tool = SharedTool(tool=tool, shared_by=request.user)
        shared_tool.save()
        shared_tool.shared_with.add(*shared_with_users)  # Use the * to unpack the list

        return Response({"detail": "Tool shared successfully"}, status=status.HTTP_201_CREATED)



class RemoveSharedToolView(APIView):

    @permission_classes([IsAuthenticated])
    def delete(self, request, tool_id, shared_tool_id):  
        try:
            shared_tool = SharedTool.objects.get(pk=shared_tool_id,shared_by=request.user)
          
        except SharedTool.DoesNotExist:
            return Response({"detail": "Shared tool not found or you don't have permission to remove it"}, status=status.HTTP_404_NOT_FOUND)

        # Additional check: Ensure the shared tool's associated tool matches the provided tool_id
        if shared_tool.tool.id != tool_id:
            return Response({"detail": "The shared tool does not correspond to the provided tool_id"}, status=status.HTTP_400_BAD_REQUEST)

        shared_tool.delete()

        return Response({"detail": "Shared tool removed successfully"}, status=status.HTTP_204_NO_CONTENT)


class AddToFavoritesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, tool_id):
        try:
            tool = Tool.objects.get(pk=tool_id)
        except Tool.DoesNotExist:
            return Response({"detail": "Tool not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the tool is already in the user's favorites
        if Favorite.objects.filter(user=request.user, tool=tool).exists():
            return Response({"detail": "Tool is already in your favorites"}, status=status.HTTP_400_BAD_REQUEST)

        # Add the tool to the user's favorites
        favorite = Favorite(user=request.user, tool=tool)
        favorite.save()

        return Response({"detail": "Tool added to favorites successfully"}, status=status.HTTP_201_CREATED)


class UserFavoritesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get the favorite tools for the authenticated user
        favorite_tools = Favorite.objects.filter(user=request.user).values('tool')

        # Extract the tool IDs from the queryset
        tool_ids = [entry['tool'] for entry in favorite_tools]

        # Retrieve the actual Tool instances using the IDs
        favorite_tools = Tool.objects.filter(id__in=tool_ids)

        # Serialize the favorite tools using ToolSerializer
        serializer = ToolSerializer(favorite_tools, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class RemoveFavoriteToolView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, tool_id):
        try:
            tool = Tool.objects.get(pk=tool_id)
        except Tool.DoesNotExist:
            return Response({"detail": "Tool not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the tool is in the user's favorites
        favorite_entry = Favorite.objects.filter(user=request.user, tool=tool).first()

        if favorite_entry:
            favorite_entry.delete()
            return Response({"detail": "Tool removed from favorites"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "Tool is not in your favorites"}, status=status.HTTP_400_BAD_REQUEST)
        




class DeleteToolView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, tool_id):
        try:
            tool = Tool.objects.get(pk=tool_id, owner=request.user)
        except Tool.DoesNotExist:
            return Response({"detail": "Tool not found or you don't have permission to delete it"}, status=status.HTTP_404_NOT_FOUND)

        tool.delete()

        return Response({"detail": "Tool deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



class UpdateToolView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, tool_id):
        try:
            tool = Tool.objects.get(pk=tool_id, owner=request.user)
        except Tool.DoesNotExist:
            return Response({"detail": "Tool not found or you don't have permission to edit it"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ToolUpdateSerializer(tool, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Tool updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AverageRatingsAndReviewsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve the user's tools and annotate them with average ratings
        user_tools = Tool.objects.filter(owner=request.user).annotate(
            avg_ratings=Avg('ratings__value')
        )

        # Create a list to store reviews for each tool
        user_tools_with_reviews = []

        for user_tool in user_tools:
            reviews = user_tool.reviews.values_list('content', flat=True)
            user_tool.avg_reviews = list(reviews)  # Convert to a list

            # Add the tool with its reviews to the list
            user_tools_with_reviews.append(user_tool)

        # Serialize the list of tools with reviews
        serializer = AverageRatingsAndReviewsSerializer(user_tools_with_reviews, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    

    

class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Use serializer.save() to create and save the user
            serializer.save()
            return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer