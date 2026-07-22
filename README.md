CLI tool to generate team report from Jira
==========================================

Installation and Running
------------------------

This repository uses [uv](https://github.com/astral-sh/uv) to manage and run the application.

### Ephemeral Run (No Cloning Required)

You can run the CLI tool directly from GitHub without cloning the repository or manually setting up an environment:

    uvx --from git+https://github.com/jhutar/jira_query.git jira-cli --help

### Running in Development (After Cloning)

If you have cloned the repository, you can run the tool in its development environment using:

    uv run jira-cli --help

### System-wide Installation

To install `jira-cli` system-wide into an isolated environment:

    uv tool install git+https://github.com/jhutar/jira_query.git

Or if you have cloned the repository locally:

    uv tool install .


Configuration
-------------

To get the Jira token, go to Jira -> your profile -> Personal Access Tokens
and put it into `~/.jira_query.yaml` in `server -> auth -> auth_token`.
Template for the config is in `config.yaml`.


Generate report
---------------

Generate to stdout:

    jira-cli

If template generates MarkDown, convert to HTML like this:

    sudo dnf -y install multimarkdown
    jira-cli | multimarkdown

And also put it into clipboard so you can paste to any office suite editor:

    sudo dnf -y install xclip
    jira-cli | multimarkdown | xclip -sel clip -t "text/html"
