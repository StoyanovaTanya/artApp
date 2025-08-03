from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from artwork.models import Artwork  # Change to your actual model

class Command(BaseCommand):
    help = 'Creates initial user groups with appropriate permissions.'

    def handle(self, *args, **options):
        # Define group names
        admin_group_name = 'Admins'
        staff_group_name = 'Staff'

        # Get content type for the target model
        content_type = ContentType.objects.get_for_model(Artwork)

        # Define permissions
        all_permissions = Permission.objects.filter(content_type=content_type)
        limited_permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=['add_artwork', 'change_artwork', 'view_artwork']
        )

        # Create or get Admin group
        admin_group, created = Group.objects.get_or_create(name=admin_group_name)
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created group: {admin_group_name}'))
        admin_group.permissions.set(all_permissions)
        self.stdout.write(self.style.SUCCESS(f'Set full permissions to {admin_group_name}'))

        # Create or get Staff group
        staff_group, created = Group.objects.get_or_create(name=staff_group_name)
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created group: {staff_group_name}'))
        staff_group.permissions.set(limited_permissions)
        self.stdout.write(self.style.SUCCESS(f'Set limited permissions to {staff_group_name}'))

        self.stdout.write(self.style.SUCCESS('Groups and permissions were successfully configured.'))