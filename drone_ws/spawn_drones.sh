#!/bin/bash

OFFSET=-12

spawn() {
  NAME=$1
  X=$2
  Y=$3

  gz service -s /world/default/create \
  --reqtype gz.msgs.EntityFactory \
  --reptype gz.msgs.Boolean \
  --timeout 300 \
  --req "sdf: '<sdf version=\"1.7\"><model name=\"$NAME\"><static>true</static><pose>$X $Y 2 0 0 0</pose><link name=\"base_link\"><inertial><mass>1.0</mass></inertial><visual name=\"body\"><geometry><cylinder><radius>0.2</radius><length>0.08</length></cylinder></geometry><material><diffuse>0.2 0.2 0.8 1</diffuse></material></visual><visual name=\"arm1\"><pose>0.4 0 0 0 0 0</pose><geometry><box><size>0.8 0.05 0.02</size></box></geometry><material><diffuse>0.8 0.2 0.2 1</diffuse></material></visual><visual name=\"arm2\"><pose>0 0.4 0 0 0 0</pose><geometry><box><size>0.05 0.8 0.02</size></box></geometry><material><diffuse>0.2 0.8 0.2 1</diffuse></material></visual></link></model></sdf>'"
}

# 2D GRID (WITH OFFSET)
spawn drone1 $((2+OFFSET)) $((2+OFFSET))
spawn drone2 $((12+OFFSET)) $((2+OFFSET))
spawn drone3 $((22+OFFSET)) $((2+OFFSET))
spawn drone4 $((2+OFFSET)) $((12+OFFSET))
spawn drone5 $((12+OFFSET)) $((12+OFFSET))
spawn drone6 $((22+OFFSET)) $((12+OFFSET))