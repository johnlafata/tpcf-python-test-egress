# TCP Egress Tester

A lightweight FastAPI app that probes TCP connectivity to a host and port — useful for confirming network egress is open without needing a full database connection.

## Setup

### 1. Create a virtual environment

```bash
python3 -m venv .venv
```

### 2. Activate the virtual environment

**macOS / Linux:**
```bash
source .venv/bin/activate
```

**Windows:**
```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python main.py
```

Or equivalently:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Usage

### Probe a host and port

```bash
curl "http://localhost:8000/probe?host=your-sql-server.example.com&port=1433"
```

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `host`    | yes      | —       | Hostname or IP to probe |
| `port`    | no       | `1433`  | TCP port to test |
| `timeout` | no       | `5.0`   | Timeout in seconds |

### Example responses

**Reachable:**
```json
{
  "host": "your-sql-server.example.com",
  "port": 1433,
  "reachable": true,
  "latency_ms": 12.4,
  "error": null
}
```

**Not reachable:**
```json
{
  "host": "your-sql-server.example.com",
  "port": 1433,
  "reachable": false,
  "latency_ms": null,
  "error": "Connection timed out"
}
```

### Interactive API docs

Visit `http://localhost:8000/docs` in your browser.

---

## Deploy to Cloud Foundry

```bash
cf push
```

Once deployed, replace `localhost:8000` with your CF app URL.

## Deactivate the virtual environment

```bash
deactivate
```
