#!/bin/sh
coverage run --source='amtrak_decal_form/' manage.py test --verbosity=2 && coverage report --show-missing --fail-under=95 --omit="*test*.py" && find amtrak_decal_form -name '*.py' | xargs flake8
