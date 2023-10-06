from rest_framework import serializers

from .models import Tool, Review, Rating, User, Category, Tag ,Favorite # Import related models as needed
from django.db.models import Avg


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'is_superuser',  'first_name', 'last_name')

class ReviewSerializer(serializers.ModelSerializer):
    # tool_name = serializers.CharField(source='tool.name')
    reviewer_name = serializers.CharField(source='user.username')
    
    class Meta:
        model = Review
        fields = [
            'reviewer_name',
            'content',
            'created_at',
            'updated_at',
        ]

class RatingSerializer(serializers.ModelSerializer):
    rater_name = serializers.CharField(source='user.username')
    class Meta:
        model = Rating
        fields = [
            'value',
            'rater_name',
        ]
        # exclude =('id',)
        





class CreateToolSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    license = serializers.CharField(max_length=255)
    download_link = serializers.URLField()
    description = serializers.CharField()
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all()) 
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),  write_only=True)

    #image = serializers.ImageField(required=False)

    def create(self, validated_data):
        # Try to create the Tool object and set categories/tags within a try block
        try:
            # Extract and create the Tool object here
            categories = validated_data.pop('categories')
            owner = validated_data.pop('owner')
            tags = validated_data.pop('tags')
            tool = Tool.objects.create(owner_id=owner, **validated_data)
            
            # Assuming you have a 'categories' and 'tags' field in your Tool model as ManyToMany relationships
            tool.categories.set(categories)
            tool.tags.set(tags)
            

            return tool
        except Exception as e:
            # Handle any exceptions that may occur during the creation process
            raise serializers.ValidationError(str(e))






class ToolSerializer(serializers.ModelSerializer):
    categories = serializers.StringRelatedField(many=True)
    tags = serializers.StringRelatedField(many=True)
    owner_name = serializers.CharField(source='owner')
    avg_ratings = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)

    class Meta:
        model = Tool
        fields = [
            'id',
            'name',
            'description',
            'download_link',
            'image',
            'license',
            'categories',  # Include the category name
            'tags',       # Include the tag name
            'owner_name',     # Include the owner's username
            'avg_ratings',
            'posted_at'
        ]
        


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model= Category
        fields = '__all__'
 
class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= Tag
        fields = '__all__'

class ToolDetailSerializer(serializers.ModelSerializer):

    # Define nested serializers for related fields    
    owner = UserSerializer()
    reviews = ReviewSerializer(many=True)
    ratings = RatingSerializer(many=True)
    categories = CategorySerializer(many=True)
    tags = CategorySerializer(many=True)
    
    class Meta:
        model = Tool
        fields = '__all__'




class ToolRatingsAndReviewsSerializer(serializers.Serializer):
    ratings = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    def get_ratings(self, tool):
        ratings = Rating.objects.filter(tool=tool)
        return [rating.value for rating in ratings]

    def get_reviews(self, tool):
        reviews = Review.objects.filter(tool=tool)
        return [{'content': review.content, 'user': review.user.username} for review in reviews]



    
class ToolUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = [
            'name',
            'description',
            'download_link',
            'image',
            'license',
            'categories',
            'tags',
        ]

class AverageRatingsAndReviewsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    avg_ratings = serializers.FloatField()
   

    class Meta:
        fields = ['id', 'name', 'avg_ratings']
        

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        # Create a new user with a hashed password
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
            
        )
        return user

    def validate_username(self, value):
        # Check if the username already exists
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        # Check if the email already exists
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        if not value:
            raise serializers.ValidationError("Email cannot be empty.")
        return value

