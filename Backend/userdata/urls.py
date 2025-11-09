from django.urls import include, path
from . import views

urlpatterns = [
    # --- Library Management ---
    path('library/', views.get_library, name='get_library'),
    path('add-to-library/', views.add_to_library, name='add_to_library'),
    path('cards/<int:card_id>/transfer/<int:new_owner_id>/', views.card_transaction, name='card-transaction'),
    
    # --- Group Management ---
    path('<int:friendgroup_id>/', views.get_group, name='get_group'),
    path('<int:friendgroup_id>/add-to-group/', views.add_to_group, name='add_to_group'),
    
    # --- Leaderboards ---
    path('global-leaderboard/', views.get_global_leaderboard, name='get_global_leaderboard'),
    path('<int:friendgroup_id>/global-group-leaderboard/', views.get_global_group_leaderboard_view, name='get_global_group_leaderboard'),
    path('<int:friendgroup_id>/group-spec-leaderboard/', views.get_group_specific_leaderboard_view, name='get_group_spec_leaderboard'),
    
    # --- Friendship Manager ---
    path("friendship/", include("friendship.urls"))
    # urls here: https://github.com/revsys/django-friendship/blob/main/friendship/urls.py
    # call them by doing: /api/userdata/friendship/<rest of the path>
]