"""Config flow for Klyqa Integration integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.components import onboarding, zeroconf
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import (
    CONF_ACCESS_TOKEN,
    CONF_HOST,
    CONF_MAC,
    CONF_NAME,
    CONF_PASSWORD,
    CONF_PORT,
    CONF_USERNAME,
)
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from klyqa.cloud import KlyqaCloud
from klyqa.device import KlyqaDevice
from klyqa.exceptions import KlyqaError

from .const import DOMAIN, LOGGER


class KlyqaConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Klyqa Integration."""

    VERSION = 1

    host: str
    port: int
    access_token: str
    device_id: str | None = None
    device_name: str | None = "Klyqa Device"
    service_name: str | None = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle a flow initiated by the user."""
        LOGGER.debug("KLYQA KlyqaConfigFlow async_step_user")
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_HOST): str,
                        vol.Required(CONF_PORT, default=3333): int,
                        vol.Required(CONF_ACCESS_TOKEN): str,
                    }
                ),
            )

        self.host = user_input[CONF_HOST]
        self.port = user_input[CONF_PORT]
        self.access_token = user_input[CONF_ACCESS_TOKEN]

        try:
            await self._get_klyqa_local_service_name(raise_on_progress=False)
        except KlyqaError:
            return self._async_show_setup_form({"base": "cannot_connect"})

        return self.async_create_entry(
            title=self.device_name,
            data={
                CONF_HOST: self.host,
                CONF_PORT: self.port,
                CONF_MAC: self.device_id,
                CONF_ACCESS_TOKEN: self.access_token,
                CONF_NAME: self.device_name,
            },
        )

    async def async_step_zeroconf(
        self, discovery_info: zeroconf.ZeroconfServiceInfo
    ) -> ConfigFlowResult:
        """Handle zeroconf discovery."""
        LOGGER.debug("KLYQA KlyqaConfigFlow async_step_zeroconf")
        # Abort quick if the device id is provided by discovery info
        if device_id := discovery_info.properties.get("localDeviceId"):
            await self.async_set_unique_id(device_id)
            self._abort_if_unique_id_configured(
                updates={CONF_HOST: discovery_info.host}
            )

        self.host = discovery_info.host
        self.device_id = discovery_info.properties.get("localDeviceId")
        self.port = discovery_info.port or 3333

        LOGGER.debug(f"KLYQA KlyqaConfigFlow local device id {self.device_id}")

        if not onboarding.async_is_onboarded(self.hass):
            return self._async_create_entry()

        self._set_confirm_only()
        self.context.update(
            {
                "title_placeholders": {"name": self.device_id},
                "configuration_url": f"http://{self.host}",
            }
        )

        return await self.async_step_zeroconf_confirm()

    async def async_step_zeroconf_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle a flow initiated by zeroconf."""
        LOGGER.debug("KLYQA KlyqaConfigFlow async_step_zeroconf_confirm")

        if user_input is not None or not onboarding.async_is_onboarded(self.hass):
            LOGGER.debug(f"KLYQA user_input {user_input}")
            LOGGER.debug(f"KLYQA device name: {self.device_name}")
            try:
                cloud = KlyqaCloud(user_input[CONF_USERNAME], user_input[CONF_PASSWORD])
                await cloud.login()
            except Exception:
                return self.async_abort(reason="invalid_auth")

            try:
                self.access_token = await cloud.get_device_access_token(self.device_id)
            except KlyqaError:
                await cloud.close()
                return self.async_abort(reason="device_not_found")

            self.device_name = await cloud.get_device_name(self.device_id)
            await cloud.close()

            try:
                await self._get_klyqa_local_service_name()
            except KlyqaError:
                return self.async_abort(reason="cannot_connect")

            return self.async_create_entry(
                title=self.device_name,
                data={
                    CONF_HOST: self.host,
                    CONF_PORT: self.port,
                    CONF_MAC: self.device_id,
                    CONF_ACCESS_TOKEN: self.access_token,
                    CONF_NAME: self.device_name,
                },
            )

        data_schema = {
            vol.Required(CONF_USERNAME): str,
            vol.Required(CONF_PASSWORD): str,
        }
        return self.async_show_form(
            step_id="zeroconf_confirm",
            description_placeholders={"name": self.device_id},
            data_schema=vol.Schema(data_schema),
        )

    async def _get_klyqa_local_service_name(
        self, raise_on_progress: bool = True
    ) -> None:
        """Get device information from an Klyqa Light device."""
        session = async_get_clientsession(self.hass)
        LOGGER.debug(f"KLYQA local access token {self.access_token}")
        device = KlyqaDevice(
            host=self.host,
            port=self.port,
            access_token=self.access_token,
            session=session,
        )
        info = await device.info()

        # Check if already configured
        await self.async_set_unique_id(
            info.device_id, raise_on_progress=raise_on_progress
        )
        self._abort_if_unique_id_configured(
            updates={
                CONF_HOST: self.host,
                CONF_PORT: self.port,
                CONF_MAC: self.device_id,
                CONF_ACCESS_TOKEN: self.access_token,
                CONF_NAME: self.device_name,
            }
        )

        self.service_name = info.service_name
        self.device_id = info.device_id


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
