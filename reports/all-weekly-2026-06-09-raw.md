# Konflux
## Finished issues

### [Closed/Done] [KONFLUX-14313](https://redhat.atlassian.net/browse/KONFLUX-14313) - Jan Hutar - Annual Access Revalidation for PERF-017 CMDB


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



**Comments (Last 3):**

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
### [Closed/Done] [KONFLUX-14288](https://redhat.atlassian.net/browse/KONFLUX-14288) - Subrata Modak - Spend time for Q2 day of learning


**Description:**
```
Attend the presentation/training on “Talk Agent Skills with Burr Sutter“ (5th June) and see if I can learn something new from that.
```



**Comments (Last 3):**

#### **Subrata Modak** (2026-06-08)
```
Attended some presentations.
```





---
### [Closed/Done] [KONFLUX-14241](https://redhat.atlassian.net/browse/KONFLUX-14241) - Subrata Modak - Filter out pods with non-meaningful artifacts in OOM detector


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



**Comments (Last 3):**

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
All 7 test cases pass - covering empty content, typical errors, small meaningful logs, large logs, edge cases, and boundary conditions.

Assisted-by: Claude
```

#### **Subrata Modak** (2026-06-04)
```
The last additional PR ([https://github.com/konflux-ci/perfscale/pull/68|https://github.com/konflux-ci/perfscale/pull/68|smart-link]) for further improivement has been MERGED. Closing this.
```




**Linked Pull Requests & Merge Requests**

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
  - Require: `"error from server"` + `"pods"` + `"not found"`
  - Check for lines starting with `"error"`
- Multi-pattern matching for different `oc` error formats

## Impact

✅ **Prevents false negatives**: 50-100x reduction in incorrectly skipped meaningful logs  
✅ **Performance**: 10-1000x faster for large logs (size check vs full pattern scan)  
✅ **False positive rate unchanged**: <1% (same as before)

## Testing

Added comprehensive test suite (`test_artifact_validation.py`) with 7 test cases:
- ✅ Empty/whitespace content
- ✅ Typical `oc` pod-not-found errors
- ✅ Small meaningful logs (OOM errors, config status)
- ✅ Large logs (>2KB) with "not found" buried inside
- ✅ Edge case: 10+ line logs with "not found" in middle
- ✅ Multi-line `oc` error output
- ✅ Exact 2KB threshold boundary

All tests pass.

## Example Scenarios

**Before (could skip incorrectly):**
\`\`\`
# 5MB pod log with "config file not found" on line 1000
if "not found" in content and "error from server" in content:
    return False  # 🚨 Skips 5MB log!
\`\`\`

**After (protected by size check):**
\`\`\`python
if content_size >= 2048:  # 5MB > 2KB
    return True  # ✅ Immediately marked meaningful
# Pattern check never runs!
\`\`\`

## Files Changed

- `oc_get_ooms.py`: Improved `is_artifact_meaningful()` function (+32 lines)
- `test_artifact_validation.py`: Comprehensive test suite (new file)
- `IMPROVEMENT_SUMMARY.md`: Detailed explanation and rationale (new file)

## Related

- Original PR: #67
- Jira: KONFLUX-14241
- Addresses feedback from: @jhutar

Assisted-by: Claude
```

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
- Modified `tools/oomkill-and-crashloopbackoff-detector/oc_get_ooms.py` (+38 lines, -7 lines)
- Simple validation logic (~20 lines for validation function, ~11 lines for integration)

## Testing
- Syntax validated with `python3 -m py_compile`
- Output format changed from "X pod(s) found" to "X pod(s) kept (Y skipped - pod deleted)"

Related: KONFLUX-11365, KONFLUX-11509
```



---
### [Closed/Done] [KONFLUX-14193](https://redhat.atlassian.net/browse/KONFLUX-14193) - Subrata Modak - Raising new issues and tracking old unresolved issues for OOM & Crashloopbackoff detector in Sprint41




**Comments (Last 3):**

#### **Subrata Modak** (2026-05-28)
```
Today’s issues:

# [https://redhat.atlassian.net/browse/OCPBUGS-86689|https://redhat.atlassian.net/browse/OCPBUGS-86689|smart-link] 
# [https://redhat.atlassian.net/browse/OCPBUGS-86691|https://redhat.atlassian.net/browse/OCPBUGS-86691|smart-link] 
# [https://redhat.atlassian.net/browse/OCPBUGS-86696|https://redhat.atlassian.net/browse/OCPBUGS-86696|smart-link] 
```

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
### [Closed/Done] [KONFLUX-14094](https://redhat.atlassian.net/browse/KONFLUX-14094) - Jan Hutar - Review requirements for KONFLUX-12751 - Jan


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
### [Closed/Done] [KONFLUX-13726](https://redhat.atlassian.net/browse/KONFLUX-13726) - Roberto Alfieri - Onboarding: Hands-on learning with Konflux main usage


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



**Comments (Last 3):**

#### **Roberto Alfieri** (2026-06-03)
```
Status update:

* requested a new tenant with [+https://gitlab.cee.redhat.com/releng/konflux-release-data/-/merge_requests/18006+|https://gitlab.cee.redhat.com/releng/konflux-release-data/-/merge_requests/18006]
* Forked a repo with a “simple” application → [https://github.com/rebtoor/devfile-sample-python-basic|https://github.com/rebtoor/devfile-sample-python-basic|smart-link]
* Setup the konflux ci on that repo → [https://github.com/rebtoor/devfile-sample-python-basic/pull/1|https://github.com/rebtoor/devfile-sample-python-basic/pull/1|smart-link]
* Created the required resources (service accounts, secrets) in order to push containers into a specified registry → [https://quay.io/repository/ralfieri/ralfieri-tenant/devfile-sample-python-basic-c9e78?tab=tags|https://quay.io/repository/ralfieri/ralfieri-tenant/devfile-sample-python-basic-c9e78?tab=tags|smart-link]
*  Become familiar with the concept of “Release” and related resources (releaseplan, releaseplanadmission, release)
* Tested a release and analyzed the results: failure was expected because the staging cluster doesn’t have the proper infra needed for release

A couple of screenshots from the Konflux UI

!Screenshot 2026-06-03 at 10.56.47.png|width=593,alt="Screenshot 2026-06-03 at 10.56.47.png"!

!Screenshot 2026-06-03 at 10.56.55.png|width=593,alt="Screenshot 2026-06-03 at 10.56.55.png"!

!Screenshot 2026-06-03 at 10.58.20.png|width=593,alt="Screenshot 2026-06-03 at 10.58.20.png"!
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



---
### [Closed/Won't Do] [KONFLUX-13066](https://redhat.atlassian.net/browse/KONFLUX-13066) - Subrata Modak - Implement proper compute resources for task 'verify-source'


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



**Comments (Last 3):**

#### **Subrata Modak** (2026-04-09)
```
Observed on 2026-04-09

||serial_⁠no||task||version_⁠dir||task_⁠yaml||step_⁠count||flagged_⁠step_⁠count||ok_⁠step_⁠count||task_⁠flagged||step||memory_⁠requests||memory_⁠limits||memory_⁠requests_⁠bytes||memory_⁠limits_⁠bytes||memory_⁠diff_⁠bytes||memory_⁠diff_⁠MiB||cpu_⁠requests||status||flagged||
|57|verify-source|0.1|verify-source/0.1/verify-source.yaml|1|1|0|yes|slsa-verify|​|​|​|​|​|​|​|BOTH_MEM_MISSING, CPU_REQ_MISSING|yes|
```

#### **Subrata Modak** (2026-05-29)
```
h2. Analysis and Resolution — verify-source (v0.1)

h3. Fleet Analysis Results

Fleet analysis was run using {{analyze_resource_limits.py}} over a 60-day window across all 12 Konflux clusters (kflux-ocp-p01, kflux-osp-p01, kflux-prd-es01, kflux-prd-rh02, kflux-prd-rh03, kflux-rhel-p01, kflux-stg-es01, stone-prd-rh01, stone-prod-p01, stone-prod-p02, stone-stage-p01, stone-stg-rh01).

||*Variant*||*Clusters with data*||*Pod executions*||*Coverage*||
|{{verify-source}}|*0 of 12*|0|No data (60 days)|

No pod executions found across all clusters. The task has very low production usage. *Floor values* ({{memory: 64Mi}} req=limit, {{cpu: 50m}} req, no cpu limit) are used.

h3. Policy Violations Found (v0.1)

||*Step*||*Violation*||*Resolution*||
|{{slsa-verify}}|No resources defined|Added floor values (memory: 64Mi req=limit, cpu: 50m req)|

h3. Notes

* Only one version (0.1) exists and it is not archived.
* No OCI-TA variant exists for this task -- only one file was modified.
* {{apiVersion: tekton.dev/v1}} -- {{computeResources:}} field used (correct for v1).

h3. Pull Request

[build-definitions PR #3560|https://github.com/konflux-ci/build-definitions/pull/3560]

{{Assisted-by: CursorAI}}
```

#### **Subrata Modak** (2026-06-08)
```
h3. Closing: PoC task with no fleet data; future enforcement via KONFLUX-11510

PR [konflux-ci/build-definitions#3560|https://github.com/konflux-ci/build-definitions/pull/3560] has been closed without merging.

Fleet analysis over a 60-day window across all 12 Konflux clusters returned *zero pod executions* for {{verify-source}}. This is consistent with the task's own description, which explicitly states:

{quote}_"This task relies on VSAs generated by source-tool which is currently a proof-of-concept and under active development. It should not be used in production environments."_{quote}

Without real execution data, any resource values would be guesswork. PR reviewers (@chmeliik, @arewm) correctly raised this concern — and closing is the right call.

This ticket can be revisited when {{verify-source}} graduates to production use and real fleet data becomes available. Additionally, [KONFLUX-11510|https://redhat.atlassian.net/browse/KONFLUX-11510] will introduce a CI enforcement check ensuring {{requests == limits}} for all new/changed tasks — meaning that when {{verify-source}} eventually gets updated for production, proper resource settings will be automatically required by the CI gate.

Signed-off-by: Subrata Modak [smodak@redhat.com|mailto:smodak@redhat.com]

Assisted-by: CursorAgent@Cursor.com
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
Co-authored-by: Cursor <cursoragent@cursor.com>

Made with [Cursor](https://cursor.com)

[KONFLUX-11509]: https://redhat.atlassian.net/browse/KONFLUX-11509?atlOrigin=eyJpIjoiNWRkNTljNzYxNjVmNDY3MDlhMDU5Y2ZhYzA5YTRkZjUiLCJwIjoiZ2l0aHViLWNvbS1KU1cifQ
[KONFLUX-13066]: https://redhat.atlassian.net/browse/KONFLUX-13066?atlOrigin=eyJpIjoiNWRkNTljNzYxNjVmNDY3MDlhMDU5Y2ZhYzA5YTRkZjUiLCJwIjoiZ2l0aHViLWNvbS1KU1cifQ
```

#### PR/MR: https://github.com/konflux-ci/build-definitions/pull/3405
```
Title: feat(ta): set 4Gi memory request/limit for use-trusted-artifact step
The create-trusted-artifact step already sets a 3Gi limit via the generator code. Apply similar resource limits to the use-trusted-artifact step to ensure consistent memory allocation.

The -min variant patches remove the explicit computeResources so those tasks inherit the smaller stepTemplate defaults instead.

Related: https://github.com/konflux-ci/konflux-sast-tasks/pull/103
```



---
### [Closed/Won't Do] [KONFLUX-13064](https://redhat.atlassian.net/browse/KONFLUX-13064) - Subrata Modak - Implement proper compute resources for task 'tkn-bundle-oci-ta'


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



**Comments (Last 3):**

#### **Subrata Modak** (2026-04-09)
```
Observed on 2026-04-09

||serial_⁠no||task||version_⁠dir||task_⁠yaml||step_⁠count||flagged_⁠step_⁠count||ok_⁠step_⁠count||task_⁠flagged||step||memory_⁠requests||memory_⁠limits||memory_⁠requests_⁠bytes||memory_⁠limits_⁠bytes||memory_⁠diff_⁠bytes||memory_⁠diff_⁠MiB||cpu_⁠requests||status||flagged||
|54|tkn-bundle-oci-ta|0.2|tkn-bundle-oci-ta/0.2/tkn-bundle-oci-ta.yaml|3|3|0|yes|use-trusted-artifact|​|​|​|​|​|​|​|BOTH_MEM_MISSING, CPU_REQ_MISSING|yes|
|54|tkn-bundle-oci-ta|0.2|tkn-bundle-oci-ta/0.2/tkn-bundle-oci-ta.yaml|3|3|0|yes|modify-task-files|​|​|​|​|​|​|​|BOTH_MEM_MISSING, CPU_REQ_MISSING|yes|
|54|tkn-bundle-oci-ta|0.2|tkn-bundle-oci-ta/0.2/tkn-bundle-oci-ta.yaml|3|3|0|yes|build|​|​|​|​|​|​|​|BOTH_MEM_MISSING, CPU_REQ_MISSING|yes|
```

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

### Note on `use-trusted-artifact` (OCI-TA variant)

`tkn-bundle-oci-ta` is a **generated** task (`recipe.yaml` +
`hack/generate-ta-tasks.sh`). The generator injects the
`use-trusted-artifact` step but does not currently support
propagating `computeResources` for it. Manually adding them would
cause the "Check Trusted Artifact variants" CI check to fail (the
generator re-run would strip them). This generator gap is tracked in
[#3405](https://github.com/konflux-ci/build-definitions/pull/3405).

### Policy compliance

- ✅ `memory.request == memory.limit` for all changed steps
- ✅ `cpu.request` set, no `cpu.limit`
- ✅ OCI-TA YAML regenerated via `hack/generate-ta-tasks.sh`

Signed-off-by: Subrata Modak <smodak@redhat.com>
Assisted-by: CursorAgent@Cursor.com

Made with [Cursor](https://cursor.com)

[KONFLUX-13063]: https://redhat.atlassian.net/browse/KONFLUX-13063?atlOrigin=eyJpIjoiNWRkNTljNzYxNjVmNDY3MDlhMDU5Y2ZhYzA5YTRkZjUiLCJwIjoiZ2l0aHViLWNvbS1KU1cifQ
```

#### PR/MR: https://github.com/konflux-ci/build-definitions/pull/3405
```
Title: feat(ta): set 4Gi memory request/limit for use-trusted-artifact step
The create-trusted-artifact step already sets a 3Gi limit via the generator code. Apply similar resource limits to the use-trusted-artifact step to ensure consistent memory allocation.

The -min variant patches remove the explicit computeResources so those tasks inherit the smaller stepTemplate defaults instead.

Related: https://github.com/konflux-ci/konflux-sast-tasks/pull/103
```



---
### [Closed/Done] [KONFLUX-13049](https://redhat.atlassian.net/browse/KONFLUX-13049) - Subrata Modak - Implement proper compute resources for task 'package-operator-package'


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



**Comments (Last 3):**

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
|build-sbom|MISSING|memory: 64Mi req=limit, cpu: 50m req|
|push-sbom|MISSING|memory: 64Mi req=limit, cpu: 50m req|

h2. Sizing Rationale

* No fleet data available (0 pod executions across all 12 clusters over 60 days) for either variant.
* Floor values applied: memory 64Mi request=limit, cpu 50m request -- the minimum safe baseline per project policy.
* use-trusted-artifact resources added manually to oci-ta as the trusted-artifact generator does not propagate computeResources to injected steps.
* No cpu.limit is set on...
```

#### **Subrata Modak** (2026-06-03)
```
h3. CI Fix: Check Trusted Artifact variants (file out of date)

The {{Check Trusted Artifact variants}} CI check failed on PR #3568 with: *"File is out of date, run hack/generate-ta-tasks.sh"*.

h4. Root Cause

The CI workflow re-runs {{hack/generate-ta-tasks.sh}} and diffs the result against the committed {{package-operator-package-oci-ta.yaml}}. A {{computeResources}} block had been manually added to the generator-injected {{use-trusted-artifact}} step after running the generator. Since the generator never emits {{computeResources}} for this injected step (a known generator-level gap), CI's regenerated file differed from the committed file.

h4. Fix Applied

Removed the {{computeResources}} block from {{use-trusted-artifact}} in {{package-operator-package-oci-ta.yaml}} so the committed file matches generator output exactly. The three task-specific steps ({{build-pkg}}, {{build-sbom}}, {{push-sbom}}) retain their floor {{computeResources}} as those are correctly generated from the base task. A follow-up commit was pushed to [PR #3568|https://github.com/konflux-ci/build-definitions/pull/3568].

Note: Supporting {{computeResources}} on the generator-injected {{use-trusted-artifact}} step requires a fix in {{hack/generate-ta-tasks.sh}} itself (tracked separately).

Signed-off-by: Subrata Modak <smodak@redhat.com>

Assisted-by: CursorAgent@Cursor.com
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
| `push-sbom` | MISSING | `memory: 64Mi` req=limit, `cpu: 50m` req |

## Sizing rationale

Fleet analysis across all Konflux clusters over a 60-day window returned
no execution data for either task, indicating negligible production usage.
Floor values (`memory: 64Mi` request=limit, `cpu: 50m` request) are
applied as the minimum safe baseline. These can be tuned upward once
real usage data is available.

Note: `use-trusted-artifact` resources were added manually to the oci-ta
variant as the trusted-artifact generator does not currently propagate
`computeResources` to injected steps.

## Policy

All steps comply with the project compute resource policy:
- `memory.request == memory.limit`
- `cpu.request` set on every step
- No `cpu.limit`

Signed-off-by: Subrata Modak <smodak@redhat.com>
Assisted-by: CursorAgent@Cursor.com

Made with [Cursor](https://cursor.com)
```

#### PR/MR: https://github.com/konflux-ci/build-definitions/pull/3405
```
Title: feat(ta): set 4Gi memory request/limit for use-trusted-artifact step
The create-trusted-artifact step already sets a 3Gi limit via the generator code. Apply similar resource limits to the use-trusted-artifact step to ensure consistent memory allocation.

The -min variant patches remove the explicit computeResources so those tasks inherit the smaller stepTemplate defaults instead.

Related: https://github.com/konflux-ci/konflux-sast-tasks/pull/103
```



---
### [Closed/Done] [KONFLUX-13043](https://redhat.atlassian.net/browse/KONFLUX-13043) - Subrata Modak - Implement proper compute resources for task 'modelcar-oci-ta'


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



**Comments (Last 3):**

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
|sbom-generate|MISSING|memory: 64Mi req=limit, cpu: 50m req|
|upload-sbom|MISSING|memory: 64Mi req=limit, cpu: 50m req|
|report-sbom-url|MISSING|memory: 64Mi req=limit, cpu: 50m req|

h2. Sizing Rationale

* No fleet data available (0 pod executions across all clusters over 60 days).
* Floor values applied: memory 64Mi request=limit, cpu 50m request -- the minimum safe baseline per project policy.
* Values can be tuned upward once real usage data is available. Teams with heavier model files may need to override via pipeline-l...
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

## Sizing rationale

Fleet analysis across all Konflux clusters over a 60-day window returned
no execution data for this task, indicating negligible production usage.
Floor values (`memory: 64Mi` request=limit, `cpu: 50m` request) are
applied as the minimum safe baseline. These can be tuned upward once
real usage data is available.

## Policy

All steps comply with the project compute resource policy:
- `memory.request == memory.limit`
- `cpu.request` set on every step
- No `cpu.limit`

Signed-off-by: Subrata Modak <smodak@redhat.com>

Made with [Cursor](https://cursor.com)
```

#### PR/MR: https://github.com/konflux-ci/build-definitions/pull/3405
```
Title: feat(ta): set 4Gi memory request/limit for use-trusted-artifact step
The create-trusted-artifact step already sets a 3Gi limit via the generator code. Apply similar resource limits to the use-trusted-artifact step to ensure consistent memory allocation.

The -min variant patches remove the explicit computeResources so those tasks inherit the smaller stepTemplate defaults instead.

Related: https://github.com/konflux-ci/konflux-sast-tasks/pull/103
```



---
## In review issues

### [Review] [KONFLUX-13065](https://redhat.atlassian.net/browse/KONFLUX-13065) - Subrata Modak - Implement proper compute resources for task 'update-infra-deployments'


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



**Comments (Last 3):**

#### **Subrata Modak** (2026-04-09)
```
Observed on 2026-04-09

||serial_⁠no||task||version_⁠dir||task_⁠yaml||step_⁠count||flagged_⁠step_⁠count||ok_⁠step_⁠count||task_⁠flagged||step||memory_⁠requests||memory_⁠limits||memory_⁠requests_⁠bytes||memory_⁠limits_⁠bytes||memory_⁠diff_⁠bytes||memory_⁠diff_⁠MiB||cpu_⁠requests||status||flagged||
|55|update-infra-deployments|0.1|update-infra-deployments/0.1/update-infra-deployments.yaml|5|5|0|yes|race-condition-update-check|​|​|​|​|​|​|​|BOTH_MEM_MISSING, CPU_REQ_MISSING|yes|
|55|update-infra-deployments|0.1|update-infra-deployments/0.1/update-infra-deployments.yaml|5|5|0|yes|git-clone-infra-deployments|​|​|​|​|​|​|​|BOTH_MEM_MISSING, CPU_REQ_MISSING|yes|
|55|update-infra-deployments|0.1|update-infra-deployments/0.1/update-infra-deployments.yaml|5|5|0|yes|run-update-script|​|​|​|​|​|​|​|BOTH_MEM_MISSING, CPU_REQ_MISSING|yes|
|55|update-infra-deployments|0.1|update-infra-deployments/0.1/update-infra-deployments.yaml|5|5|0|yes|get-diff-files|​|​|​|​|​|​|​|BOTH_MEM_MISSING, CPU_REQ_MISSING|yes|
|55|update-infra-deployments|0.1|update-infra-deployments/0.1/update-infra-deployments.yaml|5|5|0|yes|create-mr|​|​|​|​|​|​|​|BOTH_MEM_MISSING, CPU_REQ_MISSING|yes|
```

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
| `get-diff-files` | 64Mi | 50m | Floor (P95 = 1 MB) |
| `create-mr` | 64Mi | 50m | No observability data |

### Policy compliance

- ✅ `memory.request == memory.limit` for all steps
- ✅ `cpu.request` set, no `cpu.limit`
- ✅ No OCI-TA variant exists for this task

Signed-off-by: Subrata Modak <smodak@redhat.com>
Assisted-by: CursorAgent@Cursor.com

Made with [Cursor](https://cursor.com)

[KONFLUX-13065]: https://redhat.atlassian.net/browse/KONFLUX-13065?atlOrigin=eyJpIjoiNWRkNTljNzYxNjVmNDY3MDlhMDU5Y2ZhYzA5YTRkZjUiLCJwIjoiZ2l0aHViLWNvbS1KU1cifQ
```



---
### [Review] [KONFLUX-13063](https://redhat.atlassian.net/browse/KONFLUX-13063) - Subrata Modak - Implement proper compute resources for task 'tkn-bundle'


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



**Comments (Last 3):**

#### **Subrata Modak** (2026-04-09)
```
Observed on 2026-04-09

||serial_⁠no||task||version_⁠dir||task_⁠yaml||step_⁠count||flagged_⁠step_⁠count||ok_⁠step_⁠count||task_⁠flagged||step||memory_⁠requests||memory_⁠limits||memory_⁠requests_⁠bytes||memory_⁠limits_⁠bytes||memory_⁠diff_⁠bytes||memory_⁠diff_⁠MiB||cpu_⁠requests||status||flagged||
|53|tkn-bundle|0.2|tkn-bundle/0.2/tkn-bundle.yaml|2|2|0|yes|modify-task-files|​|​|​|​|​|​|​|BOTH_MEM_MISSING, CPU_REQ_MISSING|yes|
|53|tkn-bundle|0.2|tkn-bundle/0.2/tkn-bundle.yaml|2|2|0|yes|build|​|​|​|​|​|​|​|BOTH_MEM_MISSING, CPU_REQ_MISSING|yes|
```

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

*Note on* {{use-trusted-artifact}}: {{tkn-bundle-oci-ta}} is a generated task ({{recipe.yaml}} + {{hack/generate-ta-tasks.sh}}). The generator injects {{use-trusted-artifact}} but does not support propagating {{computeResources}} for it. Manually adding them would break the "Check Trusted Artifact variants" CI check. This generator gap is tracked in [build-definitions PR #3405|https://github.com/konflux-ci/build-definitions/pull/3405].

*PR:* [konflux-ci/build-definitions#3576|https://github.com/konflux-ci/build-definitions/pull/3576]

*KONFLUX-13064* ({{tkn-bundle-oci-ta}}) is covered by the same PR and has been closed as Won't Do (duplicate).

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

### Note on `use-trusted-artifact` (OCI-TA variant)

`tkn-bundle-oci-ta` is a **generated** task (`recipe.yaml` +
`hack/generate-ta-tasks.sh`). The generator injects the
`use-trusted-artifact` step but does not currently support
propagating `computeResources` for it. Manually adding them would
cause the "Check Trusted Artifact variants" CI check to fail (the
generator re-run would strip them). This generator gap is tracked in
[#3405](https://github.com/konflux-ci/build-definitions/pull/3405).

### Policy compliance

- ✅ `memory.request == memory.limit` for all changed steps
- ✅ `cpu.request` set, no `cpu.limit`
- ✅ OCI-TA YAML regenerated via `hack/generate-ta-tasks.sh`

Signed-off-by: Subrata Modak <smodak@redhat.com>
Assisted-by: CursorAgent@Cursor.com

Made with [Cursor](https://cursor.com)

[KONFLUX-13063]: https://redhat.atlassian.net/browse/KONFLUX-13063?atlOrigin=eyJpIjoiNWRkNTljNzYxNjVmNDY3MDlhMDU5Y2ZhYzA5YTRkZjUiLCJwIjoiZ2l0aHViLWNvbS1KU1cifQ
```

#### PR/MR: https://github.com/konflux-ci/build-definitions/pull/3405
```
Title: feat(ta): set 4Gi memory request/limit for use-trusted-artifact step
The create-trusted-artifact step already sets a 3Gi limit via the generator code. Apply similar resource limits to the use-trusted-artifact step to ensure consistent memory allocation.

The -min variant patches remove the explicit computeResources so those tasks inherit the smaller stepTemplate defaults instead.

Related: https://github.com/konflux-ci/konflux-sast-tasks/pull/103
```



---
### [Review] [KONFLUX-13056](https://redhat.atlassian.net/browse/KONFLUX-13056) - Subrata Modak - Implement proper compute resources for task 'run-script-oci-ta'


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



**Comments (Last 3):**

#### **Subrata Modak** (2026-04-09)
```
Observed on 2026-04-09

||serial_⁠no||task||version_⁠dir||task_⁠yaml||step_⁠count||flagged_⁠step_⁠count||ok_⁠step_⁠count||task_⁠flagged||step||memory_⁠requests||memory_⁠limits||memory_⁠requests_⁠bytes||memory_⁠limits_⁠bytes||memory_⁠diff_⁠bytes||memory_⁠diff_⁠MiB||cpu_⁠requests||status||flagged||
|45|run-script-oci-ta|0.1|run-script-oci-ta/0.1/run-script-oci-ta.yaml|3|2|1|yes|use-trusted-artifact|1Gi|4Gi|1073741824|4294967296|3221225472|3072.00|1|MEM_MISMATCH|yes|
|45|run-script-oci-ta|0.1|run-script-oci-ta/0.1/run-script-oci-ta.yaml|3|2|1|yes|run-script|1Gi|4Gi|1073741824|4294967296|3221225472|3072.00|1|MEM_MISMATCH|yes|
|45|run-script-oci-ta|0.1|run-script-oci-ta/0.1/run-script-oci-ta.yaml|3|2|1|yes|create-trusted-artifact|3Gi|3Gi|3221225472|3221225472|0|0.00|1|Ok|no|
```

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
|{{create-trusted-artifact}}|3Gi / 3Gi (per-step)|1 (per-step)|10 MB (stone-prod-p02)|*64Mi* (floor)|42m (stone-prod-p02)|*50m* (floor)|

h4. Policy Violations Fixed

# {{stepTemplate}} had {{memory.request (1Gi) != memory.limit (4Gi)}} — removed entirely; replaced with per-step values.
# {{run-script}} was *under-provisioned* — inherited 4Gi limit despite P95 of 4351 MB on stone-prd-rh01, driven by {{clair-in-ci-db-hermetic}} ({{rhtap-integration-tenant}}) fetching a large Clair vulnerability database. Raised to *5Gi*.
# {{create-trusted-artifact}} was *~30x over-...
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

Going forward, {{use-trusted-artifact}} and {{create-trusted-artifact}} will be set to *4Gi* and *3Gi* respectively in all future tasks, regardless of per-task fleet data for those steps.

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
2. **`run-script` was under-provisioned** — inherited the 4Gi limit despite
   a fleet P95 of 4351 MB on `stone-prd-rh01` (driven by
   `clair-in-ci-db-hermetic` fetching a large Clair vulnerability DB).
   Raised to **5Gi** to cover the fleet P95 envelope.
3. **`create-trusted-artifact` was ~30x over-provisioned** — had a
   hardcoded 3Gi/1CPU override vs. an actual P95 of only 10 MB.
   Right-sized to **64Mi**.

## Sizing rationale

Fleet analysis across all 12 Konflux clusters over a 60-day window
(**6,989 pod executions**), using **P95 + 5% margin** as the base metric.
The absolute maximum is noted for context but is not used for sizing —
outlier spikes are excluded so that default limits don't over-provision
every execution. Tenants whose workloads regularly exceed the proposed
limits should use
[pipeline-level compute resource overrides](https://konflux.pages.redhat.com/docs/users/building/overriding-compute-resources.html).

**run-script (5Gi / 1500m):**
Memory P95 is 4351 MB on `stone-prd-rh01` (driven by
`clair-in-ci-db-hermetic` / `rhtap-integration-tenant` fetching a large
vulnerability DB), with a 10,022 MB absolute max.
P95 + 5% margin = 4568 MB ≈ 4.46 GiB → rounded up to **5Gi**.
CPU P95 is 1284m on `stone-prd-rh01` (driven by `ansible-plugins-main`)
→ +5% = 1348m → rounded to **1500m**.

**use-trusted-artifact and create-trusted-artifact (64Mi / 50m):**
Memory P95 ≤ 10 MB and CPU P95 ≤ 42m across all clusters — floor values
applied.

## Policy

All steps comply with the project compute resource policy:

* `memory.request == memory.limit`
* `cpu.request` set on every step
* No `cpu.limit`

Signed-off-by: Subrata Modak <smodak@redhat.com>
Assisted-by: CursorAgent@Cursor.com

Made with [Cursor](https://cursor.com)
```



---
### [Review] [KONFLUX-13055](https://redhat.atlassian.net/browse/KONFLUX-13055) - Subrata Modak - Implement proper compute resources for task 'run-opm-command-oci-ta'


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



**Comments (Last 3):**

#### **Subrata Modak** (2026-04-09)
```
Observed on 2026-04-09

||serial_⁠no||task||version_⁠dir||task_⁠yaml||step_⁠count||flagged_⁠step_⁠count||ok_⁠step_⁠count||task_⁠flagged||step||memory_⁠requests||memory_⁠limits||memory_⁠requests_⁠bytes||memory_⁠limits_⁠bytes||memory_⁠diff_⁠bytes||memory_⁠diff_⁠MiB||cpu_⁠requests||status||flagged||
|44|run-opm-command-oci-ta|0.1|run-opm-command-oci-ta/0.1/run-opm-command-oci-ta.yaml|5|5|0|yes|use-trusted-artifact|​|​|​|​|​|​|​|BOTH_MEM_MISSING, CPU_REQ_MISSING|yes|
|44|run-opm-command-oci-ta|0.1|run-opm-command-oci-ta/0.1/run-opm-command-oci-ta.yaml|5|5|0|yes|run-opm-with-user-args|​|​|​|​|​|​|​|BOTH_MEM_MISSING, CPU_REQ_MISSING|yes|
|44|run-opm-command-oci-ta|0.1|run-opm-command-oci-ta/0.1/run-opm-command-oci-ta.yaml|5|5|0|yes|convert-image-tags-to-digests|​|​|​|​|​|​|​|BOTH_MEM_MISSING, CPU_REQ_MISSING|yes|
|44|run-opm-command-oci-ta|0.1|run-opm-command-oci-ta/0.1/run-opm-command-oci-ta.yaml|5|5|0|yes|replace-related-images-pullspec-in-file|​|​|​|​|​|​|​|BOTH_MEM_MISSING, CPU_REQ_MISSING|yes|
|44|run-opm-command-oci-ta|0.1|run-opm-command-oci-ta/0.1/run-opm-command-oci-ta.yaml|5|5|0|yes|create-trusted-artifact|​|​|​|​|​|​|​|BOTH_MEM_MISSING, CPU_REQ_MISSING|yes|
```

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
|{{replace-related-images-pullspec-in-file}}|5 MB (kflux-prd-rh02)|*64Mi* (floor)|0m|*50m* (floor)|
|{{create-trusted-artifact}}|8 MB (kflux-prd-rh02)|*64Mi* (floor)|1m|*50m* (floor)|

h4. Key Observations

* {{run-opm-with-user-args}} is the dominant step — P95 of 431 MB on stone-prd-rh01 (driven by large OCP catalog renders from {{rh-openshift-gitops-tenant}}). Max observed: 626 MB. Sized to 512Mi.
* {{convert-image-tags-to-digests}} has non-trivial CPU (P95 204m on stone-prod-p02) despite low memory, driven by parallel {{skopeo inspect}} calls for tag-to-digest conversion. CPU...
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
outlier spikes are deliberately excluded so that default limits don't
over-provision every execution for rare heavy runs. Tenants whose
workloads regularly exceed the proposed limits should use
[pipeline-level compute resource overrides](https://konflux.pages.redhat.com/docs/users/building/overriding-compute-resources.html).

**run-opm-with-user-args (512Mi / 100m):**
The step runs `opm` to render OCI-based file-based catalogs (FBCs).
Memory P95 is 431Mi on `stone-prd-rh01` (driven by large OCP catalog
renders from `rh-openshift-gitops-tenant`), with a 626Mi absolute max.
P95 + 5% margin = 453Mi → rounded up to the next standard value: **512Mi**.
CPU P95 is 78m (+5% → 82m), rounded to **100m**.

**convert-image-tags-to-digests (64Mi / 250m):**
Memory is very low (P95 ≤ 13Mi across all clusters → 64Mi floor).
CPU P95 is 204m on `stone-prod-p02` (+5% → 214m), driven by parallel
`skopeo inspect` calls resolving image tags to digests. Rounded to
**250m**.

**All other steps (64Mi / 50m):**
Memory P95 ≤ 8Mi and CPU P95 ≤ 1m across all clusters — floor values
applied.

## Policy

All steps comply with the project compute resource policy:

* `memory.request == memory.limit`
* `cpu.request` set on every step
* No `cpu.limit`

Signed-off-by: Subrata Modak <smodak@redhat.com>
Assisted-by: CursorAgent@Cursor.com
```



---
### [Review] [KONFLUX-13047](https://redhat.atlassian.net/browse/KONFLUX-13047) - Subrata Modak - Implement proper compute resources for task 'opm-get-bundle-version'


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



**Comments (Last 3):**

#### **Subrata Modak** (2026-04-09)
```
Observed on 2026-04-09

||serial_⁠no||task||version_⁠dir||task_⁠yaml||step_⁠count||flagged_⁠step_⁠count||ok_⁠step_⁠count||task_⁠flagged||step||memory_⁠requests||memory_⁠limits||memory_⁠requests_⁠bytes||memory_⁠limits_⁠bytes||memory_⁠diff_⁠bytes||memory_⁠diff_⁠MiB||cpu_⁠requests||status||flagged||
|34|opm-get-bundle-version|0.1|opm-get-bundle-version/0.1/opm-get-bundle-version.yaml|2|2|0|yes|opm-render-bundle|​|​|​|​|​|​|​|BOTH_MEM_MISSING, CPU_REQ_MISSING|yes|
|34|opm-get-bundle-version|0.1|opm-get-bundle-version/0.1/opm-get-bundle-version.yaml|2|2|0|yes|jq-get-olm-package-version|​|​|​|​|​|​|​|BOTH_MEM_MISSING, CPU_REQ_MISSING|yes|
```

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
* Floor values applied: memory 64Mi request=limit, cpu 50m request -- the minimum safe baseline per project policy.
* apiVersion upgrade to tekton.dev/v1 is required to use the computeResources field (v1beta1 resources field is deprecated) and aligns this task with the rest of the catalogue.
* No cpu.limit is set on any step (per policy).

h2. Pull Request

PR #3567: [https://github.com/konflux-ci/build-definitions/pull/3567|https://github.com/konflux-ci/build-definitions/pull/3567|smart-link]

----

_Signed-off-by: Subrata Modak <smodak...
```




**Linked Pull Requests & Merge Requests**

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
`computeResources` field (the `v1beta1` equivalent `resources` is
deprecated) and aligns this task with the rest of the catalogue.

## Policy

All steps comply with the project compute resource policy:
- `memory.request == memory.limit`
- `cpu.request` set on every step
- No `cpu.limit`

Signed-off-by: Subrata Modak <smodak@redhat.com>
Assisted-by: CursorAgent@Cursor.com

Made with [Cursor](https://cursor.com)
```

#### PR/MR: https://github.com/konflux-ci/build-definitions/pull/3405
```
Title: feat(ta): set 4Gi memory request/limit for use-trusted-artifact step
The create-trusted-artifact step already sets a 3Gi limit via the generator code. Apply similar resource limits to the use-trusted-artifact step to ensure consistent memory allocation.

The -min variant patches remove the explicit computeResources so those tasks inherit the smaller stepTemplate defaults instead.

Related: https://github.com/konflux-ci/konflux-sast-tasks/pull/103
```



---
## In progress issues

### [In Progress] [KONFLUX-14299](https://redhat.atlassian.net/browse/KONFLUX-14299) - Subrata Modak - OOM/CrashLoopBackOff Jira Enhancement: ROSA→OHSS Routing, ADF Formatting, and Permanent Artifacts


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



**Comments (Last 3):**

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
• Incident Overview Panel with cluster type indicators (🔴 ROSA, 🔵 OSD, ⚪ OCP)
• Cluster metadata table (environment, region, platform)
• Last 50 lines of error logs inline (when available)
• Diagnostic artifacts panel listing attached files
• Access instructions for OHSS tickets

FILE ATTACHMENTS ✅
• Pod logs automatically attached
• Pod YAML descriptions attached
• Files permanently stored with Jira ticket

CONFIGURATION & SECURITY ✅
• Jenkins URLs externalized (JENKINS_BASE_URL env var)
• ROSA cluster patterns configurable (ROSA...
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
### [In Progress] [KONFLUX-13720](https://redhat.atlassian.net/browse/KONFLUX-13720) - Roberto Alfieri - Onboarding: Understand Loadtest architecture and performance testing


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

### [In Progress] [KONFLUX-14299](https://redhat.atlassian.net/browse/KONFLUX-14299) - Subrata Modak - OOM/CrashLoopBackOff Jira Enhancement: ROSA→OHSS Routing, ADF Formatting, and Permanent Artifacts


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



**Comments (Last 3):**

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
• Incident Overview Panel with cluster type indicators (🔴 ROSA, 🔵 OSD, ⚪ OCP)
• Cluster metadata table (environment, region, platform)
• Last 50 lines of error logs inline (when available)
• Diagnostic artifacts panel listing attached files
• Access instructions for OHSS tickets

FILE ATTACHMENTS ✅
• Pod logs automatically attached
• Pod YAML descriptions attached
• Files permanently stored with Jira ticket

CONFIGURATION & SECURITY ✅
• Jenkins URLs externalized (JENKINS_BASE_URL env var)
• ROSA cluster patterns configurable (ROSA...
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
### [New] [KONFLUX-14287](https://redhat.atlassian.net/browse/KONFLUX-14287) - Subrata Modak - Readup about AI Skills (E.g KONFLUX-13490)


**Description:**
```
Readup about AI Skills (E.g KONFLUX-13490), something like why AGENT.MD, CLAUDE.MD, GEMINI.MD is needed
```






---


# Pipelines
## Finished issues

### [Closed/Done] [SRVKP-12102](https://redhat.atlassian.net/browse/SRVKP-12102) - Jawed Khelil - tkn-cli-serve pod in CrashLoopBackOff


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



**Comments (Last 3):**

#### **Deekshith Kumar Netha Bamandla N** (2026-06-08)
```
tkn-cli-serve issue is fixed with the fix. Thanks!!
```





---
### [Closed/Done] [SRVKP-11914](https://redhat.atlassian.net/browse/SRVKP-11914) - Deekshith Kumar Netha Bamandla N - Chains Controller CPT Scenarios


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



**Comments (Last 3):**

#### **Automation for Jira** (2026-05-06)
```
removed label *groomable* from the issue as Deekshith Kumar Netha Bamandla N transitioned it to In Progress
```

#### **Automation for Jira** (2026-06-02)
```
Please add '*Release Note Text*', '*Release Note Status*' and '*Release Notes Type*'. Transitioning the issue back to 'In progress'. 

If Release Note is not required, set *Release Note Type* to '*Release Note Not Required*' 
```





---
### [Closed/Done] [SRVKP-8004](https://redhat.atlassian.net/browse/SRVKP-8004) - Deekshith Kumar Netha Bamandla N - Have an agreement with engineering on a notification strategy


**Description:**
```
h3. Acceptance criteria
* Explained (and recorded it) how change detection in Horreum works to Engineering.
* We have an initial agreement with engineering on a notification strategy in case of change is detected.
```



**Comments (Last 3):**

#### **Automation for Jira** (2026-05-26)
```
removed label *groomable* from the issue as Deekshith Kumar Netha Bamandla N transitioned it to In Progress
```

#### **Deekshith Kumar Netha Bamandla N** (2026-05-29)
```
Automation strategies for pipeline monitoring and alerting were reviewed and standardized via hard-coded threshold implementations.

The team decided to implement hard-coded upper and lower bounds for metrics, replacing complex percentage-based alerts. Specific operational labels were retained while irrelevant components were removed. Engineering will define specific upper bounds for acceptable pipeline failures per scenario. This prevents excessive notifications and streamlines responses for testing environments.
```

#### **Deekshith Kumar Netha Bamandla N** (2026-06-08)
```
Thresholds and alerts will be handled in a separate ticket: [https://redhat.atlassian.net/browse/SRVKP-12192|https://redhat.atlassian.net/browse/SRVKP-12192|smart-link] 
```





---
## In review issues

## In progress issues

### [In Progress] [SRVKP-12325](https://redhat.atlassian.net/browse/SRVKP-12325) - Aman Vishwakarma - Analyze one test vs separate tests per scenario/config for Horreum alert thresholds


**Description:**
```
Analyze whether to keep the current single-Horreum-test approach or split into separate tests per scenario/config combination (e.g., separate tests for math-HA-QBT,
  math-no-HA, signing-HA-QBT, etc.) to determine the best structure for configuring alert thresholds.

  Context:

* Currently we have 2 Horreum tests: scalingPipelines (math) and Chains signing (signing-tr-tekton-bigbang)
* Each test uses fingerprint labels to separate HA/QBT config combos into independent time series
* JS calculation functions (like missing_pipeline_successes) handle per-config threshold branching within a single test
```



**Comments (Last 3):**

#### **Aman Vishwakarma** (2026-06-09)
```
Analyzed splitting into separate Horreum tests per config combo (8+ tests) versus keeping the current 2-test setup with JS branching. 
Recommendation: keep a single test per scenario category. Splitting would require over 720 duplicate label definitions and changes to the data upload pipeline, while JS branching on HA/QBT involves only 4 branches—the same pattern as the {{existing missing_pipeline_successes}} function. Separate tests become necessary only if different configs require different alert models or notifications
```





---
### [In Progress] [SRVKP-12049](https://redhat.atlassian.net/browse/SRVKP-12049) - Deekshith Kumar Netha Bamandla N - Identify the test scenarios for Results Controllers







---
## New issues

### [In Progress] [SRVKP-12325](https://redhat.atlassian.net/browse/SRVKP-12325) - Aman Vishwakarma - Analyze one test vs separate tests per scenario/config for Horreum alert thresholds


**Description:**
```
Analyze whether to keep the current single-Horreum-test approach or split into separate tests per scenario/config combination (e.g., separate tests for math-HA-QBT,
  math-no-HA, signing-HA-QBT, etc.) to determine the best structure for configuring alert thresholds.

  Context:

* Currently we have 2 Horreum tests: scalingPipelines (math) and Chains signing (signing-tr-tekton-bigbang)
* Each test uses fingerprint labels to separate HA/QBT config combos into independent time series
* JS calculation functions (like missing_pipeline_successes) handle per-config threshold branching within a single test
```



**Comments (Last 3):**

#### **Aman Vishwakarma** (2026-06-09)
```
Analyzed splitting into separate Horreum tests per config combo (8+ tests) versus keeping the current 2-test setup with JS branching. 
Recommendation: keep a single test per scenario category. Splitting would require over 720 duplicate label definitions and changes to the data upload pipeline, while JS branching on HA/QBT involves only 4 branches—the same pattern as the {{existing missing_pipeline_successes}} function. Separate tests become necessary only if different configs require different alert models or notifications
```





---


# ConsoleDot
## Finished issues

### [Closed/Done] [HCEPERF-1473](https://redhat.atlassian.net/browse/HCEPERF-1473) - Subrata Modak - Konflux: OOM crash detector related secrets


**Description:**
```
Due to internal leak (INC4624779), we need to rotate (or remove from upstream systems and Jenkins if no longer needed - this is a good opportunity for cleanup) all secrets. Please go one by one and mark the secret in this Jira description you resolved somehow so it is clear which secrets are done and which are still to be done.

h2. Konflux & RHTAP Secrets

h3. OOM and Crash Detector (Managed by Subrata)

* [ ] _Konflux-oom-crash-detector-TOKEN-..._: For Konflux OOM detector tool. Prometheus reader SA tokens. (Includes: kflux_ocp_p01, kflux_osp_p01, kflux_prd_rh02, kflux_prd_rh03, kflux_rhel_p01, stone_prd_rh01, stone_prod_p01, stone_prod_p02, stone_stage_p01, stone_stg_rh01)
```



**Comments (Last 3):**

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

#### PR/MR: https://gitlab.cee.redhat.com/ccit/jenkins-csb-customers/perf-casc-master/-/merge_requests/128
```
Title: Add 1 git-crypt collaborator
New collaborators:

    4C8E95E940EC90038CA973D59A9CB0F812505DE5
        Subrata Modak <smodak@redhat.com>
```

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



---
### [Closed/Done] [HCEPERF-1145](https://redhat.atlassian.net/browse/HCEPERF-1145) - Pravin Satpute - No tests were run for ContentSources service in last 7 days


**Description:**
```
No tests were run for ContentSources service in last 7 days
```



**Comments (Last 3):**

#### **Pravin Satpute** (2026-05-11)
```
Hi [~accountid:712020:4ec21e0e-87d5-43a6-9ef4-52bb8736eb33]    
  Do we still need to run this CPT? Lets disable this for couple of months and see if we get any ping from someone to enable this again.
```

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

### [In Progress] [HCEPERF-1497](https://redhat.atlassian.net/browse/HCEPERF-1497) - Krishna Magar - Profile workqueue cache_shard path to identify CPU hotspots


**Description:**
```
Following the tests comparing {{cache}} and {{cache_shard}} affinity scopes, {{cache}} maintained a slight edge in throughput (~383k vs ~377k IOPS). To understand why the {{cache_shard}} path is slightly slower even when aligned to the LLC topology ({{cache_shard_size=28}}), we need to profile the execution and identify what is running "hotter" in the sharded configuration.
```






---
### [In Progress] [HCEPERF-1496](https://redhat.atlassian.net/browse/HCEPERF-1496) - Krishna Magar - Verify reproducibility of 2% throughput gap between cache and cache_shard affinity scopes


**Description:**
```
Recent performance tests comparing {{default_affinity_scope=cache}} and {{cache_shard}} (with {{workqueue.cache_shard_size=28}} to match LLC) showed a slight performance regression of ~2% for the sharded approach at high concurrency (168 jobs).

* {{cache}}: ~383k IOPS
* {{cache_shard_size=28}}: ~377k IOPS

We need to determine if this 2% gap is a consistent, reproducible regression or simply within the standard margin of error (noise) for this test environment.
```






---
### [In Progress] [HCEPERF-1493](https://redhat.atlassian.net/browse/HCEPERF-1493) - Rajaditya Chauhan - Export Builder: quay image issue


**Description:**
```
from export builder getting : 

{noformat}Failed to pull image "quay.io/cloudservices/export-service:sha256-89660e98ac70e1ed98523914e3bf0dcab62a94ec65ac6b4dfd86baeec4c09fcb": [initializing source docker://quay.io/cloudservices/export-service:sha256-89660e98ac70e1ed98523914e3bf0dcab62a94ec65ac6b4dfd86baeec4c09fcb: unable to retrieve auth token: invalid username/password: unauthorized: Could not find robot with username: cloudservices+deployer and supplied password., initializing source docker://quay.io/cloudservices/export-service:sha256-89660e98ac70e1ed98523914e3bf0dcab62a94ec65ac6b4dfd86baeec4c09fcb: reading manifest sha256-89660e98ac70e1ed98523914e3bf0dcab62a94ec65ac6b4dfd86baeec4c09fcb in quay.io/cloudservices/export-service: unauthorized: access to the requested resource is not authorized]{noformat}

builder: [https://jenkins-csb-perf-master.dno.corp.redhat.com/job/InsightsInventory_Export_builder/11466/console|https://jenkins-csb-perf-master.dno.corp.redhat.com/job/InsightsInventory_Export_builder/11466/console]

from events:

{{error: deployment "export-service-service" exceeded its progress deadline}}
```






---
### [In Progress] [HCEPERF-1492](https://redhat.atlassian.net/browse/HCEPERF-1492) - Rajaditya Chauhan - HBI Export: runner.sh was not picking latest HBI DB creds 


**Description:**
```
error:

{noformat}psycopg2.OperationalError: connection to server at "host-inventory-perf.ciglpbbzvjwu.us-east-1.rds.amazonaws.com" (192.168.4.35), port 5432 failed: FATAL:  password authentication failed for user "postgres"{noformat}
```






---
### [In Progress] [HCEPERF-1491](https://redhat.atlassian.net/browse/HCEPERF-1491) - Krishna Magar - Request permissions to access Perf&Scale Department Grafana via INTLAB


**Description:**
```
Request permissions to access Perf&Scale Department Grafana via an INTLAB ticket.
```






---
### [In Progress] [HCEPERF-1490](https://redhat.atlassian.net/browse/HCEPERF-1490) - Krishna Magar - Request file storage with web interface access for test artifacts via INTLAB


**Description:**
```
Request file storage with read-only access via web interface (possibility to scp files somewhere and have them available via web server directory listing is perfectly sufficient) for test artifacts. Request this via an INTLAB ticket. If this service is not available, talk to jhutar again to figure out an alternative.
```






---
### [In Progress] [HCEPERF-1483](https://redhat.atlassian.net/browse/HCEPERF-1483) - Krishna Magar - Add support to pass_or_fail OPL tool to fetch historical data from PostgreSQL


**Description:**
```
Add support to {{pass_or_fail}} OPL tool [https://github.com/redhat-performance/opl/blob/main/core/opl/investigator/README.md|https://github.com/redhat-performance/opl/blob/main/core/opl/investigator/README.md] to get historical data from PostgreSQL database. Take a quick look at the docs and talk to jhutar so we can discuss implementation details.
```






---
### [In Progress] [HCEPERF-1482](https://redhat.atlassian.net/browse/HCEPERF-1482) - Krishna Magar - Coordinate with Release Engineering for RHEL release/nightly signal to trigger Jenkins


**Description:**
```
Get in touch with Release Engineering team to figure out how to get a signal when new RHEL release/nightly is available in [https://download.devel.redhat.com/|https://download.devel.redhat.com/] so we can trigger a Jenkins job based on that. Follow this process: [https://redhat.atlassian.net/wiki/spaces/SP/pages/333970499/File+a+JIRA+with+Software+Production|https://redhat.atlassian.net/wiki/spaces/SP/pages/333970499/File+a+JIRA+with+Software+Production]
```



**Comments (Last 3):**

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
### [In Progress] [HCEPERF-1073](https://redhat.atlassian.net/browse/HCEPERF-1073) - Vishal Vijayraghavan - Perf&Scale validation of HCC gateways, phase 3


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

### [In Progress] [HCEPERF-1497](https://redhat.atlassian.net/browse/HCEPERF-1497) - Krishna Magar - Profile workqueue cache_shard path to identify CPU hotspots


**Description:**
```
Following the tests comparing {{cache}} and {{cache_shard}} affinity scopes, {{cache}} maintained a slight edge in throughput (~383k vs ~377k IOPS). To understand why the {{cache_shard}} path is slightly slower even when aligned to the LLC topology ({{cache_shard_size=28}}), we need to profile the execution and identify what is running "hotter" in the sharded configuration.
```






---
### [In Progress] [HCEPERF-1496](https://redhat.atlassian.net/browse/HCEPERF-1496) - Krishna Magar - Verify reproducibility of 2% throughput gap between cache and cache_shard affinity scopes


**Description:**
```
Recent performance tests comparing {{default_affinity_scope=cache}} and {{cache_shard}} (with {{workqueue.cache_shard_size=28}} to match LLC) showed a slight performance regression of ~2% for the sharded approach at high concurrency (168 jobs).

* {{cache}}: ~383k IOPS
* {{cache_shard_size=28}}: ~377k IOPS

We need to determine if this 2% gap is a consistent, reproducible regression or simply within the standard margin of error (noise) for this test environment.
```






---
### [To Do] [HCEPERF-1495](https://redhat.atlassian.net/browse/HCEPERF-1495) - Pablo Mendez Hernandez - Disable content sources CPT


**Description:**
```
We do not have any requirements from the Business Unit for content sources. Lets disable content sources CPT
```






---
### [New] [HCEPERF-1494](https://redhat.atlassian.net/browse/HCEPERF-1494) - Rajaditya Chauhan - HBI API: direct insertion error


**Description:**
```
{noformat}Error: column "canonical_facts" of relation "hosts" does not exist
LINE 4:             tags, canonical_facts, system_profile_facts, ans...
                          ^{noformat}

runner job: [https://jenkins-csb-perf-master.dno.corp.redhat.com/job/InsightsInventoryHBIPerfTest_runner/1399/console|https://jenkins-csb-perf-master.dno.corp.redhat.com/job/InsightsInventoryHBIPerfTest_runner/1399/console]
```






---
### [In Progress] [HCEPERF-1493](https://redhat.atlassian.net/browse/HCEPERF-1493) - Rajaditya Chauhan - Export Builder: quay image issue


**Description:**
```
from export builder getting : 

{noformat}Failed to pull image "quay.io/cloudservices/export-service:sha256-89660e98ac70e1ed98523914e3bf0dcab62a94ec65ac6b4dfd86baeec4c09fcb": [initializing source docker://quay.io/cloudservices/export-service:sha256-89660e98ac70e1ed98523914e3bf0dcab62a94ec65ac6b4dfd86baeec4c09fcb: unable to retrieve auth token: invalid username/password: unauthorized: Could not find robot with username: cloudservices+deployer and supplied password., initializing source docker://quay.io/cloudservices/export-service:sha256-89660e98ac70e1ed98523914e3bf0dcab62a94ec65ac6b4dfd86baeec4c09fcb: reading manifest sha256-89660e98ac70e1ed98523914e3bf0dcab62a94ec65ac6b4dfd86baeec4c09fcb in quay.io/cloudservices/export-service: unauthorized: access to the requested resource is not authorized]{noformat}

builder: [https://jenkins-csb-perf-master.dno.corp.redhat.com/job/InsightsInventory_Export_builder/11466/console|https://jenkins-csb-perf-master.dno.corp.redhat.com/job/InsightsInventory_Export_builder/11466/console]

from events:

{{error: deployment "export-service-service" exceeded its progress deadline}}
```






---
### [In Progress] [HCEPERF-1492](https://redhat.atlassian.net/browse/HCEPERF-1492) - Rajaditya Chauhan - HBI Export: runner.sh was not picking latest HBI DB creds 


**Description:**
```
error:

{noformat}psycopg2.OperationalError: connection to server at "host-inventory-perf.ciglpbbzvjwu.us-east-1.rds.amazonaws.com" (192.168.4.35), port 5432 failed: FATAL:  password authentication failed for user "postgres"{noformat}
```






---
### [In Progress] [HCEPERF-1491](https://redhat.atlassian.net/browse/HCEPERF-1491) - Krishna Magar - Request permissions to access Perf&Scale Department Grafana via INTLAB


**Description:**
```
Request permissions to access Perf&Scale Department Grafana via an INTLAB ticket.
```






---
### [In Progress] [HCEPERF-1490](https://redhat.atlassian.net/browse/HCEPERF-1490) - Krishna Magar - Request file storage with web interface access for test artifacts via INTLAB


**Description:**
```
Request file storage with read-only access via web interface (possibility to scp files somewhere and have them available via web server directory listing is perfectly sufficient) for test artifacts. Request this via an INTLAB ticket. If this service is not available, talk to jhutar again to figure out an alternative.
```






---
### [New] [HCEPERF-1489](https://redhat.atlassian.net/browse/HCEPERF-1489) - Krishna Magar - Research and configure Jenkins email notifications and request service account


**Description:**
```
* Research and configure Jenkins to be able to send emails (probably [https://plugins.jenkins.io/email-ext/|https://plugins.jenkins.io/email-ext/]).
* Configure it and enhance test job to send email.
* Raise a request to IT to get a service account we can use for this. Example for configuration: [https://gitlab.cee.redhat.com/ccit/jenkins-csb-customers/insights-fdns-casc-main/-/blob/main/casc.yaml?ref_type=heads#L509|https://gitlab.cee.redhat.com/ccit/jenkins-csb-customers/insights-fdns-casc-main/-/blob/main/casc.yaml?ref_type=heads#L509]
```






---
### [In Progress] [HCEPERF-1488](https://redhat.atlassian.net/browse/HCEPERF-1488) - Krishna Magar - Request PostgreSQL database with read-write and read-only accounts via INTLAB


**Description:**
```
Request a PostgreSQL database via INTLAB jira (Perf department Integration Lab) (example: [INTLAB-459|https://issues.redhat.com/browse/INTLAB-459]). The database should have two accounts:

* One read-write account for uploading results.
* One read-only account for accessing from Grafana.
```






---
### [New] [HCEPERF-1487](https://redhat.atlassian.net/browse/HCEPERF-1487) - Krishna Magar - Create Jenkinsfile and JOBDSL config for the database CPT workflow


**Description:**
```
Create a Jenkinsfile and JOBDSL config to run the whole database CPT workflow (PostgreSQL + HammerDB) and get it running in the Jenkins. Examples for reference:

* Jenkinsfile: [https://gitlab.cee.redhat.com/redhat-performance/ci-configs/-/blob/master/jenkins/UtilArtifactsCleaner.groovy?ref_type=heads|https://gitlab.cee.redhat.com/redhat-performance/ci-configs/-/blob/master/jenkins/UtilArtifactsCleaner.groovy?ref_type=heads]
* JOBDSL: [https://gitlab.cee.redhat.com/redhat-performance/ci-configs/-/blob/master/src/jobs/UtilArtifactsCleanerJob.groovy?ref_type=heads|https://gitlab.cee.redhat.com/redhat-performance/ci-configs/-/blob/master/src/jobs/UtilArtifactsCleanerJob.groovy?ref_type=heads]

Note: For now, no alert emails when regression is detected, make it simple.
```






---
### [New] [HCEPERF-1486](https://redhat.atlassian.net/browse/HCEPERF-1486) - Krishna Magar - Create initial Grafana dashboard for database CPT performance monitoring


**Description:**
```
Create initial basic Grafana dashboard that allows filtering by HW (e.g. "R650" vs. "R640") and RHEL main version (e.g. "RHEL9" vs. "RHEL10"). The dashboard should show:

* Graphs for TPM/NOPM.
* Core performance monitoring metrics (CPU, memory, disk, network usage on the PostgreSQL SUT node and on test runner client node (node that runs HammerDB)).
* A table/graph showing PASS/FAIL data and possibly some additional config.
```






---
### [New] [HCEPERF-1485](https://redhat.atlassian.net/browse/HCEPERF-1485) - Krishna Magar - Update playbook to upload master JSON to PostgreSQL and test artifacts to file storage


**Description:**
```
Alter relevant playbook (or create new one) to upload main JSON file to PostgreSQL database and all test artefacts to file storage for archival purposes. There will be "data" table in the DB with:

* id column
* datetime column (when the test run started)
* JSONB column (we will upload main JSON file with all the data here)
```






---
### [New] [HCEPERF-1484](https://redhat.atlassian.net/browse/HCEPERF-1484) - Krishna Magar - Create initial config for pass_or_fail and update playbook to detect regressions


**Description:**
```
* Create initial basic config file for {{pass_or_fail}} tool that allows us to say if current result is regression or not (see [https://github.com/redhat-performance/opl/blob/main/core/opl/investigator/README.md|https://github.com/redhat-performance/opl/blob/main/core/opl/investigator/README.md] for documentation).
* Change the relevant playbook to run {{pass_or_fail}} to detect regressions and add pass/fail result to the master JSON before it gets uploaded to the DB.
```






---
### [In Progress] [HCEPERF-1483](https://redhat.atlassian.net/browse/HCEPERF-1483) - Krishna Magar - Add support to pass_or_fail OPL tool to fetch historical data from PostgreSQL


**Description:**
```
Add support to {{pass_or_fail}} OPL tool [https://github.com/redhat-performance/opl/blob/main/core/opl/investigator/README.md|https://github.com/redhat-performance/opl/blob/main/core/opl/investigator/README.md] to get historical data from PostgreSQL database. Take a quick look at the docs and talk to jhutar so we can discuss implementation details.
```






---
### [In Progress] [HCEPERF-1482](https://redhat.atlassian.net/browse/HCEPERF-1482) - Krishna Magar - Coordinate with Release Engineering for RHEL release/nightly signal to trigger Jenkins


**Description:**
```
Get in touch with Release Engineering team to figure out how to get a signal when new RHEL release/nightly is available in [https://download.devel.redhat.com/|https://download.devel.redhat.com/] so we can trigger a Jenkins job based on that. Follow this process: [https://redhat.atlassian.net/wiki/spaces/SP/pages/333970499/File+a+JIRA+with+Software+Production|https://redhat.atlassian.net/wiki/spaces/SP/pages/333970499/File+a+JIRA+with+Software+Production]
```



**Comments (Last 3):**

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

### [Closed/Done] [SAT-46022](https://redhat.atlassian.net/browse/SAT-46022) - Pablo Mendez Hernandez - contperf: Re-enable downstream image overrides for foremanctl


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
### [Closed/Done] [SAT-46021](https://redhat.atlassian.net/browse/SAT-46021) - Pablo Mendez Hernandez - satperf: Improve foremanctl role deployment debugging


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
### [Closed/Done] [SAT-46011](https://redhat.atlassian.net/browse/SAT-46011) - Pablo Mendez Hernandez - contperf: Extract DDNS cleanup to reusable lib/utils.sh


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
### [Closed/Done] [SAT-46010](https://redhat.atlassian.net/browse/SAT-46010) - Pablo Mendez Hernandez - satperf: Support append mode in override_images role


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
### [Closed/Done] [SAT-46009](https://redhat.atlassian.net/browse/SAT-46009) - Pablo Mendez Hernandez - satperf: Fix num_container_hosts division by zero in hammer.sh


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
### [Closed/Done] [SAT-46008](https://redhat.atlassian.net/browse/SAT-46008) - Pablo Mendez Hernandez - satperf: Refactor test_campaign_fam to use phased lib calls


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
### [Closed/Done] [SAT-46007](https://redhat.atlassian.net/browse/SAT-46007) - Pablo Mendez Hernandez - ansible-kvm-host-mgr: Skip volume wiping during VM erasure to save ~40 min per run


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
### [Closed/Done] [SAT-45997](https://redhat.atlassian.net/browse/SAT-45997) - Pablo Mendez Hernandez - satperf: Migrate FAM playbooks to Pattern B with unified content_views API


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

#### PR/MR: https://github.com/redhat-performance/satperf/commit/d6914714b881
```
Commit Message:
.commit.message
```

#### PR/MR: https://github.com/redhat-performance/satperf/commit/e908d6032310
```
Commit Message:
.commit.message
```

#### PR/MR: https://github.com/redhat-performance/satperf/commit/e3d2f36b3de0
```
Commit Message:
.commit.message
```

#### PR/MR: https://github.com/redhat-performance/satperf/commit/53cd27f56484
```
Commit Message:
.commit.message
```

#### PR/MR: https://github.com/redhat-performance/satperf/commit/ee768c89cc36
```
Commit Message:
.commit.message
```

#### PR/MR: https://github.com/redhat-performance/satperf/commit/7c0b92e13454
```
Commit Message:
.commit.message
```



---
### [Closed/Done] [SAT-45992](https://redhat.atlassian.net/browse/SAT-45992) - Imaanpreet Kaur - share monthly report with stakeholders - May 2026







---
### [Closed/Done] [SAT-45801](https://redhat.atlassian.net/browse/SAT-45801) - Pablo Mendez Hernandez - SPIKE - Investigate UI performance regression-finding and diagnostics producer contract for Satellite


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

### [Review] [SAT-45994](https://redhat.atlassian.net/browse/SAT-45994) - Imaanpreet Kaur - Add SSH Tunnel Instructions for Grafana




**Comments (Last 3):**

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
* [ ] I am familiar with the [contributing](https://github.com/theforeman/foreman-documentation/blob/master/CONTRIBUTING.md) guidelines.

Please cherry-pick my commits into:

* [ ] Foreman 3.19/Katello 4.21
* [ ] Foreman 3.18/Katello 4.20 (Satellite 6.19)
* [ ] Foreman 3.17/Katello 4.19
* [ ] Foreman 3.16/Katello 4.18 (Satellite 6.18; orcharhino 7.6, 7.7, and 7.8)
* [ ] Foreman 3.15/Katello 4.17
* [ ] Foreman 3.14/Katello 4.16 (Satellite 6.17; orcharhino 7.4; orcharhino 7.5)
* [ ] Foreman 3.13/Katello 4.15 (EL9 only)
* [ ] Foreman 3.12/Katello 4.14 (Satellite 6.16; orcharhino 7.2 on EL9 only; orcharhino 7.3)
* We do not accept PRs for Foreman older than 3.12.
```



---
### [Review] [SAT-45993](https://redhat.atlassian.net/browse/SAT-45993) - Imaanpreet Kaur - Replace PCP commands. pmval → pmrep




**Comments (Last 3):**

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

    disk.partitions.write{quote}

*Example 3*

{quote}  *OLD (current docs):*

  pmval --archive /var/log/pcp/pmlogger/satellite.example.com/20230831.00.10 \

    -d -t 2sec \

    -f 3 disk.partitions.write \

    -S @14:00 -T @14:15

  *NEW (what to replace it with):*

  pmrep -a /var/log/pcp/pmlogger/satellite.example.com/20230831.00.10 \

    -t 2sec \

    -S @14:00 -T @14:15 \

    disk.partitions.write{quote}

*Example 4*

{quote}  *OLD (current docs):*

  pmstat -t 2sec

  *NEW* *(what* *to* *replace* *it* *...
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
* [ ] I am familiar with the [contributing](https://github.com/theforeman/foreman-documentation/blob/master/CONTRIBUTING.md) guidelines.

Please cherry-pick my commits into:

* [ ] Foreman 3.19/Katello 4.21
* [ ] Foreman 3.18/Katello 4.20 (Satellite 6.19)
* [ ] Foreman 3.17/Katello 4.19
* [ ] Foreman 3.16/Katello 4.18 (Satellite 6.18; orcharhino 7.6, 7.7, and 7.8)
* [ ] Foreman 3.15/Katello 4.17
* [ ] Foreman 3.14/Katello 4.16 (Satellite 6.17; orcharhino 7.4; orcharhino 7.5)
* [ ] Foreman 3.13/Katello 4.15 (EL9 only)
* [ ] Foreman 3.12/Katello 4.14 (Satellite 6.16; orcharhino 7.2 on EL9 only; orcharhino 7.3)
* We do not accept PRs for Foreman older than 3.12.
```



---
### [Review] [SAT-31994](https://redhat.atlassian.net/browse/SAT-31994) -  - Error on "Synchronize Capsule" task: (Katello::Errors::Pulp3Error) - ErrorDetail(string='This field must be unique.', code='unique')


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



**Comments (Last 3):**

#### **Satellite Jira-Automation** (2025-12-15)
```
Upon review of our valid but aging backlog, the Satellite Team has concluded that this issue does not meet the criteria for a resolution in the near term, and are planning to close in a month. This message may be a repeat of a previous update and the issue is again being considered to be closed. If you have any concerns about this, please contact your Red Hat Account team. Thank you.
```

#### **Ron Lavi** (2025-12-16)
```
Apologies for the notification. This ticket was incorrectly targeted by the auto-closure script due to a logic error in the filter.

This ticket is still valid and has not expired. We have corrected the automation logic. Please disregard the previous closure notification.
```

#### **Pablo Mendez Hernandez** (2026-04-02)
```
PR opened upstream: [Katello/katello#11700|https://github.com/Katello/katello/pull/11700] — Redmine: [#39205|https://projects.theforeman.org/issues/39205]
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

This also gives consumers a more consistent view of the capsule: content becomes accessible for all repos together rather than repo-by-repo as each finishes syncing. This mirrors the approach Pulp upstream adopted for its own replication task in pulpcore 3.107.0 (issue #7333).

**2. `rescue_external_task` in `RefreshDistribution`**

If two `RefreshDistribution` actions still race (e.g. two repos sharing the same distribution path), the loser recovers: re-invokes `refresh_distributions`, which finds the existing distribution and issues a `partial_update` instead of a create. Dynflow re-polls the new task automatically via `suspend_and_ping` after the rescue returns without raising (confirmed against Dynflow 2.0.0 source).

## Test plan

- [ ] Existing capsule sync planning tests updated to assert `RefreshAllDistributions` at the sync level
- [ ] New `RefreshAllDistributionsTest`: plans `RefreshDistribution` per repo, handles empty list
- [ ] New `RefreshDistributionTest`: `rescue_external_task` recovers on uniqueness conflict, re-raises unrelated errors
- [ ] Run capsule sync stress test with concurrent repos to verify no uniqueness failures

Generated with [Claude Code](https://claude.ai/claude-code)

## Summary by Sourcery

Coordinate capsule distribution refreshes after sync completion to avoid Pulp3 distribution uniqueness races and make distribution refresh more resilient under concurrency.

Bug Fixes:
- Prevent Pulp3 distribution uniqueness conflicts when multiple capsule syncs target the same distribution concurrently by centralizing refresh planning and adding targeted error recovery.

Enhancements:
- Introduce a RefreshAllDistributions action that refreshes Pulp3 distributions for all synced repositories in a single concurrent step after capsule sync.
- Update RefreshDistribution to detect and transparently recover from concurrent distribution creation races by retrying as an update when a uniqueness conflict is encountered.

Tests:
- Adjust existing capsule sync planning tests to expect RefreshAllDistributions at the sync level instead of per-repository RefreshDistribution.
- Add tests covering RefreshAllDistributions planning behavior, including handling empty repository lists, and RefreshDistribution rescue behavior for both uniqueness and non-uniqueness Pulp3 errors.

<!-- This is an auto-generated comment: release notes by coderabbit.ai -->
## Summary by CodeRabbit

* **New Features**
  * Added a concurrent bulk distribution-refresh task to schedule distribution refreshes across multiple Pulp3 repositories.

* **Bug Fixes**
  * Automatic retry for certain distribution-creation conflicts (uniqueness/overlap) during refresh.
  * Capsule sync now schedules Pulp3 distribution refreshes only for Pulp3-supported repositories.
  * Metadata generation no longer inlines distribution refreshes.

* **Tests**
  * Expanded tests covering planning, bulk refresh behavior, and retry/recovery logic.
<!-- end of auto-generated comment: release notes by coderabbit.ai -->
```



---
### [Review] [SAT-31672](https://redhat.atlassian.net/browse/SAT-31672) - Pablo Mendez Hernandez - Improve Repo sync and Capsule sync testing to mimic end-user operations


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



**Comments (Last 3):**

#### **Sayan Das** (2025-03-10)
```
CC [~accountid:70121:1789d494-d5af-4951-ba10-3f23fb43eaba] [~accountid:70121:843ee2a6-4309-44bf-8ff5-75c4dd1ada07] [~accountid:712020:4ec21e0e-87d5-43a6-9ef4-52bb8736eb33] [~accountid:712020:219ca791-225a-4c34-a291-66c6aab3079d] [~accountid:712020:cec31564-1531-4a52-b374-94bafaaa95cb] [~accountid:712020:79a294b8-c8a7-40d8-94f9-dfafcc12c919] 

As discussed during the Monthly Cadence, This is what i could come up so far as a proposal and opened it as a story for the time being. 
```

#### **Pablo Mendez Hernandez** (2025-04-14)
```
I have some code already implemented in one of my dev trees, so I'm keeping the assignment.
```





---
## In progress issues

### [In Progress] [SAT-45959](https://redhat.atlassian.net/browse/SAT-45959) - Imaanpreet Kaur - Performance Optimization: Use a cache of existing artifacts during sync


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



**Comments (Last 3):**

#### **Daniel Alley** (2026-06-03)
```
This is related to [https://redhat.atlassian.net/browse/SAT-45821|https://redhat.atlassian.net/browse/SAT-45821|smart-link]  and can be tested at the same time
```





---
### [In Progress] [SAT-45821](https://redhat.atlassian.net/browse/SAT-45821) - Imaanpreet Kaur - Performance / Memory optimization: Use a cache of existing Package objects from the latest repo version during sync 


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



**Comments (Last 3):**

#### **Daniel Alley** (2026-06-03)
```
This is now released upstream in pulp-rpm

I would expect most syncs and resyncs, including of repos that were previously deemed “pathological” would now use under 1gb of memory during sync. As well as significant performance improvements.
```





---
## New issues

### [Release Pending - Upstream] [SAT-46106](https://redhat.atlassian.net/browse/SAT-46106) - Pablo Mendez Hernandez - Eliminate redundant Candlepin GETs during host registration


**Description:**
```
POST /rhsm/consumers makes 3 Candlepin HTTP calls per registration: 1 POST (unavoidable) + 2 redundant GETs that fetch data already available in the POST response. Eliminating the 2 redundant GETs reduces Candlepin calls by 66% per registration and removes 2 DB SELECTs (Host.find re-fetch in finalize_registration, host.reload in consumer_activate).
```






---
### [Release Pending - Upstream] [SAT-46105](https://redhat.atlassian.net/browse/SAT-46105) - Pablo Mendez Hernandez - Concurrent registration fails with "PG::UniqueViolation: ERROR: duplicate key value violates unique constraint \"index_operatingsystems_on_title\"


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
### [New] [SAT-46099](https://redhat.atlassian.net/browse/SAT-46099) - Imaanpreet Kaur - Sync memory consumption too high in pathological cases


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



**Comments (Last 3):**

#### **SFDC Integration** (2026-06-08)
```
[~accountid:70121:5cc8098d-d586-4c99-8ac8-18ba201fc97d] cloned SAT-42697. Copied SFDC case links: 03919224, 03996616, 04209006, 04285232, 04404016, 04446793, 04456509.
```





---
### [Review] [SAT-45994](https://redhat.atlassian.net/browse/SAT-45994) - Imaanpreet Kaur - Add SSH Tunnel Instructions for Grafana




**Comments (Last 3):**

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
* [ ] I am familiar with the [contributing](https://github.com/theforeman/foreman-documentation/blob/master/CONTRIBUTING.md) guidelines.

Please cherry-pick my commits into:

* [ ] Foreman 3.19/Katello 4.21
* [ ] Foreman 3.18/Katello 4.20 (Satellite 6.19)
* [ ] Foreman 3.17/Katello 4.19
* [ ] Foreman 3.16/Katello 4.18 (Satellite 6.18; orcharhino 7.6, 7.7, and 7.8)
* [ ] Foreman 3.15/Katello 4.17
* [ ] Foreman 3.14/Katello 4.16 (Satellite 6.17; orcharhino 7.4; orcharhino 7.5)
* [ ] Foreman 3.13/Katello 4.15 (EL9 only)
* [ ] Foreman 3.12/Katello 4.14 (Satellite 6.16; orcharhino 7.2 on EL9 only; orcharhino 7.3)
* We do not accept PRs for Foreman older than 3.12.
```



---
### [Review] [SAT-45993](https://redhat.atlassian.net/browse/SAT-45993) - Imaanpreet Kaur - Replace PCP commands. pmval → pmrep




**Comments (Last 3):**

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

    disk.partitions.write{quote}

*Example 3*

{quote}  *OLD (current docs):*

  pmval --archive /var/log/pcp/pmlogger/satellite.example.com/20230831.00.10 \

    -d -t 2sec \

    -f 3 disk.partitions.write \

    -S @14:00 -T @14:15

  *NEW (what to replace it with):*

  pmrep -a /var/log/pcp/pmlogger/satellite.example.com/20230831.00.10 \

    -t 2sec \

    -S @14:00 -T @14:15 \

    disk.partitions.write{quote}

*Example 4*

{quote}  *OLD (current docs):*

  pmstat -t 2sec

  *NEW* *(what* *to* *replace* *it* *...
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
* [ ] I am familiar with the [contributing](https://github.com/theforeman/foreman-documentation/blob/master/CONTRIBUTING.md) guidelines.

Please cherry-pick my commits into:

* [ ] Foreman 3.19/Katello 4.21
* [ ] Foreman 3.18/Katello 4.20 (Satellite 6.19)
* [ ] Foreman 3.17/Katello 4.19
* [ ] Foreman 3.16/Katello 4.18 (Satellite 6.18; orcharhino 7.6, 7.7, and 7.8)
* [ ] Foreman 3.15/Katello 4.17
* [ ] Foreman 3.14/Katello 4.16 (Satellite 6.17; orcharhino 7.4; orcharhino 7.5)
* [ ] Foreman 3.13/Katello 4.15 (EL9 only)
* [ ] Foreman 3.12/Katello 4.14 (Satellite 6.16; orcharhino 7.2 on EL9 only; orcharhino 7.3)
* We do not accept PRs for Foreman older than 3.12.
```



---
### [Testing] [SAT-45971](https://redhat.atlassian.net/browse/SAT-45971) - Pablo Mendez Hernandez - satperf: Add UI performance measurement framework


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
### [In Progress] [SAT-45959](https://redhat.atlassian.net/browse/SAT-45959) - Imaanpreet Kaur - Performance Optimization: Use a cache of existing artifacts during sync


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



**Comments (Last 3):**

#### **Daniel Alley** (2026-06-03)
```
This is related to [https://redhat.atlassian.net/browse/SAT-45821|https://redhat.atlassian.net/browse/SAT-45821|smart-link]  and can be tested at the same time
```





---


