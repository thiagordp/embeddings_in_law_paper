import random
import statistics

from sklearn import metrics
from sklearn.metrics import classification_report
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

from utils.constants import FONT

plt.rcParams['font.family'] = 'serif'


def evaluate_balanced_accuracy(y_true, y_pred):
    try:
        return metrics.balanced_accuracy_score(y_true, y_pred)
    except:
        return 0.0


def evaluate_accuracy(y_true, y_pred):
    try:
        return metrics.accuracy_score(y_true, y_pred)
    except:
        return 0.0


def evaluate_f_score(y_true, y_pred):
    try:
        return metrics.f1_score(y_true, y_pred, average="macro", zero_division=0)
    except:
        return 0


def confusion_matrix(y_true, y_pred):
    # try:
    return metrics.confusion_matrix(y_true, y_pred)
    # except:
    #   return 0.0


def evaluate_precision(y_true, y_pred):
    # try:
    return metrics.precision_score(y_true, y_pred, average="macro", zero_division=0)
    # except:
    #    return 0.0


def evaluate_recall(y_true, y_pred):
    # try:
    return metrics.recall_score(y_true, y_pred, average="macro", zero_division=0)
    # except:
    #    return 0.0


def evaluate_roc_auc(y_true, y_pred):
    # try:

    return 0
    # except:
    #    return 0


def full_evaluation(y_true, y_pred):
    print("================================")
    print("CLASSIFIER EVALUATION")

    print("Accuracy:         ", evaluate_accuracy(y_true, y_pred))
    print("Balanced Acc:     ", evaluate_balanced_accuracy(y_true, y_pred))
    print("F1-Score:         ", evaluate_f_score(y_true, y_pred))
    print("Precision:        ", evaluate_precision(y_true, y_pred))
    print("Recall:           ", evaluate_recall(y_true, y_pred))
    print("ROC AUC:          ", evaluate_roc_auc(y_true, y_pred))
    print("Confusion Matrix\n", confusion_matrix(y_true, y_pred))
    print("Full report:    ")

    full_report = classification_report(y_true, y_pred, zero_division=0)

    print(full_report)


def summarize_results():
    file_path = "results/full_results.csv"

    full_results_df = pd.read_csv(file_path)
    consumer_df = full_results_df[full_results_df["context"] == "consumer"]
    general_df = full_results_df[full_results_df["context"] == "general"]
    air_transport_df = full_results_df[full_results_df["context"] == "air_transport"]
    standard_df = full_results_df[full_results_df["context"] == "standard"]
    mixed_df = full_results_df[full_results_df["context"] == "mixed"]

    print("========= DESCRIBE =========")

    print("Full\n", full_results_df.describe())
    print("General\n", general_df.describe())
    print("Consumer\n", consumer_df.describe())
    print("Air transport\n", air_transport_df.describe())
    print("Standard\n", standard_df.describe())
    print("Mixed\n", mixed_df.describe())

    print("======== PROCESS ===========")
    general_acc_dict, general_f1_dict = get_acc_f1(general_df)
    consumer_acc_dict, consumer_f1_dict = get_acc_f1(consumer_df)
    air_transport_acc_dict, air_transport_f1_dict = get_acc_f1(air_transport_df)
    standard_acc_dict, standard_f1_dict = get_acc_f1(standard_df)
    mixed_acc_dict, mixed_f1_dict = get_acc_f1(mixed_df)

    print("======== PLOT ===========")
    plt.rc('xtick', labelsize=16)
    plt.rc('ytick', labelsize=16)
    plt.rc('ytick', labelsize=16)

    plot_acc_f1(general_acc_dict, consumer_acc_dict, air_transport_acc_dict, standard_acc_dict, mixed_acc_dict, True)
    plot_acc_f1(general_f1_dict, consumer_f1_dict, air_transport_f1_dict, standard_f1_dict, mixed_f1_dict, False)
    # plot_box_plot_acc_f1(general_acc_dict, consumer_acc_dict, air_transport_acc_dict, standard_acc_dict, mixed_f1_dict, True)
    # plot_box_plot_acc_f1(general_f1_dict, consumer_f1_dict, air_transport_f1_dict, standard_f1_dict, mixed_f1_dict, False)
    keys = list()
    keys.extend(general_acc_dict.keys())
    keys.extend(air_transport_acc_dict.keys())
    keys.extend(general_acc_dict.keys())
    keys = np.sort(list(set(keys)))

    air_general = []
    air_mixed = []
    for key in keys:
        print("\n" ,key)

        air = general = mixed = 0

        try:
            air = np.mean(air_transport_acc_dict[key])
        except:
            pass

        try:
            general = np.mean(general_acc_dict[key])
        except:
            pass
        try:
            mixed = np.mean(mixed_acc_dict[key])
        except:
            pass
        try:
            if key <= 100000000:
                perc_air_gen = (air / general) - 1
        except:
            perc_air_gen = 0

        try:
            perc_air_mixed = (air / mixed) - 1
        except:
            perc_air_mixed = 0


        print("Air/general:", perc_air_gen)
        print("Air/mixed:", perc_air_mixed)


