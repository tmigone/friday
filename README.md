# friday
Assortment of useful stuff running on my home Raspberry Pi. 

Deployed and managed using [balenaCloud](https://www.balena.io/cloud)

Services (so far):
- [pihole]()
- [homeassistant]()
  

## PiHole
Changes reference: 
- https://forums.balena.io/t/pihole-in-debian-container-on-balenaos/4645/3
- https://github.com/klutchell/balena-pihole

### Configuration
- Provide environment variables via balenaCloud:
  - TZ: Set your [timezone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
  - WEBPASSWORD: Set your admin password
- Configure router
  - Set your only DNS to your PiHole's IP
  - [Tomato firmware] Disable 'Use internal DNS' on Advanced Settings/DNS

