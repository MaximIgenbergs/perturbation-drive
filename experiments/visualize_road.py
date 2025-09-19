from perturbationdrive import CustomRoadGenerator
from perturbationdrive.RoadGenerator.Roads.road_visualizer import visualize_road

road_angles = [
0, # straight
0, # long straight to build speed
-35, # hard right
35, # chicane left
-35, # snap back right
20, # start left sweeper
30, # tighten more
35 # decreasing-radius left to the limit
]

road_segments = [45, 35, 15, 16, 14, 22, 18, 22]

road_gen = CustomRoadGenerator()
_ = road_gen.generate(starting_pos=(0, 0, 0, 4), angles=road_angles, seg_length=road_segments)
road = road_gen.previous_road

visualize_road(road, "Example Road")
