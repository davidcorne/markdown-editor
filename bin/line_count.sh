#!/bin/sh
# Written by: DGC

# should be run from project directory i.e markdown-editor

#==============================================================================
pycount() {
  # removes all space lines and comments
  cat $* | grep -v '^ *$' | grep -v '^ *#' | wc -l
}

echo "Production Code lines : $(pycount *.py)"
echo "Unit test lines       : $(pycount utest/*.py)"
echo "Integration test lines: $(pycount Integration/*.py)"
