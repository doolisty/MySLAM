import os
import time

people_init_score_range = [0.1, 0.6, 0.1]
dynamic_thresh_range = [0.1, 0.6, 0.1]
alpha_range = [0.1, 0.7, 0.1]
beta_range = [19.0, 30.0, 1.0]
search_range = [1.0, 100.0, 1.0]

dataset = "fr3_w_xyz"
result_lst = []
repeat = 10

# python3 tools/evaluate_rpe.py /root/Dataset/fr3_w_xyz/groundtruth.txt /root/catkin_ws/src/MySLAM/Examples/RGB-D/CameraTrajectory.txt --verbose
def core_cmd(pi, dt, a, b, ss, dataset, repeat_id=-1):
    cmd = f"./rgbd_tum /root/catkin_ws/src/MySLAM/Vocabulary/ORBvoc.txt /root/catkin_ws/src/MySLAM/Examples/RGB-D/TUM1.yaml /root/Dataset/{dataset} /root/Dataset/{dataset}/associate.txt"
    cmd += f" {pi} {dt} {a} {b} -1 {ss}"

    os.chdir(os.getcwd() + "/Examples/RGB-D") # cd Examples/RGB-D
    os.system(cmd)
    os.chdir("/".join(os.getcwd().split("/")[:-2])) # cd ../../

    gt_path, cur_res_path = f"/root/Dataset/{dataset}/groundtruth.txt", "/root/catkin_ws/src/MySLAM_beta/Examples/RGB-D/CameraTrajectory.txt"

    # eval ATE
    os.system(f"python3 tools/evaluate_ate.py {gt_path} {cur_res_path} --verbose > tools/tmp_res_log")
    result_dict = {"params": [pi, dt, a, b, ss]}
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
    print(f"[repeat {repeat_id}] pi = {pi}, dt = {dt}, a = {a}, b = {b}")
    result_dict["id"] = repeat_id if repeat_id > -1 else -1
    print(result_dict)
    print("=" * 30)
    result_lst.append(result_dict)


def sort_list(key, top_k=10):
    lst = sorted(result_lst, key=lambda x: x[key])[:top_k]
    pair_key = key.split("_")[0] + "_pairs"
    return [x["params"] + [x[key], x[pair_key], x["id"]] for x in lst]


# core_cmd(0.6, 0.6, 0.4, 15.0, dataset)
# core_cmd(0.6, 0.8, 0.3, 12.0, dataset)

range2lst_func = lambda lst: [lst[0] + idx * lst[2] for idx in range(int(lst[1] // lst[2] - lst[0] // lst[2]))]

# for pi in range2lst_func(people_init_score_range):
# for dt in range2lst_func(dynamic_thresh_range):
#     for a in range2lst_func(alpha_range):
#         for b in range2lst_func(beta_range):
# for ss in range2lst_func(search_range):
#     now = time.time()
#     core_cmd(0.6, 0.3, 0.3, 30.0, ss, dataset)
#     end = time.time()
#     print(f"time elapsed: {end - now}")
#     with open("./profile_params_result/eval_result_log", "w") as f:
#         f.write(str(result_lst))

for i in range(repeat):
    core_cmd(0.6, 0.3, 0.05, 300.0, 0, dataset, i)
    with open("./profile_params_result/eval_result_log", "w") as f:
        f.write(str(result_lst))

rankings = ""
for key in ["ate_rmse", "rpe_trans_rmse", "rpe_rot_rmse"]:
    rankings += key
    rankings += "\n\n"
    params = sort_list(key)
    for pi, dt, a, b, _, res, pairs, id in params:
        if id > -1:
            rankings += f"(id = {id}) "
        rankings += f"[{key} = {res} in {pairs} pairs] people_init_score = {pi}, dynamic_thresh = {dt}, alpha = {a}, beta = {b}\n"
    rankings += "\n\n"

# os.system("rm profile_params_result/ranking_result_log")
with open("./profile_params_result/ranking_result_log", "w") as f:
    f.write(rankings)