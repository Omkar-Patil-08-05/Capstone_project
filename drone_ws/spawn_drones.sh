#!/bin/bash

OFFSET=-12

spawn() {
  NAME=$1
  X=$2
  Y=$3

  gz service -s /world/default/create \
  --reqtype gz.msgs.EntityFactory \
  --reptype gz.msgs.Boolean \
  --timeout 3000 \
  --req "name: '$NAME', sdf_filename: 'model://simple_drone', pose: {position: {x: $X, y: $Y, z: 2}}" \
  > /dev/null 2>&1
}

spawn drone1 $((2+OFFSET)) $((2+OFFSET))
spawn drone2 $((12+OFFSET)) $((2+OFFSET))
spawn drone3 $((22+OFFSET)) $((2+OFFSET))
spawn drone4 $((2+OFFSET)) $((12+OFFSET))
spawn drone5 $((12+OFFSET)) $((12+OFFSET))
spawn drone6 $((22+OFFSET)) $((12+OFFSET))