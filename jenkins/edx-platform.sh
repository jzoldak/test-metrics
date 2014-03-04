#!/usr/bin/env bash

virtualenv venv
source ./venv/bin/activate
pip install -r requirements.txt

cat > unit_test_groups.json <<END
{
    "unit.lms": "lms/*.py",
    "unit.studio": "cms/*.py",
    "unit.javascript": "*.js",
    "unit.common_lib": "common/lib/*.py",
    "unit.common_app": "common/djangoapps/*.py"
}
END

cat > acceptance_test_groups.json <<END
{
    "acceptance.lms": "lms/*.py",
    "acceptance.studio": "cms/*.py",
    "acceptance.common_lib": "common/lib/*.py",
    "acceptance.common_app": "common/djangoapps/*.py"
}
END

python -m metrics.coverage unit_test_groups.json `find reports -name "coverage.xml"`
python -m metrics.coverage acceptance_test_groups.json `find reports -name "acceptance_coverage.xml"`
