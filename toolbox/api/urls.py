from django.urls import ( path,include)


from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'api'

urlpatterns = [
   
path("", views.home),

# api app

    #Return all tools
    path('tools/', views.ToolList.as_view(), name='tool-list'),
    #return tools with much key world
    path('tools/search/', views.ToolViewSet.as_view({'get': 'list'}), name='tool-search'),
    # Return  Tool detail endpoint with the tool's ID
    path('tools/<int:pk>/', views.ToolDetailAPIView.as_view(), name='tool-detail'),
    #authenticated user Return Ratings and reviews of specific Tool
    path('tools/<int:pk>/ratings/', views.ToolRatingsAndReviewsView.as_view(), name='tool-ratings-and-reviews'),
    #authenticated user Give Rate to a Specific Tool value passed to the body
    path('tools/<int:tool_id>/submit-rating/', views.SubmitRatingView.as_view(), name='submit-rating'),
    #authenticated Give Review to a Specific Tool content passed to the body
    path('tools/<int:tool_id>/submit-review/', views.SubmitReviewView.as_view(), name='submit-review'),
    # authenticated share tool to a single or many user list of user's ids passed to the body 
    path('tools/<int:tool_id>/share/', views.ShareToolView.as_view(), name='share-tool'),
    #authenticated user Remove SheredTool from a  his/her sharedlist Actual ToolId and ToolId in sharedList must be passed Respectively 
    path('tools/<int:tool_id>/share/<int:shared_tool_id>/', views.RemoveSharedToolView.as_view(), name='remove-shared-tool'),

    #authenticated users to add a tool to their favorites but does not add it if it's already in their favorites
    path('tools/<int:tool_id>/add-to-favorites/', views.AddToFavoritesView.as_view(), name='add-to-favorites'),
    #allows an authenticated user to get the tools from their favorites
    path('favorites/', views.UserFavoritesView.as_view(), name='user-favorites'),
    #allows an authenticated user to remove a tool from their favorites
    path('favorites/remove/<int:tool_id>/',views.RemoveFavoriteToolView.as_view(), name='remove-favorite-tool'),
    #allows an authenticated user to create a new tool
    path('tools/create/', views.ToolListCreateView.as_view(), name='create-tool'),
    #allows an authenticated user to delete his/her own tool 
    path('tools/<int:tool_id>/delete/', views.DeleteToolView.as_view(), name='delete_tool'),
    #allows an authenticated user to update his/her own tool 
    path('tools/<int:tool_id>/update/',views.UpdateToolView.as_view(), name='update-tool'),
    #allows an authenticated user to get Average ratigs of his/her own tools 
    path('tools/average-ratings/',views.AverageRatingsAndReviewsView.as_view(), name='average_ratings_reviews'),
    #allows an authenticated user to get All Tools With Average ratigs 
    path('tools/average-ratings-all/', views.ToolListWithAverageRatings.as_view(), name='average-ratings-list'),
    path('register/', views.UserRegistrationView.as_view(), name='user-registration'),
    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('tags/', views.TagList.as_view(), name='tag-list'),
    
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    
]