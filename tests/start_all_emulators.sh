#!/bin/bash

###############################################################################
# Since Flask does not support multiple parallel apps, it needs to be done
# at OS/script level
###############################################################################

python "./fixtures/start_single_emulator.py" --port 5000 --device_id "adora_slq_active" & 
python "./fixtures/start_single_emulator.py" --port 5001 --device_id "adora_tslq_wp" & 
