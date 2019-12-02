from django.db import models
from django.http import HttpResponse
from django.shortcuts import render

from django_filters import rest_framework as filters
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

from .models import Tag, Branch
from .serializers import TagWithContextSerializer


def index(request):
    return render(request, "tagtable/index.html")


class TagListResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page-size"
    max_page_size = 50


class IDSearchFilter(filters.ModelMultipleChoiceFilter):
    pass


class TagFilter(filters.FilterSet):
    author = filters.CharFilter(field_name="commits__author_name",
                                lookup_expr="icontains",
                                distinct=True)
    branch = filters.CharFilter(field_name="branch__name",
                                       lookup_expr="icontains")
    order = filters.OrderingFilter(fields={
        ("branch", "branch"),
        ("name", "name"),
        ("dependency1_version", "dependency1_version"),
        ("dependency2_version", "dependency2_version"),
        ("dependency3_version", "dependency3_version"),
        ("release_time", "release_time"),
    })
    # issue_id = IDSearchFilter(quer)

    class Meta:
        model = Tag
        fields = "__all__"
        filter_overrides = {
             models.CharField: {
                 'filter_class': filters.CharFilter,
                 'extra': lambda f: {
                     'lookup_expr': 'icontains',
                 },
             },
        }


class TagList(generics.ListAPIView):
    serializer_class = TagWithContextSerializer
    pagination_class = TagListResultsPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TagFilter

    def get_queryset(self):
        qs = Tag.objects.all()
        issue_id = self.request.query_params.get("issue_id", None)
        if not issue_id:
            return qs
        return (qs.filter(commits__rn_data__issue_id__iexact=issue_id)
                | qs.filter(commits__rn_data__comment__icontains=issue_id)
                | qs.filter(commits__subject__icontains=issue_id)).distinct()


class UploadTag(generics.CreateAPIView):
    serializer_class = TagWithContextSerializer


class FetchTag(generics.RetrieveAPIView):
    serializer_class = TagWithContextSerializer
    queryset = Tag.objects.all()
    lookup_field = "name"


@api_view(["PUT"])
def branch_obsolete(request, name):
    if name.lower() == "trunk":
        return HttpResponse(status=status.HTTP_403_FORBIDDEN)
    try:
        branch = Branch.objects.get(name__iexact=name)
    except Branch.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    branch.obsolete = True
    branch.save()
    return HttpResponse(status=status.HTTP_202_ACCEPTED)


@api_view(["PUT"])
def tag_broken(request, name):
    try:
        tag = Tag.objects.get(name=name)
    except Tag.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    tag.broken = True
    tag.save()
    return HttpResponse(status=status.HTTP_202_ACCEPTED)


@api_view(["PUT"])
def tag_unbroken(request, name):
    try:
        tag = Tag.objects.get(name=name)
    except Tag.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    tag.broken = False
    tag.save()
    return HttpResponse(status=status.HTTP_202_ACCEPTED)
