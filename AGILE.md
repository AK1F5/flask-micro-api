# Agile work log

## Sprint goal

Deliver a minimal Flask API with JSON responses, demonstrate real GET and POST
requests, and provide reproducible evidence for MC - SDIR | Flask Micro-API.

## Product backlog and acceptance criteria

| ID | User story | Acceptance criteria | Status |
| --- | --- | --- | --- |
| API-1 | As an API consumer, I want a welcome endpoint. | GET /hello returns HTTP 200 and a JSON welcome message. | Ready |
| API-2 | As an API consumer, I want to read and add sample items. | GET /data returns structured JSON; POST /data validates input and returns HTTP 201; a subsequent GET includes the new item. | Ready |
| API-3 | As a reviewer, I want reproducible proof. | A Python requests script checks both methods, captures actual responses, and produces evidence; setup and limitations are documented. | Ready |

## Workflow

Use a small Kanban board (Ready, In progress, Done), prioritize the working
endpoints, and inspect each increment before moving a story to Done. Keep the
definition of done visible: readable code, passing HTTP checks, JSON error
responses, documentation, and captured evidence.

## Iteration log

- Planning: reviewed the Canvas instructions and rubric, split the work into the
  three stories above, and defined acceptance criteria before implementation.
- Implementation and review: pending.
- Demonstration and retrospective: pending.
