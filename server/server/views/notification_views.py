from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Notification
from ..serializers.notification_serializers import NotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def unread(self, request):
        unread = self.get_queryset().filter(is_read=False)
        return Response(NotificationSerializer(unread, many=True).data)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'marked as read'})
