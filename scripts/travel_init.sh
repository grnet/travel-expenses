#!/bin/sh

CONFIGBASE=/etc/travel
RESOURCES=/usr/lib/travel/resources

cmd () {
    echo " "
    echo "--- $@"
    "$@"
}

cmd travel migrate

cmd travel loaddata "${RESOURCES}/data.json"
cmd travel loadlocations "${RESOURCES}/countriesTZ.csv"
cmd travel loadprojects "${RESOURCES}/ListProjects.csv"
cmd travel loadtaxoffices "${RESOURCES}/ListEfories.csv"
cmd travel migrate collectstatic

echo ' '
