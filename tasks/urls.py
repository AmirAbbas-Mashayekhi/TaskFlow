from django.urls import path
from rest_framework_nested import routers
from .views import InvitationViewSet, ParticipantViewSet, TeamMemberViewSet, TeamViewSet

router = routers.DefaultRouter()

router.register("participants", ParticipantViewSet, basename="participants")
router.register("teams", TeamViewSet, basename="teams")
router.register("invitations", InvitationViewSet, basename="invitations")

teams_router = routers.NestedDefaultRouter(router, "teams", lookup="teams")
teams_router.register("members", TeamMemberViewSet, basename="members")

urlpatterns = router.urls + teams_router.urls

urlpatterns += [
    path(
        "invitations/accept/<uuid:token>/",
        InvitationViewSet.as_view({"get": "accept_invitation"}),
        name="invitation-accept",
    ),
]
