"""Base entity for the Klyqa integration."""

from __future__ import annotations

from homeassistant.const import ATTR_CONNECTIONS, CONF_MAC
from homeassistant.helpers.device_registry import (
    CONNECTION_NETWORK_MAC,
    DeviceInfo,
    format_mac,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, LOGGER
from .coordinator import KlyqaDataUpdateCoordinator


class KlyqaEntity(CoordinatorEntity[KlyqaDataUpdateCoordinator]):
    """Defines an Klyqa entity."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: KlyqaDataUpdateCoordinator) -> None:
        """Initialize an Klyqa entity."""
        LOGGER.debug("KLYQA KlyqaEntity init")
        super().__init__(coordinator=coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.data.info.device_id)},
            serial_number=coordinator.data.info.device_id,
            manufacturer="Klyqa",
            model=coordinator.data.info.product_id,
            name=coordinator.data.info.service_name,
            sw_version=f"{coordinator.data.info.firmware_version}",
            hw_version=str(coordinator.data.info.hardware_revision),
            # model_id=coordinator.data.info.product_id,
            modified_at=coordinator.data.info.firmware_date,
        )
        if (mac := coordinator.config_entry.data.get(CONF_MAC)) is not None:
            self._attr_device_info[ATTR_CONNECTIONS] = {
                (CONNECTION_NETWORK_MAC, format_mac(mac))
            }
