from django.db import models

class Link(models.Model):
    url = models.URLField()
    when = models.DateTimeField()

    class Meta:
        ordering = ['when']


    def __str__(self):
        return "%s" % self.url

    def as_dict(self):
        return dict(
            url=self.url,
            when=self.when,
        )


