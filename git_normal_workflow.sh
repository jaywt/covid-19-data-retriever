#!/bin/bash
echo "Starting the workflow"
echo ""
git add .
git commit -m "Daily updated: `date +'%Y-%m-%d %H:%M:%S'`"
git push origin master
echo "**Workflow done**"
