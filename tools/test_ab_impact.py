import os
from collections import defaultdict

datasets = ["fr2_desk", "fr3_s_halfsphere", "fr3_s_rpy", "fr3_s_xyz", "fr3_s_static", "fr3_w_halfsphere", "fr3_w_rpy", "fr3_w_static", "fr3_w_xyz"]
params = {
    "people_init_score": 0.8,
    "dynamic_thresh": 0.3,
    "alpha": 0.05,
    "beta": 300.0,
    "block_size": -1,
    "search_size": 0
}
alpha_set = [1.0, 0.8, 0.6, 0.4, 0.2, 0.1, 0.05, 0.02, 0.005, 0.001]
beta_set = [5, 10, 20, 40, 80, 120, 200, 300, 500, 1000]
ab_set = [alpha_set, beta_set]
repeat = 10
proj_home = "MySLAM_beta"

for dataset in datasets:
    result_log = ""
    for i in range(2):
        for param in ab_set[i]:
            pi, dt, a, b, bs, ss = params["people_init_score"], params["dynamic_thresh"], params["alpha"], params["beta"], params["block_size"], params["search_size"]
            if i == 0:
                a = param
            else:
                b = param
            cmd = f"./rgbd_tum /root/catkin_ws/src/MySLAM/Vocabulary/ORBvoc.txt /root/catkin_ws/src/MySLAM/Examples/RGB-D/TUM1.yaml /root/Dataset/{dataset} /root/Dataset/{dataset}/associate.txt"
            cmd += f" {pi} {dt} {a} {b} {bs} {ss}"

            result_dict = defaultdict(float)
            for _ in range(repeat):
                os.chdir(f"/root/catkin_ws/src/{proj_home}/Examples/RGB-D") # cd Examples/RGB-D
                os.system(cmd)
                os.chdir(f"/root/catkin_ws/src/{proj_home}")

                gt_path, cur_res_path = f"/root/Dataset/{dataset}/groundtruth.txt", f"/root/catkin_ws/src/{proj_home}/Examples/RGB-D/CameraTrajectory.txt"

                # eval ATE
                os.system(f"python3 tools/evaluate_ate.py {gt_path} {cur_res_path} --verbose > tools/tmp_res_log")
                with open("tools/tmp_res_log", "r") as f:
                    lines = f.readlines()
                for line in lines:
                    lst = line.split()
                    if lst[0] == "compared_pose_pairs":
                        result_dict["ate_pairs"] += float(lst[1])
                    elif lst[0] == "absolute_translational_error.rmse":
                        result_dict["ate_rmse"] += float(lst[1])
                    elif lst[0] == "absolute_translational_error.mean":
                        result_dict["ate_mean"] += float(lst[1])
                    elif lst[0] == "absolute_translational_error.median":
                        result_dict["ate_median"] += float(lst[1])
                    elif lst[0] == "absolute_translational_error.std":
                        result_dict["ate_std"] += float(lst[1])
                    elif lst[0] == "absolute_translational_error.min":
                        result_dict["ate_min"] += float(lst[1])
                    elif lst[0] == "absolute_translational_error.max":
                        result_dict["ate_max"] += float(lst[1])

                # eval RPE
                os.system(f"python3 tools/evaluate_rpe.py {gt_path} {cur_res_path} --verbose > tools/tmp_res_log")
                with open("tools/tmp_res_log", "r") as f:
                    lines = f.readlines()
                for line in lines:
                    lst = line.split()
                    if lst[0] == "compared_pose_pairs":
                        result_dict["rpe_pairs"] += float(lst[1])
                    # translational
                    elif lst[0] == "translational_error.rmse":
                        result_dict["rpe_trans_rmse"] += float(lst[1])
                    elif lst[0] == "translational_error.mean":
                        result_dict["rpe_trans_mean"] += float(lst[1])
                    elif lst[0] == "translational_error.median":
                        result_dict["rpe_trans_median"] += float(lst[1])
                    elif lst[0] == "translational_error.std":
                        result_dict["rpe_trans_std"] += float(lst[1])
                    elif lst[0] == "translational_error.min":
                        result_dict["rpe_trans_min"] += float(lst[1])
                    elif lst[0] == "translational_error.max":
                        result_dict["rpe_trans_max"] += float(lst[1])
                    # rotational
                    elif lst[0] == "rotational_error.rmse":
                        result_dict["rpe_rot_rmse"] += float(lst[1])
                    elif lst[0] == "rotational_error.mean":
                        result_dict["rpe_rot_mean"] += float(lst[1])
                    elif lst[0] == "rotational_error.median":
                        result_dict["rpe_rot_median"] += float(lst[1])
                    elif lst[0] == "rotational_error.std":
                        result_dict["rpe_rot_std"] += float(lst[1])
                    elif lst[0] == "rotational_error.min":
                        result_dict["rpe_rot_min"] += float(lst[1])
                    elif lst[0] == "rotational_error.max":
                        result_dict["rpe_rot_max"] += float(lst[1])

            for key in result_dict.keys():
                if key in ["ate_pairs", "rpe_pairs"]:
                    result_dict[key] //= repeat
                else:
                    result_dict[key] /= repeat

            result_log += f"alpha = {a}, beta = {b}:\n"
            result_log += str(result_dict) + "\n\n"

    with open(f"/root/catkin_ws/src/{proj_home}/test_ab_impact_log/ab_impact_{dataset}", "w") as f:
        f.write(result_log)
