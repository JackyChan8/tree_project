from django import template

from menu.models import Item

register = template.Library()


@register.inclusion_tag('menu.html', takes_context=True)
def draw_menu(context, menu):
    try:
        items = Item.objects.filter(menu__title=menu)
        items_values = items.values()
        main_item = [el for el in items_values.filter(parent=None)]

        elem_id = int(context['request'].GET[menu])
        elem_selected = items.get(id=elem_id)
        elements_selected = get_selected(
            elem_selected,
            main_item,
            elem_id
        )

        for item in main_item:
            if item['id'] in elements_selected:
                item['child_items'] = get_child(
                    items_values,
                    item['id'],
                    elements_selected
                )
        result = {'items': main_item}

    except Exception:
        items = Item.objects.filter(menu__title=menu, parent=None)
        result = {
            'items': [item for item in items.values()]
        }

    result['menu'] = menu
    return result


def get_child(items_values: list, parent_id: int, elements_selected: list) -> list:
    """Get Children Elements"""
    items = items_values.filter(
        parent_id=parent_id
    )
    items = [item for item in items]

    for item in items:
        if item['id'] in elements_selected:
            item['child_items'] = get_child(items_values, item['id'], elements_selected)

    return items


def get_selected(parent: int, elements: list, elem_selected: int) -> list:
    """Get Selected Elements"""
    items = []

    print(parent)
    while parent:
        items.append(parent.id)
        parent = parent.parent
    if not items:
        for item in elements:
            if item['id'] == elem_selected:
                items.append(elem_selected)
    return items
