#!/usr/bin/env bash

rm homeassistant/.gitignore
cp homeassistant/.gitignores/.gitignore-balena homeassistant/.gitignore

git push balena master

rm homeassistant/.gitignore
cp homeassistant/.gitignores/.gitignore-full homeassistant/.gitignore