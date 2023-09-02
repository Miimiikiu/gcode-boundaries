# G-Code Boundaries

## Description

This script finds the WCS boundaries along X and Y, which may be needed to know where to put workpiece clamps to prevent collisions. The result factors in the radius of the tool & collet nut.

## Usage

1. Edit the top 5 variables according to your requirements. Units are arbitrary as long as you're consistent between these values and your G Code.
2. The result that you'll see is the X&Y max/min values of your G Code, and adds the extra radius of your tool/collet nut. Otherwise, you may think that anything past your tool center's boundaries is safe, which is extremely dangerous if your clamps are too close.
3. It should be safe to place the clamps anywhere past the listed boundaries, but as always, inspect your G Code carefully to ensure that no mistakes were made anywhere.

## Known Issues

-Does not fully account for G2/G3 movements
