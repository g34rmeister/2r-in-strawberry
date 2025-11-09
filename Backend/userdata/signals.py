from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FriendGroupMembership, FriendGroup # Import your models
from friendship.models import Friend # Import the Friend model from django-friendships

@receiver(post_save, sender=FriendGroupMembership)
def create_friendships_on_group_add(sender, instance, created, **kwargs):
    """
    Ensures that when a user is added to a group (via FriendGroupMembership creation),
    they are friended with all other members of that group.
    """
    if created:
        new_member = instance.member
        friend_group = instance.group
        
        # Get all members of the group *excluding* the new member
        existing_members = friend_group.members.exclude(pk=new_member.pk)
        
        for existing_member in existing_members:
            # Check if a friendship already exists or is requested (optional, but good)
            if not Friend.objects.are_friends(new_member, existing_member):
                # 1. New member sends a request to existing member
                Friend.objects.add_friend(new_member, existing_member) 
                
                # 2. Existing member accepts the request from the new member
                Friend.objects.accept_request(existing_member, new_member)