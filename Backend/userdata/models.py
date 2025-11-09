from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    Custom User model extending Django's AbstractUser to add global score.
    """
    # The new score field is added directly to the User model
    score = models.IntegerField(_("Global User Score"), default=0)
    
    def __str__(self):
        return self.username


class PlantLibrary(models.Model):
    # This is correct and points to CustomUser
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='plant_library') 
    
    def __str__(self):
        return f"{self.user}'s Library"


class PlantLibraryEntry(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="Images/")
    location_found = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    library = models.ForeignKey(
        PlantLibrary,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.name}"


class FriendGroupMembership(models.Model):
    """
    Intermediate model to link a User to a FriendGroup and store the user's score/rank
    within that specific group.
    """
    group = models.ForeignKey(
        'FriendGroup', 
        on_delete=models.CASCADE
    )
    
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    
    # The new feature to store the score for this user in this group
    score = models.IntegerField(_("Member Score"), default=0)
    
    class Meta:
        # Ensures a user can only be added to a group once
        unique_together = ('group', 'member')
        # This will be the default sorting mechanism when retrieving members
        ordering = ['-score', 'member__username'] # Sort by score (highest first), then by username

    def __str__(self):
        return f"{self.member.username} in {self.group.name} (Score: {self.score})"


# friend groups -> ordered user by rank
class FriendGroup(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name='owned_friend_groups',
    )
    
    name = models.CharField(_("Group Name"), max_length=100, default="My Friend Group")

    # Use the 'through' argument to enable group-specific scores.
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='FriendGroupMembership',
        related_name='friend_groups',
        blank=True,
    )
    
    def __str__(self):
        return f"Friend Group: {self.name}"

    class Meta:
        verbose_name = _("Friend Group")
        verbose_name_plural = _("Friend Groups")


# Example Usage:
# print("--- Global Leaderboard (All Users) ---")
# for rank, user in enumerate(get_global_leaderboard_all_users(), 1):
#     print(f"Rank {rank}: {user.username} - Global Score: {user.profile.score}")
def get_global_leaderboard_all_users():
    """
    Returns a QuerySet of ALL CustomUser objects in the application,
    ordered globally by the score stored directly on the CustomUser model.
    """
    # Query all users, and order directly by the 'score' field on CustomUser.
    leaderboard = CustomUser.objects.all().order_by(
        '-score',
        'username'
    ) 
    
    return leaderboard


# Example:
# for user in get_group_leaderboard(1):
#     print(f"{user.username}: {user.profile.score}")
def get_global_group_leaderboard(group_id):
    """
    Returns a QuerySet of all CustomUser objects (owner + members) in a FriendGroup, 
    ordered by their global score stored in CustomUser.score.
    """
    try:
        group = FriendGroup.objects.get(id=group_id)
    except FriendGroup.DoesNotExist:
        return CustomUser.objects.none() # Use CustomUser instead of User

    # 1. Get the IDs of users explicitly added as members
    member_ids = group.members.values_list('id', flat=True)
    
    # 2. Add the owner's ID to the list
    all_user_ids = list(member_ids)
    if group.owner_id and group.owner_id not in all_user_ids:
          all_user_ids.append(group.owner_id)

    # 3. Query the CustomUser model and order by the direct score field
    leaderboard = CustomUser.objects.filter(id__in=all_user_ids).order_by(
        '-score',
        'username'
    ) # Remove .select_related('profile')
    
    return leaderboard


# Example Usage:
# for rank, membership in enumerate(get_group_specific_leaderboard(1), 1):
#     print(f"Rank {rank}: {membership.member.username} - Group Score: {membership.score}")
def get_group_specific_leaderboard(group_id):
    """
    Returns a QuerySet of FriendGroupMembership objects for a group, 
    ordered by their group-specific score. 
    """
    try:
        group = FriendGroup.objects.get(id=group_id)
    except FriendGroup.DoesNotExist:
        return FriendGroupMembership.objects.none()

    # Query the reverse relation from FriendGroup to its memberships.
    # We only need to select_related the 'member' (CustomUser) now.
    leaderboard = group.friendgroupmembership_set.all().select_related('member') # Removed ', 'member__profile'
    
    return leaderboard