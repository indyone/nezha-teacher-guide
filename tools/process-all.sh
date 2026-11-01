#!/bin/sh
# Επαναδημιουργία όλων των φωτογραφιών από ../photos_raw (εκτός repo).
# Χρήση: sh tools/process-all.sh [raw-dir]
set -e
R=${1:-../photos_raw}; O=assets/img; P="python3 tools/process-photos.py"
I=$R/IMG_20261031_
$P "$R/2026-11-01 09.27.43.jpg" $O/usb.jpg --kind component
$P "$R/2026-11-01 09.27.47.jpg" $O/kit-box.jpg --kind wide
$P "$R/2026-11-01 09.27.50.jpg" $O/kit-parts.jpg --kind wide
$P ${I}205233652_HDR.jpg $O/nezha-board-ports.jpg --kind board --box 0.171,0.270,0.809,0.558
$P ${I}205255174_HDR.jpg $O/microbit-back.jpg
$P ${I}205308824_HDR.jpg $O/microbit.jpg
$P ${I}205355823_HDR.jpg $O/led.jpg --rotate 90
$P ${I}205355823_HDR.jpg $O/led-green.jpg --rotate 90 --region 0,0.15,1,0.39
$P ${I}205355823_HDR.jpg $O/led-yellow.jpg --rotate 90 --region 0,0.39,1,0.63
$P ${I}205355823_HDR.jpg $O/led-red.jpg --rotate 90 --region 0,0.64,1,0.88
$P ${I}205411559_HDR.jpg $O/line.jpg --rotate 90
$P ${I}205427765_HDR.jpg $O/crash.jpg --rotate 90
$P ${I}205436936_HDR.jpg $O/trimpot.jpg
$P ${I}205504079_HDR.jpg $O/soil.jpg --rotate 90
$P ${I}205514134_HDR.jpg $O/sonar.jpg
$P ${I}205557964_HDR.jpg $O/motor.jpg
$P ${I}205609342_HDR.jpg $O/servo.jpg
$P ${I}205635156_HDR.jpg $O/rj11.jpg
