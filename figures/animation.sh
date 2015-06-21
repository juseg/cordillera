#!/bin/bash

for rec in grip epica
do
    avconv -i frames/$rec-%04d.png -b 1M animation-$rec.mp4
done