#!/bin/bash
source /root/agent_system/.env
cd /root/agent_system/

# 1. Κεντρικός Hunter (Bountycaster & Keywords)
/usr/bin/python3 /root/agent_system/hunter.py >> /root/agent_system/hunter.log 2>&1

# 2. Νέες Αγορές (Algora & Gitcoin)
/usr/bin/python3 /root/agent_system/markets_extension.py >> /root/agent_system/markets.log 2>&1

# 3. Monitor για GitHub σχόλια & Διορθώσεις
/usr/bin/python3 /root/agent_system/automation_patch.py >> /root/agent_system/monitor.log 2>&1
/usr/bin/python3 /root/agent_system/error_reporter.py
