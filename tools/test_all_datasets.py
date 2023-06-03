import os
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--gdb", help='', action='store_true')
parser.add_argument("--repeat", help='', default=50)
parser.add_argument("--baseline", help='', action='store_true')
parser.add_argument("--video", help='', action='store_true')
args = parser.parse_args()

def sort_list(key, top_k=10):
    if not args.baseline:
        lst = sorted(result_lst, key=lambda x: x[key])[:top_k]
    else:
        lst = sorted(result_lst, key=lambda x: x[key], reverse=True)[:top_k]
    pair_key = key.split("_")[0] + "_pairs"
    return [[x[key], x[pair_key], x["id"]] for x in lst]

params = {
    "people_init_score": 0.8,
    "dynamic_thresh": 0.3,
    "alpha": 0.05,
    "beta": 300.0,
    "block_size": -1,
    "search_size": 0
}

# "fr3_s_halfsphere"
datasets = ["fr3_s_rpy", "fr3_s_xyz", "fr3_s_static", "fr3_w_halfsphere", "fr3_w_rpy", "fr3_w_static", "fr3_w_xyz"]
proj_home = "MySLAM_beta" if not args.baseline else "MySLAM_dsslam"

for dataset in datasets:
    result_lst = []
    pi, dt, a, b, bs, ss = params["people_init_score"], params["dynamic_thresh"], params["alpha"], params["beta"], params["block_size"], params["search_size"]
    cmd = ""
    if args.gdb:
        cmd += "gdb -args "
    cmd += f"./rgbd_tum /root/catkin_ws/src/MySLAM/Vocabulary/ORBvoc.txt /root/catkin_ws/src/MySLAM/Examples/RGB-D/TUM1.yaml /root/Dataset/{dataset} /root/Dataset/{dataset}/associate.txt"
    if not args.baseline:
        cmd += f" {pi} {dt} {a} {b} {bs} {ss}"

    # repeat
    for repeat_id in range(args.repeat):
        os.chdir(f"/root/catkin_ws/src/{proj_home}/Examples/RGB-D") # cd Examples/RGB-D
        start = time.time()
        os.system(cmd)
        print(f"time elapsed: {time.time() - start}")
        os.chdir(f"/root/catkin_ws/src/{proj_home}")

        gt_path, cur_res_path = f"/root/Dataset/{dataset}/groundtruth.txt", f"/root/catkin_ws/src/{proj_home}/Examples/RGB-D/CameraTrajectory.txt"

        # eval ATE
        os.system(f"python3 tools/evaluate_ate.py {gt_path} {cur_res_path} --verbose > tools/tmp_res_log")
        result_dict = {"id": repeat_id}
        with open("tools/tmp_res_log", "r") as f:
            lines = f.readlines()
        for line in lines:
            lst = line.split()
            if lst[0] == "compared_pose_pairs":
                result_dict["ate_pairs"] = int(lst[1])
            elif lst[0] == "absolute_translational_error.rmse":
                result_dict["ate_rmse"] = float(lst[1])
            elif lst[0] == "absolute_translational_error.mean":
                result_dict["ate_mean"] = float(lst[1])
            elif lst[0] == "absolute_translational_error.median":
                result_dict["ate_median"] = float(lst[1])
            elif lst[0] == "absolute_translational_error.std":
                result_dict["ate_std"] = float(lst[1])
            elif lst[0] == "absolute_translational_error.min":
                result_dict["ate_min"] = float(lst[1])
            elif lst[0] == "absolute_translational_error.max":
                result_dict["ate_max"] = float(lst[1])

        # eval RPE
        os.system(f"python3 tools/evaluate_rpe.py {gt_path} {cur_res_path} --verbose > tools/tmp_res_log")
        with open("tools/tmp_res_log", "r") as f:
            lines = f.readlines()
        for line in lines:
            lst = line.split()
            if lst[0] == "compared_pose_pairs":
                result_dict["rpe_pairs"] = int(lst[1])
            # translational
            elif lst[0] == "translational_error.rmse":
                result_dict["rpe_trans_rmse"] = float(lst[1])
            elif lst[0] == "translational_error.mean":
                result_dict["rpe_trans_mean"] = float(lst[1])
            elif lst[0] == "translational_error.median":
                result_dict["rpe_trans_median"] = float(lst[1])
            elif lst[0] == "translational_error.std":
                result_dict["rpe_trans_std"] = float(lst[1])
            elif lst[0] == "translational_error.min":
                result_dict["rpe_trans_min"] = float(lst[1])
            elif lst[0] == "translational_error.max":
                result_dict["rpe_trans_max"] = float(lst[1])
            # rotational
            elif lst[0] == "rotational_error.rmse":
                result_dict["rpe_rot_rmse"] = float(lst[1])
            elif lst[0] == "rotational_error.mean":
                result_dict["rpe_rot_mean"] = float(lst[1])
            elif lst[0] == "rotational_error.median":
                result_dict["rpe_rot_median"] = float(lst[1])
            elif lst[0] == "rotational_error.std":
                result_dict["rpe_rot_std"] = float(lst[1])
            elif lst[0] == "rotational_error.min":
                result_dict["rpe_rot_min"] = float(lst[1])
            elif lst[0] == "rotational_error.max":
                result_dict["rpe_rot_max"] = float(lst[1])

        print("=" * 30)
        print(f"[repeat {repeat_id}]")
        print(result_dict)
        print("=" * 30)
        result_lst.append(result_dict)

        # record results
        with open(f"/root/catkin_ws/src/{proj_home}/profile_params_result/eval_result_log_{dataset}", "w") as f:
            f.write(str(result_lst))
    # end repeat for loop

    rankings = "\n".join([k + ": " + str(v) for k, v in params.items()])
    for key in ["ate_rmse", "rpe_trans_rmse", "rpe_rot_rmse"]:
        rankings += "\n\n"
        rankings += key
        rankings += "\n\n"
        sort_res = sort_list(key)
        for res, pair_num, id in sort_res:
            rankings += f"[id = {id}] {key} = {res} in {pair_num} pairs\n"

    with open(f"/root/catkin_ws/src/{proj_home}/profile_params_result/ranking_result_log_{dataset}", "w") as f:
        f.write(rankings)
