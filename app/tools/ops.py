import psutil
import platform

def get_system_metrics() -> str:
    """Fetches real hardware telemetry from the host machine."""
    cpu_usage = psutil.cpu_percent(interval=0.1)
    ram = psutil.virtual_memory()
    ram_usage = ram.percent
    disk = psutil.disk_usage('/')
    
    return (
        f"Live telemetry: CPU load is at {cpu_usage} percent, "
        f"RAM utilization is {ram_usage} percent, "
        f"and {disk.percent} percent disk storage is occupied on {platform.system()}."
    )

def check_ticket_status(ticket_id: str) -> str:
    clean_id = "".join(filter(str.isalnum, ticket_id)) or "409"
    return f"Incident ticket {clean_id} is currently flagged critical and assigned to Cloud Ops team."