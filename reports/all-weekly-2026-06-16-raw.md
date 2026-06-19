# Konflux
## Finished issues

### [Closed/Done] [Task] [KONFLUX-14447](https://redhat.atlassian.net/browse/KONFLUX-14447) - 1sp - Jan Hutar - Probe results investigation, Mon, week of 2026-06-15


**Description:**
```
Goal of this task is to regularry ensure our Konflux Probe runs are running
fine, erros are recognized and reported if it makes sense.

We have the docs and tools, so you can leverage AI agents (tested with Claude Code and Gemini).

h2. Acceptance criteria

* Review probe runs status and report/update issues that were noticed
* Check Jenkins jobs are running fine (see <[https://github.com/konflux-ci/error-pattern-tests/blob/main/docs/procedures/jenkins-stability-runbook.md|https://github.com/konflux-ci/error-pattern-tests/blob/main/docs/procedures/jenkins-stability-runbook.md]>)
* Check performance degradations and overall system health (see <[https://github.com/konflux-ci/error-pattern-tests/blob/main/docs/procedures/system-health-check.md|https://github.com/konflux-ci/error-pattern-tests/blob/main/docs/procedures/system-health-check.md]>)
* Categorize new errors and raise a PR with new error patterns and tests for them and get it merged
* Categorizing unknown errors (see <[https://github.com/konflux-ci/error-pattern-tests/blob/main/docs/procedures/categorize-unknown-errors.md|https://github.com/konflux-ci/error-pattern-tests/blob/main/docs/procedures/categorize-unknown-errors.md]>)
* Adding new rule to recognize unknown error (see <[https://github.com/konflux-ci/error-pattern-tests/blob/main/docs/procedures/add-new-rule.md|https://github.com/konflux-ci/error-pattern-tests/blob/main/docs/procedures/add-new-rule.md]>)
* Let the team know how it went
* If there is something...
```



**Comments:**

#### **Jan Hutar** (2026-06-15)
```
h2. Summary for week of 2026-06-15

h3. Jenkins Jobs Health

31 jobs checked. *Production clusters are healthy* — most jobs run 24/24 successes. Known issues on stone_stg_rh01 and stone_stage_p01 (0/24 successes, persistent release pipeline timeouts) remain unchanged. *_TEST and *_STAGE jobs are experimental and excluded. Only 3 failures and 3 aborts found in recent history — all aborts were manual, all failures categorized as "Other Failure".

h3. System Health

* *Overall error rate stable:* 115 errors today vs. 115/day 7-day average.
* *Overall performance stable:* avg duration 646s today vs. 638s average.
* *One new error appeared today:* "Release Pipeline failed collecting data from github" hit 5 production clusters simultaneously (1 each) — likely a transient GitHub API issue, worth monitoring.
* *Improving trends:* gitlab.cee 429 errors down (11 to 5/day), quay.io pull back-offs down (14 to 7/day), repo templating cleanup timeouts resolved (6.3 to 0/day).
* *Staging clusters ...
```





---
### [Closed/Done] [Task] [KONFLUX-14377](https://redhat.atlassian.net/browse/KONFLUX-14377) - 1sp - Jan Hutar - Linting inventory and CI enforcement verification


**Description:**
```
This task covers the remaining steps from epic KONFLUX-14324:

* *Inventory all existing lint configs:* Enumerate every {{.golangci.yml}}, {{.eslintrc}}, and equivalent across all in-scope repos. Record which repos have none at all.
* *Verify CI can enforce lint gates:* Confirm that all repos' CI pipelines (Tekton, Prow) can run lint checks as a blocking gate, regardless of which specific lint configuration each repo uses.
```



**Comments:**

#### **Jan Hutar** (2026-06-10)
```
We already have linting config (using pre-commit hooks like [fullsend|https://github.com/fullsend-ai/fullsend] does it): [https://github.com/konflux-ci/loadtest/|https://github.com/konflux-ci/loadtest/]

Working on perfscale now: [https://github.com/konflux-ci/perfscale|https://github.com/konflux-ci/perfscale]
```

#### **Jan Hutar** (2026-06-10)
```
h2. What was done

Introduced a complete code quality and CI pipeline for the perfscale repo, modeled on the existing setups in konflux-ci--loadtest and fullsend-ai--fullsend.

h2. New files

* Makefile — bootstrap (installs Python 3.12, pre-commit via uv), check (staged changes), check-all (all files)
* .pre-commit-config.yaml — 18 hooks across 8 repos:
** General: check-yaml, end-of-file-fixer, trailing-whitespace, detect-private-key, check-added-large-files, check-merge-conflict, check-json, check-toml, mixed-line-ending
** YAML: yamllint (relaxed, 120-char line limit)
** Python: ruff lint + ruff format (strict: E/F/I/W/UP/B/SIM rules, line-length 100), bandit (security)
** Secrets: gitleaks
** Shell: shellcheck
** Jsonnet: jsonnetfmt (formatting only; jsonnet-lint removed — requires vendor path unavailable at hook time)
** GitHub Actions: actionlint
** Custom: AGENTS.md size check (<60 lines), grafonnet build verification (fails if built dashboards differ from committed)
* ruff....
```





---
### [Closed/Done] [Task] [KONFLUX-14353](https://redhat.atlassian.net/browse/KONFLUX-14353) - 2sp - Subrata Modak - Investigate remaining violations in resource definitions in repos - build and non-build definitions


**Description:**
```
h3. Overview

This task documents the gap analysis performed on *Jun 9, 2026* across all four Konflux task repositories to identify {{computeResources}} policy violations not yet addressed under [KONFLUX-11509|https://redhat.atlassian.net/browse/KONFLUX-11509]. The findings form the basis for the 19 child tasks created under [KONFLUX-14352|https://redhat.atlassian.net/browse/KONFLUX-14352].

h3. Policy Reminder

||Rule||Requirement||
|{{memory}}|{{requests.memory == limits.memory}} per step|
|{{cpu}}|{{requests.cpu}} set from fleet data (P95 + 5% margin)|
|{{cpu limit}}|*Must NOT be set* (per stakeholder consensus)|
|Floor values|64 MiB memory / 50m CPU when no fleet data|

h3. Violations Found — Jun 9, 2026

h4. {{konflux-ci/build-definitions}}

||Task||YAML||Violation Type||Detail||
|{{build-image-index}} + {{build-image-index-min}}|[link|https://github.com/konflux-ci/build-definitions/tree/main/task/build-image-index]|{{cpu.limit}} set|All steps have CPU limits defined|
|{{fbc-fips-check-matrix-based-oci-ta}}|[link|https://github.com/konflux-ci/build-definitions/tree/main/task/fbc-fips-check-matrix-based-oci-ta]|{{cpu.limit}} set|CPU limits present|
|{{fbc-fips-prepare-oci-ta}}|[link|https://github.com/konflux-ci/build-definitions/tree/main/task/fbc-fips-prepare-oci-ta]|{{cpu.limit}} set|CPU limits present|
|{{git-clone-oci-ta-min}}|[link|https://github.com/konflux-ci/build-definitions/tree/main/task/git-clone-oci-ta-min]|{{cpu.limit}} in kustomize patch|Base task was f...
```



**Comments:**

#### **Subrata Modak** (2026-06-09)
```
h3. Child Tasks Created under [KONFLUX-14352|https://redhat.atlassian.net/browse/KONFLUX-14352]

All 19 child tasks + this meta task have been created on *Jun 9, 2026*.

||Jira||Summary||Repository||Violation Type||
|[KONFLUX-14354|https://redhat.atlassian.net/browse/KONFLUX-14354]|{{build-image-index}} (+min)|[build-definitions|https://github.com/konflux-ci/build-definitions/tree/main/task/build-image-index]|{{cpu.limit}} set on all steps|
|[KONFLUX-14355|https://redhat.atlassian.net/browse/KONFLUX-14355]|{{fbc-fips-check-matrix-based-oci-ta}}|[build-definitions|https://github.com/konflux-ci/build-definitions/tree/main/task/fbc-fips-check-matrix-based-oci-ta]|{{cpu.limit}} set|
|[KONFLUX-14356|https://redhat.atlassian.net/browse/KONFLUX-14356]|{{fbc-fips-prepare-oci-ta}}|[build-definitions|https://github.com/konflux-ci/build-definitions/tree/main/task/fbc-fips-prepare-oci-ta]|{{cpu.limit}} set|
|[KONFLUX-14357|https://redhat.atlassian.net/browse/KONFLUX-14357]|{{git-clone-oci-ta-mi...
```

#### **Subrata Modak** (2026-06-10)
```
Closing this jira/task as the initial investigation to figure out the remaining tasks needed are now available. If new tasks need to be added in future, it can be added to this same parent epic.
```





---
### [Closed/Done] [Epic] [KONFLUX-14324](https://redhat.atlassian.net/browse/KONFLUX-14324) - Jan Hutar - Lint Configuration in every repository


**Description:**
```
Goal here is to implement what parent feature suggests.

h2. Acceptance Criteria

* *Inventory all existing lint configs.* Enumerate every {{.golangci.yml}}, {{.eslintrc}}, and equivalent across all in-scope repos. Record which repos have none at all.

* *-Identify repos with embedded scripts.-* -Audit repositories for scripts embedded in non-standard files (e.g., Tekton task definitions) that standard linters do not currently cover, and determine how to extend lint coverage to those cases.- - we do not have any

* *-Measure current lint-suppression density.-* -Run- {{rg "nolint" --count}} -across the org to establish the baseline- {{nolint}} -density per 1k lines.- - our repos are in {{konflux-ci}} org, so I assume somebody else will do this

* *-Provide recommended configurations.-* -Prepare recommended lint configurations for Go (golangci-lint including gosec, staticcheck, errcheck) and TypeScript (ESLint) that teams can adopt directly or use as a starting point for their own setup.- - we will use what {{fullsend}} uses

* *-Get buy-in from team leads on enforcement.-* -Agree on the approach: every repository must have linting enabled, with teams having flexibility in their specific tool choices and configuration, provided minimum coverage requirements (correctness, standards, static security analysis) are met.- - yes, you have mine buy-in

* *Verify CI can enforce lint gates.* Confirm that all repos' CI pipelines (Tekton, Prow) can run lint checks as a blocking gate, r...
```



**Comments:**

#### **Konflux Bot** (2026-06-09)
```
  * Updating Due Date to 2026-06-30, inherited from parent KONFLUX-12745.

{color:#505f79}See also [konflux.yaml|https://github.com/konflux-ci/prioritize/blob/main/config/konflux.yaml], the [source code|https://github.com/konflux-ci/prioritize], and the [runner|https://gitlab.cee.redhat.com/rbean/jira-automation/-/blob/main/.gitlab-ci.yml] for this bot.{color}

```

#### **Jan Hutar** (2026-06-10)
```
Done, see the child epic.
```





---
### [Closed/Done] [Task] [KONFLUX-14214](https://redhat.atlassian.net/browse/KONFLUX-14214) - 1sp - Jan Hutar - Migrate probe-errors-detector repo to konflux-ci as **internal**


**Description:**
```
Goal here is to make [https://gitlab.cee.redhat.com/jhutar/probe-errors-detector/|https://gitlab.cee.redhat.com/jhutar/probe-errors-detector/] easier to to cooperate on and align it with our other repos.

Original plan was to move content of this repo to {{perfscale}} repo, but that was not approved due to security/privacy concerns caused mostly by log files included in the repo. See full [discussion|https://redhat-internal.slack.com/archives/C08RRAQ3BF1/p1779377893458749].

h2. Acceptance criteria

* Migrate the repo to [https://github.com/konflux-ci|https://github.com/konflux-ci] as *internal* (not public) repo
* Update documentation on other two {{loadtest}} and {{perfscale}} repos
* Run {{agentready}} there and report follow-up tasks in [https://redhat.atlassian.net/browse/KONFLUX-14208|https://redhat.atlassian.net/browse/KONFLUX-14208]
* Possibly create a follow-up tasks for things we did to other two repos in [https://redhat.atlassian.net/browse/KONFLUX-13485|https://redhat.atlassian.net/browse/KONFLUX-13485]
```



