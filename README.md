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

### Application Security Groups

This repo includes two ASG rule files:

| File | Purpose |
|------|---------|
| `default-deny-1433.json` | Allows egress on all TCP/UDP ports except `1433` |
| `sql-access-asg.json` | Allows TCP egress to a specific SQL Server host/CIDR on `1433` |

**Create the security groups:**

```bash
cf create-security-group default-deny-1433 default-deny-1433.json
cf create-security-group sql-access sql-access-asg.json
```

Before creating `sql-access-asg.json`, replace `<sql-server-ip-or-cidr>` with your actual SQL Server destination.

**Update an existing security group's rules** (e.g. after editing a JSON file):

```bash
cf update-security-group default-deny-1433 default-deny-1433.json
cf update-security-group sql-access sql-access-asg.json
```

**Bind the groups to your space** so they apply to running/staging apps:

```bash
cf bind-security-group default-deny-1433 YOUR_ORG YOUR_SPACE
cf bind-security-group sql-access YOUR_ORG YOUR_SPACE
```

Restage or restart the app for the updated groups to take effect:

```bash
cf restage tcp-egress-tester
```

## Deactivate the virtual environment

```bash
deactivate
```
