#!/bin/sh

function q() {
    ./jira_query.py --template templates/default-list.md.j2 "$1" \
        | grep -v '^$' \
        | sed 's/^\* /    * /'
    echo
}

(

echo "# Konflux"
echo "* Finished issues"
q 'project in (KONFLUX, KFLUXINFRA, KFLUXBUGS) AND component = Performance AND resolution = Done AND resolved <= now() AND resolved >= startOfDay(-7d)'
echo "* In review issues"
q 'project in (KONFLUX, KFLUXINFRA, KFLUXBUGS) AND component = Performance AND status = Review AND updated <= now() AND updated >= startOfDay(-7d)'
echo "* In progress issues"
q 'project in (KONFLUX, KFLUXINFRA, KFLUXBUGS) AND component = Performance AND type not in (Feature, Outcome) AND status = "In Progress" AND updated <= now() AND updated >= startOfDay(-7d)'
echo "* New issues"
q 'project in (KONFLUX, KFLUXINFRA, KFLUXBUGS) AND component = Performance AND created <= now() AND created >= startOfDay(-7d)'
echo

echo "# RHDH"
echo "* Finished issues"
q 'project = RHIDP AND component = Performance AND resolution = Done AND resolved <= now() AND resolved >= startOfDay(-7d)'
echo "* In review issues"
q 'project = RHIDP AND component = Performance AND status = Review AND updated <= now() AND updated >= startOfDay(-7d)'
echo "* In progress issues"
q 'project = RHIDP AND component = Performance AND type not in (Feature, Outcome) AND status = "In Progress" AND updated <= now() AND updated >= startOfDay(-7d)'
echo "* New issues"
q 'project = RHIDP AND component = Performance AND created <= now() AND created >= startOfDay(-7d)'
echo

echo "# Pipelines"
echo "* Finished issues"
q 'project = SRVKP AND component = Performance AND resolution = Done AND resolved <= now() AND resolved >= startOfDay(-7d)'
echo "* In review issues"
q 'project = SRVKP AND component = Performance AND status in (Review, "Code Review") AND updated <= now() AND updated >= startOfDay(-7d)'
echo "* In progress issues"
q 'project = SRVKP AND component = Performance AND type not in (Feature, Outcome) AND status = "In Progress" AND updated <= now() AND updated >= startOfDay(-7d)'
echo "* New issues"
q 'project = SRVKP AND component = Performance AND created <= now() AND created >= startOfDay(-7d)'
echo

echo "# ConsoleDot"
echo "* Finished issues"
q 'project = HCEPERF AND resolution = Done AND resolved <= now() AND resolved >= startOfDay(-7d)'
echo "* In review issues"
q 'project = HCEPERF AND status in (Review, "Release Pending") AND updated <= now() AND updated >= startOfDay(-7d)'
echo "* In progress issues"
q 'project = HCEPERF AND type not in (Feature, Outcome) AND status = "In Progress" AND updated <= now() AND updated >= startOfDay(-7d)'
echo "* New issues"
q 'project = HCEPERF AND resolution is empty AND created <= now() AND created >= startOfDay(-7d)'
echo

echo "# Satellite"
echo "* Finished issues"
q '((project in (SAT) AND (component = Performance OR labels = Performance)) OR (project in (HCEPERF) AND component in ("RHIN - Image Builder", "RHIN - Provisioning", "RHIN - Pulp", "RHIN - Repositories"))) AND resolution = Done AND resolved <= now() AND resolved >= startOfDay(-7d)'
echo "* In review issues"
q '((project in (SAT) AND (component = Performance OR labels = Performance)) OR (project in (HCEPERF) AND component in ("RHIN - Image Builder", "RHIN - Provisioning", "RHIN - Pulp", "RHIN - Repositories"))) AND status = Review AND updated <= now() AND updated >= startOfDay(-7d)'
echo "* In progress issues"
q '((project in (SAT) AND (component = Performance OR labels = Performance)) OR (project in (HCEPERF) AND component in ("RHIN - Image Builder", "RHIN - Provisioning", "RHIN - Pulp", "RHIN - Repositories"))) AND type not in (Feature, Outcome) AND status = "In Progress" AND updated <= now() AND updated >= startOfDay(-7d)'
echo "* New issues"
q '((project in (SAT) AND (component = Performance OR labels = Performance)) OR (project in (HCEPERF) AND component in ("RHIN - Image Builder", "RHIN - Provisioning", "RHIN - Pulp", "RHIN - Repositories"))) AND created <= now() AND created >= startOfDay(-7d)'
echo

) | tee /tmp/report.md

echo "To copy the output, run: \`(echo '<meta http-equiv=\"content-type\" content=\"text/html; charset=utf-8\">'; cat /tmp/report.md | multimarkdown) | xclip -sel clip -t 'text/html'\`"
