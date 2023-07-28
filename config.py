from classes import Block, JumpType

ParkourVolume = (100, 100, 100)
EnforceParkourVolume = False
FillParkourVolumeWithAirFirst = False
MaxParkourLength = 20
Difficulty = 1.0
Flow = 0.0
ParkourType = "UpwardSpiral"
BlockType = "minecraft:bedrock"

StartPosition = (0, 0, 0)
StartForwardDirection = "Xpos"

StartBlock = JumpType(name="Parkour Start Structure", structure_type="Start", 
                      rel_start_block=Block("minecraft:bedrock", (0, 0, 0)), 
                      rel_finish_block=Block("minecraft:bedrock", (1, 0, 0)),
                      blocks=[Block(BlockType, (0, 0, -1)), Block(BlockType, (1, 0, -1))],
                      difficulty=0.0, 
                      flow=1.0)
FinishBlock = JumpType(name="Parkour Finish Structure", structure_type="Finish", 
                      rel_start_block=Block("minecraft:bedrock", (0, 0, 0)), 
                      rel_finish_block=Block("minecraft:bedrock", (1, 0, 0)),
                      blocks=[Block(BlockType, (0, 0, -1)), Block(BlockType, (1, 0, -1))],
                      difficulty=0.0, 
                      flow=1.0)


Stages = 1