def plot_acc_f1(general_dict, consumer_dict, air_transport_dict, standard_dict, mixed_dict, acc=True):
    plt.figure(figsize=(10, 7), dpi=300)
    plt.grid(True, which="both", axis="both")
    plt.xticks(rotation=30)

    if acc:
        plt_title = "Accuracy for text classification using embeddings training w/ multiple corpus sizes"
        plt_save_path = "results/acc_mean_final.pdf"
        plt_y_label = "Accuracy"
    else:
        plt_title = "F1-Score for text classification using embeddings training w/ multiple corpus sizes"
        plt_save_path = "results/f1_score_mean_final.pdf"
        plt_y_label = "F1-Score"

    markers = ["s", "o", "v"]
    i = 0
    for data_dict in [general_dict, air_transport_dict, mixed_dict]:
        x = list()
        y = list()
        for key in data_dict.keys():
            x.append(str(format(key, ',d')))

            accs = data_dict[key]
            acc_avg = np.mean(accs)
            y.append(acc_avg)

        # x_std_mean =
        # plt.title(plt_title, **FONT)

        plt.xlabel("Embeddings Corpus Size for Training", fontsize=16)
        plt.ylabel(plt_y_label, fontsize=16)
        plt.plot(x, y, marker=markers[i], linewidth=3)

    std_keys = [key for key in standard_dict.keys()]
    all_keys = list()
    all_keys.extend(general_dict.keys())
    all_keys.extend(air_transport_dict.keys())
    all_keys = np.sort(list(set(all_keys)))
    y_std_mean = [np.mean(standard_dict[std_keys[0]]) for x in range(len(all_keys))]
    x_std_means = [str(format(key, ',d')) for key in list(all_keys)]

    # plt.plot(x_std_means, y_std_mean, "--", color="gray")

    plt.legend(["General", "Air Transport", "Global"], prop={"size": 16})
    plt.tight_layout()

    plt.yticks(np.arange(0.7, 0.8, 0.01))
    plt.savefig(plt_save_path)
    plt.show()


def plot_box_plot_acc_f1(general_dict, consumer_dict, air_transport_dict, standard_dict, mixed_dict, acc=True):
    legends = ["General", "Air Transport", "Global"]
    dicts = [general_dict, air_transport_dict, mixed_dict]
    
    for i in range(len(legends)):
        plt.figure(figsize=(13, 7), dpi=300)
        plt.grid(True, which="both", axis="both")
        plt.xticks(rotation=30)

        legend = legends[i]
        data_dict = dicts[i]

        if acc:
            plt_title = "Accuracy for text classification using embeddings training w/ multiple corpus sizes (@context)"
            plt_save_path = "results/acc_boxplot_final_@.eps".replace("@", legend)
            plt_y_label = "Accuracy"
        else:
            plt_title = "F1-Score for text classification using embeddings training w/ multiple corpus sizes (@context)"
            plt_save_path = "results/f1_score_boxplot_final_@.eps".replace("@", legend)
            plt_y_label = "F1-Score"

        plt_title = plt_title.replace("@context", legend)

        x = list()
        y = list()

        for key in data_dict.keys():
            x.append(str(format(key, ',d')))
            y.append(np.array(data_dict[key]))

        std_keys = [key for key in standard_dict.keys()]
        x.append("Standard")
        y_std = standard_dict[std_keys[0]]
        y.append(y_std)

        plt.title(plt_title)

        plt.xlabel("Embeddings Corpus Size for Training", fontsize=16)
        plt.ylabel(plt_y_label, fontsize=16)
        plt.boxplot(y)
        plt.xticks()
        labels = list()
        labels.append("")
        labels.extend(x)
        plt.xticks(np.arange(len(x) + 1), labels)
        # plt.legend(legend)

        plt.yticks(np.arange(0.7, 0.85, 0.05))
        plt.tight_layout()

        plt.savefig(plt_save_path)
        plt.show()


def remove_outliers(values):
    an_array = np.array(values)
    mean = np.mean(an_array)

    standard_deviation = np.std(an_array)

    distance_from_mean = abs(an_array - mean)

    max_deviations = 2

    indexes = distance_from_mean < max_deviations * standard_deviation
    return an_array[indexes]


