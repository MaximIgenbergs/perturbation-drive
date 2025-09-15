from perturbationdrive import PerturbationDrive,CustomRoadGenerator
from examples.udacity.udacity_simulator import UdacitySimulator
from examples.models.dave2_agent import Dave2Agent
import traceback
from datetime import datetime
import random


road_angles_list=[]
road_segments_list=[]
road_types_list=[]

def generate_simple_roads(angles_number=8):
    road_angles_list=[]
    road_segments_list=[]
    road_types_list=[]
    for i in range(10,0,-1):
        road_angles = [5 * i] * angles_number
        road_segments = [10] * angles_number
        road_angles_list.append(road_angles)
        road_segments_list.append(road_segments)
        road_types_list.append("simple")
        if i!=0:
            road_angles = [-5 * i] * angles_number
            road_segments = [10] * angles_number
            road_angles_list.append(road_angles)
            road_segments_list.append(road_segments)
            road_types_list.append("simple")
    return road_angles_list,road_segments_list,road_types_list

def generate_s_roads(angles_number=20):
    road_angles_list=[]
    road_segments_list=[]
    road_types_list=[]
    for i in range(10,0,-1):
        road_angles = [5 * i, -5 * i] * (angles_number // 2)
        road_segments = [20] * angles_number
        road_angles_list.append(road_angles)
        road_segments_list.append(road_segments)
        road_types_list.append("swiggly")
        if i!=0:
            road_angles = [-5 * i, 5 * i] * (angles_number // 2)
            road_segments = [20] * angles_number
            road_angles_list.append(road_angles)
            road_segments_list.append(road_segments)
            road_types_list.append("swiggly")
    return road_angles_list,road_segments_list,road_types_list

def generate_random_roads(angles_number=10):
    road_angles_list = []
    road_segments_list = []
    road_types_list=[]
    for i in range(10, 1, -1):
        road_angles = [random.randint(-2 * i, 2 * i) for _ in range(angles_number)]
        road_segments = [random.randint(20, 30) for _ in range(angles_number)]
        road_angles_list.append(road_angles)
        road_segments_list.append(road_segments)
        road_types_list.append("random")
        if i != 0:
            road_angles = [random.randint(-5 * i, 5 * i) for _ in range(angles_number)]
            road_segments = [random.randint(20, 30) for _ in range(angles_number)]
            road_angles_list.append(road_angles)
            road_segments_list.append(road_segments)
            road_types_list.append("random")
    return road_angles_list, road_segments_list, road_types_list



road_angles_list,road_segments_list,road_types_list=generate_random_roads()
road_angles_list2,road_segments_list2,road_types_list2=generate_simple_roads()
road_angles_list3,road_segments_list3,road_types_list3=generate_s_roads()


road_angles_list.extend(road_angles_list2)
road_segments_list.extend(road_segments_list2)
road_types_list.extend(road_types_list2)

try:
    
    for i in range(len(road_angles_list)):
            simulator = UdacitySimulator(
                simulator_exe_path="./examples/udacity/sim/udacity/udacity_sim_weather_sky_ready_angles_fortuna.app",
                host="127.0.0.1",
                port=9091
            )    
            road_generator = CustomRoadGenerator(num_control_nodes=len(road_angles_list[i]))

            benchmarking_obj = PerturbationDrive(simulator, None)
            print(f"{5 * '#'} Testing road {i} {5 * '#'}")
            time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            perturbation_names =["gaussian_noise","poisson_noise","impulse_noise","defocus_blur","glass_blur","motion_blur",
            "zoom_blur","increase_brightness","contrast","elastic","pixelate","jpeg_filter","shear_image",
            "translate_image", "scale_image", "rotate_image", "fog_mapping", "splatter_mapping",
            "dotted_lines_mapping", "zigzag_mapping","canny_edges_mapping","speckle_noise_filter","false_color_filter","high_pass_filter","low_pass_filter","phase_scrambling",
            "histogram_equalisation", "reflection_filter", "white_balance_filter", "sharpen_filter",
            "grayscale_filter", "posterize_filter", "cutout_filter", "sample_pairing_filter", "gaussian_blur",
            "saturation_filter","static_rain_filter","static_object_overlay","static_sun_filter","static_lightning_filter","static_smoke_filter"]

            benchmarking_obj.grid_seach(
                perturbation_functions=perturbation_names,
                attention_map={},
                road_generator=road_generator,
                road_angles=road_angles_list[i],
                road_segments=road_segments_list[i],
                log_dir=f"./output_logs/train_nominal/udacity_road_{road_types_list[i]}_{i}_logs_{time}.json",
                overwrite_logs=True,
                image_size=(240, 320),
                test_model=False,
                perturb=True
            )
            print(f"{5 * '#'} Finished Testing road {i} {5 * '#'}")
except Exception as e:
    print(
        f"{5 * '#'} Udacity Error: Exception type: {type(e).__name__}, \nError message: {e}\nTract {traceback.print_exc()} {5 * '#'} "
    )