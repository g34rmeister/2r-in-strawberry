from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib.auth import get_user_model

from .serializers import *
from .models import *

User = get_user_model()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def card_transaction(request, card_id, new_owner_id):
    """
    Changes the owner of the current user's selected card to belong to a new user.
    """
    # 1. Fetch the card and ensure the requesting user is the current owner (optional but recommended)
    try:
        card = Card.objects.get(id=card_id, user=request.user)
    except Card.DoesNotExist:
        return Response({"detail": "Card not found or you are not the owner."},
                        status=status.HTTP_404_NOT_FOUND)
    
    # 2. Fetch the new owner user object
    try:
        new_owner = User.objects.get(id=new_owner_id)
    except User.DoesNotExist:
        return Response({"detail": f"User with ID {new_owner_id} not found."},
                        status=status.HTTP_400_BAD_REQUEST)

    # 3. Perform the ownership change (Transaction logic)
    card.user = new_owner
    card.save()

    # 4. Serialize the updated card to return the result
    serializer = CardSerializer(card)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_library(request):
    """
    Returns the user's personal plant library entries.
    """
    # Get all entries associated with that library
    card_collection = Card.objects.filter(user=request.user)

    serializer = CardSerializer(card_collection, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST']) 
@permission_classes([IsAuthenticated])
def add_to_library(request):
    """
    Copies an existing Card (by ID) and saves the copy
    to belong to the authenticated user. Updates user and group scores.
    """
    entry_id = request.data.get('entry_id')
    user = request.user # Get the user once
    
    if not entry_id:
        return Response({"error": "Missing 'entry_id' in request data."}, 
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        # 1. Get the existing entry data
        original_entry = Card.objects.get(pk=entry_id)
    except Card.DoesNotExist:
        return Response({"error": "Card not found."}, 
                        status=status.HTTP_404_NOT_FOUND)

    # 2. Check if the entry already exists in the user's library
    # The check must be based on the entry's unique properties (e.g., name and the user's library)
    if Card.objects.filter(user=user, name=original_entry.name).exists():
        return Response({"message": f"Plant '{original_entry.name}' is already in your library."}, 
                        status=status.HTTP_200_OK) 

    # Use a transaction to ensure all score updates are atomic (all succeed or all fail)
    with transaction.atomic():
        # 3. Create a new Card by copying the data
        new_entry = Card.objects.create(
            user=user,
            name=original_entry.name,
            image=original_entry.image,
            location_found=original_entry.location_found,
            description=original_entry.description,
            difficulty=original_entry.difficulty,
            date=original_entry.date
        )

        # 4. Update the user's global score
        score_to_add = 0
        if new_entry.difficulty == "EASY": # Use the value from Difficulty choices ('E', 'M', 'H')
            score_to_add = 1
        elif new_entry.difficulty == "MID":
            score_to_add = 2
        elif new_entry.difficulty == "HARD":
            score_to_add = 3

        user.score += score_to_add
        user.save() # Save the updated user object

        # 5. Update group scores
        # Get all FriendGroupMembership records for the current user
        memberships = FriendGroupMembership.objects.filter(member=user) 

        for membership in memberships:
            # Check if the card was 'found' *after* the user joined the group
            if membership.join_date <= new_entry.date: # Check should typically be <= date, not < date
                membership.score += score_to_add
                membership.save() # Save the updated membership object

    return Response({"message": f"'{new_entry.name}' added to collection.", "id": new_entry.pk}, 
                    status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# The view now accepts 'friendgroup_id' directly from the URL path
def get_group(request, friendgroup_id): 
    """
    Retrieves details for a specific FriendGroup by ID provided in the path.
    The user must be the owner or a member of the group.
    """
    
    # 1. Retrieve the FriendGroup object
    # Use get_object_or_404 for cleaner handling of DoesNotExist
    group = get_object_or_404(FriendGroup, pk=friendgroup_id)
    
    # 2. Permission check: User must be the owner or a member
    # Check if the user is the owner OR if the user exists in the members ManyToMany field
    if group.owner != request.user and not group.members.filter(pk=request.user.pk).exists():
        return Response({"error": "Not authorized to view this group."}, 
                        status=status.HTTP_403_FORBIDDEN)
                        
    # 3. Serialize and return data
    try:
        # Replace this with your actual serializer
        serializer = FriendGroupSerializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except NameError:
        # Placeholder response if the serializer import or definition is missing
        return Response(
            {"error": "Internal Error: FriendGroupSerializer not defined."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST']) 
@permission_classes([IsAuthenticated])
def add_to_group(request, friendgroup_id): 
    """
    Adds a user to a FriendGroup, updating the group-specific score.
    Expects 'member_username' and optional 'score' in POST data.
    """
    
    member_username = request.data.get('member_username')
    score = request.data.get('score', 0) # Default score is 0

    # 1. Retrieve the FriendGroup object using the path parameter
    group = get_object_or_404(FriendGroup, pk=friendgroup_id)

    # 2. Authorization Check: Only the owner can add members
    if group.owner != request.user:
        return Response({"error": "Only the group owner can add members."}, 
                        status=status.HTTP_403_FORBIDDEN)
                        
    # 3. Retrieve the target member user
    try:
        member_user = User.objects.get(username=member_username)
    except User.DoesNotExist:
        return Response({"error": "Member user not found."}, 
                        status=status.HTTP_404_NOT_FOUND)
                        
    # 4. Add or update the membership record
    membership, created = FriendGroupMembership.objects.update_or_create(
        group=group,
        member=member_user,
        defaults={'score': score}
    )
    
    message = (
        f"User '{member_username}' added to group '{group.name}'." if created 
        else f"User '{member_username}' score updated in group '{group.name}'."
    )
          
    return Response({"message": message}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_global_leaderboard(request):
    """
    Returns the application-wide leaderboard, ordered by UserProfile.score.
    """
    leaderboard_queryset = get_global_leaderboard_all_users()
    
    # Optional: Apply limit/pagination if the dataset is large, rn set to 100
    leaderboard_queryset = leaderboard_queryset[:100]
    
    serializer = GlobalLeaderboardUserSerializer(leaderboard_queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_global_group_leaderboard_view(request, friendgroup_id): 
    """
    Returns a group's leaderboard, ordered by the User's global score (CustomUser.score).
    Uses 'friendgroup_id' from the URL path.
    """
    
    # Use the path argument directly
    group_id = friendgroup_id
    
    # 1. Check if the FriendGroup exists (get_object_or_404 handles the 404 response)
    group = get_object_or_404(FriendGroup, pk=group_id)

    # Note: We now pass the path argument (group_id) to the helper function
    leaderboard_queryset = get_global_group_leaderboard(group_id)
    
    # 2. Check if the queryset is empty
    if not leaderboard_queryset.exists():
        # If the group exists but the queryset is empty, it means the group has no members/owner set up.
        return Response({"message": f"Group '{group.name}' is empty."}, status=status.HTTP_200_OK)
            
    serializer = GlobalLeaderboardUserSerializer(leaderboard_queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_group_specific_leaderboard_view(request, friendgroup_id):
    """
    Returns a group's leaderboard, ordered by the group-specific score 
    stored in FriendGroupMembership.score.
    Uses 'friendgroup_id' from the URL path.
    """
    
    # Use the path argument directly
    group_id = friendgroup_id
    
    # 1. Check if the FriendGroup exists (get_object_or_404 handles the 404 response)
    group = get_object_or_404(FriendGroup, pk=group_id)
    
    # Note: We now pass the path argument (group_id) to the helper function
    leaderboard_queryset = get_group_specific_leaderboard(group_id)
    
    # 2. Check if the queryset is empty
    if not leaderboard_queryset.exists():
        # If the group exists but the queryset is empty, it means the group has no membership records.
        return Response({"message": f"Group '{group.name}' has no members."}, status=status.HTTP_200_OK)

    serializer = GroupMembershipLeaderboardSerializer(leaderboard_queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)