**Comments:**

#### **Jan Hutar** (2026-06-15)
```
Migrated as private (in case there are/will be external contributors in this org) to [https://github.com/konflux-ci/error-pattern-tests|https://github.com/konflux-ci/error-pattern-tests].

References in loadtest repo fixed.

Agentready follow-up tasks reported as: KONFLUX-14450, KONFLUX-14451, KONFLUX-14452, KONFLUX-14453, KONFLUX-14454, KONFLUX-14455, KONFLUX-14456, KONFLUX-14457, KONFLUX-14458, KONFLUX-14459, KONFLUX-14460, KONFLUX-14461, KONFLUX-14462, KONFLUX-14463
```





---
### [Closed/Done] [Task] [KONFLUX-13720](https://redhat.atlassian.net/browse/KONFLUX-13720) - Roberto Alfieri - Onboarding: Understand Loadtest architecture and performance testing


**Description:**
```
Research the {{load-test}} tool used by the Performance & Scale team. Understand how it simulates tenant/component load and how it measures system efficiency.

*Key objectives:*

* Understand the codebase and how it interacts with the Konflux API.
* Learn how probe tests and scalability tests are executed.
* Understand how metrics are collected and visualized (Splunk/Grafana).

*Acceptance Criteria:*

* [ ] Can explain the high-level architecture of the Loadtest tool.
* [ ] Able to run a basic load test in the development environment (e.g., {{stone-stg-rh01}}).
* [ ] Familiar with the current build performance KPIs.
```



**Comments:**

#### **Roberto Alfieri** (2026-06-11)
```
*Acceptance Criteria:*

* [x] Can explain the high-level architecture of the Loadtest tool.
** Go CLI with 3-level concurrency (user/app/component goroutines), {{Measure()}} instrumentation wrapping all stages, CSV output analyzed by {{evaluate.py}}, results uploaded to Horreum and visualized in Grafana.
* [x] Able to run a basic load test in the development environment ({{stone-stg-rh01}}).
** Ran probe-like tests (concurrency=1, 1 app, 1 component). Full journey completed including build pipeline and integration tests. Final KPI mean: 352.4s (~5m52s), 0 errors.
* [x] Familiar with the current build performance KPIs.
** KPI mean = sum of all stage durations for a successful journey. KPI errors = count of failed/incomplete journeys. Tracked hourly on 10+ clusters via probe tests. Verified Grafana dashboards showing historical trends per cluster.

*Steps taken to run the test:*

# Cloned the loadtest repo and studied the codebase structure
# Created {{users.json}} with pre-provisione...
```

#### **Jan Hutar** (2026-06-11)
```
Wow, you were able to run the test? Nice!
```

#### **Roberto Alfieri** (2026-06-11)
```
[~accountid:5a78c7f73297605c78217f31] yeah! 🙂 a lot of {{trial and error}} but it worked in the end. It was really useful to understand how the tool works!
```





---
### [Closed/Won't Do] [Task] [KONFLUX-13065](https://redhat.atlassian.net/browse/KONFLUX-13065) - 2sp - Subrata Modak - Implement proper compute resources for task 'update-infra-deployments'


**Description:**
```
h2. Process: computeResources for build-definitions tasks (approval draft)

This document proposes a standard workflow for child issues under epic [KONFLUX-11509|https://redhat.atlassian.net/browse/KONFLUX-11509]: set *memory requests = memory limits* per step, and *CPU requests only* (omit CPU limits unless policy explicitly changes). Sizing uses fleet metrics from the tasks-and-steps-resource-analyzer.

h3. Goals

* Memory: requests.memory = limits.memory for each step that defines memory.
* CPU: requests.cpu set from analysis; do not set limits.cpu (align with stakeholder guidance and common Kubernetes practice).
* Use real Konflux usage data (e.g. 15-day window) rather than legacy static defaults.

h3. Before you start

* Confirm the task lives in [build-definitions task/|https://github.com/konflux-ci/build-definitions/tree/main/task]. If CODEOWNERS or team practice points to another repo (e.g. konflux-sast-tasks, konflux-test-tasks, konflux-operator-tasks), file work there instead.
* Identify source-of-truth YAML: many *-oci-ta tasks are generated from a base Task + recipe via {{hack/generate-ta-tasks.sh}}. Prefer editing the base task and regenerating rather than hand-editing generated oci-ta YAML.
* CI: committed *-oci-ta YAML must match generator output (*Check Trusted Artifact variants*). Avoid manual drift on injected steps.

h3. Step 1 — Cluster connectivity

From your development machine, ensure kubeconfig/VPN access to the Konflux clusters used for metrics col...
```



**Comments:**

#### **Subrata Modak** (2026-06-10)
```
h3. PR #3577 Closed as WON'T DO — Jun 10, 2026

[PR #3577|https://github.com/konflux-ci/build-definitions/pull/3577] has been closed after an investigation triggered by a reviewer comment from {{@chmeliik}}.

*Root cause:* The {{analyze_resource_limits.py}} tool was run against the {{build-definitions}} YAML:

{noformat}./analyze_resource_limits.py --file https://github.com/konflux-ci/build-definitions/blob/main/task/update-infra-deployments/0.1/update-infra-deployments.yaml --analyze-again --margin 5 --days 60 --pll-clusters 4 --pll-queries 4{noformat}

However, the tool's Prometheus queries search by task name ({{update-infra-deployments}}) across all clusters and cannot distinguish which repo/bundle a task was loaded from. The 47 pod executions collected were actually from the {{release-service-catalog}} version ([tasks/managed/update-infra-deployments/update-infra-deployments.yaml|https://github.com/konflux-ci/release-service-catalog/blob/development/tasks/managed/update-infra-d...
```




**Linked Pull Requests & Merge Requests**

#### PR/MR: https://github.com/konflux-ci/build-definitions/pull/3405
```
Title: feat(ta): set 4Gi memory request/limit for use-trusted-artifact step
The create-trusted-artifact step already sets a 3Gi limit via the generator code. Apply similar resource limits to the use-trusted-artifact step to ensure consistent memory allocation.

The -min variant patches remove the explicit computeResources so those tasks inherit the smaller stepTemplate defaults instead.

Related: https://github.com/konflux-ci/konflux-sast-tasks/pull/103
```

#### PR/MR: https://github.com/konflux-ci/build-definitions/pull/3577
```
Title: feat(update-infra-deployments): add computeResources to all steps
## Summary

Adds `computeResources` (memory request = limit, CPU request only) to all
5 steps in `update-infra-deployments/0.1`, in compliance with the Konflux
resource policy.

### Fleet analysis

| Variant | Clusters with data | Pod executions | Window |
|---|---|---|---|
| `update-infra-deployments` | 3 / 12 | 47 | up to 9.4 days |

All observed steps showed P95 memory ≤ 1 MB and P95 CPU = 0m.
Two steps (`race-condition-update-check`, `create-mr`) had no observability
data at all. Floor values (64Mi / 50m) are applied throughout.
Full analysis: [KONFLUX-13065](https://redhat.atlassian.net/browse/KONFLUX-13065).

### Changes

| Step | Memory req=limit | CPU request | Rationale |
|---|---|---|---|
| `race-condition-update-check` | 64Mi | 50m | No observability data |
| `git-clone-infra-deployments` | 64Mi | 50m | Floor (P95 = 0 MB) |
| `run-update-script` | 64Mi | 50m | Floor (P95 = 1 MB) |
| `get-diff-files` ...
```



---
### [Closed/Done] [Task] [KONFLUX-13058](https://redhat.atlassian.net/browse/KONFLUX-13058) - 2sp - Subrata Modak - Implement proper compute resources for task 'slack-webhook-notification'


**Description:**
```
h2. Process: computeResources for build-definitions tasks (approval draft)

This document proposes a standard workflow for child issues under epic [KONFLUX-11509|https://redhat.atlassian.net/browse/KONFLUX-11509]: set *memory requests = memory limits* per step, and *CPU requests only* (omit CPU limits unless policy explicitly changes). Sizing uses fleet metrics from the tasks-and-steps-resource-analyzer.

h3. Goals

* Memory: requests.memory = limits.memory for each step that defines memory.
* CPU: requests.cpu set from analysis; do not set limits.cpu (align with stakeholder guidance and common Kubernetes practice).
* Use real Konflux usage data (e.g. 15-day window) rather than legacy static defaults.

h3. Before you start

* Confirm the task lives in [build-definitions task/|https://github.com/konflux-ci/build-definitions/tree/main/task]. If CODEOWNERS or team practice points to another repo (e.g. konflux-sast-tasks, konflux-test-tasks, konflux-operator-tasks), file work there instead.
* Identify source-of-truth YAML: many *-oci-ta tasks are generated from a base Task + recipe via {{hack/generate-ta-tasks.sh}}. Prefer editing the base task and regenerating rather than hand-editing generated oci-ta YAML.
* CI: committed *-oci-ta YAML must match generator output (*Check Trusted Artifact variants*). Avoid manual drift on injected steps.

h3. Step 1 — Cluster connectivity

From your development machine, ensure kubeconfig/VPN access to the Konflux clusters used for metrics col...
```



**Comments:**

#### **Subrata Modak** (2026-06-10)
```
CLOSING this jira/task as PR: [https://github.com/konflux-ci/build-definitions/pull/3562|https://github.com/konflux-ci/build-definitions/pull/3562|smart-link] has been merged to ‘main’ branch.
```




**Linked Pull Requests & Merge Requests**

#### PR/MR: https://github.com/konflux-ci/build-definitions/pull/3562
```
Title: feat(slack-webhook-notification): add computeResources to send-message
## Summary

Adds `computeResources` to the `send-message` step in `slack-webhook-notification/0.1`, which had no resource definitions, and regenerates `slack-webhook-notification-oci-ta/0.1` accordingly.

### Changes

| Step | Before | After |
|------|--------|-------|
| `send-message` | not set | `memory: 64Mi` req=limit, `cpu: 50m` req, no cpu limit |

### Sizing rationale

Fleet analysis over a 60-day window:

| Variant | Clusters with data | Pod executions | mem_max | mem_p95 |
|---|---|---|---|---|
| `slack-webhook-notification` (base) | 3 of 12 | 65 | 3 MB | 1 MB |
| `slack-webhook-notification-oci-ta` | 0 of 12 | 0 | — | — |

The `send-message` step makes a simple HTTP POST to a Slack webhook. Observed memory max is 3 MB across all clusters — well within the 64Mi floor value. Floor values (`memory: 64Mi`, `cpu: 50m`) are used for consistency with other low-traffic tasks in this series.

### Policy

...
```

#### PR/MR: https://github.com/konflux-ci/build-definitions/pull/3405
```
Title: feat(ta): set 4Gi memory request/limit for use-trusted-artifact step
The create-trusted-artifact step already sets a 3Gi limit via the generator code. Apply similar resource limits to the use-trusted-artifact step to ensure consistent memory allocation.

The -min variant patches remove the explicit computeResources so those tasks inherit the smaller stepTemplate defaults instead.

Related: https://github.com/konflux-ci/konflux-sast-tasks/pull/103
```



---
### [Closed/Done] [Task] [KONFLUX-13042](https://redhat.atlassian.net/browse/KONFLUX-13042) - 2sp - Subrata Modak - Implement proper compute resources for task 'ko-oci-ta'


