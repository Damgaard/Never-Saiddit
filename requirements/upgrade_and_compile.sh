pip-compile --output-file local.txt base.in local.in test.in -U
pip-compile --output-file production.txt base.in production.in -U
pip-compile --output-file test.txt base.in test.in -U
