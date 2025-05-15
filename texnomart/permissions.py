from rest_framework import permissions

class IsOwnerOfOrder(permissions.BasePermission):
    """
    Faqat buyurtma egasiga ruxsat beradi.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user