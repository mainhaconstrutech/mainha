from django import template

register = template.Library()


@register.filter(name="find_item")
def find_item(itens_list, id):
    for item in itens_list:
        if item.id == id:
            return item
    return None


@register.filter(name="get_standard_rule_name")
def get_standard_rule_name(item):
    if item is not None:
        return item.name
    return ""


@register.filter(name="get_standard_rule_description")
def get_standard_rule_description(item):
    if item is not None:
        return item.description
    return ""
