"""Support for Klyqa Lights."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import LOGGER
from .coordinator import KlyqaDataUpdateCoordinator

PLATFORMS = [Platform.LIGHT]

type KlyqaConfigEntry = ConfigEntry[KlyqaDataUpdateCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: KlyqaConfigEntry) -> bool:
    """Set up Klyqa Light from a config entry."""
    LOGGER.debug("KLYQA __init__ async_setup_entry")
    coordinator = KlyqaDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: KlyqaConfigEntry) -> bool:
    """Unload Klyqa Light config entry."""
    LOGGER.debug("KLYQA __init__ async_unload_entry")
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
