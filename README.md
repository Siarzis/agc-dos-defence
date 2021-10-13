# Load frequency control in RTDS

This project implements the secondary control of a power grid simulated in RTDS.
Python module communicates with RTDS via TCP sockets. 

## Motivation

In power grids, frequency is an indicator of the balance between load and demand. Any frequency deviation from its nominal (normally 50 or 60 Hz) means that there is an imbalance between generation and consumption. This deviation causes heavy damage to the power grid, if it is not regulated in time. For this reason, power systems are equipped with the following controls:

- **Primary control**: it is the standard control mechanism to stabilize frequency. It is performed locally on the generators via their governors. Its purpose is to stabilize frequency but inevitably, it leaves a steady state frequency error. To eliminate this, a secondary frequency control is executed.
- **Secondary control**: as stated before, secondary control is to eliminate the steady state error of frequency. This control is slower than the primary (operates every 2-4 s) and is usually performed remotely, withing a control center. It receives telemetries and sends remote commands.
