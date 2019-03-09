#!/usr/bin/env bash

for file in data/samples/*.wav
do
	python split.py --silence-threshold 0.01 --output-dir data/samples/fragments/ $file 
done
