#!/usr/bin/env bash

virtualenv venv
source ./venv/bin/activate
pip install -r requirements.txt

cat > unit_test_groups.json <<END
{
    "lms": "lms/*.py",
    "studio": "cms/*.py",
    "javascript": "*.js",
    "common_lib": "common/lib/*.py",
    "common_app": "common/djangoapps/*.py"
}
END

python -m metrics.coverage unit_test_groups.json `find reports -name "coverage.xml"`
