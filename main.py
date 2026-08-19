import socket
import time
from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI(title="Egress Tester")

SQLSERVER_PORT = 1433


class ProbeResult(BaseModel):
    host: str
    port: int
    reachable: bool
    latency_ms: float | None
    error: str | None


@app.get("/probe", response_model=ProbeResult)
def probe(
    host: str = Query(..., description="Hostname or IP to probe"),
    port: int = Query(SQLSERVER_PORT, description="TCP port (default 1433 for SQL Server)"),
    timeout: float = Query(5.0, description="Timeout in seconds"),
):
    start = time.monotonic()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            latency_ms = (time.monotonic() - start) * 1000
            return ProbeResult(host=host, port=port, reachable=True, latency_ms=round(latency_ms, 2), error=None)
    except (socket.timeout, TimeoutError):
        return ProbeResult(host=host, port=port, reachable=False, latency_ms=None, error="Connection timed out")
    except ConnectionRefusedError:
        return ProbeResult(host=host, port=port, reachable=False, latency_ms=None, error="Connection refused")
    except socket.gaierror as e:
        return ProbeResult(host=host, port=port, reachable=False, latency_ms=None, error=f"DNS resolution failed: {e}")
    except OSError as e:
        return ProbeResult(host=host, port=port, reachable=False, latency_ms=None, error=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