def get_acc_f1(df):
    corpus_sizes = df["corpus_size"].unique()
    corpus_sizes = np.sort(corpus_sizes)

    f1_avg_dict = dict()
    acc_avg_dict = dict()

    for corpus_size in corpus_sizes:
        data_df = df[df["corpus_size"] == corpus_size].head(n=200)
        f1 = np.array(data_df["f1_score"].values)
        acc = np.array(data_df["acc"].values)
        f1_avg_dict[corpus_size] = f1
        acc_avg_dict[corpus_size] = acc

    return acc_avg_dict, f1_avg_dict


def get_mean_acc_f1(df):
    corpus_sizes = df["corpus_size"].unique()
    corpus_sizes = np.sort(corpus_sizes)
    f1_avg_dict = dict()
    acc_avg_dict = dict()
    for corpus_size in corpus_sizes:
        data_df = df[df["corpus_size"] == corpus_size].head(n=200)
        f1_avg = np.mean(data_df["f1_score"].values)
        acc_avg = np.mean(data_df["acc"].values)
        f1_avg_dict[corpus_size] = f1_avg
        acc_avg_dict[corpus_size] = acc_avg

    return acc_avg_dict, f1_avg_dict


"""
def statistical_eval():
    results_training_df = pd.read_csv("results/results_training_airtransport.csv")

    corpus_sizes = np.sort(results_training_df["corpus_size"].unique())

    list_accs = list()
    dict_confidence = dict()
    for corpus_size in corpus_sizes:

        results_df = results_training_df[(results_training_df["corpus_size"] == corpus_size)]
        # print("====================================================================================================")
        # print(corpus_size)
        # print(results_df.describe())
        values = results_df["acc"].values
        # random.shuffle(values)

        final_mean = np.mean(values)
        means = list()

        for i in range(1, len(values) + 1):
            data = values[0:i]
            mean_rmse = np.mean(data)
            means.append(mean_rmse)

        list_accs.append([corpus_size, means])
        # plt.plot(means)
        # plt.plot([final_mean for x in range(len(means))])
        # plt.show()

        std_errors = list()
        for i in range(1, len(values) + 1):
            data = values[0:i]
            stderr = np.std(data) / np.sqrt(len(data))
            std_errors.append(stderr)

        # line plot of cumulative values
        # plt.plot(std_errors)
        #
        # plt.plot([0.002 for x in range(len(std_errors))], color='red')
        # plt.plot([0.002 for x in range(len(std_errors))], color='red')
        #
        # plt.show()

        means, confidence = list(), list()
        n = len(values) + 1
        for i in range(20, n):
            data = values[0:i]
            mean_rmse = np.mean(data)
            stderr = np.std(data) / np.sqrt(len(data))
            conf = stderr * 1.96
            means.append(mean_rmse)
            confidence.append(conf)
        # line plot of cumulative values
        # plt.errorbar(range(20, n), means, yerr=confidence)
        # plt.plot(range(20, n), [final_mean for x in range(len(means))], color='red')
        # plt.show()
        #
        # plt.title("Histogram (" + str(corpus_size) + " words)")
        # plt.hist(values, bins=7)
        # plt.show()

    # plt.xticks(major_ticks)
    # plt.xticks(minor_ticks)

    plt.figure(1, figsize=(12, 7), dpi=400)
    plt.grid(True, which="both", axis="both")

    for item in list_accs:
        corpus_size = item[0]
        accs = item[1]
        plot_data = [accs[-1] for i in range(len(accs))]
        plt.plot(plot_data, linestyle="--", color='lightgray')
        plt.plot(accs, label=str(format(corpus_size, ',d')))

    for item in list_accs:
        corpus_size = item[0]
        accs = item[1]

        # plt.plot([accs[-1] for i in range(len(accs))], linestyle="--", color='lightgray')
        plt.plot(accs, label=str(format(corpus_size, ',d')))

    plt.title("Acc Médio após X Experimentos")
    plt.xlabel("Experimentos")
    # plt.ylim(0.4, 0.6)
    plt.xlim(0, 500)
    # plt.yticks(np.arange(0.4, 0.6, 0.05))
    plt.ylabel("Acc")
    plt.legend()
    plt.show()

    accs = list()
    sizes = list()
    for item in list_accs:
        accs.append(item[1])
        sizes.append(str(format(item[0], ',d')))

    labels = [""]
    labels.extend(sizes)
    # labels.pop()
    # labels.append("Standard")

    plt.figure(1, figsize=(12, 7), dpi=400)
    plt.grid(True, which="both", axis="both")
    plt.boxplot(accs)
    plt.ylabel("Acc")
    plt.xlabel("Tamanho da Base de dados")
    plt.title("Boxplot de Acc para cada tamanho de base de treinamento")
    plt.xticks(np.arange(11), labels)
    plt.show()
"""
