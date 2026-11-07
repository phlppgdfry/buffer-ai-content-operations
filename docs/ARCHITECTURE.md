# 📐 System Architecture: Buffer AI Content Operations

This document outlines the software architecture, data contracts, security model, and execution lifecycle of the **Buffer AI Content Operations Platform**.

---

## 1. Architectural Philosophy

The platform is designed around four foundational principles:

1. **Human-in-the-Loop Governance (Zero-Accidental-Publishing)**:
   Automated content pipelines must never post directly to live audiences without explicit human sign-off. All actions stage items as `draft` in Buffer.
2. **Dual-Channel API Integration**:
   Interacts with Buffer both through high-level CLI automations (`@bufferapp/cli`) and direct GraphQL mutations (`https://api.buffer.com`), fulfilling the requirements for official API developer verification.
3. **Multi-Agent Separation of Concerns**:
   - Technical extraction is isolated from business narrative generation.
   - Narrative generation is strictly decoupled from quality and policy enforcement.
4. **Idempotency & Resiliency**:
   Every mutation supports `--dry-run` and safe retry semantics.

---

## 2. Component Diagram

```mermaid
graph TB
    subgraph "Ingestion Layer"
        GH_API["GitHub REST / GraphQL API"]
        GIT_LOCAL["Local Git Engine"]
        CHANGELOG["CHANGELOG.md Parser"]
    end

    subgraph "Multi-Agent Synthesis Engine"
        TEA["TechExtractorAgent<br/>• Conventional Commits Parsing<br/>• Tech Stack Classification<br/>• Optimization Identification"]
        BSA["BusinessStoryAgent<br/>• Problem-Solution Framework<br/>• Business Metric Framing<br/>• Hook & CTA Generation"]
        QGA["QualityGateAgent<br/>• Length Limits (&lt;3000 chars)<br/>• Tone & Fluff Filtering<br/>• Hashtag Balancing"]
    end

    subgraph "Governance Gate"
        REVIEW{"Human Review Gate<br/>• Interactive CLI Review<br/>• Webhook / CI Approval"}
    end

    subgraph "Buffer Integration Layer"
        CLI_RUNNER["Buffer CLI Runner<br/>(@bufferapp/cli 2.2.0)"]
        GQL_CLIENT["Buffer GraphQL Client<br/>(Bearer Token Auth)"]
    end

    subgraph "Destination Platforms"
        BUFFER_DRAFTS["Buffer Staging Queue (Drafts)"]
        LINKEDIN["LinkedIn Profile / Company Page"]
        INSTAGRAM["Instagram Business Channel"]
    end

    GH_API --> TEA
    GIT_LOCAL --> TEA
    CHANGELOG --> TEA

    TEA --> BSA
    BSA --> QGA
    QGA --> REVIEW

    REVIEW -->|Approved| CLI_RUNNER
    REVIEW -->|Approved| GQL_CLIENT

    CLI_RUNNER --> BUFFER_DRAFTS
    GQL_CLIENT --> BUFFER_DRAFTS
    BUFFER_DRAFTS -->|Manual Release| LINKEDIN
    BUFFER_DRAFTS -->|Manual Release| INSTAGRAM
```

---

## 3. End-to-End Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Developer / Engineer
    participant Pipeline as ContentOpsPipeline
    participant Agent1 as TechExtractorAgent
    participant Agent2 as BusinessStoryAgent
    participant Agent3 as QualityGateAgent
    participant Buffer as Buffer API (GraphQL)
    actor Reviewer as Human Reviewer

    Dev->>Pipeline: Trigger Release Ingestion (tag or repo)
    Pipeline->>Agent1: Ingest commits, PRs, release notes
    Agent1-->>Pipeline: TechnicalInsights (features, fixes, stack)

    Pipeline->>Agent2: Synthesize business narrative
    Agent2-->>Pipeline: BusinessNarrative (hook, problem, solution, ROI)

    Pipeline->>Agent3: Evaluate compliance & formatting
    Agent3-->>Pipeline: QualityGateReview (score, checks, character count)

    Pipeline->>Reviewer: Present draft for approval
    alt Rejected
        Reviewer-->>Pipeline: Reject / Request Edit
        Pipeline-->>Dev: Aborted with feedback
    else Approved
        Reviewer-->>Pipeline: Sign-off approved
        Pipeline->>Buffer: mutation createPost(channelId, text, saveToDraft: true)
        Buffer-->>Pipeline: PostActionSuccess (id: "draft_12345", status: "draft")
        Pipeline-->>Dev: Execution Report & Verification
    end
```

---

## 4. Security & Credential Isolation

- **API Keys**: Stored in standard environment variables (`BUFFER_API_KEY`) or in system keyring via `buffer init`.
- **Least-Privilege Token Scopes**: Tokens only require `publish` permissions for draft generation; no administrative or financial access is requested.
- **Dry-Run Enforcement**: In CI/CD pipelines, `--dry-run` is active by default to prevent unwanted mutation calls.
