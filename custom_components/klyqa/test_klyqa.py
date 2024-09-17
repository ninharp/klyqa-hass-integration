import asyncio

from aiohttp.client import ClientSession
from klyqa.cloud import KlyqaCloud
from klyqa.device import KlyqaDevice
from klyqa.models import Info, RGBColor, State
import json


async def main():
    # Cloud interaction
    cloud = KlyqaCloud("sauer.uetersen@gmail.com", "12345678")
    api_key = await cloud.login()

    print("Got api key")
    # print(api_key)

    # Fetch devices
    devices = await cloud.get_devices()
    print("Devices:", json.dumps(devices))

    # Device interaction
    local_device_id = "806599881770"
    print("Trying to get accessToken for device id ", local_device_id)
    access_token = await cloud.get_device_access_token(local_device_id)
    print("Found token: ", access_token)

    print("Trying to get name for device id ", local_device_id)
    device_name = await cloud.get_device_name(local_device_id)
    print("Found name: ", device_name)

    device = KlyqaDevice("192.168.2.127", 3333, access_token, ClientSession())

    info: Info = await device.info()

    state: State = await device.state()

    print(state.mode)

    print(info.firmware_version)

    await device.light(
        on=True, color=RGBColor(red=0, green=0, blue=255), brightness=100
    )

    await cloud.close()
    await device.close()


asyncio.run(main())