**Description:**
```
h2. Process: computeResources for build-definitions tasks (approval draft)

This document proposes a standard workflow for child issues under epic [KONFLUX-11509|https://redhat.atlassian.net/browse/KONFLUX-11509]: set *memory requests = memory limits* per step, and *CPU requests only* (omit CPU limits unless policy explicitly changes). Sizing uses fleet metrics from the tasks-and-steps-resource-analyzer.

h3. Goals

* Memory: requests.memory = limits.memory for each step that defines memory.
* CPU: requests.cpu set from analysis; do not set limits.cpu (align with stakeholder guidance and common Kubernetes practice).
* Use real Konflux usage data (e.g. 15-day window) rather than legacy static defaults.

h3. Before you start

* Confirm the task lives in [build-definitions task/|https://github.com/konflux-ci/build-definitions/tree/main/task]. If CODEOWNERS or team practice points to another repo (e.g. konflux-sast-tasks, konflux-test-tasks, konflux-operator-tasks), file work there instead.
* Identify source-of-truth YAML: many *-oci-ta tasks are generated from a base Task + recipe via {{hack/generate-ta-tasks.sh}}. Prefer editing the base task and regenerating rather than hand-editing generated oci-ta YAML.
* CI: committed *-oci-ta YAML must match generator output (*Check Trusted Artifact variants*). Avoid manual drift on injected steps.

h3. Step 1 — Cluster connectivity

From your development machine, ensure kubeconfig/VPN access to the Konflux clusters used for metrics col...
```



**Comments:**

#### **Subrata Modak** (2026-06-10)
```
CLOSING this jira/task as PR: [https://github.com/konflux-ci/build-definitions/pull/3563|https://github.com/konflux-ci/build-definitions/pull/3563|smart-link] has been merged to ‘main’ branch.
```




**Linked Pull Requests & Merge Requests**

#### PR/MR: https://github.com/konflux-ci/build-definitions/pull/3563
```
Title: fix(ko-oci-ta): enforce compute resource policy across all steps
## What

Fixes compute resource policy violations in `task/ko-oci-ta/0.1/ko-oci-ta.yaml`.

## Changes

| Step | Before | After | Reason |
|------|--------|-------|--------|
| `stepTemplate` | mem req 1Gi, limit 4Gi | mem req **4Gi**, limit 4Gi | `request ≠ limit` violation; aligning req to existing limit |
| `use-trusted-artifact` | inherits stepTemplate (4Gi) | **64Mi** req = limit, **50m** cpu | Lightweight step (~5 MB observed); explicit override prevents over-scheduling |
| `build` | inherits stepTemplate (4Gi / cpu 1) | **4Gi** req = limit, **cpu 3** | Go compilation is memory- and CPU-intensive; 4Gi covers p95+ observed usage; cpu 3 covers p95 with ~12% headroom |
| `prepare-sbom` | mem req 256Mi, limit 512Mi | mem req **512Mi**, limit 512Mi | `request ≠ limit` violation; aligning req to existing limit |
| `upload-sbom` | mem req 256Mi, limit 512Mi | mem req **512Mi**, limit 512Mi | Same as `prepare-sbom` ...
```

#### PR/MR: https://github.com/konflux-ci/build-definitions/pull/3405
```
Title: feat(ta): set 4Gi memory request/limit for use-trusted-artifact step
The create-trusted-artifact step already sets a 3Gi limit via the generator code. Apply similar resource limits to the use-trusted-artifact step to ensure consistent memory allocation.

The -min variant patches remove the explicit computeResources so those tasks inherit the smaller stepTemplate defaults instead.

Related: https://github.com/konflux-ci/konflux-sast-tasks/pull/103
```



---
### [Closed/Obsolete] [Task] [KONFLUX-12496](https://redhat.atlassian.net/browse/KONFLUX-12496) - 8sp -  - Phase 6: Execute Production "Game Day" (Rebuild All)


**Description:**
```
h3. Goal

Rebuild all components in all tenants on all clusters to validate the 24-hour SLO compliance.

h3. Acceptance Criteria

* Verify all preventative action items from Phase 5 are completed and deployed.
* Coordinate the "Game Day" execution with all stakeholders and tenant engineering groups.
* Execute the "Rebuild All" operation across all production clusters.
* Monitor system health and controller stability continuously during the event.
* Generate a comprehensive post-event report detailing performance, issues encountered, and overall success against the 24-hour SLO.
```



**Comments:**

#### **Jan Hutar** (2026-06-11)
```
Given the discussion outcomes on WG call yesterday (see parent epic [comment|https://redhat.atlassian.net/browse/KONFLUX-10069?focusedCommentId=17248888] for details), this is no longer needed.
```





---
### [Closed/Obsolete] [Task] [KONFLUX-12495](https://redhat.atlassian.net/browse/KONFLUX-12495) - 3sp -  - Phase 5: Project outcomes and identify action items for Production Game Day


**Description:**
```
h3. Goal

Based on the simulation and small-scale tests, estimate the possible outcomes of a full "Game Day" and present them to stakeholders. Identify action items for components that are projected to fail or be too slow.

h3. Acceptance Criteria

* Extrapolate data from Phase 2 and Phase 4 to estimate the impact of a full production "Game Day".
* Identify specific components or infrastructure elements (e.g., storage drivers, etcd, specific controllers) likely to fail or degrade under full load.
* Create a list of actionable items or preventative fixes required before executing the Production Game Day.
* Present the projections, risks, and action items to stakeholders for review and approval.
```



**Comments:**

#### **Jan Hutar** (2026-06-11)
```
Given the discussion outcomes on WG call yesterday (see parent epic [comment|https://redhat.atlassian.net/browse/KONFLUX-10069?focusedCommentId=17248888] for details), this is no longer needed.
```





---
### [Closed/Obsolete] [Task] [KONFLUX-12494](https://redhat.atlassian.net/browse/KONFLUX-12494) - 5sp -  - Phase 4: Execute small-scale "Rebuild All" test on a single namespace


**Description:**
```
h3. Goal

Trigger a wave of builds for a given namespace and evaluate the results and system behavior to identify what went wrong.

h3. Acceptance Criteria

* Select a representative namespace/tenant for the initial test.
* Execute the "Rebuild All" process (developed in Phase 3) for the selected namespace.
* Gather and analyze performance metrics and logs during the execution.
* Identify and document any errors, bottlenecks, or areas for improvement.
* Create a post-mortem report summarizing the findings of the small-scale test.
```



**Comments:**

#### **Jan Hutar** (2026-06-11)
```
Given the discussion outcomes on WG call yesterday (see parent epic [comment|https://redhat.atlassian.net/browse/KONFLUX-10069?focusedCommentId=17248888] for details), this is no longer needed.
```





---
### [Closed/Obsolete] [Task] [KONFLUX-12493](https://redhat.atlassian.net/browse/KONFLUX-12493) - 3sp -  - Phase 3: Develop process for triggering tenant-level "Rebuild All"


**Description:**
```
h3. Goal

Develop a process to trigger and evaluate a "Rebuild All" for a single tenant or cluster, involving the relevant tenant engineering groups.

h3. Acceptance Criteria

* Define a standard operating procedure (SOP) or create an automated script to safely trigger a rebuild of all components for a specific tenant.
* Establish a communication and coordination plan to notify and involve tenant engineering groups.
* Define the criteria and specific metrics for evaluating the success or failure of the tenant-level rebuild (against the 24-hour SLO).
* Document the process in the team's knowledge base.
```



**Comments:**

#### **Jan Hutar** (2026-06-11)
```
Given the discussion outcomes on WG call yesterday (see parent epic [comment|https://redhat.atlassian.net/browse/KONFLUX-10069?focusedCommentId=17248888] for details), this is no longer needed.
```





---
### [Closed/Done] [Task] [KONFLUX-12492](https://redhat.atlassian.net/browse/KONFLUX-12492) - 5sp - Jan Hutar - Phase 2: Simulate "Rebuild All" build storm in staging


**Description:**
```
h3. Goal

Reuse our existing goals around RHEL and Fedora on Konflux (e.g., from KONFLUX-11106) to run a storm of builds, all under our control. These should be real builds, but using controlled components rather than real-world customer components.

h3. Acceptance Criteria

* Create or configure a staging environment that mimics production cluster configurations.
* Execute a build storm using controlled components.
* Monitor and record system metrics (e.g., API server load, etcd performance, controller queues, MPC performance) during the simulation.
* Document any bottlenecks, rate limits (e.g., GitLab/Quay 429 errors), or failures encountered during the simulation.
```



**Comments:**

#### **Jan Hutar** (2026-06-09)
```
Results with [loadtest|https://github.com/konflux-ci/loadtest/] repo: [https://docs.google.com/document/d/1fwAMrZLpCOvlGHkGONA56-bB9XoRGD_g7ysLbE5oUtw/edit?tab=t.0#heading=h.xvh5rmmrt70h|https://docs.google.com/document/d/1fwAMrZLpCOvlGHkGONA56-bB9XoRGD_g7ysLbE5oUtw/edit?tab=t.0#heading=h.xvh5rmmrt70h]
```

#### **Jan Hutar** (2026-06-11)
```
Given all the results linked from previous comments, I consider this done.
```





---
### [Closed/Obsolete] [Epic] [KONFLUX-11480](https://redhat.atlassian.net/browse/KONFLUX-11480) - Jan Hutar - KubeArchive scale testing


**Description:**
```
Project docs: https://kubearchive.github.io/kubearchive/

Testing doc: https://docs.google.com/document/d/1jU0Incj7GeRahng6LdRRBYVR6qC9KO1g53UYsQ8QqBw/edit?tab=t.0
```



**Comments:**

#### **Jan Hutar** (2026-06-11)
```
Hello [~accountid:712020:182a04df-7253-4133-abd1-809a9c034c9f]. I was not able to force myself to work on this systematically so decided to close it, but if there is a need for this test, please let me know and I can re-open and re-prioritize.

On a related note, we (thanks Charan!) currently have 3k tenants in {{stone-stg-rh01}} and based on Konflux web UI, KubeArchive still stands :) For other testing I also ran 100 concurrent builds there recently and looks fine. Charan plans to run up to 1k concurrent builds there as part of [KONFLUX-14323|https://redhat.atlassian.net/browse/KONFLUX-14323]. That effort is not dedicated to KubeArchive, but Charan reviews restart counts so I guess he would notice if something is wrong with KA.
```





---
### [Closed/Obsolete] [Task] [KONFLUX-9556](https://redhat.atlassian.net/browse/KONFLUX-9556) - Jan Hutar - test if KubeArchive can survive on a cluster with 2k tenants


**Description:**
```
Consider testing this on a RHEL cluster together with RHEL scale test.

h3. Acceptance criteria
* Check KA works on a cluster with 2k+ tenants
* Check I can run a test with up to 500 concurrent users
```



**Comments:**

#### **Jan Hutar** (2026-06-11)
```
Closing with [https://redhat.atlassian.net/browse/KONFLUX-11480?focusedCommentId=17250153|https://redhat.atlassian.net/browse/KONFLUX-11480?focusedCommentId=17250153]
```





---
### [Closed/Obsolete] [Task] [KONFLUX-9555](https://redhat.atlassian.net/browse/KONFLUX-9555) - 3sp - Jan Hutar - test if KubeArchive can survive on a cluster with 1k tenants


