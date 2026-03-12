import asyncio
import nmap
from datetime import datetime, timezone
from app.models import ScanType, ScanStatus
from app.schemas.store import update_scan
import logging

logger = logging.getLogger(__name__)

def perform_nmap_scan(scan_id: str, target: str, scan_type: ScanType):
    try:
        nm = nmap.PortScanner()

        args_map = {
            ScanType.quick: "-T4 -F",
            ScanType.full: "-T4 -p-",
            ScanType.service_detection: "-sV",
        }

        args = args_map.get(scan_type, "")

        logger.info("Starting nmap process", extra={"scan_id": scan_id, "target": target, "arguments": args})
        start = datetime.now(timezone.utc)

        result = nm.scan(hosts=target, arguments=args)

        end = datetime.now(timezone.utc)

        host = list(result["scan"].keys())[0]
        host_data = result["scan"][host]

        open_ports_count = 0
        ports = []
        for proto in host_data.all_protocols():
            for port, port_data in host_data[proto].items():
                if port_data["state"] == "open":
                    open_ports_count += 1
                    ports.append({
                        "port": port,
                        "protocol": proto,
                        "state": port_data["state"],
                        "service": port_data.get("name")
                    })

        duration_seconds = (end - start).total_seconds()
        command = nm.command_line()

        update_scan(scan_id, {
            "status": ScanStatus.completed.value,
            "summary": {
                "open_ports_count": open_ports_count,
                "duration_seconds": duration_seconds
            },
            "results": {
                "host": host,
                "command": command,
                "ports": ports,
                "start_time": start.isoformat(),
                "end_time": end.isoformat()
            }
        })
        logger.info("Nmap scan completed successfully", extra={
            "scan_id": scan_id, 
            "duration": duration_seconds, 
            "open_ports": open_ports_count
        })

    except Exception as e:
        logger.error("Nmap scan failed", extra={"scan_id": scan_id}, exc_info=True)
        update_scan(scan_id, {"status": ScanStatus.failed.value})


async def run_nmap_scan(scan_id: str, target: str, scan_type: ScanType):
    update_scan(scan_id, {"status": ScanStatus.running.value})
    await asyncio.to_thread(perform_nmap_scan, scan_id, target, scan_type)
