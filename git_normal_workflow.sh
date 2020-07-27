#!/bin/bash
echo "Starting the workflow"
echo ""
echo ""
echo ""
echo "# last run on `date`" | cat - covid-19-data-retriever.py > temp && mv temp covid-19-data-retriever.p
python -v covid-19-data-retriever.py
echo ""
echo ""
echo ""
git add .
git commit -m "Daily updated: `date +'%Y-%m-%d %H:%M:%S'`"
git push origin master
echo ""
echo ""
echo ""

echo ""
echo ""
echo ""
echo "**Workflow done**"
