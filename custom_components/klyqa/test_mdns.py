import logging
import asyncio
from zeroconf import Zeroconf, ServiceBrowser

logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)

def on_service_state_change(zeroconf, service_type, name, state_change):
    _LOGGER.info(f"Service {name} state changed: {state_change}")
    service_info = zeroconf.get_service_info(service_type, name)
    if service_info:
        _LOGGER.info(f"Service Info: {service_info}")

async def main():
    zeroconf = Zeroconf()
    ServiceBrowser(zeroconf, "_qcxrest._tcp.local.", handlers=[on_service_state_change])
    await asyncio.sleep(10)  # Laufzeit für 10 Sekunden
    zeroconf.close()

if __name__ == "__main__":
    asyncio.run(main())
