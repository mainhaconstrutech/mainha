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


@register.filter(name="show_report_link")
def show_report_link(status):
    if status in ['archived', 'failed', 'approved']:
        return True
    return False


@register.filter(name="is_password1_field")
def is_password1_field(name):
    if name.find('password1') == -1:
        return False
    return True


@register.filter(name="is_password2_field")
def is_password1_field(name):
    if name.find('password2') == -1:
        return False
    return True
