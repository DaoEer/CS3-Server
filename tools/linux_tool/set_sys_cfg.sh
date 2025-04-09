#!/bin/bash


ulimit -c unlimited
echo "core_%e_%t_%p" > /proc/sys/kernel/core_pattern
ulimit -n 32768


