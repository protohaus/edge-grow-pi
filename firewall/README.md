# Firewall

- Checks that the WiFi is up

## Error Reporting

The application uses the environment variable `RESIN_HOST_CONFIG_sentry_dsn` to configure the address to send the error reports to. This should be set in the [Resin.io dashboard](https://dashboard.resin.io/apps/1056726/config) and the value is generated in the [sentry.io dashboard](https://sentry.io/settings/smartdigitalgarden/sdg_central_hub/keys/).

## References

- https://docs.resin.io/reference/OS/network/2.x/
- https://developer.gnome.org/NetworkManager/stable/gdbus-org.freedesktop.NetworkManager.html
- https://docs.resin.io/learn/manage/configuration/
