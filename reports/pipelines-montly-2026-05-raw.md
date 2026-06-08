# Pipelines
* Finished issues

### [Closed/Done] [SRVKP-12193](https://redhat.atlassian.net/browse/SRVKP-12193) - Deekshith Kumar Netha Bamandla N - Analyze the potential for implementing scenario-specific alerting rules within Horreum using JavaScript




**Comments (Last 3):**

* **Deekshith Kumar Netha Bamandla N** (2026-05-29): Found a way to implement JS calculation functions for each scenario using a mix of labels.
  
  {noformat}value => {
    const ha = value.__deployment_haConfig_haEnabled;
    const qbt = value.__deployment_qbtConfig_qbtEnabled;
    const ctrl = value.__deployment_haConfig_controllerType;
  
    let tol = 2;
    if (ha && qbt)                         tol = 300;
    else if (ha && ctrl === "statefulSets") tol = 15;
    else if (ha)                           tol = 10;
    else if (qbt)                          tol = 25;
  
    const succeeded = Number(value.__results_PipelineRuns_count_succeeded);
    return Math.max(0, (1000 - tol) - succeeded);
  }{noformat}
  
  Added {{missing_pipeline_successes}} to Pipelines Horreum test with per-scenario tolerance calculation.



---
### [Closed/Done] [SRVKP-12031](https://redhat.atlassian.net/browse/SRVKP-12031) - Deekshith Kumar Netha Bamandla N - [Horreum] Missing change detection values in test OpenShift Pipelines scalingPipelines test, dataset 235789#0


**Description:**
We got this email we need to act on:

