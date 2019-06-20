#!/usr/bin/env bash

# Whitelist secret stuff
echo "!secrets.yaml" | tee homeassistant/config/.gitignore
echo "!known_devices.yaml" | tee -a homeassistant/config/.gitignore
echo "!phue.conf" | tee -a homeassistant/config/.gitignore

# Push balena
balena push friday

# Delete whitelist to avoid accidentally adding secrets to git
rm homeassistant/config/.gitignore