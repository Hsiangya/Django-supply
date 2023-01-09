from rest_framework.filters import BaseFilterBackend


class BasicIDFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if not request.user:
            return queryset
        user_id = request.user.get("user_id")
        """存在认证信息时，queryset增加当前用户id查询条件"""
        if user_id:
            return queryset.filter(id=user_id)
        return queryset
