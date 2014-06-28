from rest_framework.permissions import IsAuthenticated


class JustMe(IsAuthenticated):
    """
    Custom permission to allow only user X to edit/view user X
    """

    def has_object_permission(self, request, view, obj):
        return request.method == 'POST' and obj == request.user
