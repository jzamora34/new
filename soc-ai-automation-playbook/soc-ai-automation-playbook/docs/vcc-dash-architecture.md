# VCC (Dash) architecture map

> Imported from the VCC repository analysis (Nov 2026). Relative links such as `docs/03-ARCHITECTURE.md` and `src/...` point into the VCC repository, not this one. Counts (446 source files, about 80 routes, 30 repositories, 11 source adapters) are as reported by that analysis.


I built this from the code as well as the docs. The code is a lot bigger than the original plan in [03-ARCHITECTURE.md](docs/03-ARCHITECTURE.md): there are 446 source files, about 80 routes, 30 repositories and 11 source adapters.

---

## Level 0: the whole system on one page

```
   SYSTEMS OF RECORD                 MICROSOFT BACKEND (later)               THIS REPO (frontend)
   (the real truth)                  (ingest + store + AI)                   (what users see)
 ┌──────────────────┐         ┌──────────────────────────────┐        ┌─────────────────────────┐
 │ Jira             │──┐      │ Power Automate flows          │        │  Dash web app           │
 │ ServiceNow       │  │ read │  (one per source, service     │  read  │  (Teams tab, browser)   │
 │ SharePoint       │  ├─────>│   account, SourceRegistry)    │──────> │                         │
 │ Artey            │  │      │            │                  │        │  Manager: Overview,     │
 │ Outlook / Teams  │  │      │            v                  │        │   Brief, Team, Alerts   │
 │ Planner / To Do  │  │      │ SharePoint Lists (the store:  │        │  Member: My Work,       │
 │ Mindshell (later)│  │      │  WorkItems, Alerts, Briefs,   │        │   Intake, Delay check-in│
 └──────────────────┘  │      │  Decisions, NeedsYou, ...)    │        │  Admin: Settings, flags │
          ^            │      │            │                  │        └───────────┬─────────────┘
          │            │      │ Copilot Studio agent          │<── Direct Line ───┤ Assistant (read-only)
          │            │      │  (Q&A, brief, orchestrator)   │                   │
          │            │      └──────────────────────────────┘                    │
          └──────────────── confirmed writes (sync flow, as the signed-in user) ──┘
```

What everything else rests on:
- The source systems are the record of truth. The store keeps references, summaries and links.
- Every write starts as a draft that a person confirms, then goes to the source system.

**Where things stand today:** only the right-hand column is built. Every backend call goes to a mock adapter, and every live integration sits behind a feature flag that is off.

---

## Level 1: the layers inside the frontend

```
 L1  Boot             main.tsx → load vcc-config.json → init flags → <App/>
 L2  Providers        QueryClient → Motion → DataProvider → Session → Theme → Toast → AssistantPanel → Router
 L3  Shell + Routing  AppShell (PillNav, TopBar, CommandPalette, AssistantPanel) + routes.tsx with role/flag guards
 L4  Feature pages    src/features/*  (≈40 domains)
 L5  Shared UI        src/components/* (Card, DataTable, Fit, States, SourceChip, Charts, Overlay...)
 L6  Hooks            src/data/hooks.ts + src/data/areas/*/hooks.ts  (TanStack Query, the ONLY UI↔data bridge)
 L7  Repositories     src/data/repositories/index.ts  (30 interfaces = the contract)
 L8  Adapters         mock (now) | live (later), switched per call by feature flags
 L9  Domain engines   sync/ (change sets, executor), automation/, reuse/, domain/
 L10 Source adapters  src/data/sources/* (Jira, SharePoint, Graph mail/Teams/calendar, Planner, ServiceNow, Artey, Orchestrator, links, deptSystem)
 L11 Transport/auth   tokenProvider (MSAL/Teams SSO) + http.ts + withAuthorization
 ─────────────────────────────────────────────────────────────────────
 Cross-cutting:       config/ (runtime, flags, integration TODO_CONFIRM), lib/ (roles, redact, safeUrl, workStatus, clock), theme/
```

Calls only go downward. A page never reaches past layer 6, which [CLAUDE.md](CLAUDE.md) rule 1 requires and the comment at the top of [hooks.ts](src/data/hooks.ts) restates.

---

## Level 2: each layer in detail

