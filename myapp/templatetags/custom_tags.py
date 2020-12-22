from django import template
from ..models import AllProduct, Category

register = template.Library()


@register.simple_tag
def hello_tag():
    return '<----- Hello Tag ----->'


@register.simple_tag
def show_allproduct():
    count = AllProduct.objects.count()
    return count


@register.inclusion_tag('myapp/allCategory.html')
def all_category():
    cats = Category.objects.all()
    return {'allcats': cats}