**Description:**
```
Consider testing this on a RHEL cluster together with RHEL scale test.

Keep an eye on these metrics:

{code}
sum(container_memory_working_set_bytes{container!="", namespace=~"(product-kubearchive|product-kubearchive-logging|knative-eventing|openshift-kube-apiserver|openshift-apiserver|openshift-etcd)"}) by (namespace)
{code}

{code}
sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{namespace=~"(product-kubearchive|product-kubearchive-logging|knative-eventing|openshift-kube-apiserver|openshift-apiserver|openshift-etcd)"}) by (namespace)
{code}

{code}
avg(etcd_mvcc_db_total_size_in_use_in_bytes)
avg(etcd_mvcc_db_total_size_in_bytes)
{code}

h3. Acceptance criteria
* Check KA works on a cluster with 1k+ tenants
* Check I can run a test with up to 500 concurrent users
```



**Comments:**

#### **Jan Hutar** (2026-06-11)
```
Closing with [https://redhat.atlassian.net/browse/KONFLUX-11480?focusedCommentId=17250153|https://redhat.atlassian.net/browse/KONFLUX-11480?focusedCommentId=17250153]
```




**Linked Pull Requests & Merge Requests**

#### PR/MR: https://gitlab.cee.redhat.com/releng/konflux-release-data/-/merge_requests/11981
```
Title: feat(KONFLUX-9555): Adding more namespaces 3
#### What:
Adding more namespaces (301-400).

#### Why:
To be able to test KONFLUX-9555.

#### Tickets:
KONFLUX-9555
```

#### PR/MR: https://gitlab.cee.redhat.com/releng/konflux-release-data/-/merge_requests/11941
```
Title: feat(KONFLUX-9555): Adding more namespaces 1
#### What:
Adding more namespaces.

#### Why:
To be able to test KONFLUX-9555.

#### Tickets:
KONFLUX-9555
```

#### PR/MR: https://gitlab.cee.redhat.com/releng/konflux-release-data/-/merge_requests/11976
```
Title: feat(KONFLUX-9555): Adding more namespaces 2
#### What:
Adding more namespaces (201-300).

#### Why:
To be able to test KONFLUX-9555.

#### Tickets:
KONFLUX-9555
```



---
## In review issues

### [Review] [Sub-task] [KONFLUX-14339](https://redhat.atlassian.net/browse/KONFLUX-14339) - Charan Raj Musali - Add `imagePullPolicy: IfNotPresent` to the stepTemplate in Task YAMLs in rpmbuild-pipeline


**Description:**
```
During a recent test that ran 200 RPM build pipelines concurrently on the stg-rh01 cluster, 9 builds failed with a {{TaskRunImagePullFailed}} error.

While reviewing the image references in the {{rpmbuild-pipeline}} repository, I noticed that most images are specified with both the {{latest}} tag and a fixed image digest. Even though Kubernetes pulls the image using the digest, the {{latest}} tag causes the image pull policy to be automatically set to {{Always}}. This means the image is downloaded for every pipeline run, even if the same image already exists on the node.

Removing the {{latest}} tag and relying on the image digest alone can reduce unnecessary image pulls, which should help lower the number of image pull failures and improve the overall stability and scalability of the cluster.

Apply these changes to the {{rpmbuild-pipeline}} repositories in both GitHub and GitLab.
```






---
### [Review] [Sub-task] [KONFLUX-14338](https://redhat.atlassian.net/browse/KONFLUX-14338) - Charan Raj Musali - Use rpmbuild-pipeline parameters "self-ref-url" and "self-ref-revision" to pin Tekton Git-resolved task references to commit hashes in RPM build pipelines


**Description:**
```
Previous testing showed that using branch names for Git-resolved Tekton tasks caused a high failure rate (around 50–60%). Using a specific commit SHA instead makes task resolution much more reliable when applied consistently across all pipeline and task references. Using commit SHAs also helps Tekton scale better. Since a commit SHA never changes, Tekton can cache previously resolved pipelines and tasks and reuse them for future requests instead of repeatedly fetching content from Git.

The RoK team recently updated the {{rpmbuild-pipeline}} and added parameters that allow commit SHA values to be passed to the {{revision}} field at runtime.

This change updates the performance tooling to use those parameters and pin Tekton Git-resolved task references to commit hashes in RPM build pipelines,
improving both reliability and scalability.
```






---
### [Review] [Story] [KONFLUX-14323](https://redhat.atlassian.net/browse/KONFLUX-14323) - 5sp - Charan Raj Musali - Apply validated fixes and trigger 500–1,000 builds with throttling to confirm Konflux handles backlog at scale.


**Description:**
```
We created JIRA tickets for all the issues identified during the RPM build concurrency tests. For several of these issues, the Pipelines team has provided recommended fixes and mitigations. These recommendations have already been tested and validated in a simplified environment that closely matches production, although the actual RPM build pipelines were not run on the Konflux cluster during that validation.

The goal of this task is to implement those fixes in the pipeline and rerun the concurrency tests with 500–1,000 simultaneous builds and verify that Konflux can effectively manage and process large build backlogs at scale.
```



**Comments:**

#### **Elijah DeLee** (2026-06-15)
```
Test is done, now reviewing results, charan will update soon
```





---
## In progress issues

### [In Progress] [Task] [KONFLUX-14441](https://redhat.atlassian.net/browse/KONFLUX-14441) - Carlos Esteban Feria Vila - Learning Konflux concept and key technologies high level intro


**Description:**
```
Learning Konflux Concept and Its Key Technologies High Level Intro

Welcome to the non-technical learning path that aims to introduce you to Konflux, its concept and program overview. Besides obtaining a solid understanding of what is the Konflux premise, you'll have a chance to watch a nicely prepared demo as well get a high level introduction to the technologies that were identified as key for Konflux, which are further covered by the other learning paths.

*Goal:* Go through courses defined in [Learning Konflux Concept and Its Key Technologies High Level Intro|https://source.redhat.com/departments/products_and_global_engineering/portfolio_and_delivery/pd_wiki/learning_konflux_concept_and_its_key_technologies_high_level_intro]

*Acceptance Criteria:*

* Completed the high-level intro course.
* Understand the basic concept of Konflux and its key technologies.
```






---
### [In Progress] [Task] [KONFLUX-14375](https://redhat.atlassian.net/browse/KONFLUX-14375) - 3sp - Jan Hutar - Resolve release pipelines not starting on staging clusters after ClusterRole binding change


**Description:**
```
h2. Problem

Release pipelines are not starting on staging clusters ({{stone-stg-rh01}}, {{stone-stage-p01}}) since around 2026-06-08. Root cause identified by Francesco: [infra-deployments PR #12201|https://github.com/redhat-appstudio/infra-deployments/pull/12201] changed ClusterRole bindings for {{konflux-bot-*}} SAs. The release-service tries to create a RoleBinding for SA {{konflux-bot-0}} and ClusterRole {{release-pipeline-resource-role}} but fails.

See [KONFLUX-14374|https://redhat.atlassian.net/browse/KONFLUX-14374] for the original bug report and details.

h2. Links

* Bug: [KONFLUX-14374|https://redhat.atlassian.net/browse/KONFLUX-14374]
* Causing PR: [infra-deployments #12201|https://github.com/redhat-appstudio/infra-deployments/pull/12201]
* Slack discussion: [#forum-konflux-perf|https://redhat-internal.slack.com/archives/C02CTEB3MMF/p1781072128218249]

h2. Expected outcome

Release pipelines should start on staging clusters.
```



**Comments:**

#### **Jan Hutar** (2026-06-11)
```
This is quite complicated to me, so I asked this in the Slack thread:

+Purpose of loadtest runs:+ To exercise as much of Konflux codebase as possible in a happy path end-to-end user-like scenario. And to measure duration of every stage to see a performance trend.

+What we have now:+ We create both RP and RPA in {{konflux-perfscale-1-tenant}} and we use {{konflux-bot-0}} SA [permissions configured in [here|https://gitlab.cee.redhat.com/releng/konflux-release-data/-/blob/main/staging/tenants-config/cluster/stone-stg-rh01/tenants/konflux-perfscale-1-tenant/konflux-bot-0.yaml?ref_type=heads] (make it admin) and [here|https://github.com/redhat-appstudio/infra-deployments/blob/main/components/perf-team-prometheus-reader/base/tenants-rbac/konflux-perfscale-1-tenant/tenant-rbac.yaml] (just allow collecting events)] and [e2e|https://github.com/konflux-ci/release-service-catalog/tree/development/pipelines/managed/e2e] pipeline. And we are measuring these:

* {{createReleasePlan}} - how long...
```

#### **Jan Hutar** (2026-06-15)
```
Created this PR to help us to get permissiong to read managed release pipeline runs: [https://github.com/redhat-appstudio/infra-deployments/pull/12372|https://github.com/redhat-appstudio/infra-deployments/pull/12372]
```

#### **Jan Hutar** (2026-06-16)
```
OK, after some more thinking and more discussion on Slack, decided to go with dedicated managed namespace: [https://gitlab.cee.redhat.com/releng/konflux-release-data/-/merge_requests/19106|https://gitlab.cee.redhat.com/releng/konflux-release-data/-/merge_requests/19106]
```




**Linked Pull Requests & Merge Requests**

#### PR/MR: https://github.com/redhat-appstudio/infra-deployments/pull/12201
```
Title: bind konflux-bot-* SA to allowed ClusterRoles only
We want to prevent users from binding `konflux-bot-*` to anything different from the Konflux provided ClusterRoles.

The proposed policy denies the creation of new RoleBindings that would bind the `konflux-bot-*` ServiceAccount to a not allowed ClusterRole.
It also denies binding the ServiceAccount by updating a RoleBinding.

For backward compatibility, already existing invalid RoleBinding are tolerated.
In a future effort they'll be remediated.

Signed-off-by: Francesco Ilario <filario@redhat.com>
Assisted-by: Cursor
```

#### PR/MR: https://gitlab.cee.redhat.com/releng/konflux-release-data/-/merge_requests/19106
```
Title: Add managed-konflux-perfscale-tenant on staging clusters stone-stage-p01 and stone-stg-rh01
#### What:
Adding "managed" namespace for release pipelines from probe runs on staging clusters stone-stage-p01 and stone-stg-rh01.

#### Why:
To be able to manage our own RPAs.

#### Tickets:
https://redhat.atlassian.net/browse/KONFLUX-14375
```

#### PR/MR: https://github.com/redhat-appstudio/infra-deployments/pull/12372
```
Title: KONFLUX-14375 Add perf-team SA for reading releases in managed-release-team-tenant
## What

Add ServiceAccount, Role, and RoleBinding for the perf team to read
pipeline resources in the `managed-release-team-tenant` namespace.

Clusters affected: development, staging

[KONFLUX-14375](https://issues.redhat.com/browse/KONFLUX-14375)

## Why

Loadtest needs to collect manifests and logs from the
managed-release-team-tenant namespace.

## Validation

- `kustomize build components/perf-team-prometheus-reader/development/` passes
- `kustomize build components/perf-team-prometheus-reader/staging/base/` passes
- `kustomize build components/perf-team-prometheus-reader/production/base/` passes (unaffected)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

[KONFLUX-14375]: https://redhat.atlassian.net/browse/KONFLUX-14375?atlOrigin=eyJpIjoiNWRkNTljNzYxNjVmNDY3MDlhMDU5Y2ZhYzA5YTRkZjUiLCJwIjoiZ2l0aHViLWNvbS1KU1cifQ
```



---
### [In Progress] [Task] [KONFLUX-14329](https://redhat.atlassian.net/browse/KONFLUX-14329) - Gajanan Kakade - Learning Konflux Concept and Its Key Technologies High Level Intro


