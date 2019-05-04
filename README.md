# friday
Home automation and other stuff

## PiHole configuration
- Provide environment variables via balenaCloud:
  - TZ: Set your [timezone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
  - WEBPASSWORD: Set your admin password
- Configure router
  - Set your only DNS to your PiHole's IP
  - [Tomato firmware] Disable 'Use internal DNS' on Advanced Settings/DNS

