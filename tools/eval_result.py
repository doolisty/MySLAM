import os
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--rerun', help='', action='store_true')
parser.add_argument('--gdb', help='', action='store_true')
args = parser.parse_args()

pi, dt, a, b, bs, ss = 0.6, 0.4, 0.2, 23.0, -1, 10
dataset = "fr3_w_xyz"
repeat = 1

for i in range(repeat):
    if args.rerun:
        cmd = ""
        if args.gdb:
            cmd += "gdb -args "
        cmd += f"./rgbd_tum /root/catkin_ws/src/MySLAM/Vocabulary/ORBvoc.txt /root/catkin_ws/src/MySLAM/Examples/RGB-D/TUM1.yaml /root/Dataset/{dataset} /root/Dataset/{dataset}/associate.txt"
        cmd += f" {pi} {dt} {a} {b} {bs} {ss}"

        os.chdir(os.getcwd() + "/Examples/RGB-D") # cd Examples/RGB-D
        start = time.time()
        os.system(cmd)
        print(f"time elapsed: {time.time() - start}")
        os.chdir("/".join(os.getcwd().split("/")[:-2])) # cd ../../

    gt_path, cur_res_path = f"/root/Dataset/{dataset}/groundtruth.txt", "/root/catkin_ws/src/MySLAM/Examples/RGB-D/CameraTrajectory.txt"

    print("\n" + "=" * 20 + " ATE " + "=" * 20)
    os.system(f"python3 tools/evaluate_ate.py {gt_path} {cur_res_path} --verbose")
    print("\n" + "=" * 20 + " RPE " + "=" * 20)
    os.system(f"python3 tools/evaluate_rpe.py {gt_path} {cur_res_path} --verbose")


