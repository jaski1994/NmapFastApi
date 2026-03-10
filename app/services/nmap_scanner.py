import asyncio
import nmap
from datetime import datetime, timezone
from app.models import ScanType, ScanStatus
from app.schemas.store import update_scan


def perform_nmap_scan(scan_id: str, target: str, scan_type: ScanType):
    try:
        nm = nmap.PortScanner()

        args_map = {
            ScanType.quick: "-T4 -F",
            ScanType.full: "-T4 -p-",
            ScanType.service_detection: "-sV",
        }

        args = args_map.get(scan_type, "")

        start = datetime.now(timezone.utc)

        result = nm.scan(hosts=target, arguments=args)

        end = datetime.now(timezone.utc)

        host = list(result["scan"].keys())[0]
        host_data = result["scan"][host]

        ports = []
        for proto in host_data.get("tcp", {}):
            port = host_data["tcp"][proto]
            ports.append({
                "port_id": proto,
                "state": port["state"],
                "service": port.get("name")
            })

        update_scan(scan_id, {
            "status": ScanStatus.completed.value,
            "results": {
                "host": host,
                "ports": ports,
                "start_time": start.isoformat(),
                "end_time": end.isoformat()
            }
        })

    except Exception as e:
        print(e)
        update_scan(scan_id, {"status": ScanStatus.failed.value})


async def run_nmap_scan(scan_id: str, target: str, scan_type: ScanType):
    update_scan(scan_id, {"status": ScanStatus.running.value})
    await asyncio.to_thread(perform_nmap_scan, scan_id, target, scan_type)
