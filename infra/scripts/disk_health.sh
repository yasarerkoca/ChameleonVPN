#!/bin/bash
df -h > /tmp/disk_report.txt
mail -s "ChameleonVPN Disk Raporu" yasarerkoca@gmail.com < /tmp/disk_report.txt
