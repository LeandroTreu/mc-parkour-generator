
### Settings Documentation
name|values|description
-|-|-
allowedStructureTypes|SingleBlock, TwoBlock, FourBlock| Sets which JumpTypes are allowed.
blockType|e.g. minecraft:stone|Sets the default Minecraft block type for all parkour structures.
checkpointsEnabled|true/false|If true then a checkpoint structure will be placed periodically with the defined checkpointsPeriod below.
checkpointsPeriod|int|After this many normal jumptypes, one checkpoint is placed. If not possible the checkpoint is placed as soon as possible later in the parkour.
curvesSize|float|Values: [0.1, 1.0], Changes the size of the curves: 0.1 - small, 1.0 - big
difficulty|easy, medium, hard|Choose parkour difficulty.
enforceParkourVolume|true/false|If true then the parkour will generate only inside the above defined Parkour Volume. If false it will generate to arbitrary coordinates.
fillParkourVolumeWithAir|true/false|Fills the parkour volume with Minecraft air blocks before placing the parkour. Only works when enforceParkourVolume is set to true.
maxParkourLength|int|Maximum length of the parkour including the Checkpoint and Finish structures.
mcVersion|1.21, 1.18 - 1.20.6, 1.13 - 1.17.1|Minecraft version used for compatibility of the datapack and world build height.
pace|slow, medium, fast|Choose how fast/fluent the parkour is to traverse.
parkourAscending|true/false|If true then JumpTypes which are ascending (relative y-level > 0) will be used.
parkourDescending|true/false|If true then JumpTypes which are descending (relative y-level < 0) will be used.
parkourType|Straight, Curves, Spiral, Random|Straight: Parkour only goes in the direction set by startForwardDirection. Curves: parkour goes left and right randomly. Spiral: parkour spiral with rotation and type set below. Random: completely random direction changes.
parkourVolume|[[int, int], [int, int], [int, int]]|Absolute X, Y, Z coordinate ranges in the Minecraft world.
plotColorScheme|winter, viridis, plasma, gray, hot, summer, hsv, copper|Color schemes for the parkour image.
plotCommandBlocks|true/false|If false then command blocks of the parkour will not be drawn on the image. Command blocks are used for the checkpoints.
plotFileType|jpg, png|Sets the file type of the parkour image.
randomSeed|true/false|Set true for a randomised seed. Set false for a fixed seed, defined below.
seed|int|Sets a seed for the random number generator used by the parkour generation. Only works when randomSeed is set to false.
spiralRotation|clockwise, counterclockwise|
spiralTurnProbability|float|Probability of changing direction for spiralType "Random".
spiralTurnRate|int|After how many jumps the Spiral will change direction. Only works with spiralType "Even".
spiralType|Random, Even|Even: spiral changes direction after "spiralTurnRate" many jumps. Random: spiral changes direction with probability set by spiralTurnProbability.
startForwardDirection|Xpos, Xneg, Zpos, Zneg|Sets the initial forward direction of the parkour for the first jump.
startPosition|[int, int, int]|Absolute X, Y, Z coordinates in the Minecraft world. Must be within the parkourVolume defined above if enforceParkourVolume is set to true. The Startblock structure is 3x3 blocks so make sure it is inside the volume when near the boundary.
useAllBlocks|true/false|Set to true to use all JumpTypes for generation, which will ignore allowedStructureTypes, difficulty, pace, parkourAscending below.
writeDatapackFiles|true/false|Set to true to write the Minecraft datapack files as soon as the parkour is generated (overwrites with the new parkour every time). Set to false to not write the files.