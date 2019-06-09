#!/usr/bin/env bash

mv homeassistant/.gitignore homeassistant/.gitignore.dont-ignore-me
mv homeassistant/.gitignore-balena homeassistant/.gitignore

git push balena master

mv homeassistant/.gitignore homeassistant/.gitignore-balena
mv homeassistant/.gitignore.dont-ignore-me homeassistant/.gitignore