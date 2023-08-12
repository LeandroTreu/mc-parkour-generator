import config
from classes import JumpType
from classes import Block
from typing import List
from config import BlockType

StartBlock = JumpType(name="Parkour Start Structure", structure_type="Start", 
                      rel_start_block=Block(BlockType, (0, 0, 0)), 
                      rel_finish_block=Block(BlockType, (1, 0, 0)),
                      blocks=[Block(BlockType, (0, 0, -1)), Block(BlockType, (0, 0, 1)), 
                              Block(BlockType, (1, 0, -1)), Block(BlockType, (1, 0, 1)), 
                              Block(BlockType, (-1, 0, 1)), Block(BlockType, (-1, 0, -1)), 
                              Block(BlockType, (-1, 0, 0))],
                      difficulty=0.0, 
                      flow=1.0)
FinishBlock = JumpType(name="Parkour Finish Structure", structure_type="Finish", 
                      rel_start_block=Block(BlockType, (0, 0, 0)), 
                      rel_finish_block=Block(BlockType, (1, 0, 0)),
                      blocks=[Block(BlockType, (0, 0, -1)), Block(BlockType, (0, 0, 1)), 
                              Block(BlockType, (1, 0, -1)), Block(BlockType, (1, 0, 1)), 
                              Block(BlockType, (-1, 0, 1)), Block(BlockType, (-1, 0, -1)), 
                              Block(BlockType, (-1, 0, 0))],
                      difficulty=0.0, 
                      flow=1.0)
CheckpointBlock = JumpType(name="Parkour Checkpoint Structure", structure_type="Checkpoint", 
                      rel_start_block=Block(BlockType, (2, 0, 0)), 
                      rel_finish_block=Block(BlockType, (2, 0, 0)),
                      blocks=[Block(BlockType, (0, 0, -1)), Block(BlockType, (0, 0, 1)), 
                              Block(BlockType, (1, 0, 0)), Block(BlockType, (1, 0, -1)), Block(BlockType, (1, 0, 1)), 
                              Block(BlockType, (2, 0, 1)), Block(BlockType, (2, 0, -1)), 
                              ],
                      difficulty=0.0, 
                      flow=1.0)

list_of_jumptypes: List[JumpType] = []

# SingleBlock Structures
list_of_jumptypes.append(JumpType(name="1 block gap straight", structure_type="SingleBlock", 
                                  rel_start_block=Block("minecraft:bedrock", (2, 0, 0)), 
                                  rel_finish_block=Block("minecraft:bedrock", (0, 0, 0)),  # Defined relative to the rel_start_block
                                  blocks=[], 
                                  difficulty=0.1, flow=0.2))

list_of_jumptypes.append(JumpType(name="2 blocks gap straight", structure_type="SingleBlock", 
                                  rel_start_block=Block("minecraft:bedrock", (3, 0, 0)), 
                                  rel_finish_block=Block("minecraft:bedrock", (0, 0, 0)), 
                                  blocks=[], 
                                  difficulty=0.1, flow=0.7))

list_of_jumptypes.append(JumpType(name="3 blocks gap straight", structure_type="SingleBlock", 
                                  rel_start_block=Block("minecraft:bedrock", (4, 0, 0)), 
                                  rel_finish_block=Block("minecraft:bedrock", (0, 0, 0)), 
                                  blocks=[], 
                                  difficulty=0.1, flow=1.0))

list_of_jumptypes.append(JumpType(name="4 blocks gap straight", structure_type="SingleBlock", 
                                  rel_start_block=Block("minecraft:bedrock", (5, 0, 0)), 
                                  rel_finish_block=Block("minecraft:bedrock", (0, 0, 0)), 
                                  blocks=[], 
                                  difficulty=0.8, flow=1.0))

list_of_jumptypes.append(JumpType(name="2 blocks gap displaced left", structure_type="SingleBlock", 
                                  rel_start_block=Block("minecraft:bedrock", (3, 0, -1)), 
                                  rel_finish_block=Block("minecraft:bedrock", (0, 0, 0)), 
                                  blocks=[], 
                                  difficulty=0.3, flow=0.8))

list_of_jumptypes.append(JumpType(name="2 blocks gap displaced right", structure_type="SingleBlock", 
                                  rel_start_block=Block("minecraft:bedrock", (3, 0, 1)), 
                                  rel_finish_block=Block("minecraft:bedrock", (0, 0, 0)), 
                                  blocks=[], 
                                  difficulty=0.3, flow=0.8))

list_of_jumptypes.append(JumpType(name="2 blocks gap diagonal left", structure_type="SingleBlock",  #       +
                                  rel_start_block=Block("minecraft:bedrock", (3, 0, -2)),           #
                                  rel_finish_block=Block("minecraft:bedrock", (0, 0, 0)),           #  +
                                  blocks=[],                                                        #
                                  difficulty=0.6, flow=0.8))                                        #

list_of_jumptypes.append(JumpType(name="2 blocks gap diagonal right", structure_type="SingleBlock",  #
                                  rel_start_block=Block("minecraft:bedrock", (3, 0, 2)),             #
                                  rel_finish_block=Block("minecraft:bedrock", (0, 0, 0)),            #  +
                                  blocks=[],                                                         #
                                  difficulty=0.6, flow=0.8))                                         #       +