#!/bin/bash
echo "Starting the workflow"
echo ""
echo ""
echo ""
echo "# last run on `date`" | cat - covid-19-data-retriever.py > temp && mv temp covid-19-data-retriever.py
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
cd /Users/twen08/Documents/GitHub/jaywt.github.io
pwd
/Users/twen08/Documents/GitHub/jaywt.github.io/git_normal_workflow.sh
echo ""
echo ""
echo ""
cd /Users/twen08/Documents/GitHub/covid-19-data-retriever
pwd
echo ""
echo ""
echo ""
echo "**Workflow done**"
