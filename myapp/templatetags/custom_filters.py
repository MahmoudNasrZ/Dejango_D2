from django import template

register = template.Library()

@register.filter
def multiply(num1, num2):
    """Multiplies two numbers in a Django template."""
    try:
        return float(num1) * float(num2)
    except (ValueError, TypeError):
        return 0  # Return 0 if there's an error
