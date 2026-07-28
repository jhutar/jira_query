# Team Konflux
* **Weekly Overview:** The Konflux team made significant progress on onboarding, resolved a major Prometheus-analyzer bottleneck, and advanced the RPM release measurement integration. Onboarding associates completed key hands-on training and test runs, while critical pipeline auth and PromQL query bugs were successfully resolved to restore continuous validation runs.
* **What was done:**
  * Resolved a long-running resource analyzer bug ([KONFLUX-15159](https://redhat.atlassian.net/browse/KONFLUX-15159)) that caused 12+ hour runs to fail silently due to a PromQL formatting regression, implementing diagnostic counters and list-once optimizations.
  * Resolved Quay.io push authorization errors in production and staging loadtest namespaces ([KONFLUX-14805](https://redhat.atlassian.net/browse/KONFLUX-14805)) by explicitly configuring the OCI storage parameters in cronjobs (PRs #13035 and #13036).
  * Completed architecture planning and environment setup for RPM release measurement on `kflux-rhel-p01` ([KONFLUX-8548](https://redhat.atlassian.net/browse/KONFLUX-8548)), creating a standalone test Jenkins job ([KONFLUX-15163](https://redhat.atlassian.net/browse/KONFLUX-15163)), and analyzing secret prerequisites ([KONFLUX-15161](https://redhat.atlassian.net/browse/KONFLUX-15161)).
* **What is moving:**
  * Enterprise Contract validation and trust violations ([KONFLUX-15147](https://redhat.atlassian.net/browse/KONFLUX-15147)) moved into review after resolving task digest reference failures in probe runs.
  * ServiceAccount security policy migrations ([KONFLUX-14970](https://redhat.atlassian.net/browse/KONFLUX-14970)) moved into review following a cleanup of obsolete ServiceAccounts (MR #20645).
  * Execution of the RPM release pipeline integration ([KONFLUX-15165](https://redhat.atlassian.net/browse/KONFLUX-15165)) is in progress with the creation of keytab secrets ([KONFLUX-15164](https://redhat.atlassian.net/browse/KONFLUX-15164)) and the implementation of a new `--release-plan-admission-data` loadtest CLI flag.

# Team Pipelines
* **Weekly Overview:** The Pipelines team focused on test-suite maintenance and automated release tooling. Key achievements include developing an automated CLI tool to manage CI performance cron jobs across OpenShift Pipelines versions, and refactoring prow artifact processing to integrate Results CI data into Horreum.
* **What was done:**
  * Refactored `prow-to-storage.sh` ([SRVKP-12483](https://redhat.atlassian.net/browse/SRVKP-12483)) to properly process and enrich Tekton Results job artifacts, implement cache-skip logic, and register jobs uniformly (PRs #112 and #109).
  * Drafted a new CLI utility, `manage-perf-crons.py` ([SRVKP-12000](https://redhat.atlassian.net/browse/SRVKP-12000)), to automate the cloning, promotion, and deletion of performance cron job configurations across multiple OpenShift Pipelines versions (PR #82005).
* **What is moving:**
  * Automated job scheduling tooling ([SRVKP-12000](https://redhat.atlassian.net/browse/SRVKP-12000)) has transitioned to review, though final PR merging is currently blocked by branch protection admin permissions on the `openshift-pipelines/performance` repo.

# Team ConsoleDot
* **Weekly Overview:** The ConsoleDot team successfully completed several performance automation and test modernization tasks. Key achievements include the production rollout of the lightweight GitHub PR polling service to completely replace Gosmee, the deployment of a new Jenkins Assistant AI skill, the completion of O_DIRECT disk diagnostics, and the onboarding of the database CPT pipeline.
* **What was done:**
  * Completed the deprecation and teardown of Gosmee webhook-forwarding, fully promoting the `pr-poller` service to production ([HCEPERF-1585](https://redhat.atlassian.net/browse/HCEPERF-1585)) for triggering automated Jenkins PR builds directly (e.g. notifications and inventory APIs).
  * Built and committed a new `jenkins-assistant` AI skill ([HCEPERF-1548](https://redhat.atlassian.net/browse/HCEPERF-1548)) using a Jenkins MCP server to trigger builds, fetch logs, and diagnose test failures.
  * Completed O_DIRECT disk diagnostics ([HCEPERF-1581](https://redhat.atlassian.net/browse/HCEPERF-1581)) to isolate kernel page-cache and reclaim memory contention overhead, confirming the regression is restricted to the buffered path.
  * Onboarded and configured the database CPT (PostgreSQL + HammerDB) pipeline in Jenkins ([HCEPERF-1487](https://redhat.atlassian.net/browse/HCEPERF-1487)) and restructured the repository's documentation ([HCEPERF-1459](https://redhat.atlassian.net/browse/HCEPERF-1459)).
  * Published OpenShift Virt VM creation procedures ([HCEPERF-1583](https://redhat.atlassian.net/browse/HCEPERF-1583), [HCEPERF-1587](https://redhat.atlassian.net/browse/HCEPERF-1587)) and provisioned a custom RHEL 8.6 testing image ([HCEPERF-1584](https://redhat.atlassian.net/browse/HCEPERF-1584)).
  * Delivered the June 2026 Hybrid Cloud Console Red Hat Insights Performance Report ([HCEPERF-1586](https://redhat.atlassian.net/browse/HCEPERF-1586)).
* **What is moving:**
  * Integration of the GitHub PR testing framework ([HCEPERF-877](https://redhat.atlassian.net/browse/HCEPERF-877)) is moving forward with follow-up improvements on poller state persistence and restart capabilities.
  * Deeper kernel analysis of workqueue scaling is in progress through eBPF causal-chain profiling of page reclamation and LRU contention ([HCEPERF-1582](https://redhat.atlassian.net/browse/HCEPERF-1582)).
  * Onboarding of the Chrome service CPT ([HCEPERF-1579](https://redhat.atlassian.net/browse/HCEPERF-1579)) and investigation into Jenkins email automation configurations ([HCEPERF-1489](https://redhat.atlassian.net/browse/HCEPERF-1489)) are actively progressing.

# Team Satellite
* **Weekly Overview:** The Satellite team delivered extensive performance optimization and stability updates this week. Major achievements include scaling improvements to the IPAM inventory generator for large deployments, massive SSH task overhead reductions in `satperf` playbooks, the integration of native Candlepin JVM tuning, and upstream contributions to both persistent smart-proxy connection reuse and Foreman core upgrade paths.
* **What was done:**
  * Optimized the `satperf` inventory generator and provisioning roles ([SAT-48073](https://redhat.atlassian.net/browse/SAT-48073)), adding configurable sizing controls and forwarding them via `doit.sh`.
  * Drastically reduced Ansible SSH overhead ([SAT-48070](https://redhat.atlassian.net/browse/SAT-48070)) by replacing repetitive `lineinfile` hosts tasks with a single Jinja2 template (reducing SSH calls from ~29,000 to 172 at 171-capsule scale) and tuning sshd `MaxStartups`.
  * Streamlined topology definitions ([SAT-48069](https://redhat.atlassian.net/browse/SAT-48069)) by rewriting the Ansible API playbooks to use idempotent FAM modules locally, adding retries to absorb network instability.
  * Successfully templatized and automated Candlepin JVM tuning deployment in `foremanctl` ([SAT-47760](https://redhat.atlassian.net/browse/SAT-47760), [SAT-47759](https://redhat.atlassian.net/browse/SAT-47759)), validating profile tier auto-detection on live systems ([SAT-47763](https://redhat.atlassian.net/browse/SAT-47763)).
  * Upgraded satperf test scripts to track granular per-asset web stats ([SAT-48072](https://redhat.atlassian.net/browse/SAT-48072)) and stabilized BPF stack size allocations ([SAT-48071](https://redhat.atlassian.net/browse/SAT-48071)).
* **What is moving:**
  * Investigation into Capsule 6.18 OOM failures ([SAT-45686](https://redhat.atlassian.net/browse/SAT-45686)) moved into review after scale testing demonstrated that newer pulpcore releases (3.73.30 vs 3.73.26) significantly reduce memory footprint.
  * Capsule smart-proxy HTTP connection reuse investigation ([SAT-45802](https://redhat.atlassian.net/browse/SAT-45802)) is progressing with upstream PR #944 proposed to implement persistent Faraday-based connection pools.
  * Concurrent provisioning database race conditions ([SAT-46037](https://redhat.atlassian.net/browse/SAT-46037)) are under active resolution, tracking upstream Foreman Rails 7.0 upgrade efforts.
