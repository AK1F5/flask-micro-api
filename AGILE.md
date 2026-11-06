# Agile work log

## Sprint goal

Deliver a minimal Flask API with JSON responses, demonstrate real GET and POST
requests, and provide reproducible evidence for MC - SDIR | Flask Micro-API.

## Product backlog and acceptance criteria

| ID | User story | Points | Acceptance criteria | Status |
| --- | --- | --- | --- | --- |
| API-1 | As an API consumer, I want a welcome endpoint. | 1 | GET /hello returns HTTP 200 and a JSON welcome message. | Done |
| API-2 | As an API consumer, I want to read and add sample items. | 3 | GET /data returns structured JSON; POST /data validates input and returns HTTP 201; a subsequent GET includes the new item. | Done |
| API-3 | As a reviewer, I want reproducible proof. | 2 | A Python requests script checks both methods, captures actual responses, and produces evidence; setup and limitations are documented. | Done |

## Workflow

Use a small Kanban board (Ready, In progress, Done), prioritize the working
endpoints, and inspect each increment before moving a story to Done. Keep the
definition of done visible: readable code, passing HTTP checks, JSON error
responses, documentation, and captured evidence.

## Iteration log

- Planning: reviewed the Canvas instructions and rubric, split the work into the
  three stories above, and defined acceptance criteria before implementation.
- Implementation: added the welcome route, collection GET/POST routes, input
  validation, server-assigned IDs, and consistent JSON HTTP errors.
- Review: 13 live HTTP requests passed on November 6, 2026. Confirmed creation,
  retrieval, JSON content types, expected HTTP codes, rejected-write isolation,
  and the preserved Allow header. API-1 and API-2 moved to Done.
- Course-context review: checked all 12 course announcements, Module 3 Overview
  and Resources, and the APIs/Flask lesson. No Flask-specific revision was
  present. Expanded this process record to reflect Module 3's emphasis on
  estimates, sprint planning, status checkpoints, and retrospectives.
- Demonstration review: saved Chrome screenshots of actual captured responses,
  checked the GET and POST proof, and completed setup instructions and scope
  documentation. API-3 moved to Done; all 6 story points are complete.

## One-week sprint planning exercise

Planned timebox: November 6-12, 2026. The three stories total 6 relative points.
Prioritize API-1, then API-2, then API-3; the evidence story depends on working
routes. The one-week schedule reserves the first day for the API, the second
for acceptance checks, and the remaining days for fixes, documentation, review,
and a retrospective. A small scope can finish before the timebox ends.

The points and schedule are planning exercises added during the course-context
review. They are not a claim that a week elapsed or that team meetings occurred.
The actual implementation and HTTP review took place in one working session.

## Solo standup-style checkpoints

| Checkpoint | Completed | Next | Blocker |
| --- | --- | --- | --- |
| Planning | Rubric reviewed; backlog and acceptance criteria written. | Implement the smallest working API. | Existing Python launcher did not run. |
| Implementation | Endpoints and requests demo written. | Run real GET/POST checks. | Local network permissions initially prevented the test client from reaching the server. |
| Review | Isolated Python environment runs; all 13 HTTP checks pass. | Capture screenshots and finish submission packaging. | None for API behavior. |

These are recorded solo progress checks, not team Scrum meetings. No pair
programming, external stakeholder review, or multi-day daily Scrum is claimed.

## Retrospective

- What went well: explicit acceptance criteria kept the API small, and the
  requests demonstration verified actual HTTP behavior and data changes.
- What slowed progress: the existing Python launcher failed, and the first
  client/server attempts ran with incompatible local network permissions.
  An isolated official Python environment and permitted local HTTP access
  resolved those setup issues.
- Improvement for the next iteration: verify the runtime and local connection
  with a single smoke request before implementing the complete demo. Keep
  process evidence alongside code instead of reconstructing it at submission.
- Next backlog item, outside this assignment's MVP: add persistent storage
  if data needs to survive a restart.