### L1: Boot ([main.tsx](src/main.tsx))
1. `applyInitialTheme()` runs first so dark users never see a flash of the light theme.
2. `loadRuntimeConfig()` fetches `vcc-config.json` ([runtime.ts](src/config/runtime.ts), checked with Zod). It holds the base path, auth settings, endpoints and flag overrides. One build can therefore run on any host (decision D1, hosting question Q15 is still open).
3. `initFlags()` ([flagStore.ts](src/config/flagStore.ts)) runs, then React renders. In dev only, axe-core also runs.

### L2: Providers ([App.tsx](src/app/App.tsx))
| Provider | Provides | Used by |
|---|---|---|
| `QueryClientProvider` | Caching, refetching, mutation invalidation | Every hook in L6 |
| `DataProvider` ([provider.tsx](src/data/provider.tsx)) | The `Repositories` object. `VITE_DATA_ADAPTER=mock\|live` picks the adapter | `useRepos()` in hooks |
| `SessionProvider` ([session.tsx](src/app/session.tsx)) | Current user, role and team (from `repos.auth`) | Guards, nav, hooks that scope by role |
| `ThemeProvider` ([theme.tsx](src/app/theme.tsx)) | Dark (default), light or high contrast, set via `data-theme` | [tokens.css](src/theme/tokens.css) → Tailwind |
| `AssistantPanelProvider` | The slide-in assistant on every page | Shell |

### L3: Shell and routing
- **Routes:** [routes.tsx](src/app/routes.tsx) is a single table. Each row lists `path`, `roles`, an optional `flag`, the `Component` and optional `nav` placement (primary or "More" plus a group).
- **The table drives:** the router, PillNav, the mobile tab bar, the command palette and page titles.
- **Guards:** [guards.tsx](src/app/guards.tsx) wraps each route.
  - `RequireRole` checks the role sets in [auth.ts](src/lib/auth.ts) (`M`, `ME`, `A`, `AM`, `CL`, `ALL`, `ANY`).
  - `RequireFlag` hides pages for features that are switched off.
- **Primary nav** has five items (Overview, Brief, Team, My Work, Assistant). Everything else goes under More, grouped as work, operations, insights and agents.
- **Shell chrome** is in [src/app/shell/](src/app/shell/):
  - PillNav, TopBar, CommandPalette, NotificationPanel
  - `ConnectivityBanner` and `IntegrationNotice`, which show what is live and what is mock

### L4: Feature pages ([src/features/](src/features/))
| Group | Domains |
|---|---|
| Manager EIS | overview, brief, team, alerts (+investigate, history, heatmap), insights, metrics, weekly, reports, meeting-prep, blockers, gaps, ontime |
| Member workspace | my-work, todo, intake (new, result, pipeline), updates/delays, follow-ups, decisions |
| AI | assistant (+ orchestrator subfolder), agents (fleet, runs, builder) |
| Admin | settings (≈20 pages), sources, sync (field mapping, link registry, change-set review), ops, roi |
| Other | search, help, client (intake-only role), collab, experience, similar, projects, tickets |

### L5: Shared UI ([src/components/](src/components/))
- **States:** loading, empty and error. Every page must have all three.
- **Fit:** fits a page to one desktop screen with no page scroll.
- **Provenance:** `SourceChip` shows the source system and deep link, `StaleWarning` flags stale data, and `Ai` marks Draft content.
- **Building blocks:** DataTable, Tabs, Overlay (in-app dialogs, never `window.confirm`), Charts and echarts.

### L6: Hooks: the bridge
- **Core hooks:** [hooks.ts](src/data/hooks.ts) has 75 of them, such as `useWorkItems`, `useNeedsYou`, `useAskAssistant` and `useSubmitIntake`. One `qk` object defines every query key.
- **Area hooks:** each folder under `src/data/areas/*/hooks.ts` has its own hooks for the newer domains.
- **Read path:** `useQuery` → `useRepos().x.list()`.
- **Write path:** `useMutation` → repo → invalidate the affected query keys, so the UI refreshes.

### L7: Repository contract ([repositories/index.ts](src/data/repositories/index.ts))
There are 30 interfaces, in three waves:
- **Core (19):** workItems, members, projects, tickets, dashboard, alerts, briefs, assistant, decisions, followUps, intake, updates, settings, search, insights, notifications, auth, feedback, audit
- **Wave 2 areas (8):** dataSources, workspace, metrics, collab, reports, ops, agents, experience
- **Integration areas (4), all behind flags:** sync, visibility, automation, reuse

