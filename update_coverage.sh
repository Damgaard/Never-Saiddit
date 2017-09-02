#! /bin/bash

# #################################################################
#
# Created 2 September 2017
# by Andreas Damgaard Pedersen
#
# Update coverage for the project.
#
# The updated coverage is available both as a report which is
# presented at the end of the execution as well as on a webpage.
#
# #################################################################

coverage run manage.py test > /dev/null 2>&1

if [ $? = "0" ]
then
    coverage html && coverage report
    echo
    echo "HTML Report is available at "$PWD"/htmlcov/index.html"
else
    echo "Test suite failed. Plese run py.test to identify the problem"
fi
