from django.db import models

class Report(models.Model):
    report_name = models.CharField(max_length=100)
    report_url = models.URLField()

    def _str_(self):
         return self.report_name