{noformat}From: pipelines-perfscale-team+bncbdqllcveuiorbho4tliamgqeaiaykdq@redhat.com  Fri May 15 08:37:05 2026
horreum via pipelines-perfscale-team <pipelines-perfscale-team@redhat.com>
To: pipelines-perfscale-team@redhat.com
Cc: 
Date: Fri, 15 May 2026 05:24:41 +0000 (UTC)
Subject: [Horreum] Missing change detection values in test OpenShift Pipelines scalingPipelines test, dataset 235789#0

   Hello Openshift-pipelines-team,

   the test [1]OpenShift Pipelines scalingPipelines test received a new
   run with fingerprint
   {"__deployment_version":"1.12","__parameters_test_total":"200","__param
   eters_test_concurrent":"12","__deployment_haConfig_haEnabled":"true","_
   _deployment_qbtConfig_qbtEnabled":"false","__deployment_haConfig_contro
   llerType":"deployments"} but it could not calculate values for these
   change detection variables:
     * restarts/__measurements_pipelinesAsCodeController_restarts_range
     * restarts/__measurements_pipelinesAsCodeWatcher_restarts_range

   Please [2]check it out and correct change detection variables in
   [3]OpenShift Pipelines scalingPipelines test.
   Horreum Alerting

References

   1. https://horreum.corp.redhat.com:8443/test/391
   2. https://horreum.corp.redhat.com:8443/run/235789#dataset1
   3. https://horreum.corp.redhat.com:8443/test/391#vars{noformat}

h3. Acceptance criteria

* Matter from the email is resolved



**Comments (Last 3):**

* **Deekshith Kumar Netha Bamandla N** (2026-05-19): The PAC pods ({{pipelines-as-code-controller}}, {{pipelines-as-code-watcher}}, {{pipelines-as-code-webhook}}) were removed from the {{openshift-pipelines}} namespace in the latest nightly build (rolled between May 12–19). Along with PAC, Triggers are also gone.
  
  This is an upstream nightly change not a test infra issue, our setup scripts have not changed since April 30.
  
  Since those pods no longer exist, Prometheus returns no data for their restart metrics, causing Horreum to fail the change detection calculation.

* **Deekshith Kumar Netha Bamandla N** (2026-05-19): Update: PAC wasn't removed from the build the images are still in the operator bundle. The actual blocker is the {{tkn-cli-serve}} pod crashing ({{sed: can't read /etc/httpd/conf.d/ssl.conf}}), which stalls {{TektonAddon}} and blocks the entire {{TektonConfig}} reconciliation from deploying PAC. Traces to [this commit|https://github.com/openshift-pipelines/serve-tkn-cli/commit/3e38fbfd7b88724b5e5e7d48d91fee2a64a50543].

* **Deekshith Kumar Netha Bamandla N** (2026-05-26): Bug created [https://redhat.atlassian.net/browse/SRVKP-12102|https://redhat.atlassian.net/browse/SRVKP-12102|smart-link]  and the issue is fixed



---
### [Closed/Done] [SRVKP-11922](https://redhat.atlassian.net/browse/SRVKP-11922) - Aman Vishwakarma - Ensure CI automation for Chains controller CPT scenarios


**Description:**
Integrate all new Chains controller CPT scenarios into the CI pipeline. Validate that CI runs successfully and failures are reported appropriately.



**Comments (Last 3):**

* **Automation for Jira** (2026-05-26): removed label *groomable* from the issue as Aman Vishwakarma transitioned it to In Progress

* **Aman Vishwakarma** (2026-05-26): Chains signing Prow jobs integrated as periodic jobs (versions 1.20–1.22, variants: default, HA-10, QBT, HA-10-QBT)
  
  {{prow-to-storage.sh}} updated to pull signing job results and upload to Horreum [(PR merged)|https://github.com/openshift-pipelines/performance/pull/102]
  
  End-to-end flow validated: periodic jobs → GCS → {{prow-to-storage.sh}} → Horreum Chains test (196 datasets confirmed)



---
### [Closed/Done] [SRVKP-11921](https://redhat.atlassian.net/browse/SRVKP-11921) - Deekshith Kumar Netha Bamandla N - Update Grafana dashboard for Chains controller CPT scenarios


**Description:**
Modify and enhance the Grafana dashboard to visualize metrics and results from the new Chains controller CPT scenarios. Ensure new scenarios are filterable and data is displayed correctly.



**Comments (Last 3):**

* **Automation for Jira** (2026-05-26): removed label *groomable* from the issue as Deekshith Kumar Netha Bamandla N transitioned it to In Progress

* **Jan Hutar** (2026-05-26): Status update: Deekshith working on this, facing issues to get data from PostgreSQL.

* **Deekshith Kumar Netha Bamandla N** (2026-05-29): [+Chains Signing Performance Dashboard+|http://10.0.109.83:3000/d/Chains_Signing_Performance/chains-signing-performance-dashboard]
  
  [+Chains Signing Performance Comparison Dashboard+|http://10.0.109.83:3000/d/Chains_Signing_Performance_Comparison/chains-signing-performance-comparison-dashboard]
  
  Created Chains Signing Performance and comparison dashboard. 
  
  PR: [https://github.com/openshift-pipelines/performance/pull/103|https://github.com/openshift-pipelines/performance/pull/103]



---
### [Closed/Done] [SRVKP-11920](https://redhat.atlassian.net/browse/SRVKP-11920) - Aman Vishwakarma - Configure Horreum and alerts for Chains controller CPT scenarios


**Description:**
Set up Horreum for result storage and configure alerts for the new Chains controller CPT scenarios. Ensure alerting is functional and results are accessible.



**Comments (Last 3):**

* **Automation for Jira** (2026-05-25): removed label *groomable* from the issue as Aman Vishwakarma transitioned it to In Progress

* **Aman Vishwakarma** (2026-05-26): *Verified Chains Test (ID 418) — Setup on Shared Schema (ID 274)*
  
  Setup is complete and data is flowing. Summary below:
  
  * *Schema labels:* All 65 labels present — covers Chains controller CPU/memory/workqueue, signing metrics, and shared infrastructure.
  [https://horreum.corp.redhat.com/schema/274|https://horreum.corp.redhat.com/schema/274]
  * *Change detection:* 10 groups configured:
  ** {{chains_cpu}}, {{chains_memory}} — 10% relative difference
  ** {{chains_workqueue}}, {{signing_throughput}} — 20% relative difference
  ** {{signing_count}}, {{PipelineRuns_Succeeded_count}}, {{TaskRuns_Succeeded_count}} — 1% relative difference
  ** {{PipelineRuns_TaskRuns_Failed_count}}, {{signing_unsigned_count}}, {{restarts}} — fixed threshold (max = 0)
  [https://horreum.corp.redhat.com/test/418|https://horreum.corp.redhat.com/test/418]
  * *Notifications:* Subscriptions added for the Openshift-pipelines team.



---
### [Closed/Done] [SRVKP-11919](https://redhat.atlassian.net/browse/SRVKP-11919) - Aman Vishwakarma - Implement CPT scenario: Chains controller with HA=10 and QBT Profile (50/50/32)


**Description:**
Develop and automate the CPT scenario for Chains controller with both HA=10 and QBT Profile (50/50/32) configurations. Integrate the test into CI and ensure results are collected.



**Comments (Last 3):**

* **Automation for Jira** (2026-05-10): removed label *groomable* from the issue as Aman Vishwakarma transitioned it to In Progress

* **Aman Vishwakarma** (2026-05-14): The HA=10 + QBT combined variants were evaluated and determined to *not require splitting* — these jobs are completing within the 8-hour Prow timeout (6–6.5 hours). No changes needed for this scenario at this time. Will continue monitoring execution times as test workloads evolve.

* **Jan Hutar** (2026-05-19): Aman’s results: [https://docs.google.com/document/d/1SwgUraasyxXgHtqOVQF4J7dB0CJawm-oIHRDRvjAYVs/edit?tab=t.0|https://docs.google.com/document/d/1SwgUraasyxXgHtqOVQF4J7dB0CJawm-oIHRDRvjAYVs/edit?tab=t.0]



---
### [Closed/Done] [SRVKP-11918](https://redhat.atlassian.net/browse/SRVKP-11918) - Aman Vishwakarma - Implement CPT scenario: Chains controller with HA=10 setup


**Description:**
Develop and automate the CPT scenario for Chains controller configured with High Availability (HA) set to 10. Integrate the test into CI and ensure results are captured.



**Comments (Last 3):**

* **Automation for Jira** (2026-05-10): removed label *groomable* from the issue as Aman Vishwakarma transitioned it to In Progress

* **Aman Vishwakarma** (2026-05-14): The HA=10 variants were also split to resolve the Prow 8-hour timeout:
  
  * {{ni-sign-tkn-bb-ha10}} → {{ni-sign-tkn-bb-ha10}} + {{ni-sign-tkn-bb-ha10-1500}}
  * {{1-20-sign-tkn-bb-ha10}} → {{1-20-sign-tkn-bb-ha10}} + {{1-20-sign-tkn-bb-ha10-1500}}

* **Jan Hutar** (2026-05-19): Aman’s results: [https://docs.google.com/document/d/1SwgUraasyxXgHtqOVQF4J7dB0CJawm-oIHRDRvjAYVs/edit?tab=t.0|https://docs.google.com/document/d/1SwgUraasyxXgHtqOVQF4J7dB0CJawm-oIHRDRvjAYVs/edit?tab=t.0]



---
### [Closed/Done] [SRVKP-11917](https://redhat.atlassian.net/browse/SRVKP-11917) - Aman Vishwakarma - Implement CPT scenario: Chains controller with QBT Profile (50/50/32)


**Description:**
Develop and automate the CPT scenario for Chains controller using the QBT Profile (50/50/32). Integrate the test into CI and ensure results are collected.



**Comments (Last 3):**

* **Automation for Jira** (2026-05-10): removed label *groomable* from the issue as Aman Vishwakarma transitioned it to In Progress

* **Aman Vishwakarma** (2026-05-14): As part of resolving the 8-hour Prow timeout issue affecting {{sign-tkn-bb}} periodic jobs, the QBT tuned variants were also split using the same 2-way approach:
  
  * {{1-20-sign-tkn-bb-qbt}} → {{1-20-sign-tkn-bb-qbt}} + {{1-20-sign-tkn-bb-qbt-1500}}
  * {{1-21-sign-tkn-bb-qbt}} → {{1-21-sign-tkn-bb-qbt}} + {{1-21-sign-tkn-bb-qbt-1500}}
  
  Job 1 runs 500/20 + 1000/20 scenarios, and Job 2 ({{-1500}} suffix) runs 1500/20 independently. Rehearsal runs were validated via {{/pj-rehearse}} on the PR.

* **Jan Hutar** (2026-05-19): Aman’s results: [https://docs.google.com/document/d/1SwgUraasyxXgHtqOVQF4J7dB0CJawm-oIHRDRvjAYVs/edit?tab=t.0|https://docs.google.com/document/d/1SwgUraasyxXgHtqOVQF4J7dB0CJawm-oIHRDRvjAYVs/edit?tab=t.0]



---
### [Closed/Done] [SRVKP-11916](https://redhat.atlassian.net/browse/SRVKP-11916) - Aman Vishwakarma - Implement CPT scenario: Chains controller with basic signing


**Description:**
Develop and automate the Continuous Performance Testing (CPT) scenario for Chains controller with basic signing. Ensure the test is integrated into CI and results are collected.



**Comments (Last 3):**

* **Jan Hutar** (2026-05-18): Lets only run scale we can handle in one run.

* **Aman Vishwakarma** (2026-05-18): Dropped the 1500/20 PLR scenario from all sign-tkn-bb CI jobs across all variants (base signing, QBT, HA-10, HA-10+QBT) and all versions (nightly, 1.20, 1.21, 1.22).All jobs now run TEST_SCENARIOS: 500/20 1000/20 only.
  
  Additionally, renamed the HA variant job suffixes from -ha10 to -ha-10 to align with the _PROW_VARIANT_SUFFIXES convention used by prow-to-storage.sh for GCS result collection suggested by [~accountid:712020:11aa6ff6-f1d3-4f94-9880-d5a1a144ec5a] 

* **Jan Hutar** (2026-05-19): Aman’s results: [https://docs.google.com/document/d/1SwgUraasyxXgHtqOVQF4J7dB0CJawm-oIHRDRvjAYVs/edit?tab=t.0|https://docs.google.com/document/d/1SwgUraasyxXgHtqOVQF4J7dB0CJawm-oIHRDRvjAYVs/edit?tab=t.0]



---
### [Closed/Done] [SRVKP-11915](https://redhat.atlassian.net/browse/SRVKP-11915) - Deekshith Kumar Netha Bamandla N - Add necessary labels to the Horreum schema for the Chains controller




**Comments (Last 3):**

* **Automation for Jira** (2026-05-12): removed label *groomable* from the issue as Jan Hutar transitioned it to In Progress

* **Jan Hutar** (2026-05-12): +Status report:+ Deekshith added new metrics already and now need to create new Horreum test for Chains. Once the test is created, we can merge Aman’s PR.

* **Deekshith Kumar Netha Bamandla N** (2026-05-18): Completed Chains signing test Horreum integration:
  
  * Added signing metrics computation in {{stats.sh}}
  * Created {{horreum_chains_fields.yaml}} with 65 fields covering Chains controller CPU/memory/workqueue, shared infrastructure metrics and signing-specific metrics for both PipelineRuns and TaskRuns.
  * Successfully pushed labels and change detection variables to Horreum (test ID 418, schema ID 274).
  * Reorganized horreum tooling into {{tools/horreum/}} with README documentation.
  * Updated {{ci-scripts/lib.sh}} to support Chains env vars for HA/QBT config capture and generate signing-aware scenario names.
  
  PR raised: [https://github.com/openshift-pipelines/performance/pull/101|https://github.com/openshift-pipelines/performance/pull/101|smart-link] 



---
### [Closed/Done] [SRVKP-11892](https://redhat.atlassian.net/browse/SRVKP-11892) - Deekshith Kumar Netha Bamandla N - Create Epics for Chains and Results CPT




**Comments (Last 3):**

* **Automation for Jira** (2026-05-05): removed label *groomable* from the issue as Deekshith Kumar Netha Bamandla N transitioned it to In Progress

* **Jan Hutar** (2026-05-12): +Status report:+ Epic for Chains created, Deekshith will create another one for Results. We will start with just one basic scenario for Results.

* **Deekshith Kumar Netha Bamandla N** (2026-05-18): Created Epics for Chains and Result CPT
  
  [https://redhat.atlassian.net/browse/SRVKP-11914|https://redhat.atlassian.net/browse/SRVKP-11914|smart-link] 
  
  [https://redhat.atlassian.net/browse/SRVKP-12048|https://redhat.atlassian.net/browse/SRVKP-12048|smart-link] 



---
### [Closed/Done] [SRVKP-11293](https://redhat.atlassian.net/browse/SRVKP-11293) - Aman Vishwakarma - Rerun the test with other version and generate simple report and do a comparison study


**Description:**
h3. Acceptance criteria

* Run the same test as before on a cluster with the same specs but with different input parameters to see a performance difference
* Collect results and create a simple report comparing the run from 2 different runs and do a comparison study.



**Comments (Last 3):**

* **Aman Vishwakarma** (2026-04-28): I reran the test suite on *OpenShift Pipelines v1.21* and compared the results against *v1.20*.
  Here is Comparison report I have attached
  
  [https://docs.google.com/document/d/1yU-w0qwPmR8LFKos4-jh3ds1G3rWoxqblm_T5KEdqzE/edit?usp=sharing|https://docs.google.com/document/d/1yU-w0qwPmR8LFKos4-jh3ds1G3rWoxqblm_T5KEdqzE/edit?usp=sharing|smart-card]

* **Automation for Jira** (2026-05-05): removed label *groomable* from the issue as Aman Vishwakarma transitioned it to In Progress

* **Aman Vishwakarma** (2026-05-05): Completed the version reruns, generated the summary report, and documented the comparative study. Closing this task



---
### [Closed/Done] [SRVKP-11292](https://redhat.atlassian.net/browse/SRVKP-11292) - Aman Vishwakarma - Run a test using our framework


**Description:**
h3. Acceptance criteria

* Follow README and install OpenShift Pipelines to the cluster
** If something substantial is missing open a PR to add it after discussing it with Siddardh
* Use our code to run actual test, maybe different one than one with Siddardh
** Understand logs, understand test flow
* Collect test results



**Comments (Last 3):**

* **Automation for Jira** (2026-05-05): removed label *groomable* from the issue as Aman Vishwakarma transitioned it to In Progress

* **Aman Vishwakarma** (2026-05-05): Ran build scenario on OpenShift Pipelines v1.21. with config: TEST_TOTAL=50, TEST_CONCURRENT=5. All 50 PipelineRuns succeeded — 150 TaskRuns (git-clone → go-test → buildah).



---
### [Closed/Done] [SRVKP-11291](https://redhat.atlassian.net/browse/SRVKP-11291) - Aman Vishwakarma - Have a session with Deekshith/Siddardh showing you how to install pipelines and run a test and get results


**Description:**
h3. Acceptance criteria

* Have a shadowing session with Siddardh that will cover:
** Install OpenShift Pipelines (or upstream) to fresh OpenShift cluster
** Run a test
** Explore all results generated by the test, generate and explain graphs



**Comments (Last 3):**

* **Automation for Jira** (2026-04-24): removed label *groomable* from the issue as Aman Vishwakarma transitioned it to In Progress

* **Aman Vishwakarma** (2026-04-28): Had a session with Deekshith who helped to guide  and fixing the Git-clone Pipeline
  I now have the necessary access and environmental setup to execute tests independently.
  Thanks [~accountid:712020:11aa6ff6-f1d3-4f94-9880-d5a1a144ec5a] !

* **Aman Vishwakarma** (2026-05-05): Conducted the knowledge transfer and review session with Deekshith



---
### [Closed/Done] [SRVKP-11290](https://redhat.atlassian.net/browse/SRVKP-11290) - Aman Vishwakarma - Get access to cluster from Cluster Bot and Install a Openshift Pipelines on a cluster and run a pipeline


**Description:**
h3. Acceptance criteria

* Get access to the cluster from the Cluster Bot
* Ensure you can log in to Console UI and use it to check what all namespaces are there and which one is most resource-intensive
* Ensure you can log in on CLI with oc and list all pods in the {{openshift-monitoring}} namespace
* Following the official OpenShift Pipelines, install it in the cluster
* Following some docs, run your first PipelineRun
* Install Openshift Pipelines using the web console and run a pipeline for a git repo.



**Comments (Last 3):**

* **Automation for Jira** (2026-04-23): removed label *groomable* from the issue as Aman Vishwakarma transitioned it to In Progress

* **Aman Vishwakarma** (2026-04-24): Logged into Console and CLI. Identified {{openshift-monitoring}} & {{openshift-etcd}} as a high-resource namespace and verified pod health.
  
  Installed OpenShift Pipelines Operator.
  Developed and ran a Pipeline that clones the *LogAn* GitHub repository into a shared workspace.

* **Aman Vishwakarma** (2026-05-05): Successfully obtained cluster access via the Cluster Bot, completed the installation of OpenShift Pipelines on the cluster, and verified it by running a test pipeline Closing this now..



---
### [Closed/Done] [SRVKP-11289](https://redhat.atlassian.net/browse/SRVKP-11289) - Aman Vishwakarma - Explore Openshift Pipelines (Tekton)




**Comments (Last 3):**

* **Automation for Jira** (2026-04-20): removed label *groomable* from the issue as Aman Vishwakarma transitioned it to In Progress

* **Aman Vishwakarma** (2026-04-23): [https://redhat.udemy.com/course/tekton-the-quick-start|https://redhat.udemy.com/course/tekton-the-quick-start|smart-link] 
  Referring this course for Exploration of Tekton concepts

* **Aman Vishwakarma** (2026-05-05): Explored Tekton..All relevant documentation has been reviewed and analyzed.



---
### [Closed/Done] [SRVKP-11287](https://redhat.atlassian.net/browse/SRVKP-11287) - Aman Vishwakarma - Openshift Pipelines Onboarding -  Aman


**Description:**
h1. Story (Required)

Onboarding activities for Aman for Openshift Pipelines 

h2. *Acceptance Criteria (Mandatory)*

_Understand the product and complete all the tasks under it_

h1. 



**Comments (Last 3):**

* **Aman Vishwakarma** (2026-05-05): [~accountid:712020:347f3aac-04ed-4a21-ad91-fcd7b5f35e85] I think we can close this Epic.. Thanks for Onboarding!

* **Jan Hutar** (2026-05-05): All child tacks closed. Thank you Aman!

* **Automation for Jira** (2026-05-05): Please add '*Release Note Text*', '*Release Note Status*' and '*Release Notes Type*'. Transitioning the issue back to 'In progress'. 
  
  If Release Note is not required, set *Release Note Type* to '*Release Note Not Required*' 



---
### [Closed/Done] [SRVKP-11116](https://redhat.atlassian.net/browse/SRVKP-11116) - Siddardh R A - Investigate Chains regression


**Description:**
We have a regression [https://redhat.atlassian.net/browse/SRVKP-11016|https://redhat.atlassian.net/browse/SRVKP-11016] and Siddardh spent some time investigating it.



**Comments (Last 3):**

* **Jan Hutar** (2026-03-18): Siddardh’s notes: [https://docs.google.com/spreadsheets/d/1Yg6eAe-kX6oXTmMzxxj9qFCBMXGJ-TD-EygxdLjUsu8/edit?gid=970228389#gid=970228389|https://docs.google.com/spreadsheets/d/1Yg6eAe-kX6oXTmMzxxj9qFCBMXGJ-TD-EygxdLjUsu8/edit?gid=970228389#gid=970228389]

* **Jan Hutar** (2026-03-24): +Status update:+ Tried to run the scenario with cluster bot and gather more metrics. Was not able to connect with eng. rep., so need to do so this week.

* **Siddardh R A** (2026-05-12): My work on gathering more metrics to aid Anitha in narrowing down the possibilities of the root cause. And all the work has been documented in this ticket : [https://redhat.atlassian.net/browse/SRVKP-11016|https://redhat.atlassian.net/browse/SRVKP-11016|smart-link] 
  Here is the comment :
  [https://redhat.atlassian.net/browse/SRVKP-11016?focusedCommentId=16654561|https://redhat.atlassian.net/browse/SRVKP-11016?focusedCommentId=16654561|smart-link] 



---
### [Closed/Done] [SRVKP-10973](https://redhat.atlassian.net/browse/SRVKP-10973) - Deekshith Kumar Netha Bamandla N - Pipelines Controller CPT Scenarios


**Description:**
h2. *Epic Goal*
 * Complete the test scenario coverage in CPT for pipeline controllers

h2. *Scenarios*
 # Pipelines controller with rising concurrency with HA=10 setup
 # Pipelines controller with rising concurrency with QBT Profile (50/50/32)
 # Pipelines controller with rising concurrency with HA=10 setup and QBT Profile (50/50/32)

h2. *Acceptance Criteria (Mandatory)*
 * CI - MUST be running successfully with tests automated
 * Horreum and alerts are configured correctly
 * Grafana dashboard is updated with the new scenarios

 



**Comments (Last 3):**

* **Jan Hutar** (2026-04-30): [~accountid:712020:11aa6ff6-f1d3-4f94-9880-d5a1a144ec5a] I see. So in the mean time, could you please add a task to start running it on 1.22 (probably daily so we accumulate some test runs before some dashboard is ready)? To me, Comparison Dashboard looks pretty ready, just data missing 🙂 But at this point I’m outsider, so I’m pretty sure lots is missing. Do we have a Jira to track that?

* **Automation for Jira** (2026-05-04): Please add '*Release Note Text*', '*Release Note Status*' and '*Release Notes Type*'. Transitioning the issue back to 'In progress'. 
  
  If Release Note is not required, set *Release Note Type* to '*Release Note Not Required*' 

* **Deekshith Kumar Netha Bamandla N** (2026-05-04): Added all the scenarios related to pipelines controller to CI. Updated Horreum labels related to HA, QBT and nightly. Updated the grafana dashboards.
  
  [Comparison Dashboard|http://10.0.109.83:3000/d/Pipelines_Performance_Comparison/pipelines-performance-comparison-dashboard]
  
  [Pipelines Performance Dashboard|http://10.0.109.83:3000/d/Pipelines_Performance/pipelines-performance-dashboard]
  
  



---
### [Closed/Done] [SRVKP-10658](https://redhat.atlassian.net/browse/SRVKP-10658) - Siddardh R A - Prepare a Report on the Release Testing of 1.21


**Description:**
Acceptance criteria:
 * Different Test scenarios - default, HA, QBT, HA + QBT
 * Findings for each test scenario
 * Created table with graphs comparing 1.21 vs 1.20 "math" scenario
 * Created table with graphs comparing 1.21 vs 1.20 "math" scenario with pipelines HA=10
 * Created table with graphs comparing 1.21 vs 1.20 "math" scenario with pipelines QBT=50/50/32
 * Created table with graphs comparing 1.21 vs 1.20 "math" scenario with pipelines HA=10 and QBT=50/50/32
 * Created a table with graphs comparing 1.21 vs 1.20 bigbang scenario
 * Created table with graphs comparing 1.21 vs 1.20 bigbang scenario with Chains HA=10
 * Created table with graphs comparing 1.21 vs 1.20 bigbang scenario with Chains HA=10 and QBT=50/50/32
 * Created table with graphs comparing 1.21 vs 1.20 bigbang scenario with Chains HA=10 and QBT=50/50/32
 * Presented the results to engineering
 * Write a KB article for the same



**Comments (Last 3):**

* **Siddardh R A** (2026-05-12): Since we provided an internal report to the engineering team. We didn't proceed to publish the article because we had multiple regressions in the chain controller, and no of failures increased in the Stateful set. The engineering team is working on identifying and addressing the root cause of this regression. And eventually, the 1.22 version got released, so we provided only the internal report 



---
### [Closed/Done] [SRVKP-9035](https://redhat.atlassian.net/browse/SRVKP-9035) - Siddardh R A - Investigate the failure to install via Custom Build in CI


**Description:**
PR : https://github.com/openshift/release/pull/69438

Error in CI : https://prow.ci.openshift.org/view/gs/test-platform-results/pr-logs/pull/openshift_release/69438/rehearse-69438-pull-ci-openshift-pipelines-performance-main-max-concurrency-downstream-1-20-1000-x-math-ha-10-cb/1969102024159006720



**Comments (Last 3):**

* **OpenShift Jira Bot** (2025-12-12): Hi Siddardh R A,
  
  This is an automated reminder that issue is currently in progress but does not have an estimate.
  
  Please add an estimate as soon as possible.
  

* **Jan Hutar** (2026-04-21): Hello [~accountid:712020:347f3aac-04ed-4a21-ad91-fcd7b5f35e85] . Is this [https://github.com/openshift-pipelines/performance/pull/85|https://github.com/openshift-pipelines/performance/pull/85] PR is related?

* **Siddardh R A** (2026-05-12): After multiple attempts , this issue has been fixed by this PR : [https://github.com/openshift-pipelines/performance/pull/95|https://github.com/openshift-pipelines/performance/pull/95|smart-link]  



---
### [Closed/Done] [SRVKP-7562](https://redhat.atlassian.net/browse/SRVKP-7562) - Deekshith Kumar Netha Bamandla N - Dashboard to compare different product versions results


**Description:**
* Build a dashboard to give us comparison like here: https://docs.google.com/document/d/1LMzU8vyaSipNsgMKUEz-SEygh9eiStnkKAO4QfadDr4/edit?tab=t.w8jk5w8z8qgt#heading=h.tbtfn7knxwhn
* Use Horreum data and https://github.com/Appservices-perfscale/horreum-data-mirror
* Use Jsonnet and Grafonnet



**Comments (Last 3):**

* **OpenShift Jira Bot** (2025-12-01): Hi Siddardh R A,
  
  This Issue is in progress but lacks a sprint assignment.
  Please take a moment to:
  1 - Add it to an open sprint after coordinating with your team.
  2 - Or, if it's not being worked on right now, change its status to 'To Do'.

* **Jan Hutar** (2026-03-10): Hello [~accountid:712020:347f3aac-04ed-4a21-ad91-fcd7b5f35e85]. This is in progress for almost 9 months now. How can we move it forward?

* **Deekshith Kumar Netha Bamandla N** (2026-05-04): Adds a new Grafana comparison dashboard ({{pipelines-comparison-dashboard.jsonnet}}) for side-by-side version comparison of pipelines performance metrics (e.g., 1.19 vs 1.20). Version dropdowns are dynamic query variables.
  
  Grafana Dashboard: [+Pipelines Comparison Dashboard+|http://10.0.109.83:3000/d/Pipelines_Performance_Comparison/pipelines-performance-comparison-dashboard]



---
### [Closed/Done] [SRVKP-4369](https://redhat.atlassian.net/browse/SRVKP-4369) - Siddardh R A - Create a blog comparing classic, HA and StatefulSet


**Description:**
Content:

* How it is configured, what each option does
* Perf comparison of non-HA and HA setup
* Resources usage comparison of non-HA and HA setup

*Acceptance criteria:*
* Create a blog, and discuss with engineering, publish it



**Comments (Last 3):**

* **Jan Hutar** (2026-03-17): Status update: Siddardh created core of it, looking into suggestions from jhutar and refining the blog. Jeff Burke asked for this blog and that it would be cool to publish it.

* **Jan Hutar** (2026-03-24): +Status update:+ Siddardh worked on the blog, almost done. Checking with current versions if numbers are +-OK. Will check with engineering.

* **Jan Hutar** (2026-05-05): Status update: Blog is live at [https://developers.redhat.com/articles/2026/04/30/how-statefulset-deployments-tripled-openshift-pipelines-throughput#|https://developers.redhat.com/articles/2026/04/30/how-statefulset-deployments-tripled-openshift-pipelines-throughput#]



---
* In review issues

* In progress issues

### [In Progress] [SRVKP-11997](https://redhat.atlassian.net/browse/SRVKP-11997) - Siddardh R A - Create a template for generating Report from CPT data


**Description:**
Scope here is a small script that will create a KB article summarizing resource ussage changes and so on, not the full report with all the graphs (we have a Grafana dashboard for that). We will probably use our PostgreSQL mirror of Horreum data.

h2. Acceptance criteria

* Create a mock KB article (with fake data) and got ack from the team and Khurram
* Explore data is PostgreSQL
* (Vibe?) code some report generation tool




---
### [In Progress] [SRVKP-11992](https://redhat.atlassian.net/browse/SRVKP-11992) - Siddardh R A - 1.22 Perf&Scale Regression Testing


**Description:**
h2. *Epic Goal*

* Run the perf&scale tests for 1.22, similar to how we ran tests for previous releases, and compare with the previous version
* Ensure tests do not show any 1.22 -> 1.21 regressions.
* Document a process in Jira so it can be used later to automate the pipeline.
* Validate whether the bugs raised in the previous releases have been addressed 

h2. *Acceptance Criteria (Mandatory)*

* All tasks finished
* Present the observations to the Engineering Team
* Publish the findings as a article to the general public

h2. *Done Checklist*

* Acceptance criteria are met



**Comments (Last 3):**

* **Siddardh R A** (2026-06-01): Here is the Data Point Sheet : [https://docs.google.com/spreadsheets/d/1-GWL8vjhcvcWfaKjjw52CD_qLb-AjzuILtpqselXYCY/edit?usp=sharing|https://docs.google.com/spreadsheets/d/1-GWL8vjhcvcWfaKjjw52CD_qLb-AjzuILtpqselXYCY/edit?usp=sharing|smart-link] 
  Here is the Internal Report : [https://docs.google.com/document/d/1YRmoituOKBrEWE3jSO2dtc9u-QJzZVn-45oByHG9bjs/edit?usp=sharing|https://docs.google.com/document/d/1YRmoituOKBrEWE3jSO2dtc9u-QJzZVn-45oByHG9bjs/edit?usp=sharing|smart-link] 
  KB Article Draft : [https://access.redhat.com/articles/7143289|https://access.redhat.com/articles/7143289]

* **Automation for Jira** (2026-06-01): Please add '*Release Note Text*', '*Release Note Status*' and '*Release Notes Type*'. Transitioning the issue back to 'In progress'. 
  
  If Release Note is not required, set *Release Note Type* to '*Release Note Not Required*' 



---
### [In Progress] [SRVKP-10874](https://redhat.atlassian.net/browse/SRVKP-10874) - Siddardh R A - OpenShift Pipelines CPT phase 2


**Description:**
Create OpenShift Pipelines CPT and integrate with Engineering's team workflow. This will group generic tasks not related to implementing particular controller or controller's scenario. For that we should have standalone epics all grouped under parent feature SRVKP-10876.



**Comments (Last 3):**

* **Automation for Jira** (2026-05-28): removed label *groomable* from the issue as Deekshith Kumar Netha Bamandla N transitioned it to In Progress



---
### [In Progress] [SRVKP-8004](https://redhat.atlassian.net/browse/SRVKP-8004) - Deekshith Kumar Netha Bamandla N - Have an agreement with engineering on a notification strategy


**Description:**
h3. Acceptance criteria
* Explained (and recorded it) how change detection in Horreum works to Engineering.
* We have an initial agreement with engineering on a notification strategy in case of change is detected.



**Comments (Last 3):**

* **Jan Hutar** (2026-03-10): I do not think this needs to be on Siddardh. Also moving to phase 2 as we first need to have some actual data before we start thinking about how to process issues detected.

* **Automation for Jira** (2026-05-26): removed label *groomable* from the issue as Deekshith Kumar Netha Bamandla N transitioned it to In Progress

* **Deekshith Kumar Netha Bamandla N** (2026-05-29): Automation strategies for pipeline monitoring and alerting were reviewed and standardized via hard-coded threshold implementations.
  
  The team decided to implement hard-coded upper and lower bounds for metrics, replacing complex percentage-based alerts. Specific operational labels were retained while irrelevant components were removed. Engineering will define specific upper bounds for acceptable pipeline failures per scenario. This prevents excessive notifications and streamlines responses for testing environments.



---
* New issues

### [Tasking and Estimation] [SRVKP-12192](https://redhat.atlassian.net/browse/SRVKP-12192) - Aman Vishwakarma - Configure alert thresholds and establish hard-coded upper and lower bounds for metric alerts


**Description:**
We will be fixing this to fixed threshold.



**Comments (Last 3):**

* **Jan Hutar** (2026-06-02): Status report: Aman will connect with Deekshith on a plan here. 



---
### [In Progress] [SRVKP-12152](https://redhat.atlassian.net/browse/SRVKP-12152) - Aman Vishwakarma - Familiarize yourself with Results test we have so far





---
### [Dev Complete] [SRVKP-12102](https://redhat.atlassian.net/browse/SRVKP-12102) - Jawed Khelil - tkn-cli-serve pod in CrashLoopBackOff


**Description:**
*Background:*

We noticed the {{OpenShift Pipelines scalingPipelines}} performance test is failing because it can not collect number of PAC pod restarts. During investigation we realized PAC pods are not running at all. Probably because {{tkn-cli-serve}} pod is stuck in {{CrashLoopBackOff}}.

*Issue:*

PAC pods (controller, watcher, webhook) are not being deployed. The operator's {{TektonConfig}} reconciliation is blocked because {{TektonAddon}} cannot reach ready state.

The blocker is the {{tkn-cli-serve}} pod in {{CrashLoopBackOff}}:

{noformat}sed: can't read /etc/httpd/conf.d/ssl.conf: No such file or directory{noformat}

The {{TektonConfig}} CR shows {{profile: all}} and {{pipelinesAsCode.enable: true}}. PAC is intended to be deployed but the stalled reconciliation prevents it.




---
### [Tasking and Estimation] [SRVKP-12049](https://redhat.atlassian.net/browse/SRVKP-12049) - Deekshith Kumar Netha Bamandla N - Identify the test scenarios for Results Controllers





---
### [Backlog] [SRVKP-12048](https://redhat.atlassian.net/browse/SRVKP-12048) - Deekshith Kumar Netha Bamandla N - Results Controller CPT Scenarios


**Description:**
h2. *Epic Goal*

* Complete the test scenario coverage in CPT for Results controllers

h2. *Scenarios*

# Add scenarios for Results Controllers

h2. *Acceptance Criteria (Mandatory)*

* CI - MUST be running successfully with tests automated
* Horreum and alerts are configured correctly
* Grafana dashboard is updated with the new scenarios

 




---
### [Tasking and Estimation] [SRVKP-12000](https://redhat.atlassian.net/browse/SRVKP-12000) - Deekshith Kumar Netha Bamandla N - Create tooling to manage jobs in openshift/release repo





---
### [In Progress] [SRVKP-11997](https://redhat.atlassian.net/browse/SRVKP-11997) - Siddardh R A - Create a template for generating Report from CPT data


**Description:**
Scope here is a small script that will create a KB article summarizing resource ussage changes and so on, not the full report with all the graphs (we have a Grafana dashboard for that). We will probably use our PostgreSQL mirror of Horreum data.

h2. Acceptance criteria

* Create a mock KB article (with fake data) and got ack from the team and Khurram
* Explore data is PostgreSQL
* (Vibe?) code some report generation tool




---
### [Code Review] [SRVKP-11996](https://redhat.atlassian.net/browse/SRVKP-11996) - Siddardh R A - Generate a KB article




**Comments (Last 3):**

* **Siddardh R A** (2026-06-01): Based on my findings I’ve updated summarized all those metrics and analysis into a KB article for further reference : [https://access.redhat.com/articles/7143289|https://access.redhat.com/articles/7143289] . Waiting to get an ack from [~accountid:712020:30341d31-781d-48c0-844c-6b37985cc033]  to get publsihed



---
### [In Progress] [SRVKP-11992](https://redhat.atlassian.net/browse/SRVKP-11992) - Siddardh R A - 1.22 Perf&Scale Regression Testing


**Description:**
h2. *Epic Goal*

* Run the perf&scale tests for 1.22, similar to how we ran tests for previous releases, and compare with the previous version
* Ensure tests do not show any 1.22 -> 1.21 regressions.
* Document a process in Jira so it can be used later to automate the pipeline.
* Validate whether the bugs raised in the previous releases have been addressed 

h2. *Acceptance Criteria (Mandatory)*

* All tasks finished
* Present the observations to the Engineering Team
* Publish the findings as a article to the general public

h2. *Done Checklist*

* Acceptance criteria are met



**Comments (Last 3):**

* **Siddardh R A** (2026-06-01): Here is the Data Point Sheet : [https://docs.google.com/spreadsheets/d/1-GWL8vjhcvcWfaKjjw52CD_qLb-AjzuILtpqselXYCY/edit?usp=sharing|https://docs.google.com/spreadsheets/d/1-GWL8vjhcvcWfaKjjw52CD_qLb-AjzuILtpqselXYCY/edit?usp=sharing|smart-link] 
  Here is the Internal Report : [https://docs.google.com/document/d/1YRmoituOKBrEWE3jSO2dtc9u-QJzZVn-45oByHG9bjs/edit?usp=sharing|https://docs.google.com/document/d/1YRmoituOKBrEWE3jSO2dtc9u-QJzZVn-45oByHG9bjs/edit?usp=sharing|smart-link] 
  KB Article Draft : [https://access.redhat.com/articles/7143289|https://access.redhat.com/articles/7143289]

* **Automation for Jira** (2026-06-01): Please add '*Release Note Text*', '*Release Note Status*' and '*Release Notes Type*'. Transitioning the issue back to 'In progress'. 
  
  If Release Note is not required, set *Release Note Type* to '*Release Note Not Required*' 



---


