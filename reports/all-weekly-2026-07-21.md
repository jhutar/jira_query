# Performance & Scale Weekly Status Report — July 21, 2026

## Weekly Overview
This week, the Performance & Scale organization delivered critical infrastructure enhancements and architectural migrations across all key product areas. Most notably, the **Konflux** team successfully bypassed Horreum in its continuous performance testing (CPT) pipeline by implementing a direct-to-PostgreSQL push, while the **ConsoleDot** team completed a highly requested gRPC test suite rewrite into K6 and resolved long-standing ReportPortal logging bottlenecks. Concurrently, the **Pipelines** team optimized CI execution by reducing resource saturation on build nodes by over 70%, and the **Satellite** team established net-new tuning parameters for Candlepin deployments, paving the way for improved high-concurrency host registration.

---

## 1. Konflux Team

### Key Activities & Outcomes (Team Highlights)
* **CPT Horreum-Bypass Migration ([KONFLUX-15036](https://redhat.atlassian.net/browse/KONFLUX-15036) — 3sp):** Migrated active continuous performance testing (CPT) probe jobs from the Horreum-mediated pipeline directly to PostgreSQL. Developed local python scripts (`compute-labels.py`, `labels-to-postgresql.py`, `compare-labels.py`) utilizing `jsonpath_ng` for label calculation, eliminating Horreum as a point of failure and restoring green statuses across all active probe runs on the trending dashboard.
* **Support Case Integration for Platforms ([KONFLUX-14299](https://redhat.atlassian.net/browse/KONFLUX-14299) — 5sp):** Enhanced the OOM/CrashLoopBackOff automated Jira reporting tool. Implemented a human-in-the-loop workflow via `support_case_lib.py` that routes ROSA/OSD platform namespace incidents to Red Hat Customer Portal Support Cases (utilizing offline token authentication and multipart attachments) instead of Jira tickets, meeting SRE and MCS leadership mandates. Included Atlassian Document Format (ADF) descriptions, diagnostic file attachment limits, and smart filtering, which is projected to reduce false positives by 40–60%.
* **CI Stability & Script Robustness:**
  * Fixed recurring `tenants-config-test` CI pipeline OOM failures (`exit code: 137`) caused by a shallow clone git-fetch fallback ([KONFLUX-14890](https://redhat.atlassian.net/browse/KONFLUX-14890) — 2sp). Resolved by fetching the target merge request branch and fixing merge-base diff resolution in `get-changed-tenants.sh`.
  * Rewrote `oclogin` and `oclogin-all` helper scripts ([KONFLUX-14891](https://redhat.atlassian.net/browse/KONFLUX-14891)) with color-coded status reporting, stale context cleanups, and a smart login flow that skips already-authenticated clusters, streamlining the developer feedback loop.
  * Added configurable build query windows (`--count`) to the `jenkins_investigator.py` tool ([KONFLUX-14942](https://redhat.atlassian.net/browse/KONFLUX-14942)) to support longer weekly probe investigations.
* **ArgoCD Work Planning ([KONFLUX-14431](https://redhat.atlassian.net/browse/KONFLUX-14431) — 2sp):** Established 5 Epics ([KONFLUX-15125](https://redhat.atlassian.net/browse/KONFLUX-15125) to [KONFLUX-15129](https://redhat.atlassian.net/browse/KONFLUX-15129)) and completed a detailed task breakdown for replicated ArgoCD Agent and GitOps performance testing on ScaleLab bare-metal nodes.

### Weekly Momentum & Blockers
* **Transitions to Review:**
  * Completed auditing and sanitizing user-created ServiceAccounts across multiple clusters for compliance with updated security token policies ([KONFLUX-14970](https://redhat.atlassian.net/browse/KONFLUX-14970) — 2sp).
  * Expanded read-only cluster access by adding 5 new engineers (`maypatil`, `gkakade`, `obochan`, `sudv`, `lrossett`) to the `konflux-performance` Rover group ([KONFLUX-14944](https://redhat.atlassian.net/browse/KONFLUX-14944)).
* **Active Blockers:**
  * **[ROK-2118](https://redhat.atlassian.net/browse/ROK-2118):** Escalated to **Major** priority. The Fedora RPM/hermetic Mock probe builds have been blocked for ~30 days because of a digest mismatch error in Mock 6.6. While Mock 6.7 resolves this, shipping it is currently blocked by a broken Fedora rpmbuild environment container build pipeline ([MR #129](https://gitlab.com/fedora/infrastructure/konflux/rpmbuild-pipeline-environment-container/-/merge_requests/129)). Slack outreach to `#forum-rhel-on-konflux` and Pavel Raiskup is ongoing to unblock.
  * **[KONFLUX-14805](https://redhat.atlassian.net/browse/KONFLUX-14805) (2sp):** Staging and production Quay authentication errors on `create-trusted-artifact` have been bypassed by merging PRs [#13035](https://github.com/redhat-appstudio/infra-deployments/pull/13035) and [#13036](https://github.com/redhat-appstudio/infra-deployments/pull/13036) (adding explicit `oci-storage` parameters). Validation is underway before reverting temporary write permissions.

### Looking Ahead
* **Quay.io Dependency Risk Assessment ([KONFLUX-15081](https://redhat.atlassian.net/browse/KONFLUX-15081) — 2sp):** Initiated outreach to `quay-performance-scripts` contributors (including Joe Talerico and Vishnu Challa) to assess Quay.io's capacity to handle a projected 100x increase in Konflux-shaped traffic (concurrent pipeline pushes and multi-arch image builds).
* **Tekton Reference Pinning ([KONFLUX-14479](https://redhat.atlassian.net/browse/KONFLUX-14479)):** Continuing efforts to pin mutable git references to immutable commit SHAs in `konflux-probe-test-templates` to prevent GitLab/GitHub API 429 rate-limiting and enable Tekton pipeline caching.
* **Onboarding:** Progressing several onboarding, architecture research, and hands-on learning tasks for new team members (Lucas Bacciotti Moreira, Suhaas Bhat, and Bogdan Benea) across issues [KONFLUX-15054](https://redhat.atlassian.net/browse/KONFLUX-15054) to [KONFLUX-15049](https://redhat.atlassian.net/browse/KONFLUX-15049).

---

## 2. Pipelines Team

### Key Activities & Outcomes (Team Highlights)
* **CI Infrastructure Saturation Fix ([SRVKP-12781](https://redhat.atlassian.net/browse/SRVKP-12781) — 2sp):** Diagnosed severe `aws-pipelines-performance` Boskos pool saturation on build node `build06` (jobs pending for >1 hour). Redesigned the Performance cron schedule ([PR #81738](https://github.com/openshift/release/pull/81738)) to group jobs by deployment variant (Standard, HA, QBT) on dedicated days of the week, with sequential 2-hour spacing. This optimization reduces peak normal concurrency from ~12–15 parallel jobs to a stable maximum of ~4–5, resolving the Boskos lease ceiling bottleneck.
* **OpenTelemetry Metrics Validation ([SRVKP-12643](https://redhat.atlassian.net/browse/SRVKP-12643) — 3sp):** Extended the performance validation framework to support API-level validation of OpenTelemetry metrics across the Pipelines Controller, Chains Controller, and Tekton Results. This ensures backward compatibility with OpenCensus while verifying the newer OTel metrics migration. Conducted validation runs using clusterbot and published a complete report.
* **Outage Cleanup ([SRVKP-12876](https://redhat.atlassian.net/browse/SRVKP-12876) — 2sp):** Manually cleaned up duplicate runs and orphaned labels in Horreum following a series of service outages.

### Weekly Momentum & Blockers
* **Transitions to Review:**
  * **[SRVKP-12000](https://redhat.atlassian.net/browse/SRVKP-12000) (2sp):** Developed and submitted a CLI tool (`manage-perf-crons.py`) via [PR #82005](https://github.com/openshift/release/pull/82005) to automate YAML manipulation during Pipelines version lifecycles (add, remove, promote). The pull request is currently blocked by a GitHub Actions branch protection permission error (`Bot openshift-merge-robot does not have admin access`).

### Looking Ahead
* **Metrics Discrepancy Investigation ([SRVKP-9637](https://redhat.atlassian.net/browse/SRVKP-9637) — 3sp):** Preparing to execute precise high-load testing to root-cause why the Prometheus `tekton_pipelines_controller_pipelinerun_total` metric is consistently 10% higher than the count returned by Tekton Results (testing controller restart, reconciliation retry, and Result storage write-failure theories).
* **CPT Reporting Template ([SRVKP-11997](https://redhat.atlassian.net/browse/SRVKP-11997) — 2sp):** Planning a PostgreSQL-based script to auto-generate summary KB articles on resource usage changes from Horreum-mirrored data.

---

## 3. ConsoleDot Team

### Key Activities & Outcomes (Team Highlights)
* **Kessel Test Suite Port to K6 ([HCEPERF-1547](https://redhat.atlassian.net/browse/HCEPERF-1547) — 3sp):** Fully migrated all 12 Kessel Inventory gRPC API scenarios from Locust to K6 to prevent Locust-induced response time inflation.
  * **Crucial OPL Fix:** Root-caused a critical bug in the shared `opl` library ([PR #179](https://github.com/redhat-performance/opl/pull/179)) where a `junitparser>=5` deep-copy behavior change silently dropped test cases and logs from ReportPortal. Pinned and corrected the tree mutation.
  * Corrected runner locks ([Commit #e7ed981](https://gitlab.cee.redhat.com/redhat-performance/ci-configs/-/commit/e7ed981ed16ab259e2cdf524b3997ffed6d2d752)), widened the ReportPortal-to-Elasticsearch sync window to 144 launches (3 days), and increased the K6 runner execution frequency to every 4 hours to accelerate data collection.
* **Onboarding & Containerization to Konflux:**
  * **[HCEPERF-1517](https://redhat.atlassian.net/browse/HCEPERF-1517) — 3sp:** Successfully onboarded the `db-cpt-rhel` test repository to the `hcc-perfscale-tenant` Konflux namespace, setting up automated Tekton build pipelines on push and pull requests.
  * **[HCEPERF-1516](https://redhat.atlassian.net/browse/HCEPERF-1516) — 3sp:** Designed a secure, self-contained `Dockerfile` for the Ansible controller benchmark image. Integrated build-time playbook syntax and tooling checks (`container-sanity-check.sh`) and published the public image to `quay.io/rhcloudperfscale/db-cpt-rhel` with zero embedded secrets.
* **Dead Secret Remediation ([HCEPERF-1412](https://redhat.atlassian.net/browse/HCEPERF-1412) — 1sp):** Audited and cleaned up compromised or unused secrets following an internal leak. Revoked the `consoledot-perfscale-service-account` and deleted the obsolete `Satellite6_Perf_Eng` Google Chat webhook.
* **Gosmee Server Hardening ([HCEPERF-1009](https://redhat.atlassian.net/browse/HCEPERF-1009) — 2sp):** Replaced an un-audited external image (`ghcr.io/chmouel/gosmee:main`) in the `smee-proxy` namespace with a secure, pinned, Konflux-built UBI9-based image.

### Weekly Momentum & Blockers
* **Transitions to Review:**
  * **[HCEPERF-1345](https://redhat.atlassian.net/browse/HCEPERF-1345) (5sp):** Developed an automated playbook that provisions lightweight containers on a target VM, registers them with `rhcd` on ConsoleDot Stage, and successfully verifies remote execution over MQTT networks.
* **Active Blockers:**
  * **GitHub PR CPT Triggering ([HCEPERF-781](https://redhat.atlassian.net/browse/HCEPERF-781)):** Blocked by permission limits while trying to trigger performance verification checks automatically on PR submissions (receiving "User is not allowed to trigger CI" errors). Outreach is underway with repo maintainers to gain proper write/maintainer access.

### Looking Ahead
* **HBI Inventory Views Performance Testing ([HCEPERF-1573](https://redhat.atlassian.net/browse/HCEPERF-1573)):** Planning a major perf validation of the unified `/beta/hosts-view` endpoint under concurrent load once host and downstream app metrics have been seeded in the database.
* **Agentic CPT Skill Validation ([HCEPERF-1580](https://redhat.atlassian.net/browse/HCEPERF-1580)):** Validating the `hceperf-cpt-skills` automated onboarding framework by diffing its generated configurations against Kessel's manually tuned K6 benchmarks.
* **Stale Onboarding Recovery ([HCEPERF-1579](https://redhat.atlassian.net/browse/HCEPERF-1579)):** Assessing the status of the stale Chrome service CPT to enable its automated Locust, WebSocket, and Kafka testing pipelines.

---

## 4. Satellite Team

### Key Activities & Outcomes (Team Highlights)
* **Stakeholder Monthly Report ([SAT-47767](https://redhat.atlassian.net/browse/SAT-47767) — 3sp):** Finalized and successfully emailed the June 2026 Satellite performance and scale monthly report to key stakeholders.
* **Candlepin Tuning Profile Definitions ([SAT-47759](https://redhat.atlassian.net/browse/SAT-47759) — 1sp):** Created a comprehensive matrix defining initial Candlepin tuning values (`-Xms` / `-Xmx`) for each of Satellite's standard deployment tiers (Default, Medium, Large, Extra-Large, Extra-Extra-Large) to pre-allocate heap memory and minimize Garbage Collection (GC) overhead during high-concurrency registration testing.
* **Registration Performance Epic ([SAT-47712](https://redhat.atlassian.net/browse/SAT-47712)):** Formed a centralized Epic to coordinate multiple registration-path optimization streams, targeting redundant smart-proxy, Katello, and Candlepin operations, as well as heavy fact-import overhead.

### Weekly Momentum & Blockers
* **Transitions to Review:** Defined the profile variables and custom-hiera structure to apply the net-new Candlepin values securely across different systems.
* **In-Progress Work (Tuning Role Integration):**
  * Adding Candlepin tuning configuration support to the `satperf` tune role ([SAT-47716](https://redhat.atlassian.net/browse/SAT-47716)).
  * Creating variable definition files under `playbooks/satellite/roles/tune/vars/` ([SAT-47760](https://redhat.atlassian.net/browse/SAT-47760) — 1sp).
* **Active Blockers:**
  * **API Host Provisioning Race Condition ([SAT-46037](https://redhat.atlassian.net/browse/SAT-46037) — 5sp):** Under high API concurrency (e.g., 20 parallel threads using Ansible), incomplete transactions commit blank or `NULL` host types in the Foreman database. This causes physical client registrations to fail with `422 Unprocessable Entity` errors. Investigation is active, looking into database transaction serialization.
  * **Capsule Sync OOM Killer ([SAT-45686](https://redhat.atlassian.net/browse/SAT-45686) — 5sp):** On Satellite Capsule 6.18, complete repository sync tasks trigger high memory consumption (5–9 GB RSS per process) across multiple `pulpcore-worker` processes, leading to kernel OOM killer events. This is currently blocking complete Capsule synchronizations on 32 GB RAM nodes.

### Looking Ahead
* **Candlepin Verification ([SAT-47763](https://redhat.atlassian.net/browse/SAT-47763) — 3sp):** Automating and testing Candlepin hiera changes on target systems to ensure proper CPU/RAM profile auto-detection.
* **Puma Optimization ([SAT-41838](https://redhat.atlassian.net/browse/SAT-41838) — 8sp):** Planning multi-trial tests to optimize worker counts and thread allocations across standard environment sizes.
