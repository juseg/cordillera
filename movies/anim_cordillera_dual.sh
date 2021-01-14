#!/bin/bash
# Copyright (c) 2021, Julien Seguinot (juseg.github.io)
# Creative Commons Attribution-ShareAlike 4.0 International License
# (CC BY-SA 4.0, http://creativecommons.org/licenses/by-sa/4.0/)

# parse command-line arguments
# mode="${2:-gs}"  # gs
# lang="${4:-en}"  # en

# filenames prefix
prefix="anim_cordillera_dual"

# assembling parametres (depends on frame rate)
imgs="??????.png"  # images to include, edit for quick tests
fade=12   # number of frames for fade in and fade out effects
hold=25  # number of frames to hold in the beginning and end
secs=$((120+2*hold/25))  # duration of main scene in seconds

# prepare filtergraph for main scene
filt="nullsrc=s=3840x2160:d=$secs[n]"  # create fixed duration stream
filt+=";[0]loop=$hold:1:0,[n]overlay"   # hold first frame, delay end
filt+=",minterpolate=25:blend"          # belnd consecutive frames

# add title frame and bumpers
filt+=",fade=in:0:$fade,fade=out:$((secs*25-fade)):$fade[main];"  # main scene
filt+="[1]fade=in:0:$fade,fade=out:$((4*25-fade)):$fade[head];"  # title frame
filt+="[2]fade=in:0:$fade,fade=out:$((3*25-fade)):$fade[refs];"  # references
filt+="[3]fade=in:0:$fade,fade=out:$((3*25-fade)):$fade[disc];"  # disclaimer
filt+="[4]fade=in:0:$fade,fade=out:$((3*25-fade)):$fade[bysa];"  # license
filt+="[head][main][refs][disc][bysa]concat=5" \

# assemble video
ffmpeg \
    -pattern_type glob -r 10 -i "$HOME/anim/${prefix}/$imgs" \
    -loop 1 -t 4 -i ${prefix}_head.png \
    -loop 1 -t 3 -i ${prefix}_refs.png \
    -loop 1 -t 3 -i ${prefix}_disc.png \
    -loop 1 -t 3 -i ${prefix}_bysa.png \
    -filter_complex $filt -pix_fmt yuv420p -c:v libx264 \
    $HOME/anim/${prefix}.mp4

# accelerate for social media
ffmpeg \
    -i $HOME/anim/${prefix}.mp4 \
    -s 1920x1080 -vf "trim=5:125,setpts=PTS/30" \
    $HOME/anim/${prefix}_x30.mp4