**Description:**
```
Learning Konflux Concept and Its Key Technologies High Level Intro

Welcome to the non-technical learning path that aims to introduce you to Konflux, its concept and program overview. Besides obtaining a solid understanding of what is the Konflux premise, you'll have a chance to watch a nicely prepared demo as well get a high level introduction to the technologies that were identified as key for Konflux, which are further covered by the other learning paths.

*Goal:* Go through courses defined in [Learning Konflux Concept and Its Key Technologies High Level Intro|https://source.redhat.com/departments/products_and_global_engineering/portfolio_and_delivery/pd_wiki/learning_konflux_concept_and_its_key_technologies_high_level_intro]

*Acceptance Criteria:*

* Completed the high-level intro course.
* Understand the basic concept of Konflux and its key technologies.
```






---
## New issues

### [New] [Story] [KONFLUX-14449](https://redhat.atlassian.net/browse/KONFLUX-14449) - Charan Raj Musali - Use MintMaker Re-enablement Activity to Measure Konflux Cluster Performance Under Heavy Load


**Description:**
```
This gives us a good opportunity to better understand how the Konflux cluster behaves under heavy load, especially clusters with a large number of Components. In our recent tests, we observed peak concurrency of around 125 builds, so this should help us evaluate performance at even higher levels of concurrency.

{quote}stone-prd-rh01. [components.appstudio.redhat.com|http://components.appstudio.redhat.com] 5148
kflux-prd-rh02. [components.appstudio.redhat.com|http://components.appstudio.redhat.com] 1568
kflux-prd-rh03. [components.appstudio.redhat.com|http://components.appstudio.redhat.com] 961
stone-prod-p02. [components.appstudio.redhat.com|http://components.appstudio.redhat.com] 8308
stone-prod-p01. [components.appstudio.redhat.com|http://components.appstudio.redhat.com] 37
kflux-ocp-p01. [components.appstudio.redhat.com|http://components.appstudio.redhat.com] 5651
kflux-rhel-p01 [components.appstudio.redhat.com|http://components.appstudio.redhat.com] 7.88k
kflux-osp-p01. [components.appstudio.redhat.com|http://components.appstudio.redhat.com] 1.19k
stone-stage-p01. [components.appstudio.redhat.com|http://components.appstudio.redhat.com] 76
stone-stg-rh01. [components.appstudio.redhat.com|http://components.appstudio.redhat.com] 3.98k, about 3K of it are created with empty GitHub repositories and are onboarded without ArgoCD{quote}



Recently, we ran performance tests after updating the pipeline definition based on recommendations from the Pipelines team. We executed 20...
```






---
### [New] [Task] [KONFLUX-14448](https://redhat.atlassian.net/browse/KONFLUX-14448) - 1sp - Charan Raj Musali - Probe results investigation, Wed, week of 2026-06-15


**Description:**
```
Goal of this task is to regularly ensure our Konflux Probe runs are running
fine, errors are recognized and reported if it makes sense.

We have the docs and tools, so you can leverage AI agents (tested with Claude Code and Gemini).

* Main docs on probe runs: <[https://docs.google.com/document/d/1lIWwBXeBxlyHkucNJu__NrAsPtRMgoPGjf_0EbHUhcs/edit?tab=t.0|https://docs.google.com/document/d/1lIWwBXeBxlyHkucNJu__NrAsPtRMgoPGjf_0EbHUhcs/edit?tab=t.0]>
* Overview video on probe runs: <[https://drive.google.com/file/d/1yh3bIlIxl-ITXiT6Tb4844toyNH5HhoG/view?usp=sharing|https://drive.google.com/file/d/1yh3bIlIxl-ITXiT6Tb4844toyNH5HhoG/view?usp=sharing]>
* Recording of a review process: <[https://drive.google.com/file/d/1ZNZOhqAVlP-gf_wCHNrQB7AiTeLRH_wp/view?usp=sharing|https://drive.google.com/file/d/1ZNZOhqAVlP-gf_wCHNrQB7AiTeLRH_wp/view?usp=sharing]>

h2. Acceptance criteria

* Review probe runs status and report/update issues that were noticed
* Check Jenkins jobs are running fine (see <[https://github.com/konflux-ci/error-pattern-tests/blob/main/docs/procedures/jenkins-stability-runbook.md|https://github.com/konflux-ci/error-pattern-tests/blob/main/docs/procedures/jenkins-stability-runbook.md]>)
* Check performance degradations and overall system health (see <[https://github.com/konflux-ci/error-pattern-tests/blob/main/docs/procedures/system-health-check.md|https://github.com/konflux-ci/error-pattern-tests/blob/main/docs/procedures/system-health-check.md]>)
* Categorize new err...
```






---
### [New] [Task] [KONFLUX-14443](https://redhat.atlassian.net/browse/KONFLUX-14443) - Carlos Esteban Feria Vila - Understand Loadtest architecture and performance testing


**Description:**
```
Research the {{load-test}} tool used by the Performance & Scale team. Understand how it simulates tenant/component load and how it measures system efficiency.

*Key objectives:*

* Understand the codebase and how it interacts with the Konflux API.
* Learn how probe tests and scalability tests are executed.
* Understand how metrics are collected and visualized (Splunk/Grafana).

*Acceptance Criteria:*

* [ ] Can explain the high-level architecture of the Loadtest tool.
* [ ] Able to run a basic load test in the development environment (e.g., {{stone-stg-rh01}}).
* [ ] Familiar with the current build performance KPIs.
```






---
### [New] [Task] [KONFLUX-14442](https://redhat.atlassian.net/browse/KONFLUX-14442) - Carlos Esteban Feria Vila - Hands-on learning with Konflux main usage


**Description:**
```
Follow the official Konflux [Hands-on learning guide|https://konflux.pages.redhat.com/docs/users/getting-started/hands-on-learning.html] to gain practical experience with the platform.

*Key objectives:*

* Set up a workspace and configure source code repositories.
* Onboard a sample application and create components.
* Understand the automated build and release pipeline flow.
* Trigger a build and verify the promotion through environments.

*Acceptance Criteria:*

* Successfully completed the "Hands-on learning" guide.
* Can demonstrate a successful build and release of a sample component.
* Understands the basic terminology (Workspace, Component, PipelineRun, Release).
```






---
### [In Progress] [Task] [KONFLUX-14441](https://redhat.atlassian.net/browse/KONFLUX-14441) - Carlos Esteban Feria Vila - Learning Konflux concept and key technologies high level intro


**Description:**
```
Learning Konflux Concept and Its Key Technologies High Level Intro

Welcome to the non-technical learning path that aims to introduce you to Konflux, its concept and program overview. Besides obtaining a solid understanding of what is the Konflux premise, you'll have a chance to watch a nicely prepared demo as well get a high level introduction to the technologies that were identified as key for Konflux, which are further covered by the other learning paths.

*Goal:* Go through courses defined in [Learning Konflux Concept and Its Key Technologies High Level Intro|https://source.redhat.com/departments/products_and_global_engineering/portfolio_and_delivery/pd_wiki/learning_konflux_concept_and_its_key_technologies_high_level_intro]

*Acceptance Criteria:*

* Completed the high-level intro course.
* Understand the basic concept of Konflux and its key technologies.
```






---
### [Refinement] [Task] [KONFLUX-14431](https://redhat.atlassian.net/browse/KONFLUX-14431) - 2sp - Jan Hutar - Plan ArgoCD work


**Description:**
```
Goal here is to plan ArgoCD/GitOps perf&scale work as outlined in Pradeep's gdoc: https://docs.google.com/document/d/1AmimOO1N562bk1T34Zgmf6EzzuCrHnPdGbFXHV6hVyE

Pradeep discussing details and will let me know when I should go ahead with this task.

```






---
### [Refinement] [Task] [KONFLUX-14430](https://redhat.atlassian.net/browse/KONFLUX-14430) - 2sp - Jan Hutar - Plan TPA work


**Description:**
```
Goal here is to plan perf&scale work around TPA as requested in [https://redhat.atlassian.net/browse/TC-4634|https://redhat.atlassian.net/browse/TC-4634]
```






---
### [In Progress] [Task] [KONFLUX-14375](https://redhat.atlassian.net/browse/KONFLUX-14375) - 3sp - Jan Hutar - Resolve release pipelines not starting on staging clusters after ClusterRole binding change


**Description:**
```
h2. Problem

Release pipelines are not starting on staging clusters ({{stone-stg-rh01}}, {{stone-stage-p01}}) since around 2026-06-08. Root cause identified by Francesco: [infra-deployments PR #12201|https://github.com/redhat-appstudio/infra-deployments/pull/12201] changed ClusterRole bindings for {{konflux-bot-*}} SAs. The release-service tries to create a RoleBinding for SA {{konflux-bot-0}} and ClusterRole {{release-pipeline-resource-role}} but fails.

See [KONFLUX-14374|https://redhat.atlassian.net/browse/KONFLUX-14374] for the original bug report and details.

h2. Links

* Bug: [KONFLUX-14374|https://redhat.atlassian.net/browse/KONFLUX-14374]
* Causing PR: [infra-deployments #12201|https://github.com/redhat-appstudio/infra-deployments/pull/12201]
* Slack discussion: [#forum-konflux-perf|https://redhat-internal.slack.com/archives/C02CTEB3MMF/p1781072128218249]

h2. Expected outcome

Release pipelines should start on staging clusters.
```



**Comments:**

#### **Jan Hutar** (2026-06-11)
```
This is quite complicated to me, so I asked this in the Slack thread:

+Purpose of loadtest runs:+ To exercise as much of Konflux codebase as possible in a happy path end-to-end user-like scenario. And to measure duration of every stage to see a performance trend.

+What we have now:+ We create both RP and RPA in {{konflux-perfscale-1-tenant}} and we use {{konflux-bot-0}} SA [permissions configured in [here|https://gitlab.cee.redhat.com/releng/konflux-release-data/-/blob/main/staging/tenants-config/cluster/stone-stg-rh01/tenants/konflux-perfscale-1-tenant/konflux-bot-0.yaml?ref_type=heads] (make it admin) and [here|https://github.com/redhat-appstudio/infra-deployments/blob/main/components/perf-team-prometheus-reader/base/tenants-rbac/konflux-perfscale-1-tenant/tenant-rbac.yaml] (just allow collecting events)] and [e2e|https://github.com/konflux-ci/release-service-catalog/tree/development/pipelines/managed/e2e] pipeline. And we are measuring these:

* {{createReleasePlan}} - how long...
```

#### **Jan Hutar** (2026-06-15)
```
Created this PR to help us to get permissiong to read managed release pipeline runs: [https://github.com/redhat-appstudio/infra-deployments/pull/12372|https://github.com/redhat-appstudio/infra-deployments/pull/12372]
```

#### **Jan Hutar** (2026-06-16)
```
OK, after some more thinking and more discussion on Slack, decided to go with dedicated managed namespace: [https://gitlab.cee.redhat.com/releng/konflux-release-data/-/merge_requests/19106|https://gitlab.cee.redhat.com/releng/konflux-release-data/-/merge_requests/19106]
```




**Linked Pull Requests & Merge Requests**

#### PR/MR: https://github.com/redhat-appstudio/infra-deployments/pull/12201
```
Title: bind konflux-bot-* SA to allowed ClusterRoles only
We want to prevent users from binding `konflux-bot-*` to anything different from the Konflux provided ClusterRoles.

The proposed policy denies the creation of new RoleBindings that would bind the `konflux-bot-*` ServiceAccount to a not allowed ClusterRole.
It also denies binding the ServiceAccount by updating a RoleBinding.

For backward compatibility, already existing invalid RoleBinding are tolerated.
In a future effort they'll be remediated.

Signed-off-by: Francesco Ilario <filario@redhat.com>
Assisted-by: Cursor
```

#### PR/MR: https://gitlab.cee.redhat.com/releng/konflux-release-data/-/merge_requests/19106
```
Title: Add managed-konflux-perfscale-tenant on staging clusters stone-stage-p01 and stone-stg-rh01
#### What:
Adding "managed" namespace for release pipelines from probe runs on staging clusters stone-stage-p01 and stone-stg-rh01.

#### Why:
To be able to manage our own RPAs.

#### Tickets:
https://redhat.atlassian.net/browse/KONFLUX-14375
```

