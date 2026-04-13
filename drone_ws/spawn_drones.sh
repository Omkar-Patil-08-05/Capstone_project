#!/bin/bash

spawn() {
  NAME=$1
  X=$2

  gz service -s /world/default/create \
  --reqtype gz.msgs.EntityFactory \
  --reptype gz.msgs.Boolean \
  --timeout 300 \
  --req "sdf: '<sdf version=\"1.7\"><model name=\"$NAME\"><static>true</static><pose>$X 0 1 0 0 0</pose><link name=\"base_link\"><inertial><mass>1.0</mass></inertial><collision name=\"collision\"><geometry><box><size>1 1 1</size></box></geometry></collision><visual name=\"visual\"><geometry><box><size>1 1 1</size></box></geometry></visual></link></model></sdf>'"
}

spawn drone1 0
spawn drone2 2
spawn drone3 4
spawn drone4 6
spawn drone5 8
spawn drone6 10