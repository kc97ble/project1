#!/bin/bash
export FLASK_APP='project1'
export FLASK_DEBUG=1

echo flask $@
python -m flask $@
