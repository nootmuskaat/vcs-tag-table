from rest_framework import serializers

from .models import (
        Branch,
        Commit,
        ReleaseNoteData as RND,
        Tag,
)


class RNDSerializer(serializers.ModelSerializer):
    class Meta:
        model = RND
        exclude = ["commit"]


class CommitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commit
        exclude = ["tag"]


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"
        extra_kwargs = {
            "name": {"validators": []},
        }

    def create(self, validated_data):
        Branch.objects.get_or_create(**validated_data)


class TagSerializer(serializers.ModelSerializer):
    branch = BranchSerializer()

    class Meta:
        model = Tag
        fields = "__all__"


class CommitWithRNDSerializer(CommitSerializer):
    rn_data = RNDSerializer(many=True)


class TagWithContextSerializer(TagSerializer):
    """Tag serializer for retrieving a tags full data plus the interfaces of
    its parent tag"""
    commits = CommitWithRNDSerializer(many=True)
    parent = serializers.SerializerMethodField()

    def get_parent(self, obj):
        try:
            parent = Tag.objects.get(name=obj.based_on)
        except Tag.DoesNotExist:
            return {}
        return TagSerializer(parent).data

    def create(self, validated_data):
        commits = validated_data.pop("commits")
        branch_data = validated_data.pop("branch")
        branch = Branch.objects.get_or_create(**branch_data)[0]
        tag = Tag.objects.create(branch=branch,
                                 **validated_data)
        for commit_data in commits:
            rn_data = commit_data.pop("rn_data")
            commit = Commit.objects.create(tag=tag, **commit_data)
            for line in rn_data:
                _ = RND.objects.create(commit=commit, **line)
        return tag
