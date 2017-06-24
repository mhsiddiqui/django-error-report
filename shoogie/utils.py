from django.utils   import encoding
from django.db.models import fields

class TruncateBeginning(unicode):
    "Mark string for truncation at beginning"

def truncate(strval, max_length, at_beginning=None):
    strval = encoding.force_unicode(strval)
    if len(strval) <= max_length:
        return strval
    if at_beginning is None and isinstance(strval, TruncateBeginning):
        at_end = False
    else:
        at_end = not(at_beginning)

    if at_end:
        return strval[:max_length - 3] + u'...'
    else:
        return u'...' + strval[-max_length + 3:]

def clean_data_for_insert(data, model):
    """
    Make sure the data will fit in our fields
    """
    clean_data = {}
    for f in model._meta.local_fields:
        try:
            val = data[f.name]
        except KeyError:
            continue

        if isinstance(f, (fields.CharField, fields.TextField)):
            if val is not None:
                if not isinstance(val, basestring):
                    val = repr(val)
                if f.max_length is not None:
                    val = truncate(val, f.max_length)
        clean_data[f.name] = val
    return clean_data

