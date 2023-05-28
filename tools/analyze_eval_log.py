# import argparse

# args = argparse.ArgumentParser()
# args.add_argument("")

filepath = "./profile_params_result/eval_result_log_0526"

with open(filepath, "r") as f:
    line = f.readlines()[0]

result_dict = eval(line)
for result in result_dict:
    if result["params"] == [0.6, 0.5, 0.5, 21.0]:
        print(result)
