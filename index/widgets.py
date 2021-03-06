from django.conf import settings
from django.forms.widgets import HiddenInput
from django.forms.extras.widgets import _parse_date_fmt, SelectDateWidget
from django.utils.encoding import force_str
from django.utils import datetime_safe, six
from django.utils.dates import MONTHS
from django.utils.formats import get_format
from django.utils.safestring import mark_safe
import datetime


class DayMonthWidget(SelectDateWidget):

    """ Renders a widget that splits date into two input boxes (for day and month),
    with a hidden field (for year), using a DateField. """

    def render(self, name, value, attrs=None):
        """
        Duplicates SelectDateWidget, creating a hidden field rather than
        a select input for year value.
        """
        try:
            year_val, month_val, day_val = value.year, value.month, value.day
        except AttributeError:
            year_val = month_val = day_val = None
            if isinstance(value, six.string_types):
                if settings.USE_L10N:
                    try:
                        input_format = get_format('DATE_INPUT_FORMATS')[0]
                        v = datetime.datetime.strptime(force_str(value), input_format)
                        year_val, month_val, day_val = v.year, v.month, v.day
                    except ValueError:
                        pass
                else:
                    match = RE_DATE.match(value)
                    if match:
                        year_val, month_val, day_val = [int(v) for v in match.groups()]

        year_html = self.create_hidden(name, self.year_field, '1900')

        choices = list(six.iteritems(MONTHS))
        month_html = self.create_select(name, self.month_field, value, month_val, choices)

        choices = [(i, i) for i in range(1, 32)]
        day_html = self.create_select(name, self.day_field, value, day_val,  choices)

        output = []
        for field in _parse_date_fmt():
            if field == 'year':
                output.append(year_html)
            elif field == 'month':
                output.append(month_html)
            elif field == 'day':
                output.append(day_html)

        return mark_safe('\n'.join(output))

    def value_from_datadict(self, data, files, name):
        """
        Duplicates SelectDateWidget, overriding year value.
        """
        y = data.get(self.year_field % name)
        m = data.get(self.month_field % name)
        d = data.get(self.day_field % name)
        if m == d == "0":
            y = "0"
        if y == m == d == "0":
            return None
        if y and m and d:
            if settings.USE_L10N:
                input_format = get_format('DATE_INPUT_FORMATS')[0]
                try:
                    date_value = datetime.date(int(y), int(m), int(d))
                except ValueError:
                    return '%s-%s-%s' % (y, m, d)
                else:
                    date_value = datetime_safe.new_date(date_value)
                    return date_value.strftime(input_format)
            else:
                return '%s-%s-%s' % (y, m, d)
        return data.get(name, None)

    def create_hidden(self, name, field, val):
        """
        Creates HTML for a hidden input field.
        """
        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name

        local_attrs = self.build_attrs(id=field % id_)

        h = HiddenInput()
        hidden_html = h.render(field % name, val, local_attrs)

        return hidden_html
