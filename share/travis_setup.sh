#!/bin/bash
set -evx

mkdir ~/.argoneum

# safety check
if [ ! -f ~/.argoneum/argoneum.conf ]; then
  cp share/argoneum.conf.example ~/.argoneum/argoneum.conf
fi
