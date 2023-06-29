baseline_str = "{'ate_rmse': 0.07521613999999997, 'ate_mean': 0.0715299, 'ate_median': 0.07620572, 'ate_std': 0.0232373, 'ate_min': 0.01690318, 'ate_max': 0.13201922, 'rpe_pairs': 7677.0, 'rpe_trans_rmse': 0.11684083999999997, 'rpe_trans_mean': 0.09863811999999998, 'rpe_trans_median': 0.08787972, 'rpe_trans_std': 0.06262479999999998, 'rpe_trans_min': 0.0, 'rpe_trans_max': 0.27716311999999993, 'rpe_rot_rmse': 2.0561837, 'rpe_rot_mean': 1.7879398200000012, 'rpe_rot_median': 1.7312368200000001, 'rpe_rot_std': 1.0153286200000002, 'rpe_rot_min': 0.0, 'rpe_rot_max': 6.098609219999999}"
custom_str = "{'ate_pairs': 3631.0, 'ate_rmse': 0.07219125000000001, 'ate_mean': 0.06851675, 'ate_median': 0.07233925, 'ate_std': 0.02272275, 'ate_min': 0.0158545, 'ate_max': 0.127014, 'rpe_pairs': 7677.0, 'rpe_trans_rmse': 0.113068, 'rpe_trans_mean': 0.0950735, 'rpe_trans_median': 0.084057, 'rpe_trans_std': 0.0612, 'rpe_trans_min': 0.0, 'rpe_trans_max': 0.274071, 'rpe_rot_rmse': 2.05568775, 'rpe_rot_mean': 1.7942824999999998, 'rpe_rot_median': 1.76116025, 'rpe_rot_std': 1.0031949999999998, 'rpe_rot_min': 0.0, 'rpe_rot_max': 6.08380275}"

baseline_dic = eval(baseline_str)
custom_dic = eval(custom_str)

metrics = ["rmse", "mean", "median", "std", "min", "max"]
title_prefix_map = {"ATE": "ate_", "RPE (translational)": "rpe_trans_", "RPE (rotational)": "rpe_rot_"}
cases = ["DS-SLAM", "ours"]

latex_table_str = []


def ret_begin(title):
    return "\\begin{center}\n \
\\begin{tabular}{c c c c c c c}\n \
\\multicolumn{7}{c}{" + title + "} \\\\\n \
\\hline\n \
& RMSE & mean & median & std & min & max \\\\\n \
\\hline"


def ret_end():
    return " \\hline\n \\end{tabular}\n\\end{center}"


def ret_bold(val):
    val_str = "0" if val == 0 else "%0.4f" % val
    return "\\textbf{" + val_str + "}"


def ret_color(s, color):
    return "\\textcolor[HTML]{" + color + "}{" + s + "}"

def generate_latex(baseline_dic, custom_dic, dataset, split=True):
    for t, p in title_prefix_map.items():
        latex_table_str.append(ret_begin(t))

        line = [" DS-SLAM"]
        for m in metrics:
            bval = round(baseline_dic[p + m], 4)
            line.append(ret_bold(bval))
        latex_table_str.append(" & ".join(line))
        latex_table_str.append("\\\\ [0.5ex]")

        line = [" ours"]
        for m in metrics:
            # if dataset == "fr3_w_static":
            #     print(baseline_dic)
            bval = round(baseline_dic[p + m], 4)
            cval = round(custom_dic[p + m], 4)
            color = "000000"
            if bval > cval:
                color = "008000"
            elif bval < cval:
                color = "FF0000"
            line.append(ret_color(ret_bold(cval), color))
        latex_table_str.append(" & ".join(line))
        latex_table_str.append("\\\\")

        latex_table_str.append(ret_end())

    # print("\n".join(latex_table_str))

    # filename = "./tools/tmp_latex_table_" + dataset if split else "./tools/tmp_latex_table"

    # return latex_table_str

    # with open(filename, "w") as f:
    #     f.write("\n".join(latex_table_str))

