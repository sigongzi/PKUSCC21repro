import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import copy
import argparse

header = [ ["GS","GS","GS","IAMB","IAMB","IAMB","Inter-IAMB","Inter-IAMB","Inter-IAMB"] ,["C1","C2","C3","C1","C2","C3","C1","C2","C3"] ]
algorithm_set = ["GS", "IAMB", "Inter-IAMB"]
dataset_set = ["C1", "C2", "C3"]

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--fromdir", help="give resultdir", default=f"{os.getcwd()}/../../run/output")
    parser.add_argument("-s","--storedir", help="give storedir", default=f"{os.getcwd()}/../output")
    args = parser.parse_args()
    return args

multi_index =  pd.MultiIndex.from_tuples(list(zip(*header)), names=["algorithm", "dataset"])
def get_time(filedir, dataset, algorithm, core, colname, is_weak = 0):
    app = "strong"
    if is_weak :
        app = "weak"
    src_file = os.path.join(filedir,f"{dataset}_{algorithm}_p{core}_{app}.csv")
    # print(src_file)

    if os.path.isfile(src_file):
        df = pd.read_csv(src_file, sep=",")
        return df[colname][1]
    else:
        print(f"there is no {src_file}")

    return -1

def get_strong_dataframe(filedir, ad_index, colname):
    arr = np.empty((8,9))
    strong_dir = os.path.join(filedir, "strong")
    for i in range(8) :
        j = 0
        for a, d in zip(header[0], header[1]) :
            a = a.lower().replace("-",".")
            # print(a)
            arr[i][j] = get_time(strong_dir, d, a, 2 ** i, colname, is_weak = 0)
            j += 1

    df = pd.DataFrame(arr, index=[2 ** i for i in range(8)], columns=ad_index)
    return df
def get_weak_dataframe(filedir, algorithm,colname) :
    dataset = "C2"
    arr = np.empty((8,3))
    weak_dir = os.path.join(filedir, "weak")
    for i in range(8) :
        j = 0
        for a in algorithm:
            a = a.lower().replace("-",".")
            arr[i][j] = get_time(weak_dir, dataset, a, 2 ** i, colname, is_weak = 1)
            j += 1
    df = pd.DataFrame(arr, index=[2 ** i for i in range(8)], columns=algorithm)
    return df
def get_table(dframe):
    arr = dframe.to_numpy()
    for i in range(8):
        print(f"{2 ** i}&" + " ".join([(f"& {arr[i][j]:.1f}" + ("&" if j % 3 == 2 and j != 8 else "")) for j in range(9)]) +"\\" *2);

def plot_strong(fig, X, y, column_name, algorithm_name, dataset_name, core_max):
    fmt = ["mo-", "gX-","cs-"]

    for i in range(len(fmt)):
        if column_name == "Efficiency" :
            fig.plot(range(0, core_max + 1), y[i], fmt[i],label=dataset_name[i])
        elif column_name == "Speedup" :
            fig.plot(range(0, core_max + 1), np.log2(y[i]), fmt[i],label=dataset_name[i])
    if column_name == "Speedup" :
        fig.plot(list(range(0,core_max + 1)),'--', label="Linear Speedup")
    # fig.ylabel(f"{column_name}")
    fig.axis(xmin = 0, xmax=7)
    fig.set_xticks(list(range(0,core_max +1)),minor=False)
    fig.set_xticklabels([2 ** i for i in range(0, core_max + 1)], fontdict=None, minor=False)
    fig.set_yticks([])
    if column_name == "Efficiency":
        # fig.yticks([i * 0.2 for i in range(0,6)], [i * 20 for i in range(0, 6)])
        fig.axis(ymin = 0, ymax=1)
        fig.set_yticks([i * 0.2 for i in range(0,6)],minor=False)
        fig.legend(loc="lower left")
    elif column_name == "Speedup":
        # fig.yticks(list(range(0,core_max + 1)),X)
        fig.axis(ymin = 0, ymax=7)
        fig.set_yticks(list(range(0,core_max +1)),minor=False)

        fig.legend(loc="upper left")
    # plt.xticks(list(range(0,core_max + 1)),X)
    fig.set_yticklabels([], fontdict=None, minor=False)



