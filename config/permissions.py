from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    SAFE_METHOD (GET)인 경우 누구나 접근 가능합니다.
    이외의 http method에서 작성자, 관리자 외에는
    게시글에 대한 권한이 없습니다.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            if request.user.is_admin:
                return True
            elif request.user == obj.writer:
                return True
            else:
                return False
