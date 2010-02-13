__all__ = ('register',)

class AlreadyRegistered(Exception):
    """
    An attempt was made to register a class for setting framework more than once.
    """
    pass

registry = []

def register (class_name ):

    from django.utils.translation import ugettext as _

    # Check whether class registered already or not
    if class_name in registry:
        raise AlreadyRegistered(
            _('The class %s has already been registered.') % class_name.__name__)
    registry.append(class_name)


    
    
