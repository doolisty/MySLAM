import argparse
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import seaborn as sns
import palettable
import matplotlib.pyplot as plt

# from test_ab_impact_finely import ds_params_map

parser = argparse.ArgumentParser()
parser.add_argument("--dataset", default="fr2_desk")
parser.add_argument("--write", help='', action='store_true')
parser.add_argument("--all", help='', action='store_true')
parser.add_argument("--plot", help='', action='store_true')
args = parser.parse_args()

alpha_lst_default = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
beta_lst_default = [260, 270, 280, 290, 300, 310, 320, 330, 340, 350]
beta_lst_static = [0, 1, 2, 3, 4, 5, 10, 20, 30, 40]

ds_params_map = {
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

ds_params_map_custom_1 = {
    "fr3_s_halfsphere": {
        "alpha": [0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065],
        "beta": [1.5, 2.0, 2.5]
    },
    "fr3_s_static": {
        "alpha": [0.09, 0.1, 0.11, 0.12, 0.15, 0.2],
        "beta": [30, 40, 50, 60, 80, 100]
    },
    "fr3_w_rpy": {
        "alpha": [0.7, 0.9, 1.0, 1.1, 1.2],
        "beta": [260, 270, 320, 330, 340]
    }
}

ds_params_map_custom_2 = {
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

# filepath = "/root/catkin_ws/src/MySLAM_beta/test_ab_impact_log/ab_impact_" + args.dataset + ".log"

# datasets = [args.dataset] if not args.all else ["fr2_desk", "fr3_s_halfsphere", "fr3_s_rpy", "fr3_s_xyz", "fr3_s_static", "fr3_w_halfsphere", "fr3_w_rpy", "fr3_w_static", "fr3_w_xyz"]
# datasets = ["fr2_desk", "fr3_s_halfsphere", "fr3_s_rpy", "fr3_s_xyz", "fr3_s_static", "fr3_w_halfsphere", "fr3_w_rpy", "fr3_w_static", "fr3_w_xyz"]
map_target = ds_params_map_custom_2
suffix = "" #"/0622_log"

datasets = [x for x in map_target.keys()]
# metrics = ["ate_rmse", "rpe_trans_rmse", "rpe_rot_rmse"]
metrics = ["ate_rmse"]


def sort_lst(lst, metric, k=5):
    sorted_lst = sorted(lst, key=lambda x: x[metric])[:k]
    return [[*x["params"], x[metric]] for x in sorted_lst]

# filepath_prefix = "/root/catkin_ws/src/MySLAM_beta/test_ab_impact_log"
filepath_prefix = "/home/zhaoyang/slam/MySLAM_beta/test_ab_impact_log"
filepath_prefix += suffix
for dataset in datasets:
    alpha_axis, beta_axis = map_target[dataset]["alpha"], map_target[dataset]["beta"]
    # ate_rmse = [[0 for _ in range(10)] for _ in range(10)]
    ate_rmse = np.zeros((len(alpha_axis), len(beta_axis)), dtype=np.float32)
    max_val, min_val = float("-inf"), float("inf")
    filepath = filepath_prefix + "/ab_impact_" + dataset + ".log"
    with open(filepath, "r") as f:
        lines = f.readlines()
    result_lst = []
    params = None
    for line in lines:
        segs = line.split()
        if len(segs) == 0:
            continue
        if segs[0] == "alpha":
            params = (float(segs[2][:-1]), float(segs[5][:-1]))
        else:
            result = eval(line.split("defaultdict(<class 'float'>, ")[-1][:-2])
            result["params"] = params
            result_lst.append(result)
    ranking_str = ""
    for metric in metrics:
        if args.write:
            ranking_str += metric + "\n\n"
        target_lst = [[*x["params"], x[metric]] for x in result_lst] if args.plot else sort_lst(result_lst, metric, k=10)
        for alpha, beta, val in target_lst:
            if args.write:
                ranking_str += f"alpha = {alpha}, beta = {beta}, {metric} = {val}\n"
            if args.plot:
                ate_rmse[alpha_axis.index(alpha)][beta_axis.index(beta)] = val
                max_val, min_val = max(max_val, val), min(min_val, val)
        if args.write:
            ranking_str += "\n\n\n"
    if args.write:
        with open(filepath_prefix + f"/ranking_{dataset}.log", "w") as f:
            f.write(ranking_str)
    if args.plot:
        data_frame_ab = pd.DataFrame(ate_rmse, index=alpha_axis, columns=beta_axis)
        print(data_frame_ab)
        # fig = plt.figure()
        # ax3 = plt.axes(projection='3d')
        # X, Y = np.meshgrid(np.array(alpha_axis), np.array(beta_axis))
        # Z = ate_rmse
        plt.figure(dpi=300)
        if dataset in ["fr3_s_static", "fr3_w_static"]:
            vmin_val, vmax_val = min_val, min_val + 0.002
        else:
            vmin_val, vmax_val = min_val, min_val + 0.01
        sns.heatmap(data=data_frame_ab, annot=True, annot_kws={"fontsize":6}, vmin=vmin_val, vmax=vmax_val)
        plt.ylabel("alpha")
        plt.xlabel("beta")
        plt.title(f"dataset: {dataset}")
        # ax3.plot_surface(X, Y, Z, cmap="rainbow")
        # plt.show()
        plt.savefig(filepath_prefix + f"/figs/{dataset}.png")
