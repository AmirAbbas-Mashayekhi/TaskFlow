from django.urls import path
from rest_framework_nested import routers
from .views import (
    AssigneeViewSet,
    CommentViewSet,
    InvitationViewSet,
    ParticipantViewSet,
    ProjectViewSet,
    RoleViewSet,
    TaskViewSet,
    TeamMemberViewSet,
    TeamViewSet,
)

router = routers.DefaultRouter()

router.register("participants", ParticipantViewSet, basename="participants")
router.register("teams", TeamViewSet, basename="teams")
router.register("invitations", InvitationViewSet, basename="invitations")
router.register("projects", ProjectViewSet, basename="projects")
router.register("roles", RoleViewSet, basename="roles")
router.register("tasks", TaskViewSet, basename="tasks")


teams_router = routers.NestedDefaultRouter(router, "teams", lookup="teams")
teams_router.register("members", TeamMemberViewSet, basename="members")

tasks_router = routers.NestedDefaultRouter(router, "tasks", lookup="tasks")
tasks_router.register("assignees", AssigneeViewSet, basename="assignees")
tasks_router.register("comments", CommentViewSet, basename="comments")

urlpatterns = router.urls + teams_router.urls + tasks_router.urls

urlpatterns += [
    path(
        "invitations/accept/<uuid:token>/",
        InvitationViewSet.as_view({"get": "accept_invitation"}),
        name="invitation-accept",
    ),
]
