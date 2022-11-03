from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import pagination, viewsets

from ads.models import Ad, Comment
from ads.serializers import AdSerializer, AdDetailSerializer, CommentSerializer
from rest_framework.decorators import action

from ads.permissions import ReadOrCreatePermission, OwnerOrAdminPermissionOne
from rest_framework.permissions import IsAuthenticated

from ads.filter import AdFilter


class AdPagination(pagination.PageNumberPagination):
    page_size = 4


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdFilter
    pagination_class = AdPagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create', 'me']:
            self.permission_classes = [ReadOrCreatePermission]
        else:
            self.permission_classes = [OwnerOrAdminPermissionOne]
        return super(self.__class__, self).get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AdDetailSerializer
        return AdSerializer

    def get_queryset(self):
        if self.action == 'me':
            return Ad.objects.filter(author=self.request.user).all()
        return Ad.objects.all()

    @action(detail=False, methods=['get'])
    def me(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [OwnerOrAdminPermissionOne]
        return super(self.__class__, self).get_permissions()

    def get_queryset(self):
        """
        Это представление должно возвращать список всех комментариев для ad.
        """
        ad = self.kwargs['ad_pk']
        return Comment.objects.filter(ad=ad).all()

    def perform_create(self, serializer):
        ad = self.kwargs['ad_pk']
        serializer.save(author=self.request.user)
        serializer.save(ad_id=ad)

