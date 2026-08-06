# Perf & Scale Quarterly Review for Konflux

## Top of Mind
* Finished reqs==lims compute-resource fixes across ~30 build-definitions tasks ([KONFLUX-11509](https://redhat.atlassian.net/browse/KONFLUX-11509), 18+ PRs merged)
* Shipped OOM/CrashLoopBackOff Jira automation: routing, dedup, smart filtering ([KONFLUX-14299](https://redhat.atlassian.net/browse/KONFLUX-14299), 5sp)
* Completed Critical ServiceAccount migration ahead of the July 30 deadline ([KONFLUX-14970](https://redhat.atlassian.net/browse/KONFLUX-14970))
* Ran production-scale "Rebuild All" and ArgoCD agent-mode storm tests ([KONFLUX-12492](https://redhat.atlassian.net/browse/KONFLUX-12492), [KONFLUX-12588](https://redhat.atlassian.net/browse/KONFLUX-12588))

## Risks/Concerns
* Quay.io capacity for 100x Konflux load still unconfirmed by Quay side ([KONFLUX-15081](https://redhat.atlassian.net/browse/KONFLUX-15081))
* Agentic-workflow readiness Feature stalled on scope debate, no committed end date ([KONFLUX-12747](https://redhat.atlassian.net/browse/KONFLUX-12747), Critical)
* Recurring probe instability on Fedora RPM and stone-stg-rh01 clusters (ROK-2118)
* MCO CrashLoopBackOff fix verified upstream but Konflux clusters still on unpatched 4.x (OCPBUGS-74970)

## Coming up
* GitOps-ify release pipeline secrets in konflux-release-data ([KONFLUX-15196](https://redhat.atlassian.net/browse/KONFLUX-15196))
* End-to-end release run on kflux-rhel-p01: build, snapshot, release ([KONFLUX-15166](https://redhat.atlassian.net/browse/KONFLUX-15166))
* Replicate small-scale ArgoCD agent setup on ScaleLab bare metal ([KONFLUX-15125](https://redhat.atlassian.net/browse/KONFLUX-15125))
* Identify monitoring/ownership for internal signing service ([KONFLUX-15253](https://redhat.atlassian.net/browse/KONFLUX-15253), 3sp)
* New CI check to enforce reqs==lims on every build-definitions PR ([KONFLUX-11510](https://redhat.atlassian.net/browse/KONFLUX-11510), Major)

## Collaboration Opportunities
* Engaged #quay-qe and Quay contributors to baseline quay.io capacity for 100x load ([KONFLUX-15081](https://redhat.atlassian.net/browse/KONFLUX-15081))
* Escalated kube-rbac-proxy-crio-ip restarts to MCO team via OCPBUGS-74970
* Notified Fedora/Mock maintainer on kflux-fedora-01 RPM probe failures (ROK-2118)
* Partnering with ScaleLab team on bare-metal ArgoCD agent-mode replication ([KONFLUX-15125](https://redhat.atlassian.net/browse/KONFLUX-15125))
