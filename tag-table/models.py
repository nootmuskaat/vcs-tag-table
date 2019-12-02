from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, validate_email


class Branch(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    obsolete = models.BooleanField(default=False)


class Tag(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    broken = models.BooleanField(default=False)
    based_on = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, related_name="tags", on_delete=models.CASCADE)
    dependency1_version = models.CharField(max_length=100)
    dependency2_version = models.CharField(max_length=50)
    dependency3_version = models.CharField(max_length=50)
    release_time = models.DateTimeField()

    class Meta:
        ordering = ["-release_time", "-name"]
        indexes = [
            models.Index(fields=["release_time", "name"]),
        ]


class Commit(models.Model):
    git_hash = models.CharField(max_length=40, primary_key=True,
                                validators=[RegexValidator("^[a-z0-9]{40}$")])
    svn_revision = models.IntegerField(validators=[MinValueValidator(1)])
    subject = models.CharField(max_length=255)
    author_name = models.CharField(max_length=100)
    author_email = models.CharField(max_length=100,
                                    validators=[validate_email])
    author_time = models.DateTimeField()
    committer_name = models.CharField(max_length=100)
    committer_email = models.CharField(max_length=100,
                                       validators=[validate_email])
    committer_time = models.DateTimeField()
    tag = models.ForeignKey(Tag, related_name="commits", on_delete=models.CASCADE)

    class Meta:
        ordering = ["-svn_revision"]
        indexes = [
            models.Index(fields=["tag"]),
        ]


class ReleaseNoteData(models.Model):
    commit = models.ForeignKey(Commit, related_name="rn_data", on_delete=models.CASCADE)
    codes = models.CharField(max_length=10)
    issue_id = models.CharField(max_length=30)
    comment = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["id"]
        indexes = [
            models.Index(fields=["commit"]),
        ]
