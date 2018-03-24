import gettext
import os


dir_path = os.path.dirname(os.path.realpath(__file__))
gettext.bindtextdomain('flongo-filters', dir_path)
gettext.textdomain('flongo-filters')
_ = gettext.gettext

# String  filters
contains_in = _('Contains')
eq_str = _('Coincides')

# String  filters
gt = _('Great than')
lt = _('Less than')
eq_int = _('Equals')
