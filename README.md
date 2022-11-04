CLI tool to generate team report from Jira
==========================================

Installation
------------

    python -m venv venv
    source venv/bin/activate
    python -m pip install -U pip
    python -m pip install -r requirements.txt
    ./jira_query.py --help


Configuration
-------------

To get the Jira token, go to Jira -> your profile -> Personal Access Tokens
and put it into `~/.jira_query.yaml` in `server -> auth -> auth_token`.
Template for the config is in `config.yaml`.


Generate report
---------------

Generate to stdout:

    ./jira_query.py

If template generates MarkDown, convert to HTML like this:

    sudo dnf -y install multimarkdown
    ./jira_query.py | multimarkdown

And also put it into clipboard so you can paste to any office suite editor:

    sudo dnf -y install xclip
    ./jira_query.py | multimarkdown | xclip -sel clip -t "text/html"
