# crate views here.

# teams/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Team, TeamMember
from .serializers import TeamSerializer, TeamMemberSerializer
from core.permissions import IsManager
from activity.utils import log_activity

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all().select_related("manager")
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy", "add_member"]:
            return [IsAuthenticated(), IsManager()]
        return [IsAuthenticated()]

    @action(detail=True, methods=["post"], url_path="members")
    def add_member(self, request, pk=None):
        team = self.get_object()
        serializer = TeamMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tm = serializer.save(team=team)
        log_activity(request.user, "CREATE_TEAM", f"Added {tm.user.username} to {team.name}", project=None)
        return Response(TeamMemberSerializer(tm).data, status=status.HTTP_201_CREATED)