def draw_fig3(filedir, dframe, core_max):
    plt.clf()
    target_file = os.path.join(filedir, "F3.pdf")
    fig, ax = plt.subplots(2, 3,figsize=(12,7))

    s = 0
    for title in ["Speedup", "Efficiency"] :
        t = 0
        for a in algorithm_set :
            y = copy.deepcopy(dframe[a].to_numpy()).T
            print(y[:,0])
            if title == "Speedup" :
                y = y[:, 0].reshape((3,1)) / y
            else :
                for i in range(1,y.shape[1]) :
                    y[:, i] = y[:, 0] / ((2 ** i) * y[:, i])
                y[:,0] = np.array([1,1,1]).reshape((3,))

            plot_strong(ax[s, t], [2 ** i for i in range(core_max + 1)], y, title, a, dataset_set, core_max)

            if t == 0 :
                if title == "Speedup" :
                    ax[s, t].set_ylabel(title)
                    ax[s, t].set_yticklabels([2 ** i for i in range(0, core_max + 1)], fontdict=None, minor=False)
                else :
                    ax[s, t].set_ylabel(f"{title}(%)")
                    ax[s, t].set_yticklabels([i * 20 for i in range(0, 6)], fontdict=None, minor=False)


            if s == 0 :
                ax[s, t].set_title(a)

            t += 1
        s += 1
    ax[1, 1].set_xlabel("Number of cores")
    fig.tight_layout()
    fig.savefig(target_file)
def draw_fig6(filedir, dframe, core_max, algorithm_name) :
    plt.clf()
    target_file = os.path.join(filedir, "F6.pdf")
    plt.figure(figsize=(4,3))
    y = copy.deepcopy(dframe.to_numpy())[:,1:]
    y = y[0, :] / y
    y = y.T
    print(y)
    fmt = ["mo-", "gX-","cs-"]

    for i in range(len(fmt)):
        plt.plot(range(0, core_max + 1), y[i], fmt[i],label = algorithm_name[i])
    plt.ylim((0,1))
    plt.xlim((0,7))
    plt.yticks([i * 0.2 for i in range(0,6)], [i * 20 for i in range(0, 6)])
    plt.xticks(range(0, core_max + 1), [2 ** i for i in range(core_max + 1)])
    plt.xlabel("Number of cores")
    plt.ylabel("Weak Scaling Efficiency (%)")
    plt.legend(loc="lower left")
    plt.tight_layout()
    plt.savefig(target_file)

def draw_fig4(filedir, mxx, strong, core_max, algorithm_name):
    plt.clf()
    target_file = os.path.join(filedir, "F4.pdf")
    plt.figure(figsize=(4,3))
    # print(mxx["C2"].to_numpy())
    # print(strong["C2"].to_numpy())
    y = copy.deepcopy(mxx["C2"].to_numpy()) / copy.deepcopy(strong["C2"].to_numpy())
    y = y.T
    print(y)
    fmt = ["mo-", "gX-","cs-"]

    for i in range(len(fmt)):
        plt.plot(range(0, core_max + 1), y[i], fmt[i],label = algorithm_name[i])
    plt.ylim((0,1))
    plt.xlim((0,7))
    plt.yticks([i * 0.2 for i in range(0,6)], [i * 20 for i in range(0, 6)])
    plt.xticks(range(0, core_max + 1), [2 ** i for i in range(core_max + 1)])
    plt.xlabel("Number of cores")
    plt.ylabel("Fraction of total run-time \n spent in communication (%)")
    plt.legend(loc="upper left")
    plt.tight_layout()
    plt.savefig(target_file)
def main():
    args = get_parser()
    if not os.path.isfile("strong_save.csv"):
        strong_df = get_strong_dataframe(args.fromdir, multi_index, "network")
        strong_df.to_csv("strong_save.csv")
    else:
        strong_df = pd.read_csv("./strong_save.csv", header=[0,1],index_col=0)
    get_table(strong_df)
    draw_fig3(args.storedir , strong_df, 7)
    if not os.path.isfile("weak_save.csv"):
        weak_df = get_weak_dataframe(args.fromdir,algorithm_set, "network")
        weak_df.to_csv("weak_save.csv")
    else:
        weak_df = pd.read_csv("./weak_save.csv")
    draw_fig6(args.storedir ,weak_df, 7, algorithm_set)
    if not os.path.isfile("mxx_save.csv"):
        mxx_df = get_strong_dataframe(args.fromdir, multi_index, "mxx")
        mxx_df.to_csv("mxx_save.csv")
    else:
        mxx_df = pd.read_csv("./mxx_save.csv", header=[0,1],index_col=0)
    draw_fig4(args.storedir , mxx_df.reorder_levels([1,0],axis = 1), strong_df.reorder_levels([1,0],axis = 1), 7, algorithm_set)

if __name__ == "__main__" :
    main()
