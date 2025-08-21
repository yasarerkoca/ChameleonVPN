#!/bin/bash

# Generates a disk usage report and emails it.
#
# Usage:
#   DISK_REPORT_EMAIL="admin@example.com" ./disk_health.sh
# If DISK_REPORT_EMAIL is unset, a report will be sent to admin@example.com.

REPORT_EMAIL="${DISK_REPORT_EMAIL:-admin@example.com}"
df -h > /tmp/disk_report.txt
mail -s "ChameleonVPN Disk Raporu" "$REPORT_EMAIL" < /tmp/disk_report.txt