#### PR/MR: https://github.com/redhat-appstudio/infra-deployments/pull/12372
```
Title: KONFLUX-14375 Add perf-team SA for reading releases in managed-release-team-tenant
## What

Add ServiceAccount, Role, and RoleBinding for the perf team to read
pipeline resources in the `managed-release-team-tenant` namespace.

Clusters affected: development, staging

[KONFLUX-14375](https://issues.redhat.com/browse/KONFLUX-14375)

## Why

Loadtest needs to collect manifests and logs from the
managed-release-team-tenant namespace.

## Validation

- `kustomize build components/perf-team-prometheus-reader/development/` passes
- `kustomize build components/perf-team-prometheus-reader/staging/base/` passes
- `kustomize build components/perf-team-prometheus-reader/production/base/` passes (unaffected)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

[KONFLUX-14375]: https://redhat.atlassian.net/browse/KONFLUX-14375?atlOrigin=eyJpIjoiNWRkNTljNzYxNjVmNDY3MDlhMDU5Y2ZhYzA5YTRkZjUiLCJwIjoiZ2l0aHViLWNvbS1KU1cifQ
```



---
### [New] [Sub-task] [KONFLUX-14341](https://redhat.atlassian.net/browse/KONFLUX-14341) - Charan Raj Musali - Use this task to try to reproduce bug KONFLUX-14159 and collect more detailed SSH logs.


**Description:**
```
Add the required changes to the {{rpmbuild-pipeline}} to collect more detailed SSH logs.
```






---
### [Review] [Sub-task] [KONFLUX-14339](https://redhat.atlassian.net/browse/KONFLUX-14339) - Charan Raj Musali - Add `imagePullPolicy: IfNotPresent` to the stepTemplate in Task YAMLs in rpmbuild-pipeline


**Description:**
```
During a recent test that ran 200 RPM build pipelines concurrently on the stg-rh01 cluster, 9 builds failed with a {{TaskRunImagePullFailed}} error.

While reviewing the image references in the {{rpmbuild-pipeline}} repository, I noticed that most images are specified with both the {{latest}} tag and a fixed image digest. Even though Kubernetes pulls the image using the digest, the {{latest}} tag causes the image pull policy to be automatically set to {{Always}}. This means the image is downloaded for every pipeline run, even if the same image already exists on the node.

Removing the {{latest}} tag and relying on the image digest alone can reduce unnecessary image pulls, which should help lower the number of image pull failures and improve the overall stability and scalability of the cluster.

Apply these changes to the {{rpmbuild-pipeline}} repositories in both GitHub and GitLab.
```






---
### [Review] [Sub-task] [KONFLUX-14338](https://redhat.atlassian.net/browse/KONFLUX-14338) - Charan Raj Musali - Use rpmbuild-pipeline parameters "self-ref-url" and "self-ref-revision" to pin Tekton Git-resolved task references to commit hashes in RPM build pipelines


**Description:**
```
Previous testing showed that using branch names for Git-resolved Tekton tasks caused a high failure rate (around 50–60%). Using a specific commit SHA instead makes task resolution much more reliable when applied consistently across all pipeline and task references. Using commit SHAs also helps Tekton scale better. Since a commit SHA never changes, Tekton can cache previously resolved pipelines and tasks and reuse them for future requests instead of repeatedly fetching content from Git.

The RoK team recently updated the {{rpmbuild-pipeline}} and added parameters that allow commit SHA values to be passed to the {{revision}} field at runtime.

This change updates the performance tooling to use those parameters and pin Tekton Git-resolved task references to commit hashes in RPM build pipelines,
improving both reliability and scalability.
```






---


# Pipelines
## Finished issues

### [Closed/Done] [Spike] [SRVKP-12325](https://redhat.atlassian.net/browse/SRVKP-12325) - 1sp - Aman Vishwakarma - Analyze one test vs separate tests per scenario/config for Horreum alert thresholds


**Description:**
```
Analyze whether to keep the current single-Horreum-test approach or split into separate tests per scenario/config combination (e.g., separate tests for math-HA-QBT,
  math-no-HA, signing-HA-QBT, etc.) to determine the best structure for configuring alert thresholds.

  Context:

* Currently we have 2 Horreum tests: scalingPipelines (math) and Chains signing (signing-tr-tekton-bigbang)
* Each test uses fingerprint labels to separate HA/QBT config combos into independent time series
* JS calculation functions (like missing_pipeline_successes) handle per-config threshold branching within a single test
```



**Comments:**

#### **Aman Vishwakarma** (2026-06-09)
```
Analyzed splitting into separate Horreum tests per config combo (8+ tests) versus keeping the current 2-test setup with JS branching.
Recommendation: keep a single test per scenario category. Splitting would require over 720 duplicate label definitions and changes to the data upload pipeline, while JS branching on HA/QBT involves only 4 branches—the same pattern as the {{existing missing_pipeline_successes}} function. Separate tests become necessary only if different configs require different alert models or notifications
```





---
### [Closed/Done] [Task] [SRVKP-12152](https://redhat.atlassian.net/browse/SRVKP-12152) - 2sp - Aman Vishwakarma - Familiarize yourself with Results test we have so far


**Description:**
```
Review and understand the existing Results Controller performance test suite to build foundational knowledge before contributing to new CPT scenarios.

*Objectives:*

* Identify and catalog all existing Results Controller test cases and their coverage areas.
* Understand the test framework, tooling, and infrastructure used for running Results performance tests.
* Analyze the current test scenarios to identify patterns, gaps, and areas for improvement.
* Document key findings, including test structure, configurations, and any dependencies.

*Acceptance Criteria:*

* All existing Results Controller tests have been reviewed and understood.
* A summary of the current test coverage, including what scenarios are tested
```



**Comments:**

#### **Aman Vishwakarma** (2026-06-09)
```
Currently exploring and getting familiar with the existing Results Controller test suite.Documenting things as I go - [https://docs.google.com/document/d/13NJiEXVMxWnmrUsTgeDzwK1_SUyUMFU31-2HiWlbG6I/edit?usp=sharing|https://docs.google.com/document/d/13NJiEXVMxWnmrUsTgeDzwK1_SUyUMFU31-2HiWlbG6I/edit?usp=sharing|smart-link]
```

#### **Aman Vishwakarma** (2026-06-16)
```
Now I have clear idea about how results controller works and even I checked the one result test we have
```





---
### [Closed/Done] [Task] [SRVKP-12049](https://redhat.atlassian.net/browse/SRVKP-12049) - 2sp - Deekshith Kumar Netha Bamandla N - Identify the test scenarios for Results Controllers







---
### [Closed/Done] [Task] [SRVKP-11996](https://redhat.atlassian.net/browse/SRVKP-11996) - 1sp - Siddardh R A - Generate a KB article




**Comments:**

#### **Jan Hutar** (2026-06-16)
```
Article was published.
```





---
## In review issues

### [Code Review] [Task] [SRVKP-12412](https://redhat.atlassian.net/browse/SRVKP-12412) - 2sp - Deekshith Kumar Netha Bamandla N - Add Results watcher ingestion latency metrics to CPT


**Description:**
```
The existing {{timebased-sign-pruner}} performance test captures per-run Results annotation timestamps ({{result_at}}, {{log_at}}) in {{benchmark-output.json}} via {{benchmark.py}}, but {{stats.sh}} never computes summary statistics for them.

{{stats.sh}} already does this for Chains signing metrics. We need the equivalent for Results watcher ingestion:

*Acceptance Criteria:*

* Computes Results ingestion latency (min/avg/max) and throughput for both PipelineRuns and TaskRuns
* Metrics are written to {{benchmark-tekton.json}} and available for Horreum/ResultsDashboard upload
```



**Comments:**

#### **Jan Hutar** (2026-06-16)
```
+Status report:+ Deekshith created the change and Siddardh is reviewing it now. Will merge after review is done.
```





---
## In progress issues

### [In Progress] [Task] [SRVKP-12192](https://redhat.atlassian.net/browse/SRVKP-12192) - 3sp - Aman Vishwakarma - Configure alert thresholds and establish hard-coded upper and lower bounds for metric alerts


**Description:**
```
We will be fixing this to fixed threshold.
```



**Comments:**

#### **Aman Vishwakarma** (2026-06-09)
```
Analysis completed:

* Queried 6,600+ historical runs from Horreum PostgreSQL across 8 active scenario+config combos
* Computed MIN/AVG/MAX for all resource metrics (controller CPU/memory, webhook CPU/memory, workqueue depth, etcd, cluster CPU)
* Calculated MAX/AVG ratios to determine natural variance per metric (ranges 1.3x-1.7x)

Documented with Horreum Labels and data tables with suggested upper bounds can be accessed using [https://docs.google.com/document/d/1ghrSQMdD2vrKPVCm8UBEz1o8BqpX312309cIscqyutk/edit?usp=sharing|https://docs.google.com/document/d/1ghrSQMdD2vrKPVCm8UBEz1o8BqpX312309cIscqyutk/edit?usp=sharing|smart-link]
```

#### **Aman Vishwakarma** (2026-06-12)
```
Earlier, the query results I shared did not include the controller_type dimension, so deployments and statefulSets results were combined. I've now rerun all queries with controller_type separated (deployments vs statefulSets).

What's in the sheet:
[https://docs.google.com/spreadsheets/d/1BD05rHbnuuBnxg8r6tgx2tRt_spHgSFpp1Cur4_sXek/edit?usp=sharing|https://docs.google.com/spreadsheets/d/1BD05rHbnuuBnxg8r6tgx2tRt_spHgSFpp1Cur4_sXek/edit?usp=sharing|smart-link]

The updated Excel sheet covers all 8 metric categories with per-scenario breakdowns:

* Controller CPU & Memory
* Webhook CPU & Memory
* Controller Workqueue Depth
* Etcd DB Size & Request Duration
* Cluster CPU Usage

Each row breaks down by scenario, HA config, QBT config, and controller type — with Min, Avg, Max, Max/Avg Ratio, and Suggested Upper Bound columns.

How the upper bounds are calculated:
Suggested upper = ((max/avg ratio) - 0.1) × avg
This sets the threshold just below the observed max.
```

#### **Jan Hutar** (2026-06-12)
```
Cool, nice Aman! I guess rest of the metrics will come later? I think we should not try to do all of them at one go.
```

#### **Aman Vishwakarma** (2026-06-16)
```
Added JS calculation function for each variable for per-scenario thresholds based on HA,QBT and controller_type covering 5 combinations per metric
```

#### **Aman Vishwakarma** (2026-06-16)
```
Updated success/failure count thresholds:

* PipelineRuns Succeeded: min=1000 (removed max bound), added JS function with per-scenario minimums to handle HA+QBT expected lower counts
* TaskRuns Succeeded: min=4000 (removed max bound), added JS function with per-scenario minimums
* Removed failure count thresholds (redundant — success count thresholds already catch the same regressions)
```

#### **Aman Vishwakarma** (2026-06-16)
```
Configuration applied and recalculated for last 24hrs test runs to validate new thresholds
```

#### **Aman Vishwakarma** (2026-06-16)
```
Even I have PR with modified changes for review
[https://github.com/openshift-pipelines/performance/pull/104|https://github.com/openshift-pipelines/performance/pull/104|smart-link]
```




**Linked Pull Requests & Merge Requests**

