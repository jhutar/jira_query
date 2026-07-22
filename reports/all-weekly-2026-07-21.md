# Team Konflux
* **Weekly Overview:** This week, the Konflux team completed key performance migrations and enhanced automation capabilities, most notably migrating continuous performance testing (CPT) probe jobs directly to PostgreSQL, and introducing Red Hat Support Case creation for ROSA/OSD platform incidents.
* **What was done:**
  * **Direct PostgreSQL Migration ([KONFLUX-15036](https://redhat.atlassian.net/browse/KONFLUX-15036) — 3sp):** Migrated continuous performance testing jobs from the Horreum-mediated pipeline directly to PostgreSQL, eliminating Horreum as a point of failure and restoring trending dashboard statuses using custom Python label computation scripts.
  * **Support Case Integration ([KONFLUX-14299](https://redhat.atlassian.net/browse/KONFLUX-14299) — 5sp):** Enhanced the OOM/CrashLoopBackOff automation tool to create Red Hat Support Cases for ROSA/OSD platform incidents, incorporating Atlassian Document Format (ADF) formatting and diagnostics file attachments.
  * **CI Stability and Login Rewrites:** Corrected `tenants-config-test` CI pipeline OOM failures (`exit code: 137`) caused by shallow clone merge-base issues ([KONFLUX-14890](https://redhat.atlassian.net/browse/KONFLUX-14890) — 2sp), and rewrote `oclogin`/`oclogin-all` helpers ([KONFLUX-14891](https://redhat.atlassian.net/browse/KONFLUX-14891)) with color-coded status reporting and stale context cleanup.
* **What is moving:**
  * **ServiceAccount Security Migration ([KONFLUX-14970](https://redhat.atlassian.net/browse/KONFLUX-14970) — 2sp):** Completed auditing and cleanups of user-created ServiceAccounts across clusters for security policy compliance (currently in review).
  * **Fedora RPM/Mock Build Blockage ([ROK-2118](https://redhat.atlassian.net/browse/ROK-2118)):** Escalated a 30-day block (Mock 6.6 digest mismatch) to Major and coordinated with stakeholders to unblock the Fedora rpmbuild environment container image rebuild ([MR #129](https://gitlab.com/fedora/infrastructure/konflux/rpmbuild-pipeline-environment-container/-/merge_requests/129)).
  * **Quay.io Dependency Risk Analysis ([KONFLUX-15081](https://redhat.atlassian.net/browse/KONFLUX-15081) — 2sp):** Initiated capacity outreach to `quay-performance-scripts` maintainers to evaluate Quay.io scalability readiness under 100x Konflux-shaped traffic growth (currently in progress).

# Team Pipelines
* **Weekly Overview:** The Pipelines team successfully mitigated severe CI performance saturation on build infrastructure and expanded observability by extending the validation framework to encompass modern OpenTelemetry metrics.
* **What was done:**
  * **CI Infrastructure De-saturation ([SRVKP-12781](https://redhat.atlassian.net/browse/SRVKP-12781) — 2sp):** Redesigned the Performance cron schedule ([PR #81738](https://github.com/openshift/release/pull/81738)) to group jobs sequentially by variant with 2-hour spacing, reducing peak concurrent jobs from ~12–15 to ~4, thereby preventing Boskos lease exhaustion.
  * **OpenTelemetry Validation ([SRVKP-12643](https://redhat.atlassian.net/browse/SRVKP-12643) — 3sp):** Extended the performance validation framework to support API-level validation of OpenTelemetry metrics across the Pipelines Controller, Chains Controller, and Tekton Results, establishing a unified validation suite.
* **What is moving:**
  * **Version Lifecycle CLI Tool ([SRVKP-12000](https://redhat.atlassian.net/browse/SRVKP-12000) — 2sp):** Submitted CLI tool `manage-perf-crons.py` ([PR #82005](https://github.com/openshift/release/pull/82005)) to automate YAML modifications during cron updates (currently in review and blocked by GitHub Actions branch protection permission failures).
  * **Metrics vs Results Discrepancy Investigation ([SRVKP-9637](https://redhat.atlassian.net/browse/SRVKP-9637) — 3sp):** Preparing test environments to investigate why the Prometheus `pipelinerun_total` metric is consistently 10% higher than Tekton Results counts under load (currently in progress).

# Team ConsoleDot
* **Weekly Overview:** The ConsoleDot team successfully completed a major gRPC performance suite rewrite from Locust to K6 and established robust, automated containerization pipelines in the Konflux tenant space.
* **What was done:**
  * **Kessel K6 Suite Rewrite ([HCEPERF-1547](https://redhat.atlassian.net/browse/HCEPERF-1547) — 3sp):** Ported all 12 Kessel Inventory gRPC API scenarios from Locust to K6 to prevent Locust-induced response time inflation. Resolved a critical `junitparser>=5` bug in the shared `opl` library ([PR #179](https://github.com/redhat-performance/opl/pull/179)) that silenced ReportPortal logs.
  * **Container Onboarding to Konflux ([HCEPERF-1517](https://redhat.atlassian.net/browse/HCEPERF-1517) / [HCEPERF-1516](https://redhat.atlassian.net/browse/HCEPERF-1516) — 3sp each):** Onboarded the `db-cpt-rhel` test repository to the Konflux tenant space and designed a secure, self-contained Ansible controller `Dockerfile` with automated build-time syntax checks, publishing the public image to `quay.io/rhcloudperfscale/db-cpt-rhel`.
  * **Secret Cleanup ([HCEPERF-1412](https://redhat.atlassian.net/browse/HCEPERF-1412) — 1sp):** Audited and successfully rotated compromised credentials following an internal leak, revoking the default service account and deleting an obsolete Google Chat webhook.
* **What is moving:**
  * **Lightweight Host Provisioning Playbook ([HCEPERF-1345](https://redhat.atlassian.net/browse/HCEPERF-1345) — 5sp):** Automated VM-container creation and registration of `rhcd` clients to ConsoleDot Stage over MQTT networks (currently in review).
  * **HBI Inventory Views Performance Epic ([HCEPERF-1573](https://redhat.atlassian.net/browse/HCEPERF-1573)):** Drafted testing plan and epic structure to validate the unified `/beta/hosts-view` endpoint under concurrent load once host app data is seeded (currently in progress).
  * **GitHub PR CPT Triggering ([HCEPERF-781](https://redhat.atlassian.net/browse/HCEPERF-781)):** Blocked by permission limitations ("User is not allowed to trigger CI") when trying to automatically trigger performance checks on PR submission (currently in progress).

# Team Satellite
* **Weekly Overview:** The Satellite team published critical monthly performance reports and defined initial Candlepin tuning matrices to optimize heap memory allocation during scalable host registrations.
* **What was done:**
  * **June Monthly Performance Report ([SAT-47767](https://redhat.atlassian.net/browse/SAT-47767) — 3sp):** Finalized and successfully distributed the June 2026 Satellite performance and scale report to key stakeholders.
  * **Registration Performance Alignment ([SAT-47712](https://redhat.atlassian.net/browse/SAT-47712)):** Grouped diverse registration performance tasks, Smart-Proxy bottlenecks, and heavy fact-import overhead under a unified Epic for coordinated tracking.
* **What is moving:**
  * **Candlepin Tuning Implementation ([SAT-47759](https://redhat.atlassian.net/browse/SAT-47759) — 1sp):** Defined initial tuning values (`-Xms`/`-Xmx`) to pre-allocate heap memory and minimize GC overhead. Currently in progress with associated tasks to load/apply variables via playbooks ([SAT-47760](https://redhat.atlassian.net/browse/SAT-47760) / [SAT-47716](https://redhat.atlassian.net/browse/SAT-47716) / [SAT-47762](https://redhat.atlassian.net/browse/SAT-47762)).
  * **API Provisioning Race Condition ([SAT-46037](https://redhat.atlassian.net/browse/SAT-46037) — 5sp):** Investigating database transaction serialization flaws that insert `NULL` host types under high concurrent thread provisioning, blocking physical client registration (currently in progress).
  * **Capsule Sync OOM Blockage ([SAT-45686](https://redhat.atlassian.net/browse/SAT-45686) — 5sp):** Blocked on Capsule 6.18 complete synchronizations due to `pulpcore-worker` processes consuming up to 9 GB RSS per process, triggering kernel OOM killer events on 32 GB RAM nodes (currently in progress).
