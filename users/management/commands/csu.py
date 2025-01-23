from django.contrib.auth.models import Group
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """ Для создания суперюзера """
    def handle(self, *args, **options):

        group = Group.objects.filter(name='Moderators').exists()
        if not group:
            group = Group.objects.create(name='Moderators')

        admin_user = User.objects.filter(is_superuser=True).exists()
        if not admin_user:
            user = User.objects.create(
                email='admin@sky.pro',
                is_staff=True,
                is_superuser=True,
                is_active=True,
                name='Admin',
                city='Russia'
            )
            user.set_password('1234')
            user.save()

            if group:
                user.groups.add(group)
