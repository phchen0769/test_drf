import django_filters
from .models import Students


class StudentsFilter(django_filters.FilterSet):
    """
    学生过滤类
    """

    # 根据最小、最大成绩进行过滤
    score_min = django_filters.NumberFilter(field_name="score", lookup_expr="gte")
    score_max = django_filters.NumberFilter(field_name="score", lookup_expr="lte")

    class Meta:
        model = Students
        fields = ["score_min", "score_max"]