datasets = ["fr2_desk", "fr3_s_halfsphere", "fr3_s_rpy", "fr3_s_xyz", "fr3_s_static", "fr3_w_halfsphere", "fr3_w_rpy", "fr3_w_static", "fr3_w_xyz"]

dataset_dics = {
    "fr2_desk": {
        "baseline": {'ate_rmse': 0.07521613999999997, 'ate_mean': 0.0715299, 'ate_median': 0.07620572, 'ate_std': 0.0232373, 'ate_min': 0.01690318, 'ate_max': 0.13201922, 'rpe_pairs': 7677.0, 'rpe_trans_rmse': 0.11684083999999997, 'rpe_trans_mean': 0.09863811999999998, 'rpe_trans_median': 0.08787972, 'rpe_trans_std': 0.06262479999999998, 'rpe_trans_min': 0.0, 'rpe_trans_max': 0.27716311999999993, 'rpe_rot_rmse': 2.0561837, 'rpe_rot_mean': 1.7879398200000012, 'rpe_rot_median': 1.7312368200000001, 'rpe_rot_std': 1.0153286200000002, 'rpe_rot_min': 0.0, 'rpe_rot_max': 6.098609219999999},
        "custom": {'ate_pairs': 3631.0, 'ate_rmse': 0.07219125000000001, 'ate_mean': 0.06851675, 'ate_median': 0.07233925, 'ate_std': 0.02272275, 'ate_min': 0.0158545, 'ate_max': 0.127014, 'rpe_pairs': 7677.0, 'rpe_trans_rmse': 0.113068, 'rpe_trans_mean': 0.0950735, 'rpe_trans_median': 0.084057, 'rpe_trans_std': 0.0612, 'rpe_trans_min': 0.0, 'rpe_trans_max': 0.274071, 'rpe_rot_rmse': 2.05568775, 'rpe_rot_mean': 1.7942824999999998, 'rpe_rot_median': 1.76116025, 'rpe_rot_std': 1.0031949999999998, 'rpe_rot_min': 0.0, 'rpe_rot_max': 6.08380275}
    },
    "fr3_s_halfsphere": {
        "baseline": {'ate_rmse': 0.023316209999999993, 'ate_mean': 0.020915390000000006, 'ate_median': 0.019573080000000003, 'ate_std': 0.01029649, 'ate_min': 0.0014940299999999995, 'ate_max': 0.06862908000000001, 'rpe_pairs': 9913.75, 'rpe_trans_rmse': 0.03795592, 'rpe_trans_mean': 0.03383809, 'rpe_trans_median': 0.03153312000000001, 'rpe_trans_std': 0.017188819999999997, 'rpe_trans_min': 0.0, 'rpe_trans_max': 0.11802301, 'rpe_rot_rmse': 0.9930125699999999, 'rpe_rot_mean': 0.8995580499999997, 'rpe_rot_median': 0.8590945199999999, 'rpe_rot_std': 0.42052057, 'rpe_rot_min': 0.0, 'rpe_rot_max': 2.92924753},
        "custom": {'ate_pairs': 1069.0, 'ate_rmse': 0.0190055, 'ate_mean': 0.0171085, 'ate_median': 0.015728000000000002, 'ate_std': 0.00827425, 'ate_min': 0.001466, 'ate_max': 0.05242525, 'rpe_pairs': 9914.0, 'rpe_trans_rmse': 0.029893, 'rpe_trans_mean': 0.026876999999999998, 'rpe_trans_median': 0.025152, 'rpe_trans_std': 0.0130805, 'rpe_trans_min': 0.0, 'rpe_trans_max': 0.088767, 'rpe_rot_rmse': 0.918433, 'rpe_rot_mean': 0.8241192500000001, 'rpe_rot_median': 0.767606, 'rpe_rot_std': 0.4053835, 'rpe_rot_min': 0.0, 'rpe_rot_max': 2.78076925}
    },
    "fr3_s_rpy": {
        # "baseline": {'ate_rmse': 0.030482900000000014, 'ate_mean': 0.023645530000000005, 'ate_median': 0.018135369999999998, 'ate_std': 0.019135600000000003, 'ate_min': 0.0020231199999999998, 'ate_max': 0.14040913, 'rpe_pairs': 9921.71, 'rpe_trans_rmse': 0.04714098, 'rpe_trans_mean': 0.03829523999999999, 'rpe_trans_median': 0.031992849999999996, 'rpe_trans_std': 0.027361839999999988, 'rpe_trans_min': 0.0, 'rpe_trans_max': 0.19735848999999997, 'rpe_rot_rmse': 1.0879001000000001, 'rpe_rot_mean': 0.9422932000000002, 'rpe_rot_median': 0.85017578, 'rpe_rot_std': 0.5410560499999998, 'rpe_rot_min': 0.0, 'rpe_rot_max': 4.059225130000002},
        "baseline": {'id': 63, 'ate_pairs': 722, 'ate_rmse': 0.03183, 'ate_mean': 0.023794, 'ate_median': 0.01756, 'ate_std': 0.021142, 'ate_min': 0.001807, 'ate_max': 0.146464, 'rpe_pairs': 9919, 'rpe_trans_rmse': 0.048401, 'rpe_trans_mean': 0.038677, 'rpe_trans_median': 0.031415, 'rpe_trans_std': 0.0291, 'rpe_trans_min': 0.0, 'rpe_trans_max': 0.195049, 'rpe_rot_rmse': 1.154211, 'rpe_rot_mean': 0.982874, 'rpe_rot_median': 0.862784, 'rpe_rot_std': 0.605114, 'rpe_rot_min': 0.0, 'rpe_rot_max': 4.344598},
        "custom": {'ate_pairs': 766.0, 'ate_rmse': 0.027004499999999997, 'ate_mean': 0.021189166666666665, 'ate_median': 0.016341666666666668, 'ate_std': 0.016713000000000002, 'ate_min': 0.0019706666666666666, 'ate_max': 0.127925, 'rpe_pairs': 9926.0, 'rpe_trans_rmse': 0.04079583333333333, 'rpe_trans_mean': 0.033771833333333334, 'rpe_trans_median': 0.02846716666666667, 'rpe_trans_std': 0.022836, 'rpe_trans_min': 0.0, 'rpe_trans_max': 0.180941, 'rpe_rot_rmse': 1.1478698333333333, 'rpe_rot_mean': 1.006215, 'rpe_rot_median': 0.9244183333333335, 'rpe_rot_std': 0.5515766666666666, 'rpe_rot_min': 0.0, 'rpe_rot_max': 3.7774535}
    },
    "fr3_s_xyz": {
        "baseline": {'ate_rmse': 0.022399099999999995, 'ate_mean': 0.01998, 'ate_median': 0.01792168, 'ate_std': 0.010118, 'ate_min': 0.00201951, 'ate_max': 0.07123006999999999, 'rpe_pairs': 9946.0, 'rpe_trans_rmse': 0.032477620000000006, 'rpe_trans_mean': 0.02867969, 'rpe_trans_median': 0.027042490000000013, 'rpe_trans_std': 0.015237419999999996, 'rpe_trans_min': 0.0, 'rpe_trans_max': 0.10348022999999996, 'rpe_rot_rmse': 0.6551935100000001, 'rpe_rot_mean': 0.57990411, 'rpe_rot_median': 0.52644505, 'rpe_rot_std': 0.3048771900000002, 'rpe_rot_min': 0.0, 'rpe_rot_max': 2.182936779999999},
        "custom": {'ate_pairs': 1216.0, 'ate_rmse': 0.016151333333333334, 'ate_mean': 0.014302, 'ate_median': 0.0130635, 'ate_std': 0.007500166666666666, 'ate_min': 0.001117, 'ate_max': 0.054477500000000005, 'rpe_pairs': 9946.0, 'rpe_trans_rmse': 0.023830833333333332, 'rpe_trans_mean': 0.021058833333333332, 'rpe_trans_median': 0.01965916666666667, 'rpe_trans_std': 0.011153166666666667, 'rpe_trans_min': 0.0, 'rpe_trans_max': 0.07716383333333332, 'rpe_rot_rmse': 0.5922284999999999, 'rpe_rot_mean': 0.5181101666666666, 'rpe_rot_median': 0.45891733333333334, 'rpe_rot_std': 0.286803, 'rpe_rot_min': 0.0, 'rpe_rot_max': 1.9337778333333333}
    },
    "fr3_s_static": {
        # "baseline": {'ate_rmse': 0.007210659999999999, 'ate_mean': 0.006285909999999999, 'ate_median': 0.005575719999999998, 'ate_std': 0.003529189999999999, 'ate_min': 0.0005652900000000002, 'ate_max': 0.025910079999999995, 'rpe_pairs': 9877.0, 'rpe_trans_rmse': 0.010792750000000002, 'rpe_trans_mean': 0.009532780000000001, 'rpe_trans_median': 0.008664630000000001, 'rpe_trans_std': 0.00505843, 'rpe_trans_min': 0.0, 'rpe_trans_max': 0.038318500000000005, 'rpe_rot_rmse': 0.3397188100000001, 'rpe_rot_mean': 0.30496288000000005, 'rpe_rot_median': 0.28531381, 'rpe_rot_std': 0.14966943999999993, 'rpe_rot_min': 0.0, 'rpe_rot_max': 1.0693540300000002},
        "baseline": {'id': 81, 'ate_pairs': 676, 'ate_rmse': 0.007472, 'ate_mean': 0.006526, 'ate_median': 0.005667, 'ate_std': 0.003639, 'ate_min': 0.00068, 'ate_max': 0.026891, 'rpe_pairs': 9877, 'rpe_trans_rmse': 0.011093, 'rpe_trans_mean': 0.009784, 'rpe_trans_median': 0.008879, 'rpe_trans_std': 0.005229, 'rpe_trans_min': 0.0, 'rpe_trans_max': 0.038632, 'rpe_rot_rmse': 0.352799, 'rpe_rot_mean': 0.315499, 'rpe_rot_median': 0.29297, 'rpe_rot_std': 0.157885, 'rpe_rot_min': 0.0, 'rpe_rot_max': 1.114533},
        "custom": {'ate_pairs': 676.0, 'ate_rmse': 0.007001500000000001, 'ate_mean': 0.0062265, 'ate_median': 0.0057415, 'ate_std': 0.0032012499999999997, 'ate_min': 0.0005315, 'ate_max': 0.02320925, 'rpe_pairs': 9877.0, 'rpe_trans_rmse': 0.01113925, 'rpe_trans_mean': 0.009987000000000001, 'rpe_trans_median': 0.00929675, 'rpe_trans_std': 0.00493325, 'rpe_trans_min': 0.0, 'rpe_trans_max': 0.034158499999999994, 'rpe_rot_rmse': 0.34032100000000004, 'rpe_rot_mean': 0.30655175, 'rpe_rot_median': 0.28974075, 'rpe_rot_std': 0.14778775, 'rpe_rot_min': 0.0, 'rpe_rot_max': 1.071354}
    },
    "fr3_w_halfsphere": {
        "baseline": {'ate_rmse': 0.027733520000000005, 'ate_mean': 0.02432461000000001, 'ate_median': 0.02170092, 'ate_std': 0.013309429999999994, 'ate_min': 0.00202667, 'ate_max': 0.09684618, 'rpe_pairs': 9934.95, 'rpe_trans_rmse': 0.04187030000000002, 'rpe_trans_mean': 0.037174429999999994, 'rpe_trans_median': 0.03403704, 'rpe_trans_std': 0.019253959999999994, 'rpe_trans_min': 0.0, 'rpe_trans_max': 0.13794847, 'rpe_rot_rmse': 0.9891093399999998, 'rpe_rot_mean': 0.8937733200000001, 'rpe_rot_median': 0.8425042099999999, 'rpe_rot_std': 0.42343879, 'rpe_rot_min': 0.0, 'rpe_rot_max': 3.3160249900000003},
        "custom": {'ate_pairs': 1006.0, 'ate_rmse': 0.027129, 'ate_mean': 0.023983249999999998, 'ate_median': 0.021665, 'ate_std': 0.012673, 'ate_min': 0.00193, 'ate_max': 0.07987, 'rpe_pairs': 9934.0, 'rpe_trans_rmse': 0.0408525, 'rpe_trans_mean': 0.036506500000000004, 'rpe_trans_median': 0.033702499999999996, 'rpe_trans_std': 0.0183245, 'rpe_trans_min': 0.0, 'rpe_trans_max': 0.136131, 'rpe_rot_rmse': 0.9689592499999999, 'rpe_rot_mean': 0.8765495, 'rpe_rot_median': 0.8267475, 'rpe_rot_std': 0.4129185, 'rpe_rot_min': 0.0, 'rpe_rot_max': 3.12524375}
    },
    "fr3_w_rpy": {
        # "baseline": {'ate_rmse': 0.04719134999999998, 'ate_mean': 0.039609430000000015, 'ate_median': 0.03499759000000001, 'ate_std': 0.02545437000000001, 'ate_min': 0.0030250999999999976, 'ate_max': 0.21008334999999992, 'rpe_pairs': 9943.98, 'rpe_trans_rmse': 0.06862362999999996, 'rpe_trans_mean': 0.05868927000000002, 'rpe_trans_median': 0.05161677999999999, 'rpe_trans_std': 0.035341839999999985, 'rpe_trans_min': 0.0, 'rpe_trans_max': 0.28134027000000006, 'rpe_rot_rmse': 1.34880672, 'rpe_rot_mean': 1.1261817300000005, 'rpe_rot_median': 0.9636704699999998, 'rpe_rot_std': 0.7383953700000002, 'rpe_rot_min': 0.0, 'rpe_rot_max': 6.187175339999998},
        "baseline": {'id': 62, 'ate_pairs': 864, 'ate_rmse': 0.050069, 'ate_mean': 0.042032, 'ate_median': 0.036665, 'ate_std': 0.027207, 'ate_min': 0.004309, 'ate_max': 0.210149, 'rpe_pairs': 9945, 'rpe_trans_rmse': 0.072984, 'rpe_trans_mean': 0.062673, 'rpe_trans_median': 0.055118, 'rpe_trans_std': 0.0374, 'rpe_trans_min': 0.0, 'rpe_trans_max': 0.280312, 'rpe_rot_rmse': 1.402999, 'rpe_rot_mean': 1.205043, 'rpe_rot_median': 1.057991, 'rpe_rot_std': 0.718524, 'rpe_rot_min': 0.0, 'rpe_rot_max': 5.65819},
        "custom": {'ate_pairs': 803.0, 'ate_rmse': 0.047189749999999996, 'ate_mean': 0.040182499999999996, 'ate_median': 0.034895, 'ate_std': 0.02467225, 'ate_min': 0.00445975, 'ate_max': 0.20266800000000001, 'rpe_pairs': 9943.0, 'rpe_trans_rmse': 0.0673695, 'rpe_trans_mean': 0.058174250000000004, 'rpe_trans_median': 0.051892249999999994, 'rpe_trans_std': 0.03389475, 'rpe_trans_min': 0.0, 'rpe_trans_max': 0.26076325, 'rpe_rot_rmse': 1.3174949999999999, 'rpe_rot_mean': 1.1138919999999999, 'rpe_rot_median': 0.9829822500000001, 'rpe_rot_std': 0.702386, 'rpe_rot_min': 0.0, 'rpe_rot_max': 6.248800749999999}
    },
    "fr3_w_static": {
        "baseline": {'ate_rmse': 0.009926989999999995, 'ate_mean': 0.00889903, 'ate_median': 0.00819145, 'ate_std': 0.00437106, 'ate_min': 0.0008939900000000003, 'ate_max': 0.03798003999999999, 'rpe_pairs': 9919.0, 'rpe_trans_rmse': 0.016252209999999996, 'rpe_trans_mean': 0.01441152, 'rpe_trans_median': 0.013421879999999997, 'rpe_trans_std': 0.007500250000000001, 'rpe_trans_min': 0.0, 'rpe_trans_max': 0.054623019999999994, 'rpe_rot_rmse': 0.30194937000000005, 'rpe_rot_mean': 0.2717518500000001, 'rpe_rot_median': 0.2547841300000001, 'rpe_rot_std': 0.13142353999999995, 'rpe_rot_min': 0.0, 'rpe_rot_max': 1.0269285900000005},
        "custom": {'ate_pairs': 714.0, 'ate_rmse': 0.008900749999999999, 'ate_mean': 0.008030500000000001, 'ate_median': 0.007459500000000001, 'ate_std': 0.00383425, 'ate_min': 0.00071475, 'ate_max': 0.0255415, 'rpe_pairs': 9919.0, 'rpe_trans_rmse': 0.015154999999999998, 'rpe_trans_mean': 0.013444749999999998, 'rpe_trans_median': 0.01244875, 'rpe_trans_std': 0.006993, 'rpe_trans_min': 0.0, 'rpe_trans_max': 0.048192, 'rpe_rot_rmse': 0.28550425, 'rpe_rot_mean': 0.25850725, 'rpe_rot_median': 0.24306850000000002, 'rpe_rot_std': 0.12116800000000001, 'rpe_rot_min': 0.0, 'rpe_rot_max': 0.82128775}
    },
    "fr3_w_xyz": {
        "baseline": {'ate_rmse': 0.033972819999999994, 'ate_mean': 0.02863794, 'ate_median': 0.022895850000000002, 'ate_std': 0.01827216, 'ate_min': 0.00186076, 'ate_max': 0.09290445, 'rpe_pairs': 9976.0, 'rpe_trans_rmse': 0.04869199000000002, 'rpe_trans_mean': 0.04204535, 'rpe_trans_median': 0.03763303999999999, 'rpe_trans_std': 0.02455469000000001, 'rpe_trans_min': 0.0, 'rpe_trans_max': 0.18051771999999994, 'rpe_rot_rmse': 0.8347324199999997, 'rpe_rot_mean': 0.67858142, 'rpe_rot_median': 0.59430068, 'rpe_rot_std': 0.48605361, 'rpe_rot_min': 0.0, 'rpe_rot_max': 7.006936309999997},
        "custom": {'ate_pairs': 826.0, 'ate_rmse': 0.03141066666666667, 'ate_mean': 0.026678500000000004, 'ate_median': 0.022044499999999995, 'ate_std': 0.0165795, 'ate_min': 0.002021666666666667, 'ate_max': 0.08827516666666667, 'rpe_pairs': 9976.0, 'rpe_trans_rmse': 0.04517466666666667, 'rpe_trans_mean': 0.039174, 'rpe_trans_median': 0.03524616666666667, 'rpe_trans_std': 0.022495166666666667, 'rpe_trans_min': 0.0, 'rpe_trans_max': 0.17096866666666666, 'rpe_rot_rmse': 0.7854256666666668, 'rpe_rot_mean': 0.6324115, 'rpe_rot_median': 0.5505665000000001, 'rpe_rot_std': 0.4657116666666667, 'rpe_rot_min': 0.0, 'rpe_rot_max': 6.868896833333333}
    }
}

dataset_replace = {}
for key in dataset_dics.keys():
    split_key = key.split("_")
    new_key = split_key[0] + "/"
    if split_key[1] == "s":
        new_key += "sitting\_"
    elif split_key[1] == "w":
        new_key += "walking\_"
    new_key += split_key[-1]
    dataset_replace[key] = new_key

print(dataset_replace)

split = False

for dataset, dics in dataset_dics.items():
    latex_table_str.append("\n" + dataset_replace[dataset] + "\n")
    generate_latex(dics["baseline"], dics["custom"], dataset)
    if split:
        with open("./tools/tmp_latex_table_" + dataset, "w") as f:
            f.write("\n".join(latex_table_str))
        latex_table_str = []

if not split:
    with open("./tools/tmp_latex_table", "w") as f:
        f.write("\n".join(latex_table_str))
