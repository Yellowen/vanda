from django import template

register = template.Library()

def submit_config_row(context):
    """
    Displays the row of buttons for delete and save.
    """
    opts = context['opts']
    change = context['change']
    is_popup = context['is_popup']
    save_as = context['save_as']
    return {
        'onclick_attrib': (opts.get_ordered_objects() and change
                            and 'onclick="submitOrderForm();"' or ''),
        'show_delete_link': False, 
        'show_save_as_new': False, 
        'show_save_and_add_another': False,
        'is_popup': is_popup,
        'show_save': True
    }
submit_config_row = register.inclusion_tag('admin/submit_line.html', takes_context=True)(submit_config_row)    
