## Bootstrap tenants index

First run

1. Install requirements (use [virtualenv](https://pypi.python.org/pypi/virtualenv))

        $ pip install -r requirements.txt

2. Syncdb with `--noinput` to allow fixtures to create superuser

        $ python manage.py syncdb --noinput

This work is licensed under a [Creative Commons Attribution-ShareAlike 3.0 Unported License](http://creativecommons.org/licenses/by-sa/3.0)
