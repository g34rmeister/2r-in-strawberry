from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.test import APITestCase

from .models import *

User = get_user_model()

class CardTransactionTests(APITestCase):
    """
    Tests for the card_transaction view which handles card ownership transfer.
    """

    def setUp(self):
        # 1. Setup initial users
        self.owner = User.objects.create_user(username='owner', password='testpassword')
        self.new_owner = User.objects.create_user(username='new_owner', password='testpassword')
        self.unrelated_user = User.objects.create_user(username='unrelated', password='testpassword')
        
        # 2. Setup the card
        self.card = Card.objects.create(name='Test Card', user=self.owner)
        
        # cards/<int:card_id>/transfer/<int:new_owner_id>/
        # 3. Define the URL pattern
        self.base_url_name = 'card-transaction' 

    def get_url(self, card_id, new_owner_id):
        """Helper to reverse the URL with required arguments."""
        # You may need to replace 'card-transaction' with the actual name defined in your urls.py
        return reverse(self.base_url_name, args=[card_id, new_owner_id])


    # --- Test Scenarios ---

    def test_successful_card_transfer_by_owner(self):
        """Ensure an authenticated owner can successfully transfer ownership."""
        
        # 1. Authenticate as the current owner
        self.client.force_authenticate(user=self.owner)
        
        # 2. Perform the POST request
        url = self.get_url(self.card.id, self.new_owner.id)
        response = self.client.post(url, format='json')
        
        # 3. Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh the model instance from the database
        self.card.refresh_from_db()
        
        # Check that the owner has actually changed
        self.assertEqual(self.card.user, self.new_owner)

    def test_transfer_failure_by_unrelated_user(self):
        """Ensure a user who does not own the card cannot transfer it."""
        
        # 1. Authenticate as an unrelated user
        self.client.force_authenticate(user=self.unrelated_user)
        
        # 2. Perform the POST request
        url = self.get_url(self.card.id, self.new_owner.id)
        response = self.client.post(url, format='json')
        
        # 3. Assertions
        # The corrected view should return 404 Not Found (or 403 Forbidden)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 
        
        # Check that the owner is unchanged
        self.card.refresh_from_db()
        self.assertEqual(self.card.user, self.owner)

    def test_transfer_failure_unauthenticated(self):
        """Ensure unauthenticated access is denied (handled by IsAuthenticated)."""
        
        # Do not authenticate the client
        
        # 1. Perform the POST request
        url = self.get_url(self.card.id, self.new_owner.id)
        response = self.client.post(url, format='json')
        
        # 2. Assertions
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Check that the owner is unchanged
        self.card.refresh_from_db()
        self.assertEqual(self.card.user, self.owner)

    def test_transfer_failure_card_not_exists(self):
        """Ensure a 404 is returned if the card does not exist."""
        
        self.client.force_authenticate(user=self.owner)
        
        # 1. Perform the POST request with an invalid card ID (e.g., 9999)
        url = self.get_url(9999, self.new_owner.id)
        response = self.client.post(url, format='json')
        
        # 2. Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_transfer_failure_new_owner_not_exists(self):
        """Ensure a 400 is returned if the new owner user does not exist."""
        
        self.client.force_authenticate(user=self.owner)
        
        # 1. Perform the POST request with an invalid new_owner ID (e.g., 9999)
        url = self.get_url(self.card.id, 9999)
        response = self.client.post(url, format='json')
        
        # 2. Assertions
        # The corrected view returns 400 for a bad new owner ID
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LibraryAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # 1. User for the current test
        self.user = User.objects.create_user(username='botanist', password='forest123')

        # 2. Entries already in the user's library (for GET test)
        self.entry1 = Card.objects.create(
            name="Sunflower",
            image="Images/sunflower.jpg",
            location_found="Park",
            description="Yellow flower",
            user=self.user
        )
        self.entry2 = Card.objects.create(
            name="Fern",
            image="Images/fern.jpg",
            location_found="Forest",
            description="Green plant",
            user=self.user
        )

        # 3. Entry to be 'added' (for POST test)
        self.other_user = User.objects.create_user(username='gardener', password='tree456')
        
        # This is the entry that was missing and caused the error
        self.entry_to_add = Card.objects.create( 
             name="Rose",
             image="Images/rose.jpg",
             location_found="Garden Center",
             description="Red flower with thorns",
             user=self.other_user # Linked to another library
        )

    # library/
    def test_get_library_unauthenticated(self):
        """Unauthenticated users should not be able to access the library."""
        response = self.client.get(f"/api/userdata/library/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_library_authenticated(self):
        """Authenticated user should get their own plant library entries."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/userdata/library/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["name"], "Sunflower")
        self.assertEqual(response.data[1]["name"], "Fern")
    
    # library/add-to-library/
    def test_add_to_library_success(self):
        """Should successfully add a new Card to the user's library."""
        # 1. Use self.user for authentication
        self.client.force_authenticate(user=self.user)
        url = '/api/userdata/add-to-library/'
        
        # 2. Use the entry ID we created specifically for this test
        data = {'entry_id': self.entry_to_add.pk} 
        
        # 3. Check the initial state (should not exist in *this* user's library yet)
        initial_count = Card.objects.filter(user=self.user).count()
        self.assertEqual(initial_count, 2)
        
        response = self.client.post(url, data, format='json')
        
        # 4. Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check that a new entry was created and is linked to the correct library
        final_count = Card.objects.filter(user=self.user).count()
        self.assertEqual(final_count, initial_count + 1)
        
        # Optionally, check that the new entry has the expected name
        new_entry = Card.objects.get(user=self.user, name="Rose")
        self.assertEqual(new_entry.name, "Rose")


class GroupAPITests(TestCase):
    def setUp(self):
        self.user_owner = User.objects.create_user(username='owner', password='testpassword')
        self.user_member = User.objects.create_user(username='member', password='testpassword')
        self.user_non_member = User.objects.create_user(username='outsider', password='testpassword')

        # 2. Setup API Clients
        self.owner_client = APIClient()
        self.owner_client.force_authenticate(user=self.user_owner)
        self.member_client = APIClient()
        self.member_client.force_authenticate(user=self.user_member)
        self.non_member_client = APIClient()
        self.non_member_client.force_authenticate(user=self.user_non_member)

        # 3. Create FriendGroup
        self.group1 = FriendGroup.objects.create(
            owner=self.user_owner,
            name='Alpha Group'
        )

        # 4. Create Membership for the Owner (Owner is automatically a member in some setups, but 
        # explicitly creating a membership record ensures consistency and score tracking.)
        FriendGroupMembership.objects.create(
            group=self.group1,
            member=self.user_owner,
            score=100 # Example score
        )
        
        # 5. Create Membership for the Member
        self.group1_membership_member = FriendGroupMembership.objects.create(
            group=self.group1,
            member=self.user_member,
            score=50 # Example score
        )
        
    # <int:friendgroup_id>/
    def test_get_specific_group_success_member(self):
        """Member can view specific group details using the required path parameter."""
        # Using path parameter format (Solution 1 from previous response)
        url = f'/api/userdata/{self.group1.pk}/' 
        response = self.member_client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Alpha Group')

    def test_get_specific_group_forbidden_non_member(self):
        """Non-members should be forbidden from viewing private group details."""
        url = f'/api/userdata/{self.group1.pk}/' 
        response = self.non_member_client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # <int:friendgroup_id>/add-to-group/
    def test_add_to_group_success_creation(self):
        """Owner should successfully add a new user to the group with a custom score."""
        
        # 1. Setup new user to be added
        new_user = User.objects.create_user(username='new_member', password='test')
        url = f'/api/userdata/{self.group1.pk}/add-to-group/' # Adjust URL as needed

        initial_count = FriendGroupMembership.objects.filter(group=self.group1).count()
        
        data = {
            'group_id': self.group1.pk,
            'member_username': new_user.username,
            'score': 75 # Custom score
        }
        
        # Action: Only the owner client can make this request
        response = self.owner_client.post(url, data, format='json')
        
        # 2. Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("added to group", response.data['message'])
        
        # Check that membership count increased
        self.assertEqual(FriendGroupMembership.objects.filter(group=self.group1).count(), initial_count + 1)
        
        # Check that the membership object was created with the correct score
        membership = FriendGroupMembership.objects.get(group=self.group1, member=new_user)
        self.assertEqual(membership.score, 75)
        self.assertTrue(self.group1.members.filter(pk=new_user.pk).exists())
        
    def test_add_to_group_success_update(self):
        """Owner should successfully update an existing member's score."""
        
        url = f'/api/userdata/{self.group1.pk}/add-to-group/' # Adjust URL as needed
        
        # self.user_member has an initial score of 50 from setUp
        initial_score = FriendGroupMembership.objects.get(group=self.group1, member=self.user_member).score
        self.assertEqual(initial_score, 50) # Verify setup

        data = {
            'group_id': self.group1.pk,
            'member_username': self.user_member.username,
            'score': 150 # New score
        }

        # Action: Owner updates the existing member
        response = self.owner_client.post(url, data, format='json')
        
        # 2. Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("score updated in group", response.data['message'])
        
        # Check that the score was updated
        updated_score = FriendGroupMembership.objects.get(group=self.group1, member=self.user_member).score
        self.assertEqual(updated_score, 150)

    def test_add_to_group_permission_failure(self):
        """Non-owner user should be forbidden from adding a member."""
        
        new_user = User.objects.create_user(username='another_user', password='test')
        url = f'/api/userdata/{self.group1.pk}/add-to-group/' # Adjust URL as needed
        
        data = {
            'group_id': self.group1.pk,
            'member_username': new_user.username,
            'score': 10
        }

        # Action: Non-member client attempts to add
        response = self.non_member_client.post(url, data, format='json')
        
        # 2. Assertions
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("Only the group owner can add members", response.data['error'])
        
        # Ensure no membership was created
        self.assertFalse(FriendGroupMembership.objects.filter(group=self.group1, member=new_user).exists())

# global-leaderboard/
class GlobalLeaderboardAPITests(TestCase):
    def setUp(self):
        # Since we are using CustomUser, we pass the score directly
        self.client = APIClient()
        self.url = '/api/userdata/global-leaderboard/' 

        # 1. Create Users WITH SCORES
        self.user_high = User.objects.create_user(
            username='topscorer', 
            password='test', 
            score=500 # FIX: Add score here
        )
        self.user_mid = User.objects.create_user(
            username='middlescore', 
            password='test', 
            score=300 # FIX: Add score here
        )
        self.user_low = User.objects.create_user(
            username='lowscorer', 
            password='test', 
            score=100 # FIX: Add score here
        )

        self.auth_client = APIClient() # Initialize the client
        self.auth_client.force_authenticate(user=self.user_mid)

    def test_get_leaderboard_unauthenticated_fails(self):
        """Unauthenticated users should be denied access (HTTP 403 FORBIDDEN)."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_leaderboard_authenticated_success_and_order(self):
        """Authenticated users should successfully retrieve the leaderboard, ordered by score."""
        response = self.auth_client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))
        self.assertEqual(len(response.data), 3) # Should return all 3 users created

        # 1. Check Ordering: Data must be sorted highest score first (500, 300, 100)
        
        # We assume the serializer includes the 'username' field.
        # Check the username order:
        usernames = [item['username'] for item in response.data]
        self.assertEqual(usernames[0], 'topscorer', "Highest score should be first.")
        self.assertEqual(usernames[1], 'middlescore', "Middle score should be second.")
        self.assertEqual(usernames[2], 'lowscorer', "Lowest score should be third.")
        
        # 2. Check Data Integrity: Verify a specific score is correct
        self.assertEqual(response.data[0]['score'], 500)

# <int:friendgroup_id>/global-group-leaderboard/
# <int:friendgroup_id>/group-spec-leaderboard/
class GroupLeaderboardTests(TestCase):
    def setUp(self):
        # --- 1. Client Setup ---
        # Initialize an unauthenticated client for basic testing
        self.client = APIClient() 
        # Base URL for global leaderboard tests (can be overridden in specific tests)
        self.global_url = '/api/userdata/global-leaderboard/' 
        self.group_global_url = '/api/userdata/global-group-leaderboard/'
        self.group_spec_url = '/api/userdata/group-spec-leaderboard/'

        # --- 2. User Creation (CustomUser with Global Scores) ---
        # User 1: Highest Global Score (Will be the Owner)
        self.user_owner = User.objects.create_user(
            username='owner', 
            password='test', 
            score=300 # Global Score
        )
        
        # User 2: Mid Global Score (Will be a Member)
        self.user_member = User.objects.create_user(
            username='member', 
            password='test', 
            score=500 # Global Score (Higher than owner for test ordering)
        )
        
        # User 3: Lowest Global Score (Will be a Non-Member/Outsider)
        self.user_non_member = User.objects.create_user(
            username='nonmember', 
            password='test', 
            score=100 # Global Score
        )

        # --- 3. Group Creation ---
        self.group1 = FriendGroup.objects.create(
            owner=self.user_owner,
            name='Alpha Group'
        )
        
        # --- 4. Membership Creation (Group-Specific Scores) ---
        # Membership for Owner (Group Score: 100)
        FriendGroupMembership.objects.create(
            group=self.group1,
            member=self.user_owner,
            score=100 # Group-Specific Score (Highest Group Score)
        )
        
        # Membership for Member (Group Score: 50)
        FriendGroupMembership.objects.create(
            group=self.group1,
            member=self.user_member,
            score=50 # Group-Specific Score
        )

        # --- 5. Authenticated Client Setup ---
        # Client authenticated as the Owner
        self.owner_client = APIClient() 
        self.owner_client.force_authenticate(user=self.user_owner) 
        
        # Client authenticated as the Member (used for general access tests)
        self.member_client = APIClient() 
        self.member_client.force_authenticate(user=self.user_member)
        
        # Client authenticated as the Non-Member
        self.non_member_client = APIClient() 
        self.non_member_client.force_authenticate(user=self.user_non_member)

    def test_global_group_leaderboard_success_and_order(self):
        """Authenticated users should retrieve the group leaderboard ordered by GLOBAL score."""
        
        # URL now uses a query parameter: ?group_id=...
        url = f'/api/userdata/{self.group1.pk}/global-group-leaderboard/'
        
        # User scores: Member (500) > Owner (300)
        response = self.member_client.get(url) 

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # The ordering should be by CustomUser.score: Member (500) then Owner (300)
        self.assertEqual(response.data[0]['username'], self.user_member.username)
        self.assertEqual(response.data[0]['score'], 500)
        self.assertEqual(response.data[1]['username'], self.user_owner.username)
        self.assertEqual(response.data[1]['score'], 300)

    def test_global_group_leaderboard_group_not_found(self):
        """Requesting a non-existent group should return 404."""
        non_existent_id = 999
        url = f'/api/userdata/{non_existent_id}/global-group-leaderboard/' 
        
        response = self.member_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_global_group_leaderboard_invalid_id_format(self):
        """Requesting with a non-integer group ID should return 404 NOT FOUND from the URL resolver."""
        # The URL resolver expects <int:friendgroup_id>, 'invalid' will fail to match.
        url = '/api/userdata/invalid/global-group-leaderboard/'
        
        response = self.member_client.get(url)
        
        # Django returns a generic 404 when the URL pattern (requiring an int) isn't matched.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_group_specific_leaderboard_success_and_order(self):
        """Authenticated users should retrieve the group leaderboard ordered by GROUP-SPECIFIC score."""
        
        # URL uses a query parameter: ?group_id=...
        url = f'/api/userdata/{self.group1.pk}/group-spec-leaderboard/'
        
        # Group scores: Owner (100) > Member (50)
        response = self.member_client.get(url) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # The serializer (GroupMembershipLeaderboardSerializer) outputs group_specific data.
        # It should show the Owner (100) then the Member (50).
        
        # The expected output structure is usually nested (e.g., {'member': {'username': '...' }, 'score': 100})
        # Assuming the serializer puts member details under a 'member' key:
        self.assertEqual(response.data[0]['member']['username'], self.user_owner.username)
        self.assertEqual(response.data[0]['score'], 100) # Group score
        self.assertEqual(response.data[1]['member']['username'], self.user_member.username)
        self.assertEqual(response.data[1]['score'], 50) # Group score

    def test_group_specific_leaderboard_group_not_found(self):
        """Requesting a non-existent group should return 404."""
        non_existent_id = 999
        url = f'/api/userdata/{non_existent_id}/group-spec-leaderboard/'
        
        response = self.member_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_group_specific_leaderboard_empty_group(self):
        """Requesting an existing group with no members should return 200 with a message."""
        
        # Create a new, empty group
        empty_group = FriendGroup.objects.create(owner=self.user_owner, name="Empty Group")
        # URL uses path parameter now
        url = f'/api/userdata/{empty_group.pk}/group-spec-leaderboard/'
        
        response = self.member_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Assert against a guaranteed substring
        self.assertIn("has no members", response.data['message'], 
                    msg="The successful message should indicate the group is empty.")