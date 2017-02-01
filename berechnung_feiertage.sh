#!/bin/bash

function getFeiertage() {
  # Feste Feiertage werden nach dem Schema dd.mm. eingetragen
  local Feiertage="01.01. 01.05. 03.10. 25.12. 26.12."
  # 01.01. Neujahrstag
  # 01.05. Tag der Arbeit
  # 03.10. Tag der Deutschen Einheit
  # 25.12. 1.Weihnachtstag
  # 26.12. 2.Weihnachtstag
	
  # Bewegliche Feiertage (anhand Ostersonntag) berechnen
  local J=$(date +%Y)
  local a=$(( $J % 19 ))
  local b=$(( $J % 4 ))
  local c=$(( $J % 7 ))
  local m=$((( (8 * ($J / 100) + 13) / 25) - 2 ))
  local s=$(( ($J / 100) - ($J / 400) - 2 ))
  local M=$(( (15 + $s - $m) % 30 ))
  local N=$(( (6 + $s) % 7 ))
  local d=$(( ($M + 19 * $a) % 30 ))
  if [ $d = 29 ]; then
    local D=28
  elif [ $d = 28 -a $a -ge 11 ]; then
    local D=27
  else
    local D=$d
  fi
  local e=$(( (2 * $b + 4 * $c + 6 * $D + $N) % 7 ))
  local o=$( date -d ${J}-03-21+$(($D + $e + 1))days +%Y-%m-%d )
  for t in "-2 Karfreitag" "+1 Ostermontag" "+39 Christi Himmelfahrt" "+50 Pfingstmontag" "+60 Fronleichnam"; do
    local Feiertage+=" $( date -d ${o}${t%% *}days "+%d.%m." )"
  done

  echo ${Feiertage}
}

echo
d=$(date +%Y_%m_%d__%H.%M)
wt=$(date +%u)
week=$(date +%V | sed "s|^0||g")
tag=$(date +%d.%m.)
#
#
# Ermittlung, ob heute ein Feiertag ist 

#echo $tag
ft=0
for fDay in $(getFeiertage); do
	[ "$tag" = "$fDay" ] && ft=1 && break
done
#echo $ft
