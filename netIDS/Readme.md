# Network IDS first version

Network IDS first version

Current version is has support for the CAN protocol

## Requirements

## Testing 

# Linux

1) sudo modprobe can
2) sudo modprobe vcan
3) sudo ip link add dev vcan0 type vcan
4) sudo ip link set up vcan0
5) sudo python3.5 TimeIntervalsIDS.py 10 vcan0 true