The types come from [types.ts](src/data/types.ts), which mirrors [04-DATA-MODEL.md](docs/04-DATA-MODEL.md) field for field. Those field names are the backend contract.

### L8: Adapters (the swap point)
- **Mock** ([adapters/mock/](src/data/adapters/mock/)):
  - [store.ts](src/data/adapters/mock/store.ts) loads `mock/mock-data.json` into memory, adds 200–600 ms of latency and fails on purpose with `?mockError=1`.
  - Writes change the in-memory data, so demos work end to end.
  - The [assistant.ts](src/data/adapters/mock/assistant.ts) mock answers by keyword match and returns "not in the data" rather than inventing an answer.
- **Live** ([adapters/live/index.ts](src/data/adapters/live/index.ts)): each method throws `NotImplemented` for now. Its JSDoc names the target API, for example `GET /_api/web/lists/getbytitle('WorkItems')/items`.
- **[flagRouted.ts](src/data/adapters/flagRouted.ts):** a Proxy that checks a flag on every call and sends it to the `on` or `off` implementation. That is how an admin can turn on `orchestratorClient` at runtime and the assistant switches with no reload.

### L9: Domain engines (pure logic, no UI)
- **[sync/](src/data/sync/)** is the write engine:
  - `changeSet` builds a draft (via `planner` and `fieldMapper`).
  - A person confirms it.
  - `executor` runs the steps in order: Jira, then SharePoint, then the link registry, then uploads.
  - Idempotency keys make reruns safe. There is no rollback: finished steps stay and dependent steps are skipped.
  - Every write gets a Decision Log entry.
  - The same folder also has `commentSync` (loop prevention) and `statusSync`.
- **[automation/](src/data/automation/):** `staleDetector`, `delayDraft` (only rephrases what the member wrote), `gapRules` and `todoBuilder`.
- **[reuse/](src/data/reuse/):** `similarRequests` and `templates` draft tasks from past requests, and those tasks are always marked Draft.
- **[domain/](src/data/domain/):** blockers, field aliases and the integration types (ChangeSet, ChangeStep, LinkRegistryEntry).

### L10: Source adapters ([src/data/sources/](src/data/sources/))
- **Structure:** one folder per external system, each with the same four files: `adapter.ts` (interface), `mock.ts`, `live.ts` and a `README.md`.
- **Factories:** [index.ts](src/data/sources/index.ts) provides `createMockSourceAdapters()` and `createLiveSourceAdapters({tokens, fetch})`.
- **Who uses them:** only area repos and the sync engine. Pages and core repos never touch them.
- **Orchestrator** ([README](src/data/sources/orchestrator/README.md)): a Direct Line 3.0 client for Copilot Studio.
  - A server-side endpoint exchanges the user's token for a Direct Line token. The secret never reaches the browser.
  - Replies arrive by polling or WebSocket.
  - [parse.ts](src/data/sources/orchestrator/parse.ts) checks citations and draft change sets against a schema.

### L11: Transport and auth
- **[tokenProvider.ts](src/data/sources/tokenProvider.ts):** two audiences. `graph` is for Microsoft Graph and `proxy` is for the Jira, ServiceNow and orchestrator proxies.
- **[http.ts](src/data/sources/http.ts):** `liveRequest` plus `requireEndpoint`. If a value is still `TODO_CONFIRM` in [integration.ts](src/config/integration.ts), it throws `ConfigMissingError`, naming the open question that would answer it.
- **[roleContract.ts](src/lib/roleContract.ts):**
  - `may(role, op)` and `withAuthorization()` turn a 401 into a re-auth attempt and a 403 into `NotAuthorizedError`.
  - The server is the real enforcer: Entra groups, SharePoint permissions and Copilot Studio end-user auth.

---

## How the sections connect: four traced flows

**1. Read: the manager opens Overview**
```
/ route → RequireRole(M) → OverviewPage → useNeedsYou(team, role)
  → useRepos().dashboard.needsYou() → [mock: store.ts | live: SharePoint 'NeedsYou' list]
  → items carry SourceRef {system, externalId, url, timestamp} → <SourceChip> deep link
```

