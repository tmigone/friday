#!/usr/bin/env bash

rm homeassistant/.gitignore
cp homeassistant/.gitignores/.gitignore-balena homeassistant/.gitignore

balena push friday

rm homeassistant/.gitignore
cp homeassistant/.gitignores/.gitignore-full homeassistant/.gitignore