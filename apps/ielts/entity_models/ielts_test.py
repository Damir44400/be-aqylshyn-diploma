from django.db import models

from .ielts_sub_module import IeltsSubModule


class IeltsTest(models.Model):
    name = models.CharField(max_length=100)
    sub_model = models.ForeignKey(IeltsSubModule, on_delete=models.CASCADE, related_name='tests')
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='сериялық нөмірі'
    )

    class Meta:
        verbose_name_plural = "Admin | IELTS Tests"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self._state.adding and self.order == 0:
            last_order = IeltsTest.objects.filter(sub_model=self.sub_model).aggregate(models.Max('order'))[
                             'order__max'] or 0
            self.order = last_order + 1
        super().save(*args, **kwargs)
