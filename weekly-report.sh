#!/bin/sh

# ==========================================
# Team Members - Account IDs
# ==========================================

# Core
JAN_HUTAR="5a78c7f73297605c78217f31"
PRAVIN_SATPUTE="557058:3a905916-e478-4e89-be3c-51726725d067"

# Konflux Team
SUBRATA_MODAK="712020:4f482a8c-9a94-461a-bd49-3776613160f7"
CHARAN_RAJ_MUSALI="712020:ae13c278-02f4-439e-95b2-baa3d2e50049"
ELIJAH_DELEE="5c6d765aca97144c4716967d"

# Pipelines Team
SIDDARDH_R_A="rh-ee-sira"
DEEKSHITH="rh-ee-dbamandl"

# HCE Perf & Scale Team
AMAN_VISHWAKARMA="712020:db9a305a-b86c-4c0e-aa67-5d303b654855"
RAJADITYA_CHAUHAN="712020:742fe929-2f70-4ced-ad2f-464a9ba181a7"
LARRY_RIOS="712020:a9feda78-c87b-49c5-a0e9-ab848545eac0"
KRISHNA_MAGAR="712020:d528a513-118b-4b0a-bb87-71e1dddc40db"
NITIN_MUCHELI="712020:30a67e72-e47d-4a3a-a43d-5e8ff330f707"
VISHAL_VIJAYRAGHAVAN="70121:2d46d1a6-e85d-4221-b1de-03ce32638494"
SHUBHAM_BANSAL="712020:1117cd10-1326-4e0e-841e-a6a13ff6f8b3"

# Satellite Team
PABLO_MENDEZ_HERNANDEZ="rhn-engineering-pablomh"
IMAANPREET_KAUR="70121:843ee2a6-4309-44bf-8ff5-75c4dd1ada07"


# ==========================================
# Teams
# ==========================================

TEAM_KONFLUX="$JAN_HUTAR, $SUBRATA_MODAK, $CHARAN_RAJ_MUSALI, $ELIJAH_DELEE"
TEAM_PIPELINES="$SIDDARDH_R_A, $DEEKSHITH, $PRAVIN_SATPUTE, $JAN_HUTAR"
TEAM_HCEPERF="$AMAN_VISHWAKARMA, $RAJADITYA_CHAUHAN, $LARRY_RIOS, $KRISHNA_MAGAR, $NITIN_MUCHELI, $VISHAL_VIJAYRAGHAVAN, $SHUBHAM_BANSAL, $PRAVIN_SATPUTE, $JAN_HUTAR"
TEAM_SAT="$PRAVIN_SATPUTE, $PABLO_MENDEZ_HERNANDEZ, $IMAANPREET_KAUR, $JAN_HUTAR"

# Combine all for a general filter if needed
TEAM_ALL="$TEAM_KONFLUX, $TEAM_PIPELINES, $TEAM_HCEPERF, $TEAM_SAT"


# ==========================================
# Query Engine
# ==========================================

function q() {
    ./jira_query.py --template templates/default-list.md.j2 "$1" \
        | grep -v '^$' \
        | sed 's/^\* /    * /'
    echo
}

(

echo "# Konflux"
echo "* Finished issues"
q "project in (KONFLUX, KFLUXINFRA, KFLUXBUGS) AND component = Performance AND status CHANGED TO (Closed, Done) AFTER -7d"
echo "* In review issues"
q "project in (KONFLUX, KFLUXINFRA, KFLUXBUGS) AND component = Performance AND status in (Review, 'Code Review') AND status CHANGED TO (Review, 'Code Review') AFTER -7d"
echo "* In progress issues"
q "project in (KONFLUX, KFLUXINFRA, KFLUXBUGS) AND component = Performance AND type not in (Feature, Outcome) AND status = 'In Progress' AND (status CHANGED TO 'In Progress' AFTER -7d OR issuekey IN commented('-7d', 'now', $TEAM_KONFLUX))"
echo "* New issues"
q "project in (KONFLUX, KFLUXINFRA, KFLUXBUGS) AND component = Performance AND created >= -7d AND assignee is not EMPTY AND status not in (Closed, Done)"
echo

echo "# Pipelines"
echo "* Finished issues"
q "project = SRVKP AND component = Performance AND status CHANGED TO (Closed, Done) AFTER -7d"
echo "* In review issues"
q "project = SRVKP AND component = Performance AND status in (Review, 'Code Review') AND status CHANGED TO (Review, 'Code Review') AFTER -7d"
echo "* In progress issues"
q "project = SRVKP AND component = Performance AND type not in (Feature, Outcome) AND status = 'In Progress' AND (status CHANGED TO 'In Progress' AFTER -7d OR issuekey IN commented('-7d', 'now', $TEAM_PIPELINES))"
echo "* New issues"
q "project = SRVKP AND component = Performance AND created >= -7d AND assignee is not EMPTY AND status not in (Closed, Done)"
echo

echo "# ConsoleDot"
echo "* Finished issues"
q "project = HCEPERF AND status CHANGED TO (Closed, Done) AFTER -7d"
echo "* In review issues"
q "project = HCEPERF AND status in (Review, 'Release Pending') AND status CHANGED TO (Review, 'Release Pending') AFTER -7d"
echo "* In progress issues"
q "project = HCEPERF AND type not in (Feature, Outcome) AND status = 'In Progress' AND (status CHANGED TO 'In Progress' AFTER -7d OR issuekey IN commented('-7d', 'now', $TEAM_HCEPERF))"
echo "* New issues"
q "project = HCEPERF AND created >= -7d AND assignee is not EMPTY AND status not in (Closed, Done)"
echo

echo "# Satellite"
echo "* Finished issues"
q "((project in (SAT) AND (component = Performance OR labels = Performance)) OR (project in (HCEPERF) AND component in ('RHIN - Image Builder', 'RHIN - Provisioning', 'RHIN - Pulp', 'RHIN - Repositories'))) AND status CHANGED TO (Closed, Done) AFTER -7d"
echo "* In review issues"
q "((project in (SAT) AND (component = Performance OR labels = Performance)) OR (project in (HCEPERF) AND component in ('RHIN - Image Builder', 'RHIN - Provisioning', 'RHIN - Pulp', 'RHIN - Repositories'))) AND status = Review AND status CHANGED TO Review AFTER -7d"
echo "* In progress issues"
q "((project in (SAT) AND (component = Performance OR labels = Performance)) OR (project in (HCEPERF) AND component in ('RHIN - Image Builder', 'RHIN - Provisioning', 'RHIN - Pulp', 'RHIN - Repositories'))) AND type not in (Feature, Outcome) AND status = 'In Progress' AND (status CHANGED TO 'In Progress' AFTER -7d OR issuekey IN commented('-7d', 'now', $TEAM_SAT))"
echo "* New issues"
q "((project in (SAT) AND (component = Performance OR labels = Performance)) OR (project in (HCEPERF) AND component in ('RHIN - Image Builder', 'RHIN - Provisioning', 'RHIN - Pulp', 'RHIN - Repositories'))) AND created >= -7d AND assignee is not EMPTY AND status not in (Closed, Done)"
echo

) | tee /tmp/report.md

echo "To copy the output, run: \`(echo '<meta http-equiv=\"content-type\" content=\"text/html; charset=utf-8\">'; cat /tmp/report.md | multimarkdown) | xclip -sel clip -t 'text/html'\`"
