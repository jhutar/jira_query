# Konflux
## Finished issues

### [Closed/Done] [Task] [KONFLUX-14313](https://redhat.atlassian.net/browse/KONFLUX-14313) - 1sp - Jan Hutar - Annual Access Revalidation for PERF-017 CMDB


**Description:**
```
{noformat}From: Conor Peoples <cpeoples@redhat.com>
Date: Wed, 3 Jun 2026 16:20:31 +0100
To: IT-Compliance-Audit <IT-COMPLIANCE-AUDIT@redhat.com>
Cc: Pia <pia@redhat.com>, Business Controls <businesscontrols@redhat.com>,  IT-Compliance <it-compliance@redhat.com>, Sarah Reed <sareed@redhat.com>,  Mark Lancisi <mlancisi@redhat.com>,
GRC <GRC@redhat.com>, Jim Kuykendall <jkuykend@redhat.com>,  Pranshul Srivastava <pransriv@redhat.com>, Kieran Whelan <kwhelan@redhat.com>
Subject: Annual Access Revalidation Requirement - DUE JUNE 30 - Reminder 2

Dear All,

You are receiving this follow up reminder email because you are listed in
Red Hat’s CMDB
<https://redhat.service-now.com/nav_to.do?uri=%2Fcmdb_ci_business_app_list.do%3Fsysparm_query%3Dinstall_status!%3D22%5EORinstall_status%3DNULL%5Einstall_status!%3D7%5EORinstall_status%3DNULL
+%26sysparm_first_row%3D1%26sysparm_view%3D>
as
the Owner or Delegate of an application with a Criticality Rating of C1
and/or a Data Classification of "RH-RESTRICTED(+PII)" that still has an
outstanding access review. This review must be completed by June 30th.

An annual revalidation of administrative and privileged users is required
for these applications, unless more frequent reviews are mandated by
SOX(FINSIG), ASCA, or the RH Global Privacy team.

Timeline
To streamline compliance tracking and reduce review fatigue, please
complete your revalidation by June 30, unless a sooner date is required
based on your specific review frequency. You will r...
```



**Comments:**

#### **Jan Hutar** (2026-06-07)
```
Our copy of the sheet: [https://docs.google.com/spreadsheets/d/1GeoSLtLeT3XNebOBwcS2q63b7LRishlgAPlkaOoaWKQ/edit?gid=0#gid=0|https://docs.google.com/spreadsheets/d/1GeoSLtLeT3XNebOBwcS2q63b7LRishlgAPlkaOoaWKQ/edit?gid=0#gid=0]
```

#### **Jan Hutar** (2026-06-08)
```
Added screenshots of [admins|https://rover.redhat.com/groups/group/it-cloud-aws-992382442726-admin] and [powerusers|https://rover.redhat.com/groups/group/it-cloud-aws-992382442726-poweruser] rover groups (did some basic cleanup). Asked Pradeep to add his [signoff|https://docs.google.com/spreadsheets/d/1GeoSLtLeT3XNebOBwcS2q63b7LRishlgAPlkaOoaWKQ/edit?gid=1011640302#gid=1011640302&range=B8] (for second time already).
```

#### **Jan Hutar** (2026-06-08)
```
[https://redhat.service-now.com/now/nav/ui/classic/params/target/cmdb_ci_business_app.do%3Fsys_id%3Dd87d583a3b562ad02800053a85e45a5c|https://redhat.service-now.com/now/nav/ui/classic/params/target/cmdb_ci_business_app.do%3Fsys_id%3Dd87d583a3b562ad02800053a85e45a5c] updated with access revalidated link and date of today, should be all good.
```





---
### [Closed/Done] [Task] [KONFLUX-14288](https://redhat.atlassian.net/browse/KONFLUX-14288) - 1sp - Subrata Modak - Spend time for Q2 day of learning


**Description:**
```
Attend the presentation/training on “Talk Agent Skills with Burr Sutter“ (5th June) and see if I can learn something new from that.
```



**Comments:**

#### **Subrata Modak** (2026-06-08)
```
Attended some presentations.
```





---
### [Closed/Done] [Task] [KONFLUX-14241](https://redhat.atlassian.net/browse/KONFLUX-14241) - 3sp - Subrata Modak - Filter out pods with non-meaningful artifacts in OOM detector


**Description:**
```
h2. *Problem*

The OOM/CrashLoopBackOff detector creates Jira tickets for pods whose logs and descriptions cannot be collected because the pods were deleted before the tool runs. Even at 4-hour intervals, short-lived pods (like PipelineRun pods) are often gone by the time artifact collection happens.

This creates noise and unhelpful tickets where users cannot find debugging information (see KONFLUX-11365).

h2. *Solution*

* Add {{is_artifact_meaningful()}} function to validate collected artifacts
* Skip pods where {{oc describe}} or {{oc logs}} return "pod not found" errors
* Delete artifact files for skipped pods to save disk space
* Track and report count of skipped pods in console output

h2. *Implementation*

* *PR:* [https://github.com/konflux-ci/perfscale/pull/67|https://github.com/konflux-ci/perfscale/pull/67]
* *Modified file:* {{tools/oomkill-and-crashloopbackoff-detector/oc_get_ooms.py}}
* *Changes:* +38 lines, -7 lines

h2. *Impact*

* Reduces false-positive Jira tickets for already-deleted pods
* Focuses monitoring on actionable incidents with meaningful logs
* Users see clear output: "X pod(s) kept (Y skipped - pod deleted)"

----

Assisted-by: Claude
```



**Comments:**

#### **Subrata Modak** (2026-06-03)
```
PR for artifact validation improvements (addressing feedback from PR #67):
[https://github.com/konflux-ci/perfscale/pull/68|https://github.com/konflux-ci/perfscale/pull/68|smart-link] 

*Changes*:
- Implemented two-stage validation: size-based heuristic (≥2KB) + pattern matching
- Only apply strict error patterns to small files (<10 lines)
- Prevents false negatives on multi-MB logs with 'not found' buried inside
- Added comprehensive test suite with 7 test cases
- 50-100x reduction in false positives, 10-1000x performance improvement for large logs

Addresses @jhutar's concern from PR #67 about vague conditions on large logs.

Impact:
✅ Prevents false negatives: 50-100x reduction in incorrectly skipped meaningful logs
✅ Performance: 10-1000x faster for large logs (size check vs full pattern scan)
✅ False positive rate unchanged: <1% (same as before)

Testing:
All 7 test cases pass - covering empty content, typical errors, small meaningful logs, large logs, edge cases, and boundary ...
```

#### **Subrata Modak** (2026-06-04)
```
The last additional PR ([https://github.com/konflux-ci/perfscale/pull/68|https://github.com/konflux-ci/perfscale/pull/68|smart-link]) for further improivement has been MERGED. Closing this.
```




**Linked Pull Requests & Merge Requests**

