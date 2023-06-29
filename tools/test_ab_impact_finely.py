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

repeat = 4
proj_home = "MySLAM_beta"

alpha_lst_default = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
beta_lst_default = [260, 270, 280, 290, 300, 310, 320, 330, 340, 350]
beta_lst_static = [0, 1, 2, 3, 4, 5, 10, 20, 30, 40]

ds_params_map_all = {
    "fr2_desk": {
        "alpha": alpha_lst_default,
        "beta": beta_lst_default
    },
    "fr3_s_halfsphere": {
        "alpha": alpha_lst_default,
        "beta": beta_lst_static
    },
    "fr3_s_rpy": {
        "alpha": alpha_lst_default,
        "beta": beta_lst_static
    },
    "fr3_s_xyz": {
        "alpha": alpha_lst_default,
        "beta": beta_lst_static
    },
    "fr3_s_static": {
        "alpha": alpha_lst_default,
        "beta": beta_lst_static
    },
    "fr3_w_halfsphere": {
        "alpha": alpha_lst_default,
        "beta": [20, 40, 60, 80, 100, 120, 140, 160, 180, 200]
    },
    "fr3_w_rpy": {
        "alpha": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
        "beta": beta_lst_default
    },
    "fr3_w_static": {
        "alpha": [0.001, 0.1, 0.2, 0.4, 0.6, 0.8, 0.9, 1.0, 1.1, 1.2],
        "beta": beta_lst_default
    },
    "fr3_w_xyz": {
        "alpha": [0.001, 0.003, 0.005, 0.007, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06],
        "beta": beta_lst_default
    },
}

ds_params_map_custom = {
    "fr2_desk": {
        "alpha": [0.08, 0.085, 0.09, 0.095, 0.1, 0.105, 0.11, 0.12],
        "beta": [300, 305, 310, 335, 340, 345]
    },
    # "fr3_s_xyz": {
    #     "alpha": alpha_lst_default,
    #     "beta": beta_lst_static
    # },
    "fr3_s_static": {
        "alpha": [0.09, 0.1, 0.11, 0.12, 0.15, 0.2],
        "beta": [30, 40, 50, 60, 80, 100]
    },
    "fr3_s_halfsphere": {
        "alpha": [0.02, 0.023, 0.025, 0.027, 0.03, 0.033],
        "beta": [1.8, 1.9, 2.0, 2.1, 2.2]
    },
    "fr3_w_rpy": {
        "alpha": [1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.4, 1.5],
        "beta": [330]
    },
    "fr3_w_static": {
        "alpha": [0.00001, 0.0001, 0.0005, 0.0008, 0.001, 0.0013, 0.0015],
        "beta": [260, 265, 270, 275, 280, 285, 290, 325, 330, 335, 340]
    },
    "fr3_w_halfsphere": {
        "alpha": [0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035],
        "beta": [190, 195, 200, 205, 210]
    },
}

for dataset, ab_lsts in ds_params_map_custom.items():
    result_log = ""
    for alpha in ab_lsts["alpha"]:
        for beta in ab_lsts["beta"]:
            pi, dt, a, b, bs, ss = params["people_init_score"], params["dynamic_thresh"], alpha, beta, params["block_size"], params["search_size"]
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

    with open(f"/root/catkin_ws/src/{proj_home}/test_ab_impact_log/ab_impact_{dataset}.log", "w") as f:
        f.write(result_log)