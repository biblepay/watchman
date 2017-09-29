#!/bin/bash
set -evx

mkdir ~/.biblepaycore

# safety check
if [ ! -f ~/.biblepaycore/.biblepay.conf ]; then
  cp share/biblepay.conf.example ~/.biblepaycore/biblepay.conf
fi
