#!/bin/bash
#a simplified version of docker's generate-authors script
git log --format='%aN <%aE>' | LC_ALL=C.UTF-8 sort -uf > AUTHORS
