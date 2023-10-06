# create_dummy_data.py

import random
from faker import Faker

from django.core.management.base import BaseCommand
from api.models import Tool, Rating, Category, Tag, Favorite, History, Review, SharedTool,User

fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with dummy data'

    def handle(self, *args, **options):
        # Create categories and tags
        categories = [Category.objects.create(name=fake.word()) for _ in range(5)]
        tags = [Tag.objects.create(name=fake.word()) for _ in range(5)]

        # Create users
        users = []
        for _ in range(10):
            user = User.objects.create_user(fake.user_name(), fake.email(), 'password')
            users.append(user)

        # Create tools with associations
        tools = []
        for _ in range(20):
            tool = Tool.objects.create(
                name=fake.word(),
                description=fake.text(),
                download_link=fake.url(),
                license=random.choice(['Open Source', 'Commercial']),
                owner=random.choice(users),
            )
            tool.categories.set(random.sample(categories, random.randint(1, 3)))
            tool.tags.set(random.sample(tags, random.randint(1, 3)))
            tools.append(tool)

        # Create ratings for tools
        for tool in tools:
            for _ in range(random.randint(0, 10)):
                Rating.objects.create(
                    tool=tool,
                    user=random.choice(users),
                    value=random.randint(1, 5)
                )

        # Create favorites for users
        for user in users:
            for _ in range(random.randint(0, 5)):
                Favorite.objects.create(
                    user=user,
                    tool=random.choice(tools)
                )

        # Create history for users
        for user in users:
            for _ in range(random.randint(0, 5)):
                History.objects.create(
                    user=user,
                    tool=random.choice(tools)
                )

        # Create reviews for tools
        for tool in tools:
            for _ in range(random.randint(0, 5)):
                Review.objects.create(
                    tool=tool,
                    user=random.choice(users),
                    content=fake.text()
                )

        # Create shared tools
        for tool in tools:
            for _ in range(random.randint(0, 5)):
                shared_tool = SharedTool.objects.create(
                    tool=tool,
                    shared_by=random.choice(users),
                )
                shared_tool.shared_with.set(random.sample(users, random.randint(1, 3)))

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with dummy data'))
