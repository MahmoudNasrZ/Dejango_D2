from django.db import models
from decimal import Decimal

class School(models.Model):
    name = models.CharField(max_length=100, unique=True)
    number_of_classes = models.PositiveIntegerField(default=0)
    computed_area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False,
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        """Compute area only when a new value is provided."""
        if hasattr(self, '_temp_area'):
            try:
                length, width = map(Decimal, self._temp_area.lower().split('x'))
                self.computed_area = length * width
            except (ValueError, TypeError):
                raise ValueError("Invalid area format. Please enter 'length x width' (e.g., '5x10').")
        elif self.computed_area is None:
            raise ValueError("Missing area input. Please provide 'length x width' before saving.")

        super().save(*args, **kwargs)

    def set_area(self, area_value):
        """Store the temporary area value without automatically saving."""
        self._temp_area = area_value  # Temporary variable (not stored in DB)

    def __str__(self):
        return f"School: {self.name}, Classes: {self.number_of_classes}, Area: {self.computed_area:.2f} m²"


class Classes(models.Model):
    school = models.ForeignKey("School", on_delete=models.CASCADE, related_name="classes")
    name = models.CharField(verbose_name="Class", max_length=50)
    computed_area = models.DecimalField(
        verbose_name="Computed Area",
        max_digits=10,
        decimal_places=2,
        editable=False,
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        """Compute the area only when a new value is provided."""
        if hasattr(self, '_temp_area'):
            try:
                length, width = map(Decimal, self._temp_area.lower().split('x'))
                self.computed_area = length * width
            except (ValueError, TypeError):
                raise ValueError("Invalid area format. Please enter 'length x width' (e.g., '5x10').")
        elif self.computed_area is None:
            raise ValueError("Missing area input. Please provide 'length x width' before saving.")

        super().save(*args, **kwargs)

    def set_area(self, area_value):
        """Store the temporary area value without automatically saving."""
        self._temp_area = area_value  # Temporary variable (not stored in DB)

    def __str__(self):
        return f"Class: {self.name}, Area: {self.computed_area:.2f} m²"
