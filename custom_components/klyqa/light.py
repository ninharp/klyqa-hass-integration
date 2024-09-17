"""Support for Klyqa lights."""

from __future__ import annotations

from typing import Any

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_RGB_COLOR,
    ATTR_COLOR_TEMP_KELVIN,
    ColorMode,
    LightEntity,
)
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import KlyqaConfigEntry
from .const import LOGGER
from .coordinator import KlyqaDataUpdateCoordinator
from .entity import KlyqaEntity
from klyqa.device import RGBColor
from klyqa.exceptions import KlyqaError

PARALLEL_UPDATES = 1


async def async_setup_entry(
    hass: HomeAssistant,
    entry: KlyqaConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Klyqa Light based on a config entry."""
    LOGGER.info("KLYQA light.py async_setup_entry")
    coordinator = entry.runtime_data
    async_add_entities([KlyqaLight(coordinator)])

    # platform = async_get_current_platform()


class KlyqaLight(KlyqaEntity, LightEntity):
    """Defines an Klyqa Light."""

    _attr_name = None
    _attr_min_mireds = 153
    _attr_max_mireds = 285

    def __init__(self, coordinator: KlyqaDataUpdateCoordinator) -> None:
        """Initialize Klyqa Light."""
        LOGGER.debug("KLYQA KlyqaLight init")
        super().__init__(coordinator)
        self._attr_supported_color_modes = {
            # ColorMode.WHITE,
            ColorMode.RGB,
            ColorMode.COLOR_TEMP,
            ColorMode.ONOFF,
            ColorMode.BRIGHTNESS,
        }
        self._attr_unique_id = coordinator.data.info.device_id
        supported_color_modes: set[ColorMode] | None = (None,)

        # Klyqa Light supporting white, have a different temperature range
        # if (
        #     self.coordinator.data.info.product_name
        #     in (
        #         "Klyqa Strype",
        #         "Klyqa E27 RGB + CW",
        #           ...
        #     )
        #     or self.coordinator.data.state.color is not None
        # ):
        #     self._attr_supported_color_modes = {ColorMode.COLOR_TEMP, ColorMode.RGB}
        #     self._attr_min_mireds = 153
        #     self._attr_max_mireds = 285

    @property
    def brightness(self) -> int | None:
        """Return the brightness in percentage of this light between 1..100."""
        return int(self.coordinator.data.state.brightness.percentage * 255 / 100)

    @property
    def color_temp_kelvin(self) -> int | None:
        """Return the CT color value in kelvin."""
        return self.coordinator.data.state.temperature

    @property
    def color_mode(self) -> str | None:
        """Return the color mode of the light."""
        if self.coordinator.data.state.mode is not None:
            if self.coordinator.data.state.mode == "rgb":
                return ColorMode.RGB
            return ColorMode.WHITE

        return ColorMode.RGB

    @property
    def rgb_color(self) -> tuple[int, int, int] | None:
        """Return the color value."""
        return (
            self.coordinator.data.state.color.red,
            self.coordinator.data.state.color.green,
            self.coordinator.data.state.color.blue,
        )

    @property
    def is_on(self) -> bool:
        """Return the state of the light."""
        if self.coordinator.data.state.on == "on":
            return True
        return False

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the light."""
        LOGGER.debug("KLYQA KlyqaLight async_turn_off")
        try:
            await self.coordinator.client.light(on=False)
        except KlyqaError as error:
            raise HomeAssistantError(
                "An error occurred while updating the Klyqa Light"
            ) from error
        finally:
            await self.coordinator.async_refresh()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the light."""
        LOGGER.debug("KLYQA KlyqaLight async_turn_on")
        temperature = kwargs.get(ATTR_COLOR_TEMP_KELVIN)

        red = None
        green = None
        blue = None
        color = None
        if ATTR_RGB_COLOR in kwargs:
            red, green, blue = kwargs[ATTR_RGB_COLOR]
            color = RGBColor(red=red, green=green, blue=blue)

        brightness = None
        if ATTR_BRIGHTNESS in kwargs:
            brightness = round((kwargs[ATTR_BRIGHTNESS] / 255) * 100)

        if (
            brightness
            and ATTR_RGB_COLOR not in kwargs
            and ATTR_COLOR_TEMP_KELVIN not in kwargs
            and self.supported_color_modes
            and ColorMode.RGB in self.supported_color_modes
            and self.color_mode == ColorMode.COLOR_TEMP
        ):
            temperature = self.color_temp

        try:
            await self.coordinator.client.light(
                on=True,
                brightness=brightness,
                color=color,
                temperature=temperature,
            )
        except KlyqaError as error:
            raise HomeAssistantError(
                "An error occurred while updating the Klyqa Light"
            ) from error
        finally:
            await self.coordinator.async_refresh()