#### PR/MR: https://github.com/openshift-pipelines/performance/pull/104
```
Title: Add fixed-threshold change detection groups for pipelines metrics
## Summary

Adds fixed-threshold change detection groups (CDGs) to `horreum_pipeline_fields.yaml` for key Pipelines scaling test metrics, and wires Horreum fields to those groups so regressions are flagged when values exceed established baselines.

This extends Horreum alerting beyond relative-difference checks (duration, restarts) with absolute max thresholds for controller/webhook resource usage, etcd health, cluster CPU, and workqueue depth.

### New change detection groups

| Group | Metric | Max threshold |
|---|---|---|
| `controller_cpu` | tekton-pipelines-controller CPU (mean) | 1.16 cores |
| `controller_memory` | tekton-pipelines-controller memory (mean) | 7,059,328,204 bytes |
| `webhook_cpu` | tekton-pipelines-webhook CPU (mean) | 0.35 cores |
| `webhook_memory` | tekton-pipelines-webhook memory (mean) | 365,953,024 bytes |
| `workque_depth` | Controller workqueue depth (mean) | 505 |
| `etcd_databa...
```



---
## New issues

### [Code Review] [Task] [SRVKP-12412](https://redhat.atlassian.net/browse/SRVKP-12412) - 2sp - Deekshith Kumar Netha Bamandla N - Add Results watcher ingestion latency metrics to CPT


**Description:**
```
The existing {{timebased-sign-pruner}} performance test captures per-run Results annotation timestamps ({{result_at}}, {{log_at}}) in {{benchmark-output.json}} via {{benchmark.py}}, but {{stats.sh}} never computes summary statistics for them.

{{stats.sh}} already does this for Chains signing metrics. We need the equivalent for Results watcher ingestion:

*Acceptance Criteria:*

