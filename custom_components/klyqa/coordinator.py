"""DataUpdateCoordinator for Klyqa."""

from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ACCESS_TOKEN, CONF_HOST, CONF_PORT, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, LOGGER, SCAN_INTERVAL
from klyqa.device import KlyqaDevice
from klyqa.exceptions import KlyqaConnectionError
from klyqa.models import Info, State


@dataclass
class KlyqaData:
    """Klyqa data stored in the DataUpdateCoordinator."""

    device_name: str
    info: Info
    state: State


class KlyqaDataUpdateCoordinator(DataUpdateCoordinator[KlyqaData]):
    """Class to manage fetching Klyqa data."""

    config_entry: ConfigEntry

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        LOGGER.debug("KLYQA KlyqaDataUpdateCoordinator init")
        self.config_entry = entry
        self.client = KlyqaDevice(
            entry.data[CONF_HOST],
            entry.data[CONF_PORT],
            entry.data[CONF_ACCESS_TOKEN],
            session=async_get_clientsession(hass),
        )
        super().__init__(
            hass,
            LOGGER,
            name=f"{DOMAIN}_{entry.data[CONF_HOST]}",
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self) -> KlyqaData:
        """Fetch data from the Klyqa device."""
        LOGGER.debug("KLYQA KlyqaDataUpdateCoordinator _async_update_data")
        try:
            return KlyqaData(
                device_name=self.config_entry.data[CONF_NAME],
                info=await self.client.info(),
                state=await self.client.state(),
            )
        except KlyqaConnectionError as err:
            raise UpdateFailed(err) from err
