import argparse
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument("--suffix", default="")
parser.add_argument("--find", action='store_true')
parser.add_argument("--baseline", action='store_true')
args = parser.parse_args()

proj_home = "MySLAM_beta" if not args.baseline else "MySLAM_dsslam"
filepath = f"/home/zhaoyang/slam/{proj_home}/profile_params_result/eval_result_log"
if len(args.suffix) > 0:
    filepath += "_" + args.suffix

with open(filepath, "r") as f:
    line = f.readlines()[0]

all_results = defaultdict(float)
# count = 0

result_dict = eval(line)
for result in result_dict:
    if args.find and result["params"] == [0.6, 0.30000000000000004, 0.30000000000000004, 30.0, -1]:
        print(result)
    for k, v in result.items():
        if k not in ["id", "params", "ate_pairs"]:
            all_results[k] += v
        # if k == "ate_rmse" and v < 0.03:
        #     count += 1

for k in all_results.keys():
    all_results[k] /= len(result_dict)
print(all_results)
# print(f"count = {count}")
