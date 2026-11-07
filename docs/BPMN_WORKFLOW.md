# 📊 BPMN 2.0 Process Workflow: Content Operations

This document defines the formal business process model for the **AI Content Operations Platform**, structured to provide Business Analysts, Product Managers, and Technical Architects with a clear operational understanding.

---

## 1. Process Overview & Business Objectives

| Parameter | Specification |
|---|---|
| **Process Name** | Automated Technical Milestone to Social Channel Operations |
| **Owner** | Developer Relations / Product Marketing / Engineering Lead |
| **Key Performance Indicator (KPI)** | Time-to-Draft &lt; 30 seconds; Zero accidental publishing defects |
| **Governance Standard** | ISO/IEC 42001 (Artificial Intelligence Management System) aligned human sign-off |

---

## 2. BPMN Process Diagram

```mermaid
flowchart TD
    Start(["● Start: GitHub Release Tagged"]) --> Task1["Extract Git Commits & PR Metadata"]
    Task1 --> Task2["Analyze Technical Artifacts (TechExtractorAgent)"]
    Task2 --> Task3["Draft Business Narrative (BusinessStoryAgent)"]
    Task3 --> Task4["Evaluate Quality & Formatting (QualityGateAgent)"]
    
    Task4 --> Gateway1{"Quality Score &gt;= 80%?"}
    Gateway1 -->|No| SubProcess1["Auto-Refine Draft / Flag Issues"]
    SubProcess1 --> Task3
    
    Gateway1 -->|Yes| HumanTask["Human Review & Approval Gate (Interactive CLI / UI)"]
    HumanTask --> Gateway2{"Approved by Stakeholder?"}
    
    Gateway2 -->|No| EndRejected(["● Terminate: Draft Discarded / Revision Requested"])
    
    Gateway2 -->|Yes| Task5["Dispatch Mutation to Buffer API (saveToDraft=True)"]
    Task5 --> Task6["Validate Response (PostActionSuccess)"]
    Task6 --> Task7["Update Audit Log & Register API Activity"]
    Task7 --> EndSuccess(["● End: Draft Staged in Buffer Queue"])
```

---

## 3. Detailed Process Narrative

### Phase 1: Technical Ingestion
- **Trigger**: A new release tag (e.g. `v1.2.0`) is published on GitHub, or an engineer runs `content-ops publish`.
- **Action**: Ingestion engine parses conventional commits, changelogs, and pull request links.

### Phase 2: Multi-Agent Synthesis
- **Technical Extraction**: Isolates breaking changes, performance wins, and framework versions.
- **Narrative Framing**: Translates code into a three-part business story:
  1. *Challenge*: Why does this engineering work matter?
  2. *Solution*: What did we build?
  3. *Impact*: Measurable velocity, cost reduction, or architectural robustness.

### Phase 3: Governance & Review Gate
- Automated checks verify that character count is below LinkedIn's 3,000-character ceiling (target: ~1,500 chars).
- The human reviewer inspects the preview in the terminal or web dashboard.

### Phase 4: Safe Buffer Staging
- The post is created with `saveToDraft: true`.
- The draft appears inside the user's Buffer queue, where scheduling or manual broadcast can take place with 100% confidence.
