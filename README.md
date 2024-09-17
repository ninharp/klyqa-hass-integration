# Klyqa Light Integration for Home Assistant

This is a Home Assistant integration for Klyqa light devices, providing both automatic discovery and manual addition of Klyqa lights. The integration currently supports the following devices:

- Klyqa E27 RGB CW/WW
- Klyqa E14 RGB CW/WW
- Klyqa GU10 RGB CW/WW
- Klyqa Strype RGB CW/WW

## Features

- **Auto Discovery**: Automatically discover Klyqa light devices on your network without manual configuration.
- **Manual Addition**: Add Klyqa light devices manually by providing their connection details.
- **Full Control**: Manage your lights with features such as power on/off, brightness, color temperature, and full RGB control.

## HACS Installation

Easiest install is via [HACS](https://hacs.xyz/):

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ninharp&repository=klyqa-hass-integration&category=integration)

`HACS -> Integrations -> Explore & Add Repositories -> Klyqa`


## Manual Installation

1. Download this repository and place the `klyqa` folder into your Home Assistant `custom_components` directory.
2. Restart Home Assistant.
3. Go to the Home Assistant configuration screen and add the "Klyqa Light Integration" from the list of integrations.
4. Configure the devices either through auto discovery or by adding them manually.

## Supported Devices

| Device Type | Model                     |
|-------------|----------------------------|
| Bulb        | Klyqa E27 RGB CW/WW         |
| Bulb        | Klyqa E14 RGB CW/WW         |
| Spotlight   | Klyqa GU10 RGB CW/WW        |
| Light Strip | Klyqa Strype RGB CW/WW      |

## Configuration

### Auto Discovery

Once installed, this integration will automatically scan your network for supported Klyqa devices. Discovered devices will be listed in the integrations page where you can easily add them.

### Manual Configuration

For manual configuration, follow these steps:

1. Open the Home Assistant web interface.
2. Navigate to **Settings** > **Devices & Services** > **Add Integration**.
3. Search for "Klyqa Integration v2" and enter the device details, such as the IP address, port and access token.

## Requirements

- Home Assistant 2023.1 or higher
- Klyqa light devices connected to the same network as Home Assistant

## Troubleshooting

- Ensure your Klyqa devices are connected to the same local network as Home Assistant.
- If auto discovery does not find your devices, try restarting Home Assistant or manually adding the devices using the IP address.

## Contributing

If you encounter any issues or have suggestions for improvements, feel free to open an issue or contribute to this repository.

---

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