#### PR/MR: https://github.com/konflux-ci/perfscale/pull/67
```
Title: Filter out pods with non-meaningful artifacts in OOM detector
## Problem
The OOM/CrashLoopBackOff detector creates Jira tickets for pods whose logs and descriptions cannot be collected because the pods were deleted before the tool runs. Even at 4-hour intervals, short-lived pods (like PipelineRun pods) are often gone by the time artifact collection happens.

This creates noise and unhelpful tickets where users cannot find debugging information (see KONFLUX-11365).

## Solution
- Add `is_artifact_meaningful()` function to validate collected artifacts
- Skip pods where `oc describe` or `oc logs` return "pod not found" errors  
- Delete artifact files for skipped pods to save disk space
- Track and report count of skipped pods in console output

## Impact
- ✅ Reduces false-positive Jira tickets for already-deleted pods
- ✅ Focuses monitoring on actionable incidents with meaningful logs
- ✅ Users see clear output: "X pod(s) kept (Y skipped - pod deleted)"

## Changes
- Modified `...
```

#### PR/MR: https://github.com/konflux-ci/perfscale/pull/68
```
Title: Improve artifact validation robustness (addresses PR #67 feedback)
## Problem

In PR #67, @jhutar raised a valid concern:

> "These two if branches feels like very vague conditions given we are routinely (I assume) dealing with multi-MB logs full of mess"

The original validation logic could incorrectly skip meaningful multi-MB logs if they contained phrases like "not found" anywhere in the content (e.g., "config file not found" buried in a large OOM crash log).

## Solution

Implemented a **two-stage validation approach**:

### Stage 1: Size-Based Heuristic (Primary Filter)
- **If content ≥ 2KB → Always meaningful**
- Typical `oc` "pod not found" errors: ~100 bytes
- Real pod logs/descriptions: KBs to MBs
- Protects large logs regardless of content patterns

### Stage 2: Pattern Matching (Only for Small Content)
Applied **only when content < 2KB**:
- Only check patterns if file has **< 10 lines**
- More specific error patterns:
  - Require: `"error from server"` + `"pods"` +...
```



---
### [Closed/Done] [Task] [KONFLUX-14193](https://redhat.atlassian.net/browse/KONFLUX-14193) - 2sp - Subrata Modak - Raising new issues and tracking old unresolved issues for OOM & Crashloopbackoff detector in Sprint41




**Comments:**

#### **Subrata Modak** (2026-06-03)
```
Raised the OCPBUGS routing logic with the platform team on Slack. Our automated OOM detector routes incidents to OCPBUGS when all affected namespaces are ROSA/OCP platform namespaces (openshift-*), and to KONFLUX for tenant/mixed namespaces. Several OCPBUGS tickets are waiting triage - requested help getting them assigned to the appropriate platform team.

Assisted-by: Claude
```

#### **Subrata Modak** (2026-06-08)
```
Closing this now. Tracking the other improvement effort here: [https://redhat.atlassian.net/browse/KONFLUX-14299|https://redhat.atlassian.net/browse/KONFLUX-14299|smart-link]
```





---
### [Closed/Done] [Sub-task] [KONFLUX-14094](https://redhat.atlassian.net/browse/KONFLUX-14094) - Jan Hutar - Review requirements for KONFLUX-12751 - Jan


**Description:**
```
h1. Task

Please mark this issue closed once you are done reviewing. Marking this issue as closed will be considered as your Ack for the feature refinement doc mentioned in the parent feature.

h2. Feature Details (at the time this sub-task was created)
 
https://redhat.atlassian.net/browse/KONFLUX-12751 - AI-Assisted Code Review Pipeline

h2. Feature Refinement Document



[https://docs.google.com/document/d/1RFkA-D99CF3_QWH8fE1sbrZhKlGHGk8M3AQmAK_ynY0/edit?tab=t.0|https://docs.google.com/document/d/1RFkA-D99CF3_QWH8fE1sbrZhKlGHGk8M3AQmAK_ynY0/edit?tab=t.0|smart-card]

----

h2. Problem Statement

Code review is the main quality gate for every change, and it is entirely human-driven today. PRs can wait days for a first review, and different reviewers focus on different things, creating inconsistency. There is no structured data on which kinds of issues (security, correctness, style) are caught or missed most often, so there is no way to systematically improve the review process. Meanwhile, fullsend's vision for multi-agent review (specialized sub-agents for correctness, security, intent, injection defense, and style) has no foundation to build on.

h2. Recommended Theme 1 Position: Level 2 (AI review gate) -- the most expandable gate in the ladder

AI review sits after linting (Level 1) and before tests (Level 3). This is deliberate: lint catches syntax/style issues cheaply so the AI reviewer doesn't waste context on them; the AI reviewer catches logic and security issues...
```






---
### [Closed/Done] [Task] [KONFLUX-13726](https://redhat.atlassian.net/browse/KONFLUX-13726) - Roberto Alfieri - Onboarding: Hands-on learning with Konflux main usage


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



**Comments:**

#### **Roberto Alfieri** (2026-06-03)
```
Status update:

* requested a new tenant with [+https://gitlab.cee.redhat.com/releng/konflux-release-data/-/merge_requests/18006+|https://gitlab.cee.redhat.com/releng/konflux-release-data/-/merge_requests/18006]
* Forked a repo with a “simple” application → [https://github.com/rebtoor/devfile-sample-python-basic|https://github.com/rebtoor/devfile-sample-python-basic|smart-link]
* Setup the konflux ci on that repo → [https://github.com/rebtoor/devfile-sample-python-basic/pull/1|https://github.com/rebtoor/devfile-sample-python-basic/pull/1|smart-link]
* Created the required resources (service accounts, secrets) in order to push containers into a specified registry → [https://quay.io/repository/ralfieri/ralfieri-tenant/devfile-sample-python-basic-c9e78?tab=tags|https://quay.io/repository/ralfieri/ralfieri-tenant/devfile-sample-python-basic-c9e78?tab=tags|smart-link]
*  Become familiar with the concept of “Release” and related resources (releaseplan, releaseplanadmission, release)
* Tes...
```

#### **Jan Hutar** (2026-06-03)
```
Awesome, looks great, thank you! Feel free to close this.
```

#### **Roberto Alfieri** (2026-06-03)
```
As agreed with [~accountid:5a78c7f73297605c78217f31] , since the “Release” setup is hard on staging clusters, we can consider this task closed.
```




**Linked Pull Requests & Merge Requests**

#### PR/MR: https://github.com/rebtoor/devfile-sample-python-basic/pull/1
```
Title: Konflux Staging update devfile-sample-python-basic-c9e78

# Pipelines as Code configuration proposal

To start the PipelineRun, add a new comment with content `/ok-to-test`

For more detailed information about running a PipelineRun, please refer to Pipelines as Code documentation [Running the PipelineRun](https://pipelinesascode.com/docs/guide/running/)

To customize the proposed PipelineRuns after merge, please refer to [Build Pipeline customization](https://konflux-ci.dev/docs/building/customizing-the-build/)

Please follow the block sequence indentation style introduced by the proprosed PipelineRuns YAMLs, or keep using consistent indentation level through your customized PipelineRuns. When different levels are mixed, it will be changed to the proposed style.
```

#### PR/MR: https://gitlab.cee.redhat.com/releng/konflux-release-data/-/merge_requests/18006
```
Title: Add tenant ralfieri-tenant to staging cluster stone-stg-rh01
#### What:

Add tenant ralfieri-tenant to staging cluster stone-stg-rh01

Signed-off-by: Roberto Alfieri <ralfieri@redhat.com>

#### Why:
learning about konflux

#### Tickets:
https://redhat.atlassian.net/browse/KONFLUX-13726
```

#### PR/MR: https://gitlab.cee.redhat.com/releng/konflux-release-data/-/merge_requests/18005
```
Title: Fix staging add-namespace.sh for macOS compatibility
#### What:
Fix staging add-namespace.sh for macOS compatibility

The staging version of add-namespace.sh used hardcoded 'sed' with
GNU-specific multi-line patterns, which fails on macOS (BSD sed).

Changes:
- Add gsed detection block (matching the prod tenants-config script)
- Replace hardcoded 'sed' calls with ${SED_CMD}
- Simplify CODEOWNERS sed pattern to match prod approach
- Add missing --codeowner validation check
- Add missing CODEOWNERS sorting via tox -e codeowners-lint-fix
- Add missing 'tox' command check

Signed-off-by: Roberto Alfieri <ralfieri@redhat.com>

#### Why:
It seems that some fixes already applied for the "non-staging" version `add-namespace.sh` script, weren't applied to the staging version.

#### Tickets:
n/a
```



---
### [Closed/Won't Do] [Task] [KONFLUX-13066](https://redhat.atlassian.net/browse/KONFLUX-13066) - 1sp - Subrata Modak - Implement proper compute resources for task 'verify-source'


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

#### **Subrata Modak** (2026-06-08)
```
h3. Closing: PoC task with no fleet data; future enforcement via KONFLUX-11510

PR [konflux-ci/build-definitions#3560|https://github.com/konflux-ci/build-definitions/pull/3560] has been closed without merging.

Fleet analysis over a 60-day window across all 12 Konflux clusters returned *zero pod executions* for {{verify-source}}. This is consistent with the task's own description, which explicitly states:

{quote}_"This task relies on VSAs generated by source-tool which is currently a proof-of-concept and under active development. It should not be used in production environments."_{quote}

Without real execution data, any resource values would be guesswork. PR reviewers (@chmeliik, @arewm) correctly raised this concern — and closing is the right call.

This ticket can be revisited when {{verify-source}} graduates to production use and real fleet data becomes available. Additionally, [KONFLUX-11510|https://redhat.atlassian.net/browse/KONFLUX-11510] will introduce a CI enforcement che...
```




**Linked Pull Requests & Merge Requests**

#### PR/MR: https://github.com/konflux-ci/build-definitions/pull/3560
```
Title: feat(verify-source): add computeResources to slsa-verify step
## Summary

Adds `computeResources` to the `slsa-verify` step in `verify-source/0.1`, which had no resource definitions.

### Changes

| Step | Before | After |
|------|--------|-------|
| `slsa-verify` | not set | `memory: 64Mi` req=limit, `cpu: 50m` req, no cpu limit |

### Sizing rationale

Fleet analysis over a 60-day window returned no pod executions for `verify-source` across all 12 Konflux clusters. The task appears to have very low production usage. Floor values (`memory: 64Mi`, `cpu: 50m`) are used, consistent with the approach taken for other low-traffic tasks in this series.

### Policy

The step now satisfies the Konflux compute-resource policy:
- `memory.request == memory.limit`
- `cpu.request` set, no `cpu.limit`

### Related

- Epic: [KONFLUX-11509](https://redhat.atlassian.net/browse/KONFLUX-11509)
- Ticket: [KONFLUX-13066](https://redhat.atlassian.net/browse/KONFLUX-13066)

Assisted-by: CursorAI
Co...
```

#### PR/MR: https://github.com/konflux-ci/build-definitions/pull/3405
```
Title: feat(ta): set 4Gi memory request/limit for use-trusted-artifact step
The create-trusted-artifact step already sets a 3Gi limit via the generator code. Apply similar resource limits to the use-trusted-artifact step to ensure consistent memory allocation.

The -min variant patches remove the explicit computeResources so those tasks inherit the smaller stepTemplate defaults instead.

Related: https://github.com/konflux-ci/konflux-sast-tasks/pull/103
```



---
### [Closed/Won't Do] [Task] [KONFLUX-13064](https://redhat.atlassian.net/browse/KONFLUX-13064) - Subrata Modak - Implement proper compute resources for task 'tkn-bundle-oci-ta'


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

#### **Subrata Modak** (2026-06-08)
```
h3. Closing as duplicate — covered by KONFLUX-13063

{{tkn-bundle-oci-ta}} is an auto-generated Trusted Artifact variant of {{tkn-bundle}}, produced by {{hack/generate-ta-tasks.sh}}. Both files are committed together in the same PR:

* [konflux-ci/build-definitions#3576|https://github.com/konflux-ci/build-definitions/pull/3576] — covers both {{task/tkn-bundle/0.2/tkn-bundle.yaml}} *and* {{task/tkn-bundle-oci-ta/0.2/tkn-bundle-oci-ta.yaml}}

All resource work for this task family is tracked under [KONFLUX-13063|https://redhat.atlassian.net/browse/KONFLUX-13063].

Signed-off-by: Subrata Modak [smodak@redhat.com|mailto:smodak@redhat.com]

Assisted-by: CursorAgent@Cursor.com
```




**Linked Pull Requests & Merge Requests**

#### PR/MR: https://github.com/konflux-ci/build-definitions/pull/3576
```
Title: feat(tkn-bundle): add computeResources to all steps
## Summary

Adds `computeResources` (memory request = limit, CPU request only) to all
hand-editable steps in `tkn-bundle/0.2` and its generated OCI-TA variant,
in compliance with the Konflux resource policy.

### Fleet analysis

| Variant | Clusters with data | Pod executions | Window |
|---|---|---|---|
| `tkn-bundle` (base) | 0 / 12 | 0 | 60 days |
| `tkn-bundle-oci-ta` | 4 / 12 | 173 | up to 9.4 days |

All steps showed P95 memory ≤ 8 MB and P95 CPU ≤ 2m across clusters,
well below the floor values. Floor values (64Mi / 50m) are applied
throughout. Full analysis: [KONFLUX-13063](https://redhat.atlassian.net/browse/KONFLUX-13063).

### Changes

| Task | Step | Memory req=limit | CPU request |
|---|---|---|---|
| `tkn-bundle` | `modify-task-files` | 64Mi | 50m |
| `tkn-bundle` | `build` | 64Mi | 50m |
| `tkn-bundle-oci-ta` | `modify-task-files` | 64Mi | 50m |
| `tkn-bundle-oci-ta` | `build` | 64Mi | 50m |

### Note on `use-...
```

#### PR/MR: https://github.com/konflux-ci/build-definitions/pull/3405
```
Title: feat(ta): set 4Gi memory request/limit for use-trusted-artifact step
The create-trusted-artifact step already sets a 3Gi limit via the generator code. Apply similar resource limits to the use-trusted-artifact step to ensure consistent memory allocation.

The -min variant patches remove the explicit computeResources so those tasks inherit the smaller stepTemplate defaults instead.

Related: https://github.com/konflux-ci/konflux-sast-tasks/pull/103
```



---
### [Closed/Done] [Task] [KONFLUX-13049](https://redhat.atlassian.net/browse/KONFLUX-13049) - 2sp - Subrata Modak - Implement proper compute resources for task 'package-operator-package'


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

#### **Subrata Modak** (2026-06-03)
```
h2. Fleet Analysis -- package-operator-package and package-operator-package-oci-ta

The analyzer was run with a 60-day window across all 12 Konflux clusters for both the base task and its oci-ta variant. Both runs returned no execution data, indicating these tasks have negligible production usage.

h2. Policy Violations / Missing Resources

No computeResources were defined anywhere in either task. All steps are MISSING resources.

h2. Changes Applied

Base task -- package-operator-package:

||Step||Before||After||
|build-pkg|MISSING|memory: 64Mi req=limit, cpu: 50m req|
|build-sbom|MISSING|memory: 64Mi req=limit, cpu: 50m req|
|push-sbom|MISSING|memory: 64Mi req=limit, cpu: 50m req|

OCI-TA variant -- package-operator-package-oci-ta (regenerated via hack/generate-ta-tasks.sh):

||Step||Before||After||
|use-trusted-artifact|MISSING|memory: 64Mi req=limit, cpu: 50m req (manual -- generator limitation)|
|build-pkg|MISSING|memory: 64Mi req=limit, cpu: 50m req|
|build-sbom|MISSING|memory...
```

#### **Subrata Modak** (2026-06-03)
```
h3. CI Fix: Check Trusted Artifact variants (file out of date)

The {{Check Trusted Artifact variants}} CI check failed on PR #3568 with: *"File is out of date, run hack/generate-ta-tasks.sh"*.

h4. Root Cause

The CI workflow re-runs {{hack/generate-ta-tasks.sh}} and diffs the result against the committed {{package-operator-package-oci-ta.yaml}}. A {{computeResources}} block had been manually added to the generator-injected {{use-trusted-artifact}} step after running the generator. Since the generator never emits {{computeResources}} for this injected step (a known generator-level gap), CI's regenerated file differed from the committed file.

h4. Fix Applied

Removed the {{computeResources}} block from {{use-trusted-artifact}} in {{package-operator-package-oci-ta.yaml}} so the committed file matches generator output exactly. The three task-specific steps ({{build-pkg}}, {{build-sbom}}, {{push-sbom}}) retain their floor {{computeResources}} as those are correctly generated from the ...
```

#### **Subrata Modak** (2026-06-04)
```
Closing this as PR: [https://github.com/konflux-ci/build-definitions/pull/3568|https://github.com/konflux-ci/build-definitions/pull/3568|smart-link] has been merged to ‘main’ branch.
```




**Linked Pull Requests & Merge Requests**

#### PR/MR: https://github.com/konflux-ci/build-definitions/pull/3568
```
Title: fix(package-operator-package): add missing computeResources to all steps
## What

Adds `computeResources` to all steps in both
`task/package-operator-package/0.1/package-operator-package.yaml` and
its generated oci-ta variant
`task/package-operator-package-oci-ta/0.1/package-operator-package-oci-ta.yaml`.

## Changes

**`package-operator-package` (base task):**

| Step | Before | After |
|------|--------|-------|
| `build-pkg` | MISSING | `memory: 64Mi` req=limit, `cpu: 50m` req |
| `build-sbom` | MISSING | `memory: 64Mi` req=limit, `cpu: 50m` req |
| `push-sbom` | MISSING | `memory: 64Mi` req=limit, `cpu: 50m` req |

**`package-operator-package-oci-ta` (regenerated via `hack/generate-ta-tasks.sh`):**

| Step | Before | After |
|------|--------|-------|
| `use-trusted-artifact` | MISSING | `memory: 64Mi` req=limit, `cpu: 50m` req |
| `build-pkg` | MISSING | `memory: 64Mi` req=limit, `cpu: 50m` req |
| `build-sbom` | MISSING | `memory: 64Mi` req=limit, `cpu: 50m` req |
| `push...
```

#### PR/MR: https://github.com/konflux-ci/build-definitions/pull/3405
```
Title: feat(ta): set 4Gi memory request/limit for use-trusted-artifact step
The create-trusted-artifact step already sets a 3Gi limit via the generator code. Apply similar resource limits to the use-trusted-artifact step to ensure consistent memory allocation.

The -min variant patches remove the explicit computeResources so those tasks inherit the smaller stepTemplate defaults instead.

Related: https://github.com/konflux-ci/konflux-sast-tasks/pull/103
```



---
### [Closed/Done] [Task] [KONFLUX-13043](https://redhat.atlassian.net/browse/KONFLUX-13043) - 2sp - Subrata Modak - Implement proper compute resources for task 'modelcar-oci-ta'


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

#### **Subrata Modak** (2026-06-03)
```
h2. Fleet Analysis -- modelcar-oci-ta

The analyzer was run twice with a 60-day window across all 12 Konflux clusters (kflux-ocp-p01, kflux-osp-p01, kflux-prd-es01, kflux-prd-rh02, kflux-prd-rh03, kflux-rhel-p01, kflux-stg-es01, stone-prd-rh01, stone-prod-p01, stone-prod-p02, stone-stage-p01, stone-stg-rh01). Both runs returned no execution data, indicating this task has negligible production usage.

h2. Policy Violations / Missing Resources

No computeResources were defined anywhere in the task -- neither on stepTemplate nor on any of the 8 steps. All steps are MISSING resources.

h2. Changes Applied

||Step||Before||After||
|use-trusted-artifact|MISSING|memory: 64Mi req=limit, cpu: 50m req|
|download-model-files|MISSING|memory: 64Mi req=limit, cpu: 50m req|
|create-modelcar-base-image|MISSING|memory: 64Mi req=limit, cpu: 50m req|
|copy-model-files|MISSING|memory: 64Mi req=limit, cpu: 50m req|
|push-image|MISSING|memory: 64Mi req=limit, cpu: 50m req|
|sbom-generate|MISSING|memory: ...
```

#### **Subrata Modak** (2026-06-03)
```
h3. CI Fix: step-copy-model-files OOMKilled

The {{run-task-tests}} CI check failed on PR #3566 because {{step-copy-model-files}} was *OOMKilled* (exit code 137) at the 64 Mi floor.

h4. Root Cause

The step runs two memory-intensive operations:

# {{pip install olot==0.1.14}} -- pip fetches, unpacks, and installs the package into the container
# {{olot}} -- copies model files into an OCI layout

Both operations require substantially more than the 64 Mi floor value initially applied.

h4. Fix Applied

Raised {{step-copy-model-files}} memory from *64 Mi -> 512 Mi* (request = limit). All other seven steps remain at the 64 Mi floor. A follow-up commit was pushed to [PR #3566|https://github.com/konflux-ci/build-definitions/pull/3566].

Signed-off-by: Subrata Modak <smodak@redhat.com>

Assisted-by: CursorAgent@Cursor.com
```

#### **Subrata Modak** (2026-06-04)
```
CLOSING this as PR: [https://github.com/konflux-ci/build-definitions/pull/3566|https://github.com/konflux-ci/build-definitions/pull/3566|smart-link] has been merged to ‘main’ branch.
```




**Linked Pull Requests & Merge Requests**

#### PR/MR: https://github.com/konflux-ci/build-definitions/pull/3405
```
Title: feat(ta): set 4Gi memory request/limit for use-trusted-artifact step
The create-trusted-artifact step already sets a 3Gi limit via the generator code. Apply similar resource limits to the use-trusted-artifact step to ensure consistent memory allocation.

The -min variant patches remove the explicit computeResources so those tasks inherit the smaller stepTemplate defaults instead.

Related: https://github.com/konflux-ci/konflux-sast-tasks/pull/103
```

#### PR/MR: https://github.com/konflux-ci/build-definitions/pull/3566
```
Title: fix(modelcar-oci-ta): add missing computeResources to all steps
## What

Adds `computeResources` to all eight steps in `task/modelcar-oci-ta/0.1/modelcar-oci-ta.yaml`.
No `computeResources` were defined anywhere in the task (neither on `stepTemplate` nor per-step),
leaving all steps unconstrained.

## Changes

| Step | Before | After |
|------|--------|-------|
| `use-trusted-artifact` | MISSING | `memory: 64Mi` req=limit, `cpu: 50m` req |
| `download-model-files` | MISSING | `memory: 64Mi` req=limit, `cpu: 50m` req |
| `create-modelcar-base-image` | MISSING | `memory: 64Mi` req=limit, `cpu: 50m` req |
| `copy-model-files` | MISSING | `memory: 64Mi` req=limit, `cpu: 50m` req |
| `push-image` | MISSING | `memory: 64Mi` req=limit, `cpu: 50m` req |
| `sbom-generate` | MISSING | `memory: 64Mi` req=limit, `cpu: 50m` req |
| `upload-sbom` | MISSING | `memory: 64Mi` req=limit, `cpu: 50m` req |
| `report-sbom-url` | MISSING | `memory: 64Mi` req=limit, `cpu: 50m` req |

## Sizing rati...
```



---
## In review issues

### [Review] [Task] [KONFLUX-13065](https://redhat.atlassian.net/browse/KONFLUX-13065) - 2sp - Subrata Modak - Implement proper compute resources for task 'update-infra-deployments'


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

#### **Subrata Modak** (2026-06-08)
```
h3. Fleet Analysis & PR

*Fleet analysis (60-day window, 12 clusters):*

||Variant||Clusters with data||Pod executions||Window||
|{{update-infra-deployments}}|3 / 12|47|up to 9.4 days|

All observed steps: P95 memory ≤ 1 MB, P95 CPU = 0m → floor values applied.
{{race-condition-update-check}} and {{create-mr}} had no observability data — also receive floor values.

*Values applied (P95 + 5% margin, floor = 64Mi / 50m CPU):*

||Step||Memory req=limit||CPU request||Rationale||
|{{race-condition-update-check}}|64Mi|50m|No observability data|
|{{git-clone-infra-deployments}}|64Mi|50m|Floor (P95 = 0 MB)|
|{{run-update-script}}|64Mi|50m|Floor (P95 = 1 MB)|
|{{get-diff-files}}|64Mi|50m|Floor (P95 = 1 MB)|
|{{create-mr}}|64Mi|50m|No observability data|

No OCI-TA variant exists for this task.

*PR:* [konflux-ci/build-definitions#3577|https://github.com/konflux-ci/build-definitions/pull/3577]

Signed-off-by: Subrata Modak [smodak@redhat.com|mailto:smodak@redhat.com]

Assisted-by: CursorAgent...
```




**Linked Pull Requests & Merge Requests**

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

#### PR/MR: https://github.com/konflux-ci/build-definitions/pull/3405
```
Title: feat(ta): set 4Gi memory request/limit for use-trusted-artifact step
The create-trusted-artifact step already sets a 3Gi limit via the generator code. Apply similar resource limits to the use-trusted-artifact step to ensure consistent memory allocation.

The -min variant patches remove the explicit computeResources so those tasks inherit the smaller stepTemplate defaults instead.

Related: https://github.com/konflux-ci/konflux-sast-tasks/pull/103
```



---
### [Review] [Task] [KONFLUX-13063](https://redhat.atlassian.net/browse/KONFLUX-13063) - 2sp - Subrata Modak - Implement proper compute resources for task 'tkn-bundle'


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

#### **Subrata Modak** (2026-06-08)
```
h3. Fleet Analysis & PR

*Fleet analysis (60-day window, 12 clusters):*

||Variant||Clusters with data||Pod executions||Window||
|{{tkn-bundle}} (base)|0 / 12|0|60 days|
|{{tkn-bundle-oci-ta}}|4 / 12|173|up to 9.4 days|

All steps: P95 memory ≤ 8 MB, P95 CPU ≤ 2m → floor values applied (64Mi / 50m).

*Proposed values (P95 + 5% margin, floor = 64Mi / 50m CPU):*

||Task||Step||Memory req=limit||CPU request||
|{{tkn-bundle}}|{{modify-task-files}}|64Mi|50m|
|{{tkn-bundle}}|{{build}}|64Mi|50m|
|{{tkn-bundle-oci-ta}}|{{modify-task-files}}|64Mi|50m|
|{{tkn-bundle-oci-ta}}|{{build}}|64Mi|50m|

*Note on* {{use-trusted-artifact}}: {{tkn-bundle-oci-ta}} is a generated task ({{recipe.yaml}} + {{hack/generate-ta-tasks.sh}}). The generator injects {{use-trusted-artifact}} but does not support propagating {{computeResources}} for it. Manually adding them would break the "Check Trusted Artifact variants" CI check. This generator gap is tracked in [build-definitions PR #3405|https://github.com/konfl...
```




**Linked Pull Requests & Merge Requests**

#### PR/MR: https://github.com/konflux-ci/build-definitions/pull/3576
```
Title: feat(tkn-bundle): add computeResources to all steps
## Summary

Adds `computeResources` (memory request = limit, CPU request only) to all
hand-editable steps in `tkn-bundle/0.2` and its generated OCI-TA variant,
in compliance with the Konflux resource policy.

### Fleet analysis

| Variant | Clusters with data | Pod executions | Window |
|---|---|---|---|
| `tkn-bundle` (base) | 0 / 12 | 0 | 60 days |
| `tkn-bundle-oci-ta` | 4 / 12 | 173 | up to 9.4 days |

All steps showed P95 memory ≤ 8 MB and P95 CPU ≤ 2m across clusters,
well below the floor values. Floor values (64Mi / 50m) are applied
throughout. Full analysis: [KONFLUX-13063](https://redhat.atlassian.net/browse/KONFLUX-13063).

### Changes

| Task | Step | Memory req=limit | CPU request |
|---|---|---|---|
| `tkn-bundle` | `modify-task-files` | 64Mi | 50m |
| `tkn-bundle` | `build` | 64Mi | 50m |
| `tkn-bundle-oci-ta` | `modify-task-files` | 64Mi | 50m |
| `tkn-bundle-oci-ta` | `build` | 64Mi | 50m |

### Note on `use-...
```

#### PR/MR: https://github.com/konflux-ci/build-definitions/pull/3405
```
Title: feat(ta): set 4Gi memory request/limit for use-trusted-artifact step
The create-trusted-artifact step already sets a 3Gi limit via the generator code. Apply similar resource limits to the use-trusted-artifact step to ensure consistent memory allocation.

The -min variant patches remove the explicit computeResources so those tasks inherit the smaller stepTemplate defaults instead.

Related: https://github.com/konflux-ci/konflux-sast-tasks/pull/103
```



---
### [Review] [Task] [KONFLUX-13056](https://redhat.atlassian.net/browse/KONFLUX-13056) - 2sp - Subrata Modak - Implement proper compute resources for task 'run-script-oci-ta'


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

#### **Subrata Modak** (2026-06-05)
```
h3. Fleet Analysis & Resource Recommendations

Fleet data collected across all 12 Konflux clusters over a 60-day window with *6,989 total pod executions*. Metric used: *P95 + 5% margin*. PR: [konflux-ci/build-definitions#3571|https://github.com/konflux-ci/build-definitions/pull/3571].

h4. Data Coverage Note

Some clusters returned fewer than 60 days of data (stone-prd-rh01: 2.7 days, stone-prod-p02: 3.4 days). Statistics may under-represent rare heavy workloads on those clusters.

h4. Per-Step Recommendations

||Step||Before (mem req/limit)||Before (CPU req)||mem P95 (max across clusters)||Memory (req=limit)||cpu P95 (max across clusters)||CPU request||
|{{use-trusted-artifact}}|1Gi / 4Gi (stepTemplate)|1 (stepTemplate)|5 MB (stone-prod-p02)|*64Mi* (floor)|0m|*50m* (floor)|
|{{run-script}}|1Gi / 4Gi (stepTemplate)|1 (stepTemplate)|*4351 MB* (stone-prd-rh01, max 10,022 MB)|*5Gi*|*1284m* (stone-prd-rh01)|*1500m*|
|{{create-trusted-artifact}}|3Gi / 3Gi (per-step)|1 (per-step)|10 MB (s...
```

#### **Subrata Modak** (2026-06-08)
```
h3. Follow-up: TA step resource alignment with project standard

PR reviewer (@chmeliik) flagged that our initial floor values of 64Mi for {{use-trusted-artifact}} and {{create-trusted-artifact}} were inconsistent with the project-wide standard being established in [konflux-ci/build-definitions#3405|https://github.com/konflux-ci/build-definitions/pull/3405] (@sfowl).

Although our fleet data (6,989 pod executions, P95 ≤ 10 MB for both steps) supported the 64Mi floor, these two steps are identical across all tasks — same image, same code, same OCI artifact handling — so per-task fleet sizing is not appropriate for them.

*Updated values in* [*PR #3571*|https://github.com/konflux-ci/build-definitions/pull/3571]*:*

||Step||Before||After||
|{{use-trusted-artifact}}|64Mi req=limit|*4Gi* req=limit|
|{{create-trusted-artifact}}|64Mi req=limit|*3Gi* req=limit|

The {{run-script}} step sizing (5Gi / 1500m) is unchanged.

Going forward, {{use-trusted-artifact}} and {{create-trusted-artifact}...
```




**Linked Pull Requests & Merge Requests**

#### PR/MR: https://github.com/konflux-ci/build-definitions/pull/3571
```
Title: fix(run-script-oci-ta): right-size computeResources per fleet data
## What

Right-sizes `computeResources` on all three steps in
`task/run-script-oci-ta/0.1/run-script-oci-ta.yaml`, fixing three
policy violations in the existing partial configuration.

## Changes

| Step | Before (memory req / limit) | Before (CPU req) | After (memory req=limit) | After (CPU req) |
|---|---|---|---|---|
| `use-trusted-artifact` | 1Gi / 4Gi (from stepTemplate) | 1 (from stepTemplate) | **64Mi** | **50m** |
| `run-script` | 1Gi / 4Gi (from stepTemplate) | 1 (from stepTemplate) | **5Gi** | **1500m** |
| `create-trusted-artifact` | 3Gi / 3Gi (per-step) | 1 (per-step) | **64Mi** | **50m** |

## Policy violations fixed

1. **`stepTemplate` had `memory.request (1Gi) != memory.limit (4Gi)`** — removed
   the `stepTemplate.computeResources` block entirely and replaced with
   per-step values so each step is sized independently from fleet data.
2. **`run-script` was under-provisioned** — inherited the ...
```

#### PR/MR: https://github.com/konflux-ci/build-definitions/pull/3405
```
Title: feat(ta): set 4Gi memory request/limit for use-trusted-artifact step
The create-trusted-artifact step already sets a 3Gi limit via the generator code. Apply similar resource limits to the use-trusted-artifact step to ensure consistent memory allocation.

The -min variant patches remove the explicit computeResources so those tasks inherit the smaller stepTemplate defaults instead.

Related: https://github.com/konflux-ci/konflux-sast-tasks/pull/103
```



---
### [Review] [Task] [KONFLUX-13055](https://redhat.atlassian.net/browse/KONFLUX-13055) - 3sp - Subrata Modak - Implement proper compute resources for task 'run-opm-command-oci-ta'


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

#### **Subrata Modak** (2026-06-03)
```
h3. Fleet Analysis & Resource Recommendations

Fleet data collected across all 12 Konflux clusters over a 60-day window with *12,613 total pod executions*. Metric used: *P95 + 5% margin*. PR: [konflux-ci/build-definitions#3570|https://github.com/konflux-ci/build-definitions/pull/3570].

h4. Data Coverage Note

Some clusters returned fewer than 60 days of data (stone-prd-rh01: 3.8 days, stone-prod-p02: 4.7 days). Statistics may under-represent rare heavy workloads on those clusters.

h4. Per-Step Recommendations

||Step||mem P95 (max across clusters)||Memory (req=limit)||cpu P95 (max across clusters)||CPU request||
|{{use-trusted-artifact}}|7 MB (stone-stg-rh01)|*64Mi* (floor)|0m|*50m* (floor)|
|{{run-opm-with-user-args}}|*431 MB* (stone-prd-rh01, max 626 MB)|*512Mi*|78m (stone-prd-rh01)|*100m*|
|{{convert-image-tags-to-digests}}|13 MB (stone-prod-p02)|*64Mi* (floor)|*204m* (stone-prod-p02)|*250m*|
|{{replace-related-images-pullspec-in-file}}|5 MB (kflux-prd-rh02)|*64Mi* (floor)|0m|*...
```

#### **Subrata Modak** (2026-06-08)
```
h3. Follow-up: TA step resource alignment with project standard

Following reviewer feedback on PR #3571 (run-script-oci-ta) and alignment with [konflux-ci/build-definitions#3405|https://github.com/konflux-ci/build-definitions/pull/3405] (@sfowl), the {{use-trusted-artifact}} and {{create-trusted-artifact}} steps in this PR have also been updated.

Although our fleet data (12,613 pod executions, P95 ≤ 8 MB for both steps) supported the 64Mi floor, these steps are identical across all tasks and should follow the project-wide standard.

*Updated values in* [*PR #3570*|https://github.com/konflux-ci/build-definitions/pull/3570]*:*

||Step||Before||After||
|{{use-trusted-artifact}}|64Mi req=limit|*4Gi* req=limit|
|{{create-trusted-artifact}}|64Mi req=limit|*3Gi* req=limit|

All other step values (run-opm-with-user-args: 512Mi, convert-image-tags-to-digests: 64Mi) are unchanged.

Signed-off-by: Subrata Modak [smodak@redhat.com|mailto:smodak@redhat.com]

Assisted-by: CursorAgent@Cursor.com
```




**Linked Pull Requests & Merge Requests**

#### PR/MR: https://github.com/konflux-ci/build-definitions/pull/3405
```
Title: feat(ta): set 4Gi memory request/limit for use-trusted-artifact step
The create-trusted-artifact step already sets a 3Gi limit via the generator code. Apply similar resource limits to the use-trusted-artifact step to ensure consistent memory allocation.

The -min variant patches remove the explicit computeResources so those tasks inherit the smaller stepTemplate defaults instead.

Related: https://github.com/konflux-ci/konflux-sast-tasks/pull/103
```

#### PR/MR: https://github.com/konflux-ci/build-definitions/pull/3570
```
Title: feat(run-opm-command-oci-ta): add computeResources to all steps
## What

Adds `computeResources` to all five steps in
`task/run-opm-command-oci-ta/0.1/run-opm-command-oci-ta.yaml`.
No `computeResources` were defined anywhere in the task, leaving all
steps unconstrained.

## Changes

| Step | Before | After |
|---|---|---|
| use-trusted-artifact | MISSING | memory: 64Mi req=limit, cpu: 50m req |
| run-opm-with-user-args | MISSING | memory: 512Mi req=limit, cpu: 100m req |
| convert-image-tags-to-digests | MISSING | memory: 64Mi req=limit, cpu: 250m req |
| replace-related-images-pullspec-in-file | MISSING | memory: 64Mi req=limit, cpu: 50m req |
| create-trusted-artifact | MISSING | memory: 64Mi req=limit, cpu: 50m req |

## Sizing rationale

Fleet analysis across all 12 Konflux clusters over a 60-day window
(12,613 pod executions), using **P95 + 5% margin** as the base metric.
The absolute maximum is noted for context but is not used for sizing —
outlier spikes are deliberate...
```



---
### [Review] [Task] [KONFLUX-13047](https://redhat.atlassian.net/browse/KONFLUX-13047) - 2sp - Subrata Modak - Implement proper compute resources for task 'opm-get-bundle-version'


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

#### **Subrata Modak** (2026-06-03)
```
h2. Fleet Analysis -- opm-get-bundle-version

The analyzer was run with a 60-day window across all 12 Konflux clusters (kflux-ocp-p01, kflux-osp-p01, kflux-prd-es01, kflux-prd-rh02, kflux-prd-rh03, kflux-rhel-p01, kflux-stg-es01, stone-prd-rh01, stone-prod-p01, stone-prod-p02, stone-stage-p01, stone-stg-rh01). No execution data was returned, indicating this task has negligible production usage.

h2. Policy Violations / Missing Resources

* opm-render-bundle: computeResources MISSING
* jq-get-olm-package-version: computeResources MISSING
* apiVersion was tekton.dev/v1beta1 (deprecated) -- upgraded to tekton.dev/v1

h2. Changes Applied

||Step||Before||After||
|opm-render-bundle|MISSING|memory: 64Mi req=limit, cpu: 50m req|
|jq-get-olm-package-version|MISSING|memory: 64Mi req=limit, cpu: 50m req|
|apiVersion|tekton.dev/v1beta1|tekton.dev/v1|

h2. Sizing Rationale

* No fleet data available (0 pod executions across all clusters over 60 days).
* Floor values applied: memory 64Mi request...
```




**Linked Pull Requests & Merge Requests**

#### PR/MR: https://github.com/konflux-ci/build-definitions/pull/3405
```
Title: feat(ta): set 4Gi memory request/limit for use-trusted-artifact step
The create-trusted-artifact step already sets a 3Gi limit via the generator code. Apply similar resource limits to the use-trusted-artifact step to ensure consistent memory allocation.

The -min variant patches remove the explicit computeResources so those tasks inherit the smaller stepTemplate defaults instead.

Related: https://github.com/konflux-ci/konflux-sast-tasks/pull/103
```

#### PR/MR: https://github.com/konflux-ci/build-definitions/pull/3567
```
Title: fix(opm-get-bundle-version): add computeResources, upgrade API version
## What

Adds `computeResources` to both steps in
`task/opm-get-bundle-version/0.1/opm-get-bundle-version.yaml` and
upgrades the `apiVersion` from `tekton.dev/v1beta1` to `tekton.dev/v1`.

## Changes

| Step | Before | After |
|------|--------|-------|
| `opm-render-bundle` | MISSING | `memory: 64Mi` req=limit, `cpu: 50m` req |
| `jq-get-olm-package-version` | MISSING | `memory: 64Mi` req=limit, `cpu: 50m` req |

`apiVersion`: `tekton.dev/v1beta1` → `tekton.dev/v1`

## Sizing rationale

Fleet analysis across all Konflux clusters over a 60-day window returned
no execution data for this task, indicating negligible production usage.
Floor values (`memory: 64Mi` request=limit, `cpu: 50m` request) are
applied as the minimum safe baseline. These can be tuned upward once
real usage data is available.

The `apiVersion` upgrade to `tekton.dev/v1` is required to use the
`computeResources` field (the `v1beta1` equiva...
```



---
## In progress issues

### [In Progress] [Task] [KONFLUX-14299](https://redhat.atlassian.net/browse/KONFLUX-14299) - 3sp - Subrata Modak - OOM/CrashLoopBackOff Jira Enhancement: ROSA→OHSS Routing, ADF Formatting, and Permanent Artifacts


**Description:**
```
h1. 📋 Background

Our automated OOM/CrashLoopBackOff detection tool has been creating Jira tickets in OCPBUGS and KONFLUX projects. Recent feedback from the OCPBUGS/OHSS teams (Slack discussion in #forum-konflux-developer on 2026-06-04) highlighted several areas for improvement to make these tickets more actionable and useful for triagers.

{panel:bgColor=#fffae6}
h3. ⚠️  Current Problems

# *Ephemeral Artifacts* - Jenkins jobs and tarball storage get garbage-collected over time. When triagers review tickets weeks later, the diagnostic links are broken.
# *Missing Context* - Current tickets lack: cluster type detection, extracted error logs, must-gather archives.
# *Poor Formatting* - Hard to quickly identify root cause errors, affected clusters, and critical configuration details.
{panel}

h2. 🗣️  Slack Discussion Summary

*Key participants:* Subrata Modak, Elijah DeLee, Candace Sheremeta, Noreen Chhabra, Murali Krishnasamy, Joe Talerico

* *Joe Talerico:* "Why not capture a must-gather when these occur?"
* *Murali Krishnasamy:* "Do you have a way/tool to scrape the tarball and highlight the error logs like bugzooka?"
* *Candace Sheremeta:* ROSA clusters should file to OHSS project, not OCPBUGS
* *Noreen Chhabra:* Need proper Component field set for auto-assignment
* *Elijah DeLee:* Need must-gather and logs since we're looking retrospectively

h2. 🎯 Proposed Improvements (Phase 1 - This Story)

{panel:bgColor=#e3fcef}
h3. Improvements to Implement

# *Attach Diagnostic F...
```



**Comments:**

#### **Subrata Modak** (2026-06-04)
```
Starting implementation of enhanced Jira formatting with permanent artifacts.

Assisted-by: Claude
```

#### **Subrata Modak** (2026-06-04)
```
SCOPE UPDATE - Additional Improvements Added

Based on continued Slack discussion with OHSS/OCPBUGS teams, the following improvements are now IN SCOPE for this story:

NEW IMPROVEMENTS (ROSA → OHSS Routing):

1. Route ROSA Platform Issues to OHSS (Not OCPBUGS)
   - Current: ROSA clusters with openshift-* namespaces → OCPBUGS
   - New: ROSA clusters with openshift-* namespaces → OHSS project
   - Reason: Murali Krishnasamy confirmed "OHSS is the right one" for ROSA cluster issues

2. Add Cluster Metadata for OHSS Tickets
   - Cluster ID/Name (e.g., kflux-prd-rh03)
   - Environment (prod, stage, etc.)
   - Region (e.g., us-east-1, us-west-2)
   - Subscription details if available
   - Reason: SRE needs this info to access clusters

3. Set Product Field for ROSA Tickets
   - Field: Product
   - Value: "Red Hat Openshift Services on AWS"
   - Required for OHSS tickets

4. Pattern-Based Component Assignment
   - Auto-assign Component based on error patterns:
     * "splunk" or "metrics-e...
```

#### **Subrata Modak** (2026-06-05)
```
✅ IMPLEMENTATION COMPLETE - All Features Delivered

All scope items have been successfully implemented and tested:

ROSA → OHSS ROUTING ✅
• ROSA/OSD cluster detection via API + naming heuristics fallback
• Automatic routing: ROSA + openshift-* → OHSS (56% of incidents in test)
• Vanilla OCP routing preserved: OCP + openshift-* → OCPBUGS
• Tenant namespace routing preserved: → KONFLUX
• Multi-project deduplication: Searches KONFLUX, OCPBUGS, AND OHSS

CLUSTER METADATA ✅
• Cluster ID/Name extraction
• Environment detection (prod/stage/dev from cluster name patterns)
• Region and platform from OpenShift infrastructure API
• Displayed in formatted table in Jira description

COMPONENT AUTO-DETECTION ✅
• Pattern-based detection for OHSS tickets:
  - splunk, metrics-exporter → monitoring
  - router, ovnk → Networking
  - storage, authentication patterns included
• Best-effort assignment (Component field left blank if no match)

ENHANCED ADF FORMATTING ✅
• Incident Overview Panel with clust...
```

#### **Subrata Modak** (2026-06-05)
```
Posted this to channel:[https://redhat-internal.slack.com/archives/CCX9DB894/p1780622348042979|https://redhat-internal.slack.com/archives/CCX9DB894/p1780622348042979|smart-link] 

!Screenshot 2026-06-04 at 9.26.19 PM-20260605-012622.png|width=762,alt="Screenshot 2026-06-04 at 9.26.19 PM-20260605-012622.png"!
```

#### **Subrata Modak** (2026-06-05)
```
I have closed all 57 existing, unassigned OCPBUGS Jira issues that had been stagnant for a long time.

Because these issues only provided links rather than having the logs or data attached directly to the tickets, debugging them at this stage would have been highly impractical. Closing them allows us to keep the backlog clean and focus on actionable items (in future) with intact data.
```





---
### [In Progress] [Task] [KONFLUX-13720](https://redhat.atlassian.net/browse/KONFLUX-13720) - Roberto Alfieri - Onboarding: Understand Loadtest architecture and performance testing


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
## New issues

### [In Progress] [Task] [KONFLUX-14299](https://redhat.atlassian.net/browse/KONFLUX-14299) - 3sp - Subrata Modak - OOM/CrashLoopBackOff Jira Enhancement: ROSA→OHSS Routing, ADF Formatting, and Permanent Artifacts


**Description:**
```
h1. 📋 Background

Our automated OOM/CrashLoopBackOff detection tool has been creating Jira tickets in OCPBUGS and KONFLUX projects. Recent feedback from the OCPBUGS/OHSS teams (Slack discussion in #forum-konflux-developer on 2026-06-04) highlighted several areas for improvement to make these tickets more actionable and useful for triagers.

{panel:bgColor=#fffae6}
h3. ⚠️  Current Problems

# *Ephemeral Artifacts* - Jenkins jobs and tarball storage get garbage-collected over time. When triagers review tickets weeks later, the diagnostic links are broken.
# *Missing Context* - Current tickets lack: cluster type detection, extracted error logs, must-gather archives.
# *Poor Formatting* - Hard to quickly identify root cause errors, affected clusters, and critical configuration details.
{panel}

h2. 🗣️  Slack Discussion Summary

*Key participants:* Subrata Modak, Elijah DeLee, Candace Sheremeta, Noreen Chhabra, Murali Krishnasamy, Joe Talerico

* *Joe Talerico:* "Why not capture a must-gather when these occur?"
* *Murali Krishnasamy:* "Do you have a way/tool to scrape the tarball and highlight the error logs like bugzooka?"
* *Candace Sheremeta:* ROSA clusters should file to OHSS project, not OCPBUGS
* *Noreen Chhabra:* Need proper Component field set for auto-assignment
* *Elijah DeLee:* Need must-gather and logs since we're looking retrospectively

h2. 🎯 Proposed Improvements (Phase 1 - This Story)

{panel:bgColor=#e3fcef}
h3. Improvements to Implement

# *Attach Diagnostic F...
```



**Comments:**

#### **Subrata Modak** (2026-06-04)
```
Starting implementation of enhanced Jira formatting with permanent artifacts.

Assisted-by: Claude
```

#### **Subrata Modak** (2026-06-04)
```
SCOPE UPDATE - Additional Improvements Added

Based on continued Slack discussion with OHSS/OCPBUGS teams, the following improvements are now IN SCOPE for this story:

NEW IMPROVEMENTS (ROSA → OHSS Routing):

1. Route ROSA Platform Issues to OHSS (Not OCPBUGS)
   - Current: ROSA clusters with openshift-* namespaces → OCPBUGS
   - New: ROSA clusters with openshift-* namespaces → OHSS project
   - Reason: Murali Krishnasamy confirmed "OHSS is the right one" for ROSA cluster issues

2. Add Cluster Metadata for OHSS Tickets
   - Cluster ID/Name (e.g., kflux-prd-rh03)
   - Environment (prod, stage, etc.)
   - Region (e.g., us-east-1, us-west-2)
   - Subscription details if available
   - Reason: SRE needs this info to access clusters

3. Set Product Field for ROSA Tickets
   - Field: Product
   - Value: "Red Hat Openshift Services on AWS"
   - Required for OHSS tickets

4. Pattern-Based Component Assignment
   - Auto-assign Component based on error patterns:
     * "splunk" or "metrics-e...
```

#### **Subrata Modak** (2026-06-05)
```
✅ IMPLEMENTATION COMPLETE - All Features Delivered

All scope items have been successfully implemented and tested:

ROSA → OHSS ROUTING ✅
• ROSA/OSD cluster detection via API + naming heuristics fallback
• Automatic routing: ROSA + openshift-* → OHSS (56% of incidents in test)
• Vanilla OCP routing preserved: OCP + openshift-* → OCPBUGS
• Tenant namespace routing preserved: → KONFLUX
• Multi-project deduplication: Searches KONFLUX, OCPBUGS, AND OHSS

CLUSTER METADATA ✅
• Cluster ID/Name extraction
• Environment detection (prod/stage/dev from cluster name patterns)
• Region and platform from OpenShift infrastructure API
• Displayed in formatted table in Jira description

COMPONENT AUTO-DETECTION ✅
• Pattern-based detection for OHSS tickets:
  - splunk, metrics-exporter → monitoring
  - router, ovnk → Networking
  - storage, authentication patterns included
• Best-effort assignment (Component field left blank if no match)

ENHANCED ADF FORMATTING ✅
• Incident Overview Panel with clust...
```

#### **Subrata Modak** (2026-06-05)
```
Posted this to channel:[https://redhat-internal.slack.com/archives/CCX9DB894/p1780622348042979|https://redhat-internal.slack.com/archives/CCX9DB894/p1780622348042979|smart-link] 

!Screenshot 2026-06-04 at 9.26.19 PM-20260605-012622.png|width=762,alt="Screenshot 2026-06-04 at 9.26.19 PM-20260605-012622.png"!
```

#### **Subrata Modak** (2026-06-05)
```
I have closed all 57 existing, unassigned OCPBUGS Jira issues that had been stagnant for a long time.

Because these issues only provided links rather than having the logs or data attached directly to the tickets, debugging them at this stage would have been highly impractical. Closing them allows us to keep the backlog clean and focus on actionable items (in future) with intact data.
```





---
### [New] [Task] [KONFLUX-14287](https://redhat.atlassian.net/browse/KONFLUX-14287) - Subrata Modak - Readup about AI Skills (E.g KONFLUX-13490)


**Description:**
```
Readup about AI Skills (E.g KONFLUX-13490), something like why AGENT.MD, CLAUDE.MD, GEMINI.MD is needed
```






---


# Pipelines
## Finished issues

### [Closed/Done] [Bug] [SRVKP-12102](https://redhat.atlassian.net/browse/SRVKP-12102) - Jawed Khelil - tkn-cli-serve pod in CrashLoopBackOff


**Description:**
```
*Background:*

We noticed the {{OpenShift Pipelines scalingPipelines}} performance test is failing because it can not collect number of PAC pod restarts. During investigation we realized PAC pods are not running at all. Probably because {{tkn-cli-serve}} pod is stuck in {{CrashLoopBackOff}}.

*Issue:*

PAC pods (controller, watcher, webhook) are not being deployed. The operator's {{TektonConfig}} reconciliation is blocked because {{TektonAddon}} cannot reach ready state.

The blocker is the {{tkn-cli-serve}} pod in {{CrashLoopBackOff}}:

{noformat}sed: can't read /etc/httpd/conf.d/ssl.conf: No such file or directory{noformat}

The {{TektonConfig}} CR shows {{profile: all}} and {{pipelinesAsCode.enable: true}}. PAC is intended to be deployed but the stalled reconciliation prevents it.
```



**Comments:**

#### **Deekshith Kumar Netha Bamandla N** (2026-06-08)
```
tkn-cli-serve issue is fixed with the fix. Thanks!!
```





---
### [Closed/Done] [Epic] [SRVKP-11914](https://redhat.atlassian.net/browse/SRVKP-11914) - Deekshith Kumar Netha Bamandla N - Chains Controller CPT Scenarios


**Description:**
```
h2. *Epic Goal*

* Complete the test scenario coverage in CPT for Chains controllers

h2. *Scenarios*

# Chains controller with basic signing
# Chains controller with HA=10 setup
# Chains controller with QBT Profile (50/50/32)
# Chains controller with HA=10 setup and QBT Profile (50/50/32)

h2. *Acceptance Criteria (Mandatory)*

* CI - MUST be running successfully with tests automated
* Horreum and alerts are configured correctly
* Grafana dashboard is updated with the new scenarios

 
```



**Comments:**

#### **Automation for Jira** (2026-06-02)
```
Please add '*Release Note Text*', '*Release Note Status*' and '*Release Notes Type*'. Transitioning the issue back to 'In progress'. 

If Release Note is not required, set *Release Note Type* to '*Release Note Not Required*' 
```





---
### [Closed/Done] [Task] [SRVKP-8004](https://redhat.atlassian.net/browse/SRVKP-8004) - 2sp - Deekshith Kumar Netha Bamandla N - Have an agreement with engineering on a notification strategy


**Description:**
```
h3. Acceptance criteria
* Explained (and recorded it) how change detection in Horreum works to Engineering.
* We have an initial agreement with engineering on a notification strategy in case of change is detected.
```



**Comments:**

#### **Deekshith Kumar Netha Bamandla N** (2026-06-08)
```
Thresholds and alerts will be handled in a separate ticket: [https://redhat.atlassian.net/browse/SRVKP-12192|https://redhat.atlassian.net/browse/SRVKP-12192|smart-link] 
```





---
## In review issues

## In progress issues

### [In Progress] [Spike] [SRVKP-12325](https://redhat.atlassian.net/browse/SRVKP-12325) - 1sp - Aman Vishwakarma - Analyze one test vs separate tests per scenario/config for Horreum alert thresholds


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
### [In Progress] [Task] [SRVKP-12049](https://redhat.atlassian.net/browse/SRVKP-12049) - 2sp - Deekshith Kumar Netha Bamandla N - Identify the test scenarios for Results Controllers







---
## New issues

### [In Progress] [Spike] [SRVKP-12325](https://redhat.atlassian.net/browse/SRVKP-12325) - 1sp - Aman Vishwakarma - Analyze one test vs separate tests per scenario/config for Horreum alert thresholds


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


# ConsoleDot
## Finished issues

### [Closed/Done] [Task] [HCEPERF-1473](https://redhat.atlassian.net/browse/HCEPERF-1473) - 3sp - Subrata Modak - Konflux: OOM crash detector related secrets


**Description:**
```
Due to internal leak (INC4624779), we need to rotate (or remove from upstream systems and Jenkins if no longer needed - this is a good opportunity for cleanup) all secrets. Please go one by one and mark the secret in this Jira description you resolved somehow so it is clear which secrets are done and which are still to be done.

h2. Konflux & RHTAP Secrets

h3. OOM and Crash Detector (Managed by Subrata)

* [ ] _Konflux-oom-crash-detector-TOKEN-..._: For Konflux OOM detector tool. Prometheus reader SA tokens. (Includes: kflux_ocp_p01, kflux_osp_p01, kflux_prd_rh02, kflux_prd_rh03, kflux_rhel_p01, stone_prd_rh01, stone_prod_p01, stone_prod_p02, stone_stage_p01, stone_stg_rh01)
```



**Comments:**

#### **Subrata Modak** (2026-06-02)
```
*Progress update — Jun 2, 2026*

* Generated fresh 1-year SA tokens for all 10 clusters (SA: perf-team-prometheus-reader-oomcrash-sa, ns: perf-team-prometheus-reader).
* Shared all 10 tokens securely with Raj via PrivateBin and requested him to:
*# add new GPG key (4C8E95E940EC90038CA973D59A9CB0F812505DE5) as a git-crypt collaborator in perf-casc-master, and
*# update the secrets.
* Will wait for [~accountid:712020:742fe929-2f70-4ced-ad2f-464a9ba181a7] to add GPG key. Once done, will unlock the repo, update all 10 secret files, and open the MR.

_Assisted-by: CursorAgent_
```

#### **Subrata Modak** (2026-06-03)
```
*Jun 3, 2026:* Raj encountered a GPG trust issue while adding the new key as a git-crypt collaborator in {{perf-casc-master}}; provided fix instructions and a clean key export — waiting on confirmation.

_Assisted-by: CursorAgent_
```

#### **Subrata Modak** (2026-06-04)
```
*Jun 4, 2026 — Token rotation complete, MR raised*

What was done:

# Fetched latest {{perf-casc-master}} (includes [MR !128|https://gitlab.cee.redhat.com/ccit/jenkins-csb-customers/perf-casc-master/-/merge_requests/128] by [~accountid:712020:742fe929-2f70-4ced-ad2f-464a9ba181a7] adding our new GPG key as a git-crypt collaborator).
# Created branch {{rotate_oom_detector_tokens}} and ran {{git crypt unlock}} using new no-passphrase GPG key {{4C8E95E940EC90038CA973D59A9CB0F812505DE5}}.
# Copied 10 fresh 1-year SA tokens (generated via {{oc create token --duration=8760h}} for SA {{perf-team-prometheus-reader-oomcrash-sa}} in ns {{perf-team-prometheus-reader}}) into {{secrets/}}.
# Committed, pushed to fork, and raised [MR !129|https://gitlab.cee.redhat.com/ccit/jenkins-csb-customers/perf-casc-master/-/merge_requests/129].

*Pending:* [MR !129|https://gitlab.cee.redhat.com/ccit/jenkins-csb-customers/perf-casc-master/-/merge_requests/129] review/merge → CasC auto-syncs to Jenkins → trigg...
```

#### **Subrata Modak** (2026-06-05)
```
MR: [https://gitlab.cee.redhat.com/ccit/jenkins-csb-customers/perf-casc-master/-/merge_requests/129|https://gitlab.cee.redhat.com/ccit/jenkins-csb-customers/perf-casc-master/-/merge_requests/129] has been merged.
```

#### **Subrata Modak** (2026-06-05)
```
*Jun 5, 2026:* MR !129 merged; awaiting access to the {{dno--jenkins-csb-perf}} OpenShift project to run {{push-credentials.sh}} and complete the Jenkins secret deployment — pinged Jan for access.

_Assisted-by: CursorAgent_
```

#### **Subrata Modak** (2026-06-08)
```
*Jun 8, 2026 — Secrets deployed to Jenkins, verification successful*

Steps executed after MR !129 was merged:

# Gained access to {{dno--jenkins-csb-perf}} OpenShift project via Rover group {{perf-team-jenkins-admins}} (added by Jan Hutar).
# Logged in: {{oc login --web https://api.dno.ocp-hub.prod.psi.redhat.com:6443}} → {{oc project dno--jenkins-csb-perf}}
# Pulled latest and unlocked: {{git pull --rebase && git crypt unlock}}
# Pushed secrets: {{../jenkins-csb/self-service/push-credentials.sh .}} → {{secret/master-casc-secret replaced}}
# Restarted Jenkins pod: {{oc delete pod --selector 'name=master-jenkins' --namespace=dno--jenkins-csb-perf}}
# Triggered manual run of {{StoneSoupOOMDetector}} — [build #372|https://jenkins-csb-perf-master.dno.corp.redhat.com/view/Konflux/job/StoneSoupOOMDetector/372/console] confirmed all 10 clusters authenticated successfully with the new tokens.

*Token rotation for HCEPERF-1473 / INC4624779 is complete. Closing ticket.*

_Assisted-by: CursorAgent_
```

#### **Subrata Modak** (2026-06-08)
```
Thank you [~accountid:5a78c7f73297605c78217f31] [~accountid:712020:742fe929-2f70-4ced-ad2f-464a9ba181a7] for all the help.

Cc: [~accountid:5c6d765aca97144c4716967d] 
```




**Linked Pull Requests & Merge Requests**

#### PR/MR: https://gitlab.cee.redhat.com/ccit/jenkins-csb-customers/perf-casc-master/-/merge_requests/129
```
Title: feat(HCEPERF-1473): Rotate OOM crash detector SA tokens for all 10 clusters
## Summary

Rotate all 10 `Konflux-oom-crash-detector-TOKEN-*` secrets due to security incident INC4624779.

New 1-year tokens generated via `oc create token --duration=8760h` for SA `perf-team-prometheus-reader-oomcrash-sa` in namespace `perf-team-prometheus-reader` on each of the 10 clusters.

## Clusters covered

- kflux_ocp_p01
- kflux_osp_p01
- kflux_prd_rh02
- kflux_prd_rh03
- kflux_rhel_p01
- stone_prd_rh01
- stone_prod_p01
- stone_prod_p02
- stone_stage_p01
- stone_stg_rh01

## References

- Jira: HCEPERF-1473
- Incident: INC4624779

Assisted-by: CursorAgent
```

#### PR/MR: https://gitlab.cee.redhat.com/ccit/jenkins-csb-customers/perf-casc-master/-/merge_requests/128
```
Title: Add 1 git-crypt collaborator
New collaborators:

    4C8E95E940EC90038CA973D59A9CB0F812505DE5
        Subrata Modak <smodak@redhat.com>
```



---
### [Closed/Done] [Task] [HCEPERF-1145](https://redhat.atlassian.net/browse/HCEPERF-1145) - 1sp - Pravin Satpute - No tests were run for ContentSources service in last 7 days


**Description:**
```
No tests were run for ContentSources service in last 7 days
```



**Comments:**

#### **Pablo Mendez Hernandez** (2026-06-08)
```
We haven’t got any request (ever?), so I’ll disable the schedule.
```

#### **Pravin Satpute** (2026-06-08)
```
Lets close this and reopen a new ticket.
```





---
## In review issues

## In progress issues

### [In Progress] [Task] [HCEPERF-1497](https://redhat.atlassian.net/browse/HCEPERF-1497) - 3sp - Krishna Magar - Profile workqueue cache_shard path to identify CPU hotspots


**Description:**
```
Following the tests comparing {{cache}} and {{cache_shard}} affinity scopes, {{cache}} maintained a slight edge in throughput (~383k vs ~377k IOPS). To understand why the {{cache_shard}} path is slightly slower even when aligned to the LLC topology ({{cache_shard_size=28}}), we need to profile the execution and identify what is running "hotter" in the sharded configuration.
```






---
### [In Progress] [Task] [HCEPERF-1496](https://redhat.atlassian.net/browse/HCEPERF-1496) - 3sp - Krishna Magar - Verify reproducibility of 2% throughput gap between cache and cache_shard affinity scopes


**Description:**
```
Recent performance tests comparing {{default_affinity_scope=cache}} and {{cache_shard}} (with {{workqueue.cache_shard_size=28}} to match LLC) showed a slight performance regression of ~2% for the sharded approach at high concurrency (168 jobs).

* {{cache}}: ~383k IOPS
* {{cache_shard_size=28}}: ~377k IOPS

We need to determine if this 2% gap is a consistent, reproducible regression or simply within the standard margin of error (noise) for this test environment.
```






---
### [In Progress] [Bug] [HCEPERF-1493](https://redhat.atlassian.net/browse/HCEPERF-1493) - 2sp - Rajaditya Chauhan - Export Builder: quay image issue


**Description:**
```
from export builder getting : 

{noformat}Failed to pull image "quay.io/cloudservices/export-service:sha256-89660e98ac70e1ed98523914e3bf0dcab62a94ec65ac6b4dfd86baeec4c09fcb": [initializing source docker://quay.io/cloudservices/export-service:sha256-89660e98ac70e1ed98523914e3bf0dcab62a94ec65ac6b4dfd86baeec4c09fcb: unable to retrieve auth token: invalid username/password: unauthorized: Could not find robot with username: cloudservices+deployer and supplied password., initializing source docker://quay.io/cloudservices/export-service:sha256-89660e98ac70e1ed98523914e3bf0dcab62a94ec65ac6b4dfd86baeec4c09fcb: reading manifest sha256-89660e98ac70e1ed98523914e3bf0dcab62a94ec65ac6b4dfd86baeec4c09fcb in quay.io/cloudservices/export-service: unauthorized: access to the requested resource is not authorized]{noformat}

builder: [https://jenkins-csb-perf-master.dno.corp.redhat.com/job/InsightsInventory_Export_builder/11466/console|https://jenkins-csb-perf-master.dno.corp.redhat.com/job/InsightsInventory_Export_builder/11466/console]

from events:

{{error: deployment "export-service-service" exceeded its progress deadline}}
```






---
### [In Progress] [Bug] [HCEPERF-1492](https://redhat.atlassian.net/browse/HCEPERF-1492) - 2sp - Rajaditya Chauhan - HBI Export: runner.sh was not picking latest HBI DB creds 


**Description:**
```
error:

{noformat}psycopg2.OperationalError: connection to server at "host-inventory-perf.ciglpbbzvjwu.us-east-1.rds.amazonaws.com" (192.168.4.35), port 5432 failed: FATAL:  password authentication failed for user "postgres"{noformat}
```






---
### [In Progress] [Task] [HCEPERF-1491](https://redhat.atlassian.net/browse/HCEPERF-1491) - 1sp - Krishna Magar - Request permissions to access Perf&Scale Department Grafana via INTLAB


**Description:**
```
Request permissions to access Perf&Scale Department Grafana via an INTLAB ticket.
```






---
### [In Progress] [Task] [HCEPERF-1490](https://redhat.atlassian.net/browse/HCEPERF-1490) - 1sp - Krishna Magar - Request file storage with web interface access for test artifacts via INTLAB


**Description:**
```
Request file storage with read-only access via web interface (possibility to scp files somewhere and have them available via web server directory listing is perfectly sufficient) for test artifacts. Request this via an INTLAB ticket. If this service is not available, talk to jhutar again to figure out an alternative.
```






---
### [In Progress] [Task] [HCEPERF-1483](https://redhat.atlassian.net/browse/HCEPERF-1483) - 5sp - Krishna Magar - Add support to pass_or_fail OPL tool to fetch historical data from PostgreSQL


**Description:**
```
Add support to {{pass_or_fail}} OPL tool [https://github.com/redhat-performance/opl/blob/main/core/opl/investigator/README.md|https://github.com/redhat-performance/opl/blob/main/core/opl/investigator/README.md] to get historical data from PostgreSQL database. Take a quick look at the docs and talk to jhutar so we can discuss implementation details.
```






---
### [In Progress] [Task] [HCEPERF-1482](https://redhat.atlassian.net/browse/HCEPERF-1482) - 2sp - Krishna Magar - Coordinate with Release Engineering for RHEL release/nightly signal to trigger Jenkins


**Description:**
```
Get in touch with Release Engineering team to figure out how to get a signal when new RHEL release/nightly is available in [https://download.devel.redhat.com/|https://download.devel.redhat.com/] so we can trigger a Jenkins job based on that. Follow this process: [https://redhat.atlassian.net/wiki/spaces/SP/pages/333970499/File+a+JIRA+with+Software+Production|https://redhat.atlassian.net/wiki/spaces/SP/pages/333970499/File+a+JIRA+with+Software+Production]
```



**Comments:**

#### **Jan Hutar** (2026-06-02)
```
Hello [~accountid:70121:cdcb3870-d5c0-4d82-ac3a-0b20c312205a] ! Looking at [https://redhat.atlassian.net/wiki/spaces/SP/pages/333970499/File+a+JIRA+with+Software+Production|https://redhat.atlassian.net/wiki/spaces/SP/pages/333970499/File+a+JIRA+with+Software+Production] I seen your name, so figure I'll ask you directly. Could you please point me to somebody who could help me to figure out where we can find some signal for _"new RHEL release/nightly landed on_ [_https://download.devel.redhat.com/_|https://download.devel.redhat.com/]_"_? We want to run some our test every time this happens. I head something like that was available in UMB, but that is going away now, so I have no idea on where to look now.
```

#### **Lisa Smith** (2026-06-02)
```
You’ll want to ask the RHELDST team about this, as they are the ones that release the bits to CDN.  Pinging [~accountid:6358337efe5ff3752359dee3] [~accountid:70121:9bfc1e15-f831-42e6-ad56-f3be0513c063] [~accountid:712020:1daed54b-8595-48ed-a963-a8141efa0b50] to help get you started. If they don’t have the answer, they will know who you should ping next.
```

#### **Michal Haluza** (2026-06-03)
```
[https://download.devel.redhat.com/|https://download.devel.redhat.com/] is a HTTP server that makes /mnt/redhat content available, so I guess this would be a question for the team creating the composes. Pinging [~accountid:70121:d437710c-1a92-411a-9d57-86054816be34] (also cc [~accountid:712020:e7a85896-5643-4378-be1b-ebca4f6a672b] )
```

#### **Lubomir Sedlar** (2026-06-03)
```
UMB is the only source of the data for now: [https://datagrepper.engineering.redhat.com/raw?topic=/topic/VirtualTopic.eng.cts.compose-tagged|https://datagrepper.engineering.redhat.com/raw?topic=/topic/VirtualTopic.eng.cts.compose-tagged]

Eventually it will be replaced with Kafka, but I do not have a timeline for that.
```

#### **Krishna Magar** (2026-06-05)
```
Thanks everyone, this is very helpful. I appreciate the pointers and clarification.
```

#### **Jan Hutar** (2026-06-05)
```
Hello [~accountid:712020:e7a85896-5643-4378-be1b-ebca4f6a672b] . Is there a jira for tracking migration to Kafka?
```

#### **Lubomir Sedlar** (2026-06-05)
```
[~accountid:5a78c7f73297605c78217f31] [RHELCMP-14899|https://redhat.atlassian.net/browse/RHELCMP-14899]
```





---
### [In Progress] [Epic] [HCEPERF-1073](https://redhat.atlassian.net/browse/HCEPERF-1073) - Vishal Vijayraghavan - Perf&Scale validation of HCC gateways, phase 3


**Description:**
```
h3. Background
The Hybrid Cloud Console is going through the process of modernizing the architecture of its web gateways. This is a major change affecting the deployment topology as well as the tech stack used to implement the gateways.

More info:
* [ADR-081: Secure, token-agnostic identity object|https://docs.google.com/document/d/1XDMdKAff3ncmxsQl74g5GXtqfJ-M23sBjZEH4C03uDY/edit?tab=t.0]
* [ADR-077 Enable ConsoleDot Services to run on multiple clusters|https://docs.google.com/document/d/1VieGlokfGi5_pLfR54cHz_7U_s4cG-oDbFArIOHaL74/edit?tab=t.0]
* [ADR-080: Gateway Support in Multiple Clusters|https://docs.google.com/document/d/1YhFMyjLqBjJR88i3p6m0TCKsPxMBD7AB32iAebsHTyI/edit?tab=t.0]

These changes will require validation by the perf&scale team to validate the performance implications of the implemented changes

[Meeting minutes|https://docs.google.com/document/d/13LdsGt-zZ5wksbET94EhelX_cbLo5aoupmdMM01yNo8/edit?tab=t.0] from initial meeting.

h3. Goal
Goal of phase 3 is to evaluate the performance characteristics of transaction token signing (see ADR-081 for more information).
```






---
## New issues

### [In Progress] [Task] [HCEPERF-1497](https://redhat.atlassian.net/browse/HCEPERF-1497) - 3sp - Krishna Magar - Profile workqueue cache_shard path to identify CPU hotspots


**Description:**
```
Following the tests comparing {{cache}} and {{cache_shard}} affinity scopes, {{cache}} maintained a slight edge in throughput (~383k vs ~377k IOPS). To understand why the {{cache_shard}} path is slightly slower even when aligned to the LLC topology ({{cache_shard_size=28}}), we need to profile the execution and identify what is running "hotter" in the sharded configuration.
```






---
### [In Progress] [Task] [HCEPERF-1496](https://redhat.atlassian.net/browse/HCEPERF-1496) - 3sp - Krishna Magar - Verify reproducibility of 2% throughput gap between cache and cache_shard affinity scopes


**Description:**
```
Recent performance tests comparing {{default_affinity_scope=cache}} and {{cache_shard}} (with {{workqueue.cache_shard_size=28}} to match LLC) showed a slight performance regression of ~2% for the sharded approach at high concurrency (168 jobs).

* {{cache}}: ~383k IOPS
* {{cache_shard_size=28}}: ~377k IOPS

We need to determine if this 2% gap is a consistent, reproducible regression or simply within the standard margin of error (noise) for this test environment.
```






---
### [To Do] [Task] [HCEPERF-1495](https://redhat.atlassian.net/browse/HCEPERF-1495) - Pablo Mendez Hernandez - Disable content sources CPT


**Description:**
```
We do not have any requirements from the Business Unit for content sources. Lets disable content sources CPT
```






---
### [New] [Bug] [HCEPERF-1494](https://redhat.atlassian.net/browse/HCEPERF-1494) - Rajaditya Chauhan - HBI API: direct insertion error


**Description:**
```
{noformat}Error: column "canonical_facts" of relation "hosts" does not exist
LINE 4:             tags, canonical_facts, system_profile_facts, ans...
                          ^{noformat}

runner job: [https://jenkins-csb-perf-master.dno.corp.redhat.com/job/InsightsInventoryHBIPerfTest_runner/1399/console|https://jenkins-csb-perf-master.dno.corp.redhat.com/job/InsightsInventoryHBIPerfTest_runner/1399/console]
```






---
### [In Progress] [Bug] [HCEPERF-1493](https://redhat.atlassian.net/browse/HCEPERF-1493) - 2sp - Rajaditya Chauhan - Export Builder: quay image issue


**Description:**
```
from export builder getting : 

{noformat}Failed to pull image "quay.io/cloudservices/export-service:sha256-89660e98ac70e1ed98523914e3bf0dcab62a94ec65ac6b4dfd86baeec4c09fcb": [initializing source docker://quay.io/cloudservices/export-service:sha256-89660e98ac70e1ed98523914e3bf0dcab62a94ec65ac6b4dfd86baeec4c09fcb: unable to retrieve auth token: invalid username/password: unauthorized: Could not find robot with username: cloudservices+deployer and supplied password., initializing source docker://quay.io/cloudservices/export-service:sha256-89660e98ac70e1ed98523914e3bf0dcab62a94ec65ac6b4dfd86baeec4c09fcb: reading manifest sha256-89660e98ac70e1ed98523914e3bf0dcab62a94ec65ac6b4dfd86baeec4c09fcb in quay.io/cloudservices/export-service: unauthorized: access to the requested resource is not authorized]{noformat}

builder: [https://jenkins-csb-perf-master.dno.corp.redhat.com/job/InsightsInventory_Export_builder/11466/console|https://jenkins-csb-perf-master.dno.corp.redhat.com/job/InsightsInventory_Export_builder/11466/console]

from events:

{{error: deployment "export-service-service" exceeded its progress deadline}}
```






---
### [In Progress] [Bug] [HCEPERF-1492](https://redhat.atlassian.net/browse/HCEPERF-1492) - 2sp - Rajaditya Chauhan - HBI Export: runner.sh was not picking latest HBI DB creds 


**Description:**
```
error:

{noformat}psycopg2.OperationalError: connection to server at "host-inventory-perf.ciglpbbzvjwu.us-east-1.rds.amazonaws.com" (192.168.4.35), port 5432 failed: FATAL:  password authentication failed for user "postgres"{noformat}
```






---
### [In Progress] [Task] [HCEPERF-1491](https://redhat.atlassian.net/browse/HCEPERF-1491) - 1sp - Krishna Magar - Request permissions to access Perf&Scale Department Grafana via INTLAB


**Description:**
```
Request permissions to access Perf&Scale Department Grafana via an INTLAB ticket.
```






---
### [In Progress] [Task] [HCEPERF-1490](https://redhat.atlassian.net/browse/HCEPERF-1490) - 1sp - Krishna Magar - Request file storage with web interface access for test artifacts via INTLAB


**Description:**
```
Request file storage with read-only access via web interface (possibility to scp files somewhere and have them available via web server directory listing is perfectly sufficient) for test artifacts. Request this via an INTLAB ticket. If this service is not available, talk to jhutar again to figure out an alternative.
```






---
### [New] [Task] [HCEPERF-1489](https://redhat.atlassian.net/browse/HCEPERF-1489) - 5sp - Krishna Magar - Research and configure Jenkins email notifications and request service account


**Description:**
```
* Research and configure Jenkins to be able to send emails (probably [https://plugins.jenkins.io/email-ext/|https://plugins.jenkins.io/email-ext/]).
* Configure it and enhance test job to send email.
* Raise a request to IT to get a service account we can use for this. Example for configuration: [https://gitlab.cee.redhat.com/ccit/jenkins-csb-customers/insights-fdns-casc-main/-/blob/main/casc.yaml?ref_type=heads#L509|https://gitlab.cee.redhat.com/ccit/jenkins-csb-customers/insights-fdns-casc-main/-/blob/main/casc.yaml?ref_type=heads#L509]
```






---
### [In Progress] [Task] [HCEPERF-1488](https://redhat.atlassian.net/browse/HCEPERF-1488) - 1sp - Krishna Magar - Request PostgreSQL database with read-write and read-only accounts via INTLAB


**Description:**
```
Request a PostgreSQL database via INTLAB jira (Perf department Integration Lab) (example: [INTLAB-459|https://issues.redhat.com/browse/INTLAB-459]). The database should have two accounts:

* One read-write account for uploading results.
* One read-only account for accessing from Grafana.
```






---
### [New] [Task] [HCEPERF-1487](https://redhat.atlassian.net/browse/HCEPERF-1487) - 3sp - Krishna Magar - Create Jenkinsfile and JOBDSL config for the database CPT workflow


**Description:**
```
Create a Jenkinsfile and JOBDSL config to run the whole database CPT workflow (PostgreSQL + HammerDB) and get it running in the Jenkins. Examples for reference:

* Jenkinsfile: [https://gitlab.cee.redhat.com/redhat-performance/ci-configs/-/blob/master/jenkins/UtilArtifactsCleaner.groovy?ref_type=heads|https://gitlab.cee.redhat.com/redhat-performance/ci-configs/-/blob/master/jenkins/UtilArtifactsCleaner.groovy?ref_type=heads]
* JOBDSL: [https://gitlab.cee.redhat.com/redhat-performance/ci-configs/-/blob/master/src/jobs/UtilArtifactsCleanerJob.groovy?ref_type=heads|https://gitlab.cee.redhat.com/redhat-performance/ci-configs/-/blob/master/src/jobs/UtilArtifactsCleanerJob.groovy?ref_type=heads]

Note: For now, no alert emails when regression is detected, make it simple.
```






---
### [New] [Task] [HCEPERF-1486](https://redhat.atlassian.net/browse/HCEPERF-1486) - 5sp - Krishna Magar - Create initial Grafana dashboard for database CPT performance monitoring


**Description:**
```
Create initial basic Grafana dashboard that allows filtering by HW (e.g. "R650" vs. "R640") and RHEL main version (e.g. "RHEL9" vs. "RHEL10"). The dashboard should show:

* Graphs for TPM/NOPM.
* Core performance monitoring metrics (CPU, memory, disk, network usage on the PostgreSQL SUT node and on test runner client node (node that runs HammerDB)).
* A table/graph showing PASS/FAIL data and possibly some additional config.
```






---
### [New] [Task] [HCEPERF-1485](https://redhat.atlassian.net/browse/HCEPERF-1485) - 3sp - Krishna Magar - Update playbook to upload master JSON to PostgreSQL and test artifacts to file storage


**Description:**
```
Alter relevant playbook (or create new one) to upload main JSON file to PostgreSQL database and all test artefacts to file storage for archival purposes. There will be "data" table in the DB with:

* id column
* datetime column (when the test run started)
* JSONB column (we will upload main JSON file with all the data here)
```






---
### [New] [Task] [HCEPERF-1484](https://redhat.atlassian.net/browse/HCEPERF-1484) - 3sp - Krishna Magar - Create initial config for pass_or_fail and update playbook to detect regressions


**Description:**
```
* Create initial basic config file for {{pass_or_fail}} tool that allows us to say if current result is regression or not (see [https://github.com/redhat-performance/opl/blob/main/core/opl/investigator/README.md|https://github.com/redhat-performance/opl/blob/main/core/opl/investigator/README.md] for documentation).
* Change the relevant playbook to run {{pass_or_fail}} to detect regressions and add pass/fail result to the master JSON before it gets uploaded to the DB.
```






---
### [In Progress] [Task] [HCEPERF-1483](https://redhat.atlassian.net/browse/HCEPERF-1483) - 5sp - Krishna Magar - Add support to pass_or_fail OPL tool to fetch historical data from PostgreSQL


**Description:**
```
Add support to {{pass_or_fail}} OPL tool [https://github.com/redhat-performance/opl/blob/main/core/opl/investigator/README.md|https://github.com/redhat-performance/opl/blob/main/core/opl/investigator/README.md] to get historical data from PostgreSQL database. Take a quick look at the docs and talk to jhutar so we can discuss implementation details.
```






---
### [In Progress] [Task] [HCEPERF-1482](https://redhat.atlassian.net/browse/HCEPERF-1482) - 2sp - Krishna Magar - Coordinate with Release Engineering for RHEL release/nightly signal to trigger Jenkins


**Description:**
```
Get in touch with Release Engineering team to figure out how to get a signal when new RHEL release/nightly is available in [https://download.devel.redhat.com/|https://download.devel.redhat.com/] so we can trigger a Jenkins job based on that. Follow this process: [https://redhat.atlassian.net/wiki/spaces/SP/pages/333970499/File+a+JIRA+with+Software+Production|https://redhat.atlassian.net/wiki/spaces/SP/pages/333970499/File+a+JIRA+with+Software+Production]
```



**Comments:**

#### **Jan Hutar** (2026-06-02)
```
Hello [~accountid:70121:cdcb3870-d5c0-4d82-ac3a-0b20c312205a] ! Looking at [https://redhat.atlassian.net/wiki/spaces/SP/pages/333970499/File+a+JIRA+with+Software+Production|https://redhat.atlassian.net/wiki/spaces/SP/pages/333970499/File+a+JIRA+with+Software+Production] I seen your name, so figure I'll ask you directly. Could you please point me to somebody who could help me to figure out where we can find some signal for _"new RHEL release/nightly landed on_ [_https://download.devel.redhat.com/_|https://download.devel.redhat.com/]_"_? We want to run some our test every time this happens. I head something like that was available in UMB, but that is going away now, so I have no idea on where to look now.
```

#### **Lisa Smith** (2026-06-02)
```
You’ll want to ask the RHELDST team about this, as they are the ones that release the bits to CDN.  Pinging [~accountid:6358337efe5ff3752359dee3] [~accountid:70121:9bfc1e15-f831-42e6-ad56-f3be0513c063] [~accountid:712020:1daed54b-8595-48ed-a963-a8141efa0b50] to help get you started. If they don’t have the answer, they will know who you should ping next.
```

#### **Michal Haluza** (2026-06-03)
```
[https://download.devel.redhat.com/|https://download.devel.redhat.com/] is a HTTP server that makes /mnt/redhat content available, so I guess this would be a question for the team creating the composes. Pinging [~accountid:70121:d437710c-1a92-411a-9d57-86054816be34] (also cc [~accountid:712020:e7a85896-5643-4378-be1b-ebca4f6a672b] )
```

#### **Lubomir Sedlar** (2026-06-03)
```
UMB is the only source of the data for now: [https://datagrepper.engineering.redhat.com/raw?topic=/topic/VirtualTopic.eng.cts.compose-tagged|https://datagrepper.engineering.redhat.com/raw?topic=/topic/VirtualTopic.eng.cts.compose-tagged]

Eventually it will be replaced with Kafka, but I do not have a timeline for that.
```

#### **Krishna Magar** (2026-06-05)
```
Thanks everyone, this is very helpful. I appreciate the pointers and clarification.
```

#### **Jan Hutar** (2026-06-05)
```
Hello [~accountid:712020:e7a85896-5643-4378-be1b-ebca4f6a672b] . Is there a jira for tracking migration to Kafka?
```

#### **Lubomir Sedlar** (2026-06-05)
```
[~accountid:5a78c7f73297605c78217f31] [RHELCMP-14899|https://redhat.atlassian.net/browse/RHELCMP-14899]
```





---


# Satellite
## Finished issues

### [Closed/Done] [Task] [SAT-46022](https://redhat.atlassian.net/browse/SAT-46022) - 3sp - Pablo Mendez Hernandez - contperf: Re-enable downstream image overrides for foremanctl


**Description:**
```
Re-enable downstream (registry.stage.redhat.io) image overrides for foremanctl deployments in doit.sh:

* Uncomment core image overrides (candlepin, foreman, foreman-proxy, pulp, postgresql, redis) for foremanctl deployments
* Default use_downstream_images to true
* Pass sat_version directly instead of mapping foremanctl to stream
* Uncomment HOST_NAMES -> kvm_host_names assignment for QUADS integration

Commit: [https://gitlab.cee.redhat.com/redhat-performance/contperf/-/commit/e0d8999c97f3|https://gitlab.cee.redhat.com/redhat-performance/contperf/-/commit/e0d8999c97f3]
```





**Linked Pull Requests & Merge Requests**

#### PR/MR: https://gitlab.cee.redhat.com/redhat-performance/contperf/-/commit/e0d8999c97f3
```
Commit Message:
feat(doit.sh): Re-enable downstream image overrides and simplify setup

- Uncomment core image overrides (registry-based candlepin, foreman,
  foreman-proxy, pulp, postgresql, redis) for foremanctl deployments
- Default use_downstream_images to true
- Pass sat_version directly instead of mapping foremanctl to stream
- Comment out VM setup/common block (handled externally for now)
- Uncomment HOST_NAMES -> kvm_host_names assignment

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```



---
### [Closed/Done] [Task] [SAT-46021](https://redhat.atlassian.net/browse/SAT-46021) - 5sp - Pablo Mendez Hernandez - satperf: Improve foremanctl role deployment debugging


**Description:**
```
Improve the foremanctl Ansible role with better deployment diagnostics:

* Display images.yml content after override_images for verification
* Show stderr output for pull-images, deploy, and add-features steps
* Move EL9 COPR enable inside Foreman product block (was running unconditionally for Satellite)
* Reorder features: hammer before foreman-proxy

Commit: [https://github.com/redhat-performance/satperf/commit/e546d739f3e9|https://github.com/redhat-performance/satperf/commit/e546d739f3e9]
```





**Linked Pull Requests & Merge Requests**

#### PR/MR: https://github.com/redhat-performance/satperf/commit/e546d739f3e9
```
Commit Message:
.commit.message
```



---
### [Closed/Done] [Task] [SAT-46011](https://redhat.atlassian.net/browse/SAT-46011) - 2sp - Pablo Mendez Hernandez - contperf: Extract DDNS cleanup to reusable lib/utils.sh


**Description:**
```
Move the inline DDNS entry deletion logic from doit.sh into a reusable ddns_cleanup() function in lib/utils.sh. Adds dot-prefix matching to avoid partial suffix collisions.

Commit: [https://gitlab.cee.redhat.com/redhat-performance/contperf/-/commit/063b933e8f5f|https://gitlab.cee.redhat.com/redhat-performance/contperf/-/commit/063b933e8f5f]
```





**Linked Pull Requests & Merge Requests**

#### PR/MR: https://gitlab.cee.redhat.com/redhat-performance/contperf/-/commit/063b933e8f5f
```
Commit Message:
refactor(doit.sh): Extract DDNS cleanup to lib/utils.sh

Move the inline DDNS entry deletion logic into a reusable
ddns_cleanup() function. Adds dot-prefix matching to avoid
partial suffix collisions.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```



---
### [Closed/Done] [Task] [SAT-46010](https://redhat.atlassian.net/browse/SAT-46010) - 3sp - Pablo Mendez Hernandez - satperf: Support append mode in override_images role


**Description:**
```
Add append mode to the override_images role alongside the existing overwrite mode. Content starting with a newline is appended via blockinfile with SATPERF OVERRIDE markers; content starting with --- overwrites the entire images.yml. Both file paths and inline strings are handled uniformly through slurp + set_fact.

Commit: [https://github.com/redhat-performance/satperf/commit/de2b60c0b70f|https://github.com/redhat-performance/satperf/commit/de2b60c0b70f]
```





**Linked Pull Requests & Merge Requests**

#### PR/MR: https://github.com/redhat-performance/satperf/commit/de2b60c0b70f
```
Commit Message:
.commit.message
```



---
### [Closed/Done] [Task] [SAT-46009](https://redhat.atlassian.net/browse/SAT-46009) - 2sp - Pablo Mendez Hernandez - satperf: Fix num_container_hosts division by zero in hammer.sh


**Description:**
```
When running experiment scripts directly (not via doit.sh), num_container_hosts was unset, causing a division by zero in the batch size calculation for incremental concurrent execution.

Fixed by defaulting to get_num_hosts if not already defined.

Commit: [https://github.com/redhat-performance/satperf/commit/28033846e72a|https://github.com/redhat-performance/satperf/commit/28033846e72a]
```





**Linked Pull Requests & Merge Requests**

#### PR/MR: https://github.com/redhat-performance/satperf/commit/28033846e72a
```
Commit Message:
.commit.message
```



---
### [Closed/Done] [Task] [SAT-46008](https://redhat.atlassian.net/browse/SAT-46008) - 2sp - Pablo Mendez Hernandez - satperf: Refactor test_campaign_fam to use phased lib calls


**Description:**
```
Replace the 700+ line inline test_campaign_fam.sh script with the phased execution pattern using run-library functions: check_env, create_lces_fam, prepare_rh_content_fam, get_base_content_fam, concurrent_execution, sosreport, and junit_upload.

Commit: [https://github.com/redhat-performance/satperf/commit/42228e5ea880|https://github.com/redhat-performance/satperf/commit/42228e5ea880]
```





**Linked Pull Requests & Merge Requests**

#### PR/MR: https://github.com/redhat-performance/satperf/commit/42228e5ea880
```
Commit Message:
.commit.message
```



---
### [Closed/Done] [Task] [SAT-46007](https://redhat.atlassian.net/browse/SAT-46007) - 2sp - Pablo Mendez Hernandez - ansible-kvm-host-mgr: Skip volume wiping during VM erasure to save ~40 min per run


**Description:**
```
The erase-vms.yaml playbook in ansible-kvm-host-mgr had volume wiping (zeroing data before deletion) hardcoded to true. On large topologies with ~32 volumes including 2TB data disks, this added ~40 minutes of serial I/O per run.

Made wiping optional via a wipe_volumes parameter (default: false). Pass -e wipe_volumes=true to restore the old behavior.

Commit: [https://gitlab.cee.redhat.com/redhat-performance/ansible-kvm-host-mgr/-/commit/dfca47294561|https://gitlab.cee.redhat.com/redhat-performance/ansible-kvm-host-mgr/-/commit/dfca47294561]
```





**Linked Pull Requests & Merge Requests**

#### PR/MR: https://gitlab.cee.redhat.com/redhat-performance/ansible-kvm-host-mgr/-/commit/dfca47294561
```
Commit Message:
perf(erase-vms): Make volume wiping optional, default to false

Volume wiping (zeroing data before deletion) was hardcoded to true,
adding ~40 minutes of I/O per run on large topologies. For perf
testing VMs that get rebuilt every run, wiping is unnecessary.

Pass -e wipe_volumes=true to restore the old behavior.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```



---
### [Closed/Done] [Task] [SAT-45997](https://redhat.atlassian.net/browse/SAT-45997) - 7sp - Pablo Mendez Hernandez - satperf: Migrate FAM playbooks to Pattern B with unified content_views API


**Description:**
```
Migrate the core FAM playbooks from the old single-CV module calls to Pattern B (direct Katello API POST + wait_for_task) with server-side task duration extraction and a unified content_views list API.

Changes:

* New shared includes: fam_common_vars.yaml (connection variables), fam_wait_and_print.yaml (unified fire-wait-print pattern supporting both Pattern A async and Pattern B wait_for_task), wait_for_task.yaml (Foreman task wait wrapper)
* cv_publish.yaml: Rewritten to loop over content_views list with API POST to /katello/api/content_views/{id}/publish
* cv_version_promote.yaml: Unified CV/CCV promote via content_views list API with /katello/api/content_view_versions/{id}/promote
* repo_sync.yaml: Migrated to Pattern B with fam_wait_and_print for server-side duration extraction
* kill_pending_tasks.yaml: Normalized to use fam_common_vars connection variables
* 16 playbooks: Added descriptive play names for Ansible output readability
* Removed: wait_for_task.yaml (replaced by fam_wait_and_print.yaml)

Commits:

* [https://github.com/redhat-performance/satperf/commit/53cd27f56484|https://github.com/redhat-performance/satperf/commit/53cd27f56484]
* [https://github.com/redhat-performance/satperf/commit/d6914714b881|https://github.com/redhat-performance/satperf/commit/d6914714b881]
* [https://github.com/redhat-performance/satperf/commit/e908d6032310|https://github.com/redhat-performance/satperf/commit/e908d6032310]
* [https://github.com/redhat-performance/satperf/commit/e...
```





**Linked Pull Requests & Merge Requests**

#### PR/MR: https://github.com/redhat-performance/satperf/commit/ee768c89cc36
```
Commit Message:
.commit.message
```

#### PR/MR: https://github.com/redhat-performance/satperf/commit/e908d6032310
```
Commit Message:
.commit.message
```

#### PR/MR: https://github.com/redhat-performance/satperf/commit/7c0b92e13454
```
Commit Message:
.commit.message
```

#### PR/MR: https://github.com/redhat-performance/satperf/commit/53cd27f56484
```
Commit Message:
.commit.message
```

#### PR/MR: https://github.com/redhat-performance/satperf/commit/e3d2f36b3de0
```
Commit Message:
.commit.message
```

#### PR/MR: https://github.com/redhat-performance/satperf/commit/d6914714b881
```
Commit Message:
.commit.message
```



---
### [Closed/Done] [Task] [SAT-45992](https://redhat.atlassian.net/browse/SAT-45992) - 3sp - Imaanpreet Kaur - share monthly report with stakeholders - May 2026







---
### [Closed/Done] [Spike] [SAT-45801](https://redhat.atlassian.net/browse/SAT-45801) - 5sp - Pablo Mendez Hernandez - SPIKE - Investigate UI performance regression-finding and diagnostics producer contract for Satellite


**Description:**
```
Investigate and define how satperf should produce normalized UI performance run manifests and artifacts for a separate regression-finding and diagnosis project.

This spike is investigation-only. It is intended to clarify architecture, ownership boundaries, data contracts, and required observability evidence for UI regression analysis in Satellite.

Scope of the investigation:

* Define the producer/consumer boundary between satperf and the external regression-finding project.
* Define the normalized run-manifest contract for browser-based UI runs.
* Define which browser, role, platform, monitoring, and profiling dimensions satperf must emit.
* Define how UI runs correlate with resource-consumption monitoring and profiling artifacts captured during the same run window.
* Identify the minimal runtime-generated diagnostics satperf can emit cheaply for downstream analysis.
* Identify gaps in current satperf observability that matter for UI regression-finding and diagnosis.

Expected outcome:

* A documented producer contract for satperf.
* A proposed normalized manifest and artifact model for the external consumer project.
* A clear list of follow-up tasks needed to implement the producer side and enable downstream regression analysis.

Out of scope for this spike:

* Implementing the full regression-finding engine inside satperf.
* Defining historical-comparison policy inside satperf.
* Committing to a full diagnosis engine implementation in this effort.
```






---
## In review issues

### [Review] [Sub-task] [SAT-45994](https://redhat.atlassian.net/browse/SAT-45994) - 5sp - Imaanpreet Kaur - Add SSH Tunnel Instructions for Grafana




**Comments:**

#### **Imaanpreet Kaur** (2026-06-08)
```
PR created - [https://github.com/theforeman/foreman-documentation/pull/4912|https://github.com/theforeman/foreman-documentation/pull/4912|smart-link] 
```




**Linked Pull Requests & Merge Requests**

#### PR/MR: https://github.com/theforeman/foreman-documentation/pull/4912
```
Title: Add SSH tunnel documentation for remote Grafana access
  - Add new section 'Accessing Grafana remotely using an SSH tunnel'
  - Include Linux/macOS command-line instructions
  - Include Windows PuTTY GUI-based setup instructions
  - Include Windows PowerShell/OpenSSH instructions
  - Add background tunnel setup and teardown instructions

  This addresses the common issue where users cannot directly access
  http://localhost:3000 on the Satellite/Foreman server from their
  remote workstation.

  File modified:
  - guides/common/modules/proc_retrieving-metrics-in-the-web-ui.adoc

#### What changes are you introducing?

#### Why are you introducing these changes? (Explanation, links to references, issues, etc.)

#### Anything else to add? (Considerations, potential downsides, alternative solutions you have explored, etc.)

#### Contributor checklists

* [x] I am okay with my commits getting squashed when you merge this PR.
* [ ] I am familiar with the [contributing](https://git...
```



---
### [Review] [Sub-task] [SAT-45993](https://redhat.atlassian.net/browse/SAT-45993) - 3sp - Imaanpreet Kaur - Replace PCP commands. pmval → pmrep




**Comments:**

#### **Imaanpreet Kaur** (2026-06-04)
```
Research indicates that the command *pmrep(1)* should replace *pmval(1)* due to its capability to monitor multiple metrics simultaneously, offer flexible output formatting (CSV, JSON, table), and consolidate functionalities from various tools into a single interface. The document provides several examples demonstrating how to update existing commands from *pmval* to *pmrep* for different use cases, including archiving and time specifications. The proposed changes enhance the efficiency and consistency of monitoring commands in the PCP toolkit.

*Example 1*

{quote}  *OLD (current docs):*

  pmval -f 1 disk.partitions.write

  *NEW (what to replace it with):*

  pmrep disk.partitions.write{quote}

*Example 2*

{quote}  *OLD* *(current* *docs):*

  pmval --archive /var/log/pcp/pmlogger/satellite.example.com/20230831.00.10 \

    -f 1 disk.partitions.write

  *NEW (what to replace it with):*

  pmrep -a /var/log/pcp/pmlogger/satellite.example.com/20230831.00.10 \

    disk.partitions.w...
```

#### **Imaanpreet Kaur** (2026-06-05)
```
PR - [https://github.com/theforeman/foreman-documentation/pull/4909|https://github.com/theforeman/foreman-documentation/pull/4909|smart-link] 
```




**Linked Pull Requests & Merge Requests**

#### PR/MR: https://github.com/theforeman/foreman-documentation/pull/4909
```
Title: Replace pmval and pmstat with pmrep in PCP metrics documentation   - …
…Replace pmval with pmrep for live metrics retrieval

  - Replace pmval --archive with pmrep -a for archived metrics
  - Replace pmstat with pmrep using SAR metric sets (:sar-u, :sar-r, :sar-d)
  - Remove deprecated flags (-f, -d) that are not needed with pmrep

  Benefits:
  - pmrep can monitor multiple metrics in a single command
  - Consolidates multiple tools (pmval, pmstat) into one consistent interface
  - Provides better output formatting options (CSV, JSON, table)
  - Reduces cognitive load for readers learning PCP monitoring

#### What changes are you introducing?

#### Why are you introducing these changes? (Explanation, links to references, issues, etc.)

#### Anything else to add? (Considerations, potential downsides, alternative solutions you have explored, etc.)

#### Contributor checklists

* [x] I am okay with my commits getting squashed when you merge this PR.
* [ ] I am familiar with the ...
```



---
### [Review] [Bug] [SAT-31994](https://redhat.atlassian.net/browse/SAT-31994) - 3sp -  - Error on "Synchronize Capsule" task: (Katello::Errors::Pulp3Error) - ErrorDetail(string='This field must be unique.', code='unique')


**Description:**
```
*Description of problem:*

A "Synchronize Capsule" task fails when performing a Library sync just after finishing downloading content to the Satellite server.

*How reproducible:*

It's not very easy to reproduce: maybe 1 out of 5 tries:

*Is this issue a regression from an earlier version:*

We don't know. We are adding more coverage to our sync tests and we've seen these errors in both Stream and 6.17.0.

I'll make sure to test it in previous releases for confirmation. 

*Steps to Reproduce:*

1. Sync big RPM repositories (in this case, RHEL 6 and/or RHEL 7 related ones) to the Satellite

2. Synchronize Library to some capsule(s)

3.

*Actual behavior:*
After downloading several RPM repositories, in our case and in that order:
 * Red Hat Enterprise Linux 7 Server - Extended Life Cycle Support RPMs x86_64
 * Red Hat Enterprise Linux 7 Server Kickstart x86_64 7.9
 * Red Hat Enterprise Linux 7 Server - Extras RPMs x86_64

an immediate capsule Library synchronization may end up in Warning state with the following error and backtrace:

 
{code:java}
2025-03-21T12:18:37 [E|bac|ac8e083a] {'base_path': [ErrorDetail(string='This field must be unique.', code='unique')], 'name': [ErrorDetail(string='This field must be unique.', code='unique')]} (Katello::Errors::Pulp3Error)
 ac8e083a | /usr/share/gems/gems/katello-4.16.0/app/lib/actions/pulp3/abstract_async_task.rb:107:in `block in check_for_errors'
 ac8e083a | /usr/share/gems/gems/katello-4.16.0/a...
```





**Linked Pull Requests & Merge Requests**

#### PR/MR: https://github.com/Katello/katello/pull/11700
```
Title: Fixes #39211 - Refresh capsule distributions atomically after all syncs
## Problem

When `SyncCapsule` runs multiple repos concurrently, each repo's `RefreshDistribution` was planned inline inside `GenerateMetadata`. Two repos sharing the same Pulp3 distribution (same `base_path`/`name`) could race to create it. The loser fails with a uniqueness `Pulp3Error` that surfaces only during async task polling - too late for a service-level rescue to catch.

Observed under concurrent capsule sync stress tests across multiple content types (RPM, container). Tracked in SAT-31994.

## Solution

Two changes working together:

**1. `RefreshAllDistributions` - new post-sync action**

Move distribution refresh out of per-repo `GenerateMetadata` into a single `RefreshAllDistributions` action planned by `SyncCapsule` after all sync batches complete. Distributions for all repos are refreshed concurrently (`concurrence` block).

This also gives consumers a more consistent view of the capsule: c...
```



---
### [Review] [Story] [SAT-31672](https://redhat.atlassian.net/browse/SAT-31672) - 13sp - Pablo Mendez Hernandez - Improve Repo sync and Capsule sync testing to mimic end-user operations


**Description:**
```
As discussed with Imaan and other participants of the SD\QE\Dev\Perf cadence sync-up with Pune team, I am outlining what I had in my mind about testing out concurrent capsule sync performances by mimicking end-user operations. 

 

*Flow:* 
 * Install a Satellite and two capsules 

 * Import a manifest in satellite with some standard RHEL subs ( or Employee SKU ) 

 * Create a two lifecycle environment path like 
{code:java}
Library --> QA --> Prod
Library --> Dev --> Test{code}

 * Edit *Capsule 1* and add {*}Library{*}, *QA* and *Prod* for content syncing 

 * Edit *Capsule 2* and add {*}Library{*}, *Dev* and *Test* for content syncing

 * Now, it's a good time to start monitoring the satellite and capsule's load, resource utilization etc and also, at the end of everything, find out how much time it took to complete all the Capsule sync tasks and Update Content Count tasks to complete

 * Enable and sync the following repos in Satellite and ({*}on_demand{*}) sync them batchwise [ e.g. *bulk-sync one batch and then when sync completed, bulk-sync the next batch* ]

*Batch 1:  ( RHEL7_CV )*
{code:java}
Red Hat Enterprise Linux 7 Server - Extended Life Cycle Support RPMs x86_64
Red Hat Enterprise Linux 7 Server - Extras RPMs x86_64
Red Hat Enterprise Linux 7 Server Kickstart x86_64 7.9
Red Hat Enterprise Linux 7 Server RPMs x86_64 7Server
Red Hat Satellite Client 6 for RHEL 7 Server - ELS RPMS x86_64
Red Hat Satellite Client 6 for RHEL 7 Server R...
```






---
## In progress issues

### [In Progress] [Story] [SAT-45959](https://redhat.atlassian.net/browse/SAT-45959) - 5sp - Imaanpreet Kaur - Performance Optimization: Use a cache of existing artifacts during sync


**Description:**
```
*Description of problem:*

 Pulp performs an excessive number of database queries during the process of looking up which artifacts have already been saved during immediate syncs

*How reproducible:*

 Very

*Is this issue a regression from an earlier version:*

 No

*Steps to Reproduce:*

Perform the following on a patched and unpatched system. 

# Sync a medium-sized repository in “immediate” mode
# Sync it again, with the sync optimizations turned off, measuring the total runtime of an “immediate” sync where nothing has changed and nothing needs to downloaded

 The measured time required for step 2 on the patched system should be substantially less.

*Actual behavior:*
[Describe the issue in detail, including what is happening and where]

*Expected behavior:*
[Describe what should be happening instead]

*Business Impact / Additional info:*

 
```



**Comments:**

#### **Daniel Alley** (2026-06-03)
```
This is related to [https://redhat.atlassian.net/browse/SAT-45821|https://redhat.atlassian.net/browse/SAT-45821|smart-link]  and can be tested at the same time
```





---
### [In Progress] [Story] [SAT-45821](https://redhat.atlassian.net/browse/SAT-45821) - 5sp - Imaanpreet Kaur - Performance / Memory optimization: Use a cache of existing Package objects from the latest repo version during sync 


**Description:**
```
The existing Pulp sync pipeline works as follows (simplified to what matters):

1. Parse the repository metadata, create unsaved Package model objects
2. For any model objects marked unsaved, query existing package objects which have the same natural key and replace the unsaved model with the existing one
3. Save any remaining unsaved models
4. Download artifacts etc. etc.

If, in step 1, we build a cache of existing Package model objects that were present in the previous repository version, then for subsequent syncs where a high degree of overlap is expected, a lot of work can be avoided throughout the sync pipeline.  The cache requires less queries to populate and uses more efficient queries than the QueryExistingContents pipeline stage, so handling as much of the work up-front based on the cache should reduce database load and overall runtime, and also avoid the memory and FFI overhead of materializing millions of strings representing the package “filelists” into Python.

The measured impact of a patch which implements this cache is an approximately 30-60% reduction in sync time (of an already-synced RHEL9 BaseOS repo, on-demand, with the nothing-changed sync optimization turned off). This is highly situationally dependent and so the numbers themselves are variable, but the average net impact is expected to be high with no real downsides (perhaps a slight regression in the rare scenario where a user changes the remote URL, making the cache useless).

An 87% reduction in...
```



**Comments:**

#### **Daniel Alley** (2026-06-03)
```
This is now released upstream in pulp-rpm

I would expect most syncs and resyncs, including of repos that were previously deemed “pathological” would now use under 1gb of memory during sync. As well as significant performance improvements.
```





---
## New issues

### [Release Pending - Upstream] [Bug] [SAT-46106](https://redhat.atlassian.net/browse/SAT-46106) - Pablo Mendez Hernandez - Eliminate redundant Candlepin GETs during host registration


**Description:**
```
POST /rhsm/consumers makes 3 Candlepin HTTP calls per registration: 1 POST (unavoidable) + 2 redundant GETs that fetch data already available in the POST response. Eliminating the 2 redundant GETs reduces Candlepin calls by 66% per registration and removes 2 DB SELECTs (Host.find re-fetch in finalize_registration, host.reload in consumer_activate).
```






---
### [Release Pending - Upstream] [Bug] [SAT-46105](https://redhat.atlassian.net/browse/SAT-46105) - 2sp - Pablo Mendez Hernandez - Concurrent registration fails with "PG::UniqueViolation: ERROR: duplicate key value violates unique constraint \"index_operatingsystems_on_title\"


**Description:**
```
*Description of problem:*

While testing concurrent registrations in batches we see the following error leading to some hosts (2, 3 usually) with the same OS version failing to register:

{code:java}PG::UniqueViolation: ERROR:  duplicate key value violates unique constraint "index_operatingsystems_on_title"
DETAIL:  Key (title)=(RedHat 9.2) already exists.{code}

After these errors, the rest of registrations work without problems.

 

*How reproducible:*

We see it frequently in our test runs.

 

*Is this issue a regression from an earlier version:*

It’s new in 6.19.

 

*Steps to Reproduce:*

1. Set up concurrent registrations with enough concurrency (in our tests with around 50 concurrent content hosts)

2. Check registration logs

 

*Actual behavior:*

The affected hosts fail to register initially but success in the next try.

 

We can see the following in production.log:

 

{code:java}[root@satellite ~]# grep f7522f9e  /var/log/foreman/production.log
2026-03-09T12:40:36 [I|app|f7522f9e] Started POST "/rhsm/consumers?owner=Default_Organization&activation_keys=AK_8_Test" for 10.1.61.8 at 2026-03-09 12:40:36 +0000
2026-03-09T12:40:36 [I|app|f7522f9e] Processing by Katello::Api::Rhsm::CandlepinProxiesController#consumer_activate as JSON
2026-03-09T12:40:36 [I|app|f7522f9e]   Parameters: {"type"=>"system", "name"=>"el8-u-a-1-container016.red.ddns.perf.redhat.com", "facts"=>"[FILTERED]", "installedProducts"=>[{"productId"=>"479", "productName"=>"Red Hat Enterprise L...
```






---
### [New] [Bug] [SAT-46099](https://redhat.atlassian.net/browse/SAT-46099) - 5sp - Imaanpreet Kaur - Sync memory consumption too high in pathological cases


**Description:**
```
Several repositories, including but not limited to

[https://yum.oracle.com/repo/OracleLinux/OL9/developer/x86_64/|https://yum.oracle.com/repo/OracleLinux/OL9/developer/x86_64/]
[https://packages.cloud.google.com/yum/repos/cloud-sdk-el9-x86_64/|https://packages.cloud.google.com/yum/repos/cloud-sdk-el9-x86_64/]
[https://artifacts.elastic.co/packages/8.x/yum/|https://artifacts.elastic.co/packages/8.x/yum/]
[https://packages.grafana.com/oss/rpm/|https://packages.grafana.com/oss/rpm/]
 

Are known to cause very high memory consumption of pulp_rpm when synced - often more than 6gb or as high as 10gb for the OL9 developer repo.  The cause of this is having many different versions of packages with very long and extensive "filelists" as the strings representing those files are held for a long time prior to the package being saved.  We need to reduce the peak memory usage.

 

[https://github.com/pulp/pulp_rpm/issues/4086|https://github.com/pulp/pulp_rpm/issues/4086]
```



**Comments:**

#### **SFDC Integration** (2026-06-08)
```
[~accountid:70121:5cc8098d-d586-4c99-8ac8-18ba201fc97d] cloned SAT-42697. Copied SFDC case links: 03919224, 03996616, 04209006, 04285232, 04404016, 04446793, 04456509.
```





---
### [Review] [Sub-task] [SAT-45994](https://redhat.atlassian.net/browse/SAT-45994) - 5sp - Imaanpreet Kaur - Add SSH Tunnel Instructions for Grafana




**Comments:**

#### **Imaanpreet Kaur** (2026-06-08)
```
PR created - [https://github.com/theforeman/foreman-documentation/pull/4912|https://github.com/theforeman/foreman-documentation/pull/4912|smart-link] 
```




**Linked Pull Requests & Merge Requests**

#### PR/MR: https://github.com/theforeman/foreman-documentation/pull/4912
```
Title: Add SSH tunnel documentation for remote Grafana access
  - Add new section 'Accessing Grafana remotely using an SSH tunnel'
  - Include Linux/macOS command-line instructions
  - Include Windows PuTTY GUI-based setup instructions
  - Include Windows PowerShell/OpenSSH instructions
  - Add background tunnel setup and teardown instructions

  This addresses the common issue where users cannot directly access
  http://localhost:3000 on the Satellite/Foreman server from their
  remote workstation.

  File modified:
  - guides/common/modules/proc_retrieving-metrics-in-the-web-ui.adoc

#### What changes are you introducing?

#### Why are you introducing these changes? (Explanation, links to references, issues, etc.)

#### Anything else to add? (Considerations, potential downsides, alternative solutions you have explored, etc.)

#### Contributor checklists

* [x] I am okay with my commits getting squashed when you merge this PR.
* [ ] I am familiar with the [contributing](https://git...
```



---
### [Review] [Sub-task] [SAT-45993](https://redhat.atlassian.net/browse/SAT-45993) - 3sp - Imaanpreet Kaur - Replace PCP commands. pmval → pmrep




**Comments:**

#### **Imaanpreet Kaur** (2026-06-04)
```
Research indicates that the command *pmrep(1)* should replace *pmval(1)* due to its capability to monitor multiple metrics simultaneously, offer flexible output formatting (CSV, JSON, table), and consolidate functionalities from various tools into a single interface. The document provides several examples demonstrating how to update existing commands from *pmval* to *pmrep* for different use cases, including archiving and time specifications. The proposed changes enhance the efficiency and consistency of monitoring commands in the PCP toolkit.

*Example 1*

{quote}  *OLD (current docs):*

  pmval -f 1 disk.partitions.write

  *NEW (what to replace it with):*

  pmrep disk.partitions.write{quote}

*Example 2*

{quote}  *OLD* *(current* *docs):*

  pmval --archive /var/log/pcp/pmlogger/satellite.example.com/20230831.00.10 \

    -f 1 disk.partitions.write

  *NEW (what to replace it with):*

  pmrep -a /var/log/pcp/pmlogger/satellite.example.com/20230831.00.10 \

    disk.partitions.w...
```

#### **Imaanpreet Kaur** (2026-06-05)
```
PR - [https://github.com/theforeman/foreman-documentation/pull/4909|https://github.com/theforeman/foreman-documentation/pull/4909|smart-link] 
```




**Linked Pull Requests & Merge Requests**

#### PR/MR: https://github.com/theforeman/foreman-documentation/pull/4909
```
Title: Replace pmval and pmstat with pmrep in PCP metrics documentation   - …
…Replace pmval with pmrep for live metrics retrieval

  - Replace pmval --archive with pmrep -a for archived metrics
  - Replace pmstat with pmrep using SAR metric sets (:sar-u, :sar-r, :sar-d)
  - Remove deprecated flags (-f, -d) that are not needed with pmrep

  Benefits:
  - pmrep can monitor multiple metrics in a single command
  - Consolidates multiple tools (pmval, pmstat) into one consistent interface
  - Provides better output formatting options (CSV, JSON, table)
  - Reduces cognitive load for readers learning PCP monitoring

#### What changes are you introducing?

#### Why are you introducing these changes? (Explanation, links to references, issues, etc.)

#### Anything else to add? (Considerations, potential downsides, alternative solutions you have explored, etc.)

#### Contributor checklists

* [x] I am okay with my commits getting squashed when you merge this PR.
* [ ] I am familiar with the ...
```



---
### [Testing] [Task] [SAT-45971](https://redhat.atlassian.net/browse/SAT-45971) - 7sp - Pablo Mendez Hernandez - satperf: Add UI performance measurement framework


**Description:**
```
Implement the UI performance measurement framework in satperf, based on the metrics contract defined in [SAT-45801|https://redhat.atlassian.net/browse/SAT-45801].

Commits:

* UI performance measurement framework and metrics contract: [72b736cf80a1|https://github.com/redhat-performance/satperf/commit/72b736cf80a1]
* Finalize regression contract and wrapper normalization: [f60ed4a8bdfa|https://github.com/redhat-performance/satperf/commit/f60ed4a8bdfa]
* Add dedicated UI phase plumbing in full_fam.sh: [25a5b7fd483f|https://github.com/redhat-performance/satperf/commit/25a5b7fd483f]
```





**Linked Pull Requests & Merge Requests**

#### PR/MR: https://github.com/redhat-performance/satperf/commit/f60ed4a8bdfa
```
Commit Message:
.commit.message
```

#### PR/MR: https://github.com/redhat-performance/satperf/commit/25a5b7fd483f
```
Commit Message:
.commit.message
```

#### PR/MR: https://github.com/redhat-performance/satperf/commit/72b736cf80a1
```
Commit Message:
.commit.message
```



---
### [In Progress] [Story] [SAT-45959](https://redhat.atlassian.net/browse/SAT-45959) - 5sp - Imaanpreet Kaur - Performance Optimization: Use a cache of existing artifacts during sync


**Description:**
```
*Description of problem:*

 Pulp performs an excessive number of database queries during the process of looking up which artifacts have already been saved during immediate syncs

*How reproducible:*

 Very

*Is this issue a regression from an earlier version:*

 No

*Steps to Reproduce:*

Perform the following on a patched and unpatched system. 

# Sync a medium-sized repository in “immediate” mode
# Sync it again, with the sync optimizations turned off, measuring the total runtime of an “immediate” sync where nothing has changed and nothing needs to downloaded

 The measured time required for step 2 on the patched system should be substantially less.

*Actual behavior:*
[Describe the issue in detail, including what is happening and where]

*Expected behavior:*
[Describe what should be happening instead]

*Business Impact / Additional info:*

 
```



**Comments:**

#### **Daniel Alley** (2026-06-03)
```
This is related to [https://redhat.atlassian.net/browse/SAT-45821|https://redhat.atlassian.net/browse/SAT-45821|smart-link]  and can be tested at the same time
```





---


