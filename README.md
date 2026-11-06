# Flask Micro-API

MC - SDIR | Flask Micro-API, CIS3590. A minimal Flask app with JSON endpoints
and a reproducible Python `requests` demonstration.

## Setup and run

Use Python 3.12 or newer. In a terminal in this repository:

```text
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Or activate it on macOS/Linux:

```sh
source .venv/bin/activate
```

Install dependencies and run the local development server:

```text
python -m pip install -r requirements.txt
python app.py
```

The API listens at `http://127.0.0.1:5000` with debug mode off.

## Endpoints

| Method | Path | Success response | HTTP status |
| --- | --- | --- | --- |
| GET | `/hello` | `{"message": "Welcome to the Flask Micro-API!"}` | 200 |
| GET | `/data` | `{"count": 2, "items": [{"id": 1, "name": "Notebook", "category": "school"}, ...]}` | 200 |
| POST | `/data` | `{"item": {"id": 3, "name": "Pencil", "category": "school"}}` | 201 |

POST requires `Content-Type: application/json` and an object such as:

```json
{
  "name": "Pencil",
  "category": "school"
}
```

Both fields must be non-empty strings. Leading and trailing whitespace is
trimmed. IDs are assigned by the server. A successful POST adds an item that
appears in later GET requests. Malformed JSON or invalid fields return 400;
an unsupported content type returns 415. Unknown routes return 404 and
unsupported methods return 405. All these responses use JSON.

## Demonstration and evidence

With the server running, open a second terminal, activate the environment,
and run:

```text
python demo_requests.py
```

The script makes **13 real HTTP requests**, checks status codes and JSON
content types, verifies creation and persistence, and verifies that rejected
writes do not change the collection. It also checks whitespace trimming,
server-assigned IDs, input validation, and the preserved `Allow` header.

The committed run passed all 13 checks. The generated evidence includes:

- [`evidence/results.json`](evidence/results.json): timestamp, versions,
  request bodies, HTTP statuses, and actual response bodies.
- [`evidence/console_output.txt`](evidence/console_output.txt): script output.
- [`evidence/successful_calls.html`](evidence/successful_calls.html): captured
  GET /hello, GET /data, POST /data, and GET after creation.
- [`evidence/validation_calls.html`](evidence/validation_calls.html): captured
  error responses and the final collection check.
- [`evidence/successful_calls.jpg`](evidence/successful_calls.jpg): Chrome
  screenshot of the successful GET calls.
- [`evidence/post_and_get.jpg`](evidence/post_and_get.jpg): Chrome screenshot
  of POST creation and the subsequent GET with the new item.
- [`evidence/validation_calls.jpg`](evidence/validation_calls.jpg): Chrome
  screenshot of the input-validation results. All error cases are recorded
  in the JSON and HTML evidence.

The HTML pages display saved responses from the script; they do not simulate
or replace HTTP calls. Run the script again to regenerate them. The demo adds
one item per run, so restart the API first to reproduce the initial two-item
collection exactly.

## Structure and Agile process

- `app.py`: app factory, routes, validation, and JSON HTTP error handler.
- `requirements.txt`: pinned Flask and requests versions used for the demo.
- `demo_requests.py`: live HTTP acceptance checks and evidence generation.
- `AGILE.md`: user stories, estimates, Kanban status, sprint planning,
  status checkpoints, review, and retrospective.

The implementation was delivered in small increments: plan the backlog,
implement the API and demonstration, then review the live results and document
the outcome. See [`AGILE.md`](AGILE.md) for the work log.

## Scope and limitations

This is a local teaching example. Data is stored in memory and resets when
the server restarts. There is no database, authentication, or production
deployment. Flask's development server is used only for this demonstration.

Flask and requests are open-source dependencies. They reduce setup effort and
provide established routing and HTTP-client tools; version compatibility and
dependency updates still need maintenance. The pinned requirements document
the versions exercised here.

## References

- [Flask Quickstart](https://flask.palletsprojects.com/en/stable/quickstart/)
- [Requests Quickstart](https://requests.readthedocs.io/en/latest/user/quickstart/)
