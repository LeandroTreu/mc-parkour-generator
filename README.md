# Minecraft Parkour Generator
This is a parkour generator for Minecraft Java Edition (Vanilla). It is based on Minecraft function files which allow to place multiple blocks in a Minecraft world with only one in-game command.

Supported Minecraft Java Edition versions: 1.13 (TODO: test 1.12, 1.13 - 1.21)

## Usage
The app creates a datapack which you can copy and paste into your Minecraft world's datapack directory.

### Settings
name|values|description
-|-|-
parkourVolume|[[int, int], [int, int], [int, int]]|Absolute X, Y, Z coordinate ranges in the minecraft world.
enforceParkourVolume|true/false|If true then the parkour will generate only inside the above defined Parkour Volume. If false it will generate to arbitrary coordinates.
fillParkourVolumeWithAir|true/false|Only works when enforceParkourVolume is set to true.
maxParkourLength|int|Maximum length of the parkour including the Start, Checkpoint and Finish structures.
startPosition|[int, int, int]|Absolute X, Y, Z coordinates in the minecraft world. Must be within the parkourVolume defined above if enforceParkourVolume is set to true. The startblock structure is 3x3 blocks so set this to (1, 0, 1) for the start to be within the volume.
startForwardDirection|Xpos, Xneg, Zpos, Zneg|Sets the initial forward direction of the parkour for the first jump.
blockType|e.g. minecraft:stone|Sets the default minecraft block type for all parkour structures, except for special structures like ladders and ice.
randomSeed|true/false|Set true for a randomised seed. Set false for a set seed, defined below.
seed|int|Sets a seed for the random number generator used by the parkour generation.
checkpointsEnabled|true/false|If true then a checkpoint structure will be placed periodically with the defined CheckPointsPeriod below.
checkpointsPeriod|int|After this many normal jumptypes, one checkpoint is placed. If not possible the checkpoint is placed as soon as possible later in the parkour.
useAllBlocks|true/false|Set to false for the below settings to take effect. Set to true to use all JumpTypes for generation.
allowedStructureTypes||
difficulty|float|Choose parkour difficulty in range [0.0, 1.0]. 0.0 - very easy, 1.0 - very hard
flow|float|Choose how fast/flowing/fluent the parkour is to traverse in range [0.0, 1.0]. 0.0 - slow/halting, 1.0 - fast/fluent
parkourType|Spiral, Straight, Curves, Random|
parkourAscending|true/false|Set to true if the parkour should have an upwards elevation change. Set to false for the parkour to stay on the same height/y-level.
curvesSize|float|Values: [0.1, 1.0], Changes the size of the curves: 0.1 - small, 1.0 - big
spiralRotation|clockwise, counterclockwise|
spiralType|Random, Even|
spiralTurnRate|int|After how many jumps the Spiral will change direction. Only works with SpiralType = "Even"
spiralTurnProbability|float|Probability for changing direction for SpiralType = "Random"
plotFileType|jpg, png|
plotColorScheme|winter, viridis, plasma, gray, hot, summer, hsv, copper|
plotCommandBlocks|true/false|
writeDatapackFiles|true/false|Set to true to write the minecraft datapack files as soon as the parkour is generated (overwrites with the new parkour every time). Set to false to not write the files.


## Installation

## Advanced Installation and Usage
### License

## Credits
### Idea for the Checkpoint System
The idea for how to make the checkpoints and teleport system was inspired by the following YouTube video:

Author: Phibby27

Name: How To Make A Parkour Checkpoint Teleporter In Minecraft

Video: https://www.youtube.com/watch?v=Rx2kBtBlPso&list=WL&index=1
