from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()

# --- Base Serializers ---
class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'name', 'image', 'location_found', 'description', 'user']
        read_only_fields = ['id']


# --- Leaderboard Serializers ---
class GlobalLeaderboardUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the global leaderboard. 
    It accesses the 'score' field directly from the CustomUser model.
    """

    class Meta:
        model = User
        # Include the score field directly alongside standard user fields
        fields = ['id', 'username', 'score']


class GroupMembershipLeaderboardSerializer(serializers.ModelSerializer):
    # Nested serializer to get the member's details and global score
    member = GlobalLeaderboardUserSerializer(read_only=True)

    class Meta:
        model = FriendGroupMembership
        # Includes the group-specific score and the member details
        fields = ['member', 'score']
        # The ordering is already defined in the FriendGroupMembership model Meta


# --- Other Serializers ---

class FriendGroupSerializer(serializers.ModelSerializer):
    # Use SlugRelatedField for M2M to display usernames instead of IDs
    members = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='username'
    )
    # Display the owner's username
    owner = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = FriendGroup
        fields = ['id', 'name', 'owner', 'members']
        read_only_fields = ['id', 'owner']