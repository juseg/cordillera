#!/bin/bash

avconv -i frames/%04d.png -b 1M animation.mp4 -y
avconv -i frames/%04d.png -b 1M animation.ogg -y
zip animations.zip animation.{mp4,ogg}