**2. Write: a member submits an intake request (fan-out)**
```
IntakeNewPage (RHF+Zod) → intake.preview() → FanOutPreviewPanel (per-system fields, missing fields)
  [flag syncEngine on] → sync.buildChangeSet() → ChangeSetReview dialog (names every target system)
  → person confirms → executor: Jira create → SharePoint item → link registry → uploads
  → DecisionLog entry → IntakeResultPage shows GRN-2xx / GTL-0xxx with links
  live: confirmed set POSTs to endpoints.syncFlowUrl, which writes as the signed-in user
```

**3. Assistant question**
```
AssistantChat → useAskAssistant → repos.assistant (flagRouted on 'orchestratorClient')
  off: mock keyword answer          on: Orchestrator → Direct Line → Copilot Studio
  → AssistantAnswer {text, sources[], confidence, draft?} → AnswerTraceDrawer shows sources + timestamps
  Any draft change set → DraftChangeSetReview → same confirm path as flow 2. The assistant never writes.
```

**4. Delay check-in (automation)**
```
staleDetector flags item → Delay Check-in page (badge 'stale') → member types reason
  → delayDraft rephrases ONLY that text (Draft label) → member confirms
  → sync.postDelayComment: Jira comment → commentSync copies to SharePoint (reverse direction is governance-gated)
```

---

## Feature-flag phases (how the integration turns on)
[flags.ts](src/config/flags.ts) groups the flags by rollout phase. All default to off.

| Phase | Flags |
|---|---|
| 1 | syncEngine, linkRegistry, syncCommentsJiraToSharePoint, syncCommentsReverse (gated), decisionLogForWrites |
| 2 | blockersPanel, intakePipeline, onTimeChart |
| 3 | orchestratorClient |
| 4 | delayAutomation, delayDraftAssist, morningTodo, morningTodoMailTraining (gated), gapDetection |
| 5 | similarRequests, roiInstrumentation |
| 6 | deptSystemConnector |

Flags can switch in three places:
- **Routes:** `RequireFlag` hides or shows pages.
- **Repositories:** `flagRouted` picks the mock or live implementation per call.
- **Area repos:** the code that calls them is itself behind a flag.

---

## The documents that govern each layer
| Layer | Governing doc |
|---|---|
| Why and who | [01-PROJECT-CONTEXT](docs/01-PROJECT-CONTEXT.md), [02-REQUIREMENTS](docs/02-REQUIREMENTS.md) |
| L7 contract / types | [04-DATA-MODEL](docs/04-DATA-MODEL.md) |
| L3/L4 routes and pages | [05-PAGE-MAP](docs/05-PAGE-MAP.md), [09-USER-FLOWS](docs/09-USER-FLOWS.md) |
| L5 and theme | [06-DESIGN-SYSTEM](docs/06-DESIGN-SYSTEM.md) |
| L8–L11 integration | [docs/integration/](docs/integration/): implementation plan, adapters, hosting, role contract, open questions, phase 0–6 summaries |
| Cross-cutting rules | [08-STANDARDS](docs/08-STANDARDS.md), [SECURITY-CONTROLS](docs/SECURITY-CONTROLS.md) |
| Status | [TRACKER](docs/TRACKER.md) |

**The swap point:** going live means doing three things, and the UI does not change.
1. Fill in `live.ts` in each source and area.
2. Replace the `TODO_CONFIRM` values in `integration.ts` and `vcc-config.json` with confirmed ones.
3. Turn on flags phase by phase.

## Where the playbook items plug in

| Playbook item | VCC layer |
| --- | --- |
| A5 grounding (trec_eval, lm-text-property-eval, NIST probes) | Offline tooling in `measurement/`; acceptance gate for flag phase 3 (`orchestratorClient`) |
| A1 Automata checks on assistant drafts | L9 domain engines: a deterministic check before a draft change set reaches ChangeSetReview |
| A4 agent identity | L11 tokenProvider + server-side Direct Line token exchange; one Copilot Studio agent identity per agent |
| AgentOps approval and audit | Decision Log entries on every write (phase 1 `decisionLogForWrites`); add actor and hash chain as in agentops/app.py |
| ROI metrics | Phase 5 `roiInstrumentation` flag; use tools/embedding-roi/metrics.py formulas |
| OSCAL control IDs | `SECURITY-CONTROLS.md` and `08-STANDARDS.md` wording from oscal-content |