* Computes Results ingestion latency (min/avg/max) and throughput for both PipelineRuns and TaskRuns
* Metrics are written to {{benchmark-tekton.json}} and available for Horreum/ResultsDashboard upload
```



**Comments:**

#### **Jan Hutar** (2026-06-16)
```
+Status report:+ Deekshith created the change and Siddardh is reviewing it now. Will merge after review is done.
```





---


# ConsoleDot
## Finished issues

### [Closed/Done] [Task] [HCEPERF-1503](https://redhat.atlassian.net/browse/HCEPERF-1503) - 2sp - Rajaditya Chauhan - Cyndi deommission: remove jenkins jobs


**Description:**
```
As a part of full decommission , remove builder and runner job from perf cluster.
```



**Comments:**

#### **Rajaditya Chauhan** (2026-06-12)
```
Removed jenkins jobs [https://gitlab.cee.redhat.com/redhat-performance/ci-configs/-/merge_requests/596|https://gitlab.cee.redhat.com/redhat-performance/ci-configs/-/merge_requests/596]
```




**Linked Pull Requests & Merge Requests**

#### PR/MR: https://gitlab.cee.redhat.com/redhat-performance/ci-configs/-/merge_requests/596
```
Title: Decommission cyndi jobs from perf jenkins
As a part of cyndi decommission, removing jenkins jobs.
```



---
### [Closed/Done] [Task] [HCEPERF-1501](https://redhat.atlassian.net/browse/HCEPERF-1501) - Nitin Krishna Mucheli - Migrate usages of CloudServices token to RedHat Services Prod token




**Comments:**

#### **Nitin Krishna Mucheli** (2026-06-10)
```
Migrated both CI-Configs and IPerf repos to use the current token, RedHat Services Prod:
[https://github.com/Appservices-perfscale/iperf/commit/a6435d007e459779cc50643ee80e8e9b03841757|https://github.com/Appservices-perfscale/iperf/commit/a6435d007e459779cc50643ee80e8e9b03841757]
[https://gitlab.cee.redhat.com/redhat-performance/ci-configs/-/commit/141b9ac4873448550c695bdfb79f7e62806bad49|https://gitlab.cee.redhat.com/redhat-performance/ci-configs/-/commit/141b9ac4873448550c695bdfb79f7e62806bad49]
```




**Linked Pull Requests & Merge Requests**

#### PR/MR: https://github.com/Appservices-perfscale/iperf/commit/a6435d007e459779cc50643ee80e8e9b03841757
```
Commit Message:
.commit.message
```

#### PR/MR: https://gitlab.cee.redhat.com/redhat-performance/ci-configs/-/commit/141b9ac4873448550c695bdfb79f7e62806bad49
```
Commit Message:
migrate to RedHat services prod secret from cloudservices
```



---
### [Closed/Done] [Task] [HCEPERF-1500](https://redhat.atlassian.net/browse/HCEPERF-1500) - 3sp - Rajaditya Chauhan - Remove Cyndi saas file


**Description:**
```
End goal:

# Delete namespace file
# Delete saas file
```



**Comments:**

#### **Rajaditya Chauhan** (2026-06-12)
```
To remove saas file :

# [https://gitlab.cee.redhat.com/service/app-interface/-/merge_requests/192183|https://gitlab.cee.redhat.com/service/app-interface/-/merge_requests/192183]
# [https://gitlab.cee.redhat.com/service/app-interface/-/merge_requests/192260|https://gitlab.cee.redhat.com/service/app-interface/-/merge_requests/192260]
```




**Linked Pull Requests & Merge Requests**

#### PR/MR: https://gitlab.cee.redhat.com/service/app-interface/-/merge_requests/192260
```
Title: Final decommission of Cyndi from perf cluster
#### Why
Cyndi is decommissioned, removing from perf as well
```

#### PR/MR: https://gitlab.cee.redhat.com/service/app-interface/-/merge_requests/192183
```
Title: Try2 decommission cyndi perf
#### What
Trying to follow the comment here https://gitlab.cee.redhat.com/service/app-interface/-/merge_requests/191972#note_21824930


#### Why
Decommission cyndi namespace from perf cluster
```



---
### [Closed/Done] [Task] [HCEPERF-1498](https://redhat.atlassian.net/browse/HCEPERF-1498) - 2sp - Krishna Magar - Document all the results from the profile tests and stability tests




**Comments:**

#### **Krishna Magar** (2026-06-10)
```
Documented the stability and profiling test results in a report and supporting spreadsheet. Shared both with Breno for review and feedback on the findings.

report: [https://docs.google.com/document/d/1DVK1hAk_vYs5zD8kym_arHmJYD5UunBHcN7soFxJiHY/edit?usp=sharing|https://docs.google.com/document/d/1DVK1hAk_vYs5zD8kym_arHmJYD5UunBHcN7soFxJiHY/edit?usp=sharing|smart-link]
Results: [https://docs.google.com/spreadsheets/d/1SiulXWeGtM2cBeivRywgG7sfljQCrhBKvGgnN_UQjc0/edit?usp=sharing|https://docs.google.com/spreadsheets/d/1SiulXWeGtM2cBeivRywgG7sfljQCrhBKvGgnN_UQjc0/edit?usp=sharing|smart-link]
```





---
### [Closed/Done] [Task] [HCEPERF-1497](https://redhat.atlassian.net/browse/HCEPERF-1497) - 3sp - Krishna Magar - Profile workqueue cache_shard path to identify CPU hotspots


**Description:**
```
Following the tests comparing {{cache}} and {{cache_shard}} affinity scopes, {{cache}} maintained a slight edge in throughput (~383k vs ~377k IOPS). To understand why the {{cache_shard}} path is slightly slower even when aligned to the LLC topology ({{cache_shard_size=28}}), we need to profile the execution and identify what is running "hotter" in the sharded configuration.
```



**Comments:**

#### **Krishna Magar** (2026-06-10)
```
Profiling data was collected using perf stat and perf lock for the cache, cache_shard_size=28, and cache_shard_size=8 configurations.

Repeated benchmark runs did not reproduce the previously observed ~2% throughput gap. Average throughput across configurations was nearly identical, suggesting the earlier difference was likely within normal benchmark variation.

Profiling showed minor differences in scheduler activity, CPU migrations, and context-switch behavior between configurations, but no clear hotspot or lock contention pattern that consistently explains a performance regression in the LLC-aligned cache_shard configuration.

Based on the benchmark and profiling results, cache_shard_size=28 appears to perform similarly to the default cache affinity mode for this workload.
```





---
### [Closed/Done] [Task] [HCEPERF-1496](https://redhat.atlassian.net/browse/HCEPERF-1496) - 3sp - Krishna Magar - Verify reproducibility of 2% throughput gap between cache and cache_shard affinity scopes


**Description:**
```
Recent performance tests comparing {{default_affinity_scope=cache}} and {{cache_shard}} (with {{workqueue.cache_shard_size=28}} to match LLC) showed a slight performance regression of ~2% for the sharded approach at high concurrency (168 jobs).

* {{cache}}: ~383k IOPS
* {{cache_shard_size=28}}: ~377k IOPS

We need to determine if this 2% gap is a consistent, reproducible regression or simply within the standard margin of error (noise) for this test environment.
```



**Comments:**

#### **Krishna Magar** (2026-06-10)
```
Completed 5 repeated runs for the cache, cache_shard_size=28, and cache_shard_size=8 configurations.

The previously observed ~2% throughput difference was not reproduced. Average throughput across runs was 327.0k IOPS (cache), 326.4k IOPS (cache_shard_size=28), and 325.2k IOPS (cache_shard_size=8), indicating the earlier gap was likely within normal benchmark variation.

Detailed results have been documented and shared with Breno for review.
```





---
### [Closed/Done] [Task] [HCEPERF-1484](https://redhat.atlassian.net/browse/HCEPERF-1484) - 3sp - Krishna Magar - Create initial config for pass_or_fail and update playbook to detect regressions


**Description:**
```
* Create initial basic config file for {{pass_or_fail}} tool that allows us to say if current result is regression or not (see [https://github.com/redhat-performance/opl/blob/main/core/opl/investigator/README.md|https://github.com/redhat-performance/opl/blob/main/core/opl/investigator/README.md] for documentation).
* Change the relevant playbook to run {{pass_or_fail}} to detect regressions and add pass/fail result to the master JSON before it gets uploaded to the DB.
```



**Comments:**

#### **Krishna Magar** (2026-06-16)
```
OPL pass/fail integrated for NOPM regression detection

* Regression checking compares each run’s NOPM against prior results in the shared database (same test, virtual users, and RHEL version). A run passes if NOPM is at least as good as the worst historical result; only real drops are flagged as failures. Decision details are stored for audit.
* After each benchmark, the pipeline builds the master result file, runs the pass/fail check, and records *PASS* or *FAIL* on that file before anything is archived or uploaded.
* A failed regression check does *not* stop the playbook; the outcome is saved and shown in the run summary.
* Results are still archived and uploaded to the database whether the run passed or failed.
* Benchmark metrics are stored in a format the OPL tool can analyze correctly.
```





---
### [Closed/Done] [Task] [HCEPERF-1483](https://redhat.atlassian.net/browse/HCEPERF-1483) - 5sp - Krishna Magar - Add support to pass_or_fail OPL tool to fetch historical data from PostgreSQL


**Description:**
```
Add support to {{pass_or_fail}} OPL tool [https://github.com/redhat-performance/opl/blob/main/core/opl/investigator/README.md|https://github.com/redhat-performance/opl/blob/main/core/opl/investigator/README.md] to get historical data from PostgreSQL database. Take a quick look at the docs and talk to jhutar so we can discuss implementation details.
```



**Comments:**

#### **Krishna Magar** (2026-06-16)
```
* Implemented PostgreSQL as a history source and decisions storage plugin for the OPL investigator ({{pass_or_fail.py}}), aligned with the existing ElasticSearch/CSV pattern.
*Delivered:*
** History loader: query PostgreSQL for past results (JSON/JSONB status data via configurable SQL)
** Decisions storage: append pass/fail decisions to a configured table ({{data}} JSON/JSONB column)
** Config support in {{config.py}}, examples in {{sample_config.yaml}}, docs in {{investigator/README.md}} and root {{README.md}}
** {{core/setup.py}} — optional {{[postgresql]}} extra for {{psycopg2-binary}} (keeps core install lightweight)
*
```





---
### [Closed/Done] [Task] [HCEPERF-1450](https://redhat.atlassian.net/browse/HCEPERF-1450) - 3sp - Krishna Magar - Prepare OS of the machines


**Description:**
```
Create a playbook in the [db-perf-comparison|https://github.com/Appservices-perfscale/db-perf-comparison] repository to prepare the OS on both the DB server and the test runner. It should remove existing repositories in {{/etc/yum.repos.d/}}, configure specific BaseOS and AppStream repos for the requested RHEL version (e.g., {{https://download.devel.redhat.com/rhel-9/rel-eng/RHEL-9/RHEL-9.7.0-RC-1.3/}}), run a {{dnf distro-sync}} to ensure no unexpected packages remain, and reboot the machines. After reboot, dump all Ansible facts to a {{facts.json}} file.

Note: Discuss upgrading from RHEL 9 to RHEL 10 with ScaleLab support on [Google Chat|https://chat.google.com/app/chat/AAAAO5aQ7lo] and create a separate task for this effort if necessary.

h3. Acceptance Criteria

* OS upgraded/synced to the exact requested RHEL version.
* Machines rebooted successfully with the correct kernel.
* {{facts.json}} is generated containing facts as detected by Ansible setup task.
```






---
### [Closed/Done] [Task] [HCEPERF-1413](https://redhat.atlassian.net/browse/HCEPERF-1413) - 1sp - Nitin Krishna Mucheli - ConsoleDot: GitHub Tokens


**Description:**
```
Due to internal leak (INC4624779), we need to rotate (or remove from upstream systems and Jenkins if no longer needed - this is a good opportunity for cleanup) all secrets. Please go one by one and mark the secret in this Jira description you resolved somehow so it is clear which secrets are done and which are still to be done.

h2. GitHub Tokens

* -*github-token-for-iperf-insights-core*: GitHub personal access token for iperf/insights-core test to interact with [https://github.com/RedHatInsights/insights-core|https://github.com/RedHatInsights/insights-core] repo-
* -*github-token-for-iperf-insights-rbac*: GitHub personal access token for iperf/rbac test to interact with [https://github.com/RedHatInsights/insights-rbac|https://github.com/RedHatInsights/insights-rbac] repo-
* -*github-token-for-iperf-insights-subscription-watch*: GitHub personal access token for iperf/rbac test to interact with [https://github.com/RedHatInsights/rhsm-subscriptions|https://github.com/RedHatInsights/rhsm-subscriptions] repo-
```



**Comments:**

#### **Nitin Krishna Mucheli** (2026-06-10)
```
PR has been merged
```




**Linked Pull Requests & Merge Requests**

#### PR/MR: https://gitlab.cee.redhat.com/ccit/jenkins-csb-customers/perf-casc-master/-/merge_requests/126
```
Title: removed unused secrets

```



---
### [Closed/Done] [Task] [HCEPERF-1205](https://redhat.atlassian.net/browse/HCEPERF-1205) - 2sp - Rajaditya Chauhan - Remove HCC - Cyndi from Perf Cluster


**Description:**
```
*Description:* Delete the HCC - Cyndi service from the perf cluster to reduce AWS costs. Follow the standard app-interface service deletion process.

*Acceptance Criteria:*
 * App-interface MR submitted and merged to remove service
 * All associated AWS resources cleaned up
 * Verified service is no longer running in perf cluster
```



**Comments:**

#### **Rajaditya Chauhan** (2026-06-12)
```
broken into 2 tasks:

# [https://redhat.atlassian.net/browse/HCEPERF-1500|https://redhat.atlassian.net/browse/HCEPERF-1500|smart-link]
# [https://redhat.atlassian.net/browse/HCEPERF-1503|https://redhat.atlassian.net/browse/HCEPERF-1503|smart-link]
```





---
## In review issues

## In progress issues

### [In Progress] [Task] [HCEPERF-1504](https://redhat.atlassian.net/browse/HCEPERF-1504) - 3sp - Rajaditya Chauhan - RBAC rds engine version upgrade issue


**Description:**
```
From rds logs:

{noformat}------------------------------------------------------------------
Upgrade could not be run on Tue Jun 09 04:53:47 2026
------------------------------------------------------------------
The instance could not be upgraded from 14.17.R1 to 16.11.R1 because of following reasons. Please take appropriate action on databases that have usages incompatible with requested major engine version upgrade and try again.
- The instance could not be upgraded because it has one or more logical replication slots. Please drop all logical replication slots and try again.

----------------------- END OF LOG ---------------------- {noformat}

From RBAC DB:

{noformat}postgres=> SELECT slot_name, plugin, slot_type, active
FROM pg_replication_slots
WHERE slot_type = 'logical';
 slot_name |  plugin  | slot_type | active
-----------+----------+-----------+--------
 debezium  | pgoutput | logical   | t
(1 row){noformat}
```






---
### [In Progress] [Task] [HCEPERF-1485](https://redhat.atlassian.net/browse/HCEPERF-1485) - 3sp - Krishna Magar - Update playbook to upload master JSON to PostgreSQL and test artifacts to file storage


**Description:**
```
Alter relevant playbook (or create new one) to upload main JSON file to PostgreSQL database and all test artefacts to file storage for archival purposes. There will be "data" table in the DB with:

* id column
* datetime column (when the test run started)
* JSONB column (we will upload main JSON file with all the data here)
```






---
## New issues

### [In Progress] [Task] [HCEPERF-1504](https://redhat.atlassian.net/browse/HCEPERF-1504) - 3sp - Rajaditya Chauhan - RBAC rds engine version upgrade issue


**Description:**
```
From rds logs:

{noformat}------------------------------------------------------------------
Upgrade could not be run on Tue Jun 09 04:53:47 2026
------------------------------------------------------------------
The instance could not be upgraded from 14.17.R1 to 16.11.R1 because of following reasons. Please take appropriate action on databases that have usages incompatible with requested major engine version upgrade and try again.
- The instance could not be upgraded because it has one or more logical replication slots. Please drop all logical replication slots and try again.

----------------------- END OF LOG ---------------------- {noformat}

From RBAC DB:

{noformat}postgres=> SELECT slot_name, plugin, slot_type, active
FROM pg_replication_slots
WHERE slot_type = 'logical';
 slot_name |  plugin  | slot_type | active
-----------+----------+-----------+--------
 debezium  | pgoutput | logical   | t
(1 row){noformat}
```






---
### [New] [Sub-task] [HCEPERF-1502](https://redhat.atlassian.net/browse/HCEPERF-1502) - Pablo Mendez Hernandez - Rotate tokens used in containers/satellite perf tests


**Description:**
```
The following are to be rotated, as they are being used:

* *registry-redhat-io_username*: [registry.redhat.io|http://registry.redhat.io] service account username created by pablomh for downloading containers from it
* *registry-redhat-io_password*: [registry.redhat.io|http://registry.redhat.io] service account password created by pablomh for downloading containers from it
* *registry-stage-redhat-io_username*: [registry.stage.redhat.io|http://registry.stage.redhat.io] service account username created by pablomh for downloading containers from it
* *registry-stage-redhat-io_password*: [registry.stage.redhat.io|http://registry.stage.redhat.io] service account password created by pablomh for downloading containers from it



These tokens are being used here:


|[ContPerf619EL9|https://jenkins-csb-perf-master.dno.corp.redhat.com/job/ContPerf619EL9/]|#76  [Unstable #77|https://jenkins-csb-perf-master.dno.corp.redhat.com/job/ContPerf619EL9/77/] |
|[ContPerfForemanctlEL9|https://jenkins-csb-perf-master.dno.corp.redhat.com/job/ContPerfForemanctlEL9/]|[Failed #54|https://jenkins-csb-perf-master.dno.corp.redhat.com/job/ContPerfForemanctlEL9/54/]-[In progress #70|https://jenkins-csb-perf-master.dno.corp.redhat.com/job/ContPerfForemanctlEL9/70/] |
|[ContPerfStreamEL9|https://jenkins-csb-perf-master.dno.corp.redhat.com/job/ContPerfStreamEL9/]|[Unstable #302|https://jenkins-csb-perf-master.dno.corp.redhat.com/job/ContPerfStreamEL9/302/] |
|[Sat_Red|https://jenkins-csb-perf-master.dno.c...
```






---
### [New] [Task] [HCEPERF-1499](https://redhat.atlassian.net/browse/HCEPERF-1499) - Vishal Vijayraghavan - Report Portal is broken presently, its impacting all CPT jobs


**Description:**
```
Report Portal is broken presently, its impacting all CPT jobs. Upon checking with [~accountid:70121:2d46d1a6-e85d-4221-b1de-03ce32638494] we noticed that the payload we are sending is incorrect with the new version

[https://source.redhat.com/departments/products_and_global_engineering/hybrid_cloud_experience_perfscale_team/mbu_perfscale_team_wiki/using_mbu_perf_reportportal_instance#it-s-broken-how-do-i-ask-for-support-|https://source.redhat.com/departments/products_and_global_engineering/hybrid_cloud_experience_perfscale_team/mbu_perfscale_team_wiki/using_mbu_perf_reportportal_instance#it-s-broken-how-do-i-ask-for-support-|smart-link]

Acceptance Criteria:

* Fix Jenkins builder job currently is failing [https://jenkins-csb-perf-master.dno.corp.redhat.com/job/UtilResultsFromRPToES/|https://jenkins-csb-perf-master.dno.corp.redhat.com/job/UtilResultsFromRPToES/]
* Fix security token issue - [https://reportportal-perf.apps.dno.ocp-hub.prod.psi.redhat.com/ui/#rhclou wedcpt/launches/-1/33216/268021/268022/log|https://reportportal-perf.apps.dno.ocp-hub.prod.psi.redhat.com/ui/#rhcloudcpt/launches/-1/33216/268021/268022/log]
```






---


# Satellite
## Finished issues

## In review issues

## In progress issues

### [In Progress] [Task] [SAT-12000](https://redhat.atlassian.net/browse/SAT-12000) - 5sp - Imaanpreet Kaur - How many files in RPM can Satellite handle?


**Description:**
```
This was raised in satellite-brq-gss-eng-mtg by [~accountid:616d5075209722007194ea15] 

[https://docs.google.com/document/d/1VSWYngBNs_76pLipQLmFGae-vFATtS4Mkjk-AWxh2-c/edit#bookmark=id.o0640wyhnngn]

Goal here would be to test sync, publish and promote rpm with something like:
 * 1k files with average path size 100 chars
 * 10k files
 * 100k files
 * 1M files

Not sure what we will be able to generate.

Regadring to pulpcore schema, we should be able to handle 255MB with paths in JSON.

Generate some sane amount of these packages and create a repo from these.

During this testing, keep an eye on memory consumption.

Once tested, open a documentation BZ so we can document Satellite limit (or at least max tested size).

Test case here would be:

# generate RPM with 1k files with average path size 100 chars
# create a repository directory and put it there (we will abuse Satellite's httpd to host it, but it can be easily different machine with httpd or so - this is not important from the test point of view): mkdir /var/www/html/pub/myrepo; cp <rpm_file_1k> /var/www/html/pub/myrepo
# create a repodata in that file to turn it into yum repo: createrepo /var/www/html/pub/myrepo (have not tried, maybe some other options will be needed)
# setup that repo in the Satellite using URL like http://loclhost/pub/myrepo
# sync it in Satellite - ensure the rpm was synced and you can view it's details in Sat UI, including it's package list (if it is possible); if it...
```






---
## New issues
