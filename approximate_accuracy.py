import csv
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

x_1_list = [30.29, 30.21, 30.29, 30.395, 30.305]
x_2_list = [30.315, 30.305, 30.305, 30.42, 30.315]
y_1_list = [59.93, 59.925, 59.942, 59.921, 59.937]
y_2_list = [59.936, 59.958, 59.955, 59.943, 59.943]

unknown_set = {"signals": []}


def square_plot(x_1, x_2, y_1, y_2, format_):
    v_y = np.arange(y_1, y_2, 0.0001)
    v_1 = [x_1] * len(v_y)
    v_2 = [x_2] * len(v_y)
    h_x = np.arange(x_1, x_2, 0.0001)
    h_1 = [y_1] * len(h_x)
    h_2 = [y_2] * len(h_x)
    plt.plot(h_x, h_1, format_, h_x, h_2, format_, v_1, v_y, format_, v_2, v_y, format_, alpha=1)


def plotting(x, y, format_, alpha):
    left_x = 30.21
    right_x = 30.45
    left_y = 59.92
    right_y = 59.96
    formats_ = ['b', 'g', 'r', 'r', 'm']
    for i in range(5):
        square_plot(x_1_list[i], x_2_list[i], y_1_list[i], y_2_list[i], formats_[i])
    plt.plot(x, y, format_, alpha=alpha)
    plt.xlim((left_x, right_x))
    plt.ylim((left_y, right_y))
    plt.xticks(np.arange(left_x, right_x, 0.005), fontsize=7)
    plt.yticks(np.arange(left_y, right_y, 0.001), fontsize=7)
    plt.tick_params('x', labelrotation=90)
    plt.grid(True)
    plt.show()


def estimate():
    unknown_signals = []
    with open("transport_data.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[-1] == '?':
                unknown_set["signals"].append(
                    {"longitude": float(row[0]), "latitude": float(row[1]), "time": float(row[3]), "label": 0})

    longitude_0 = []
    latitude_0 = []
    longitude_1 = []
    latitude_1 = []
    longitude_2 = []
    latitude_2 = []
    square_incorrect = 0
    square_signals = 0
    counter = 0
    with open("transport_output.txt", 'r') as f:
        for row in f.read():
            if row != '\n':
                unknown_set["signals"][counter]['label'] = int(row)
                unknown_signals.append(int(row))
                counter += 1

    for counter, value in enumerate(unknown_set["signals"]):
        # сначала проверка на попадание в места локализации
        # blue
        if (x_1_list[0] < value["longitude"] < x_2_list[0]) and (y_1_list[0] < value["latitude"] < y_2_list[0]):
            longitude_0.append(value["longitude"])
            latitude_0.append(value["latitude"])
            square_signals += 1
            if unknown_signals[counter] != 0:
                square_incorrect += 1
        # red
        elif ((x_1_list[2] < value["longitude"] < x_2_list[2]) and (y_1_list[2] < value["latitude"] < y_2_list[2])) or \
                ((x_1_list[3] < value["longitude"] < x_2_list[3]) and (y_1_list[3] < value["latitude"] < y_2_list[3])):
            longitude_2.append(value["longitude"])
            latitude_2.append(value["latitude"])
            square_signals += 1
            if unknown_signals[counter] != 2:
                square_incorrect += 1
        # green
        elif (x_1_list[1] < value["longitude"] < x_2_list[1]) and (y_1_list[1] < value["latitude"] < y_2_list[1]):
            longitude_1.append(value["longitude"])
            latitude_1.append(value["latitude"])
            square_signals += 1
            if unknown_signals[counter] != 1:
                square_incorrect += 1
        if unknown_signals[counter] == 0:
            longitude_0.append(value["longitude"])
            latitude_0.append(value["latitude"])
        elif unknown_signals[counter] == 1:
            longitude_1.append(value["longitude"])
            latitude_1.append(value["latitude"])
        elif unknown_signals[counter] == 2:
            longitude_2.append(value["longitude"])
            latitude_2.append(value["latitude"])

    df = pd.read_csv('transport_data.csv')
    reference_proportion = df[df['label'] != '?'][df['label'] != '-']['label'].value_counts(normalize=True)
    print(reference_proportion)
    proportions = list(reference_proportion)
    # reference_proportion_0 = reference_proportion[0]
    # reference_proportion_1 = reference_proportion[1]
    # reference_proportion_2 = reference_proportion[2]

    count_0 = 0
    count_1 = 0
    count_2 = 0
    for signal in unknown_signals:
        if signal != '\n':
            if int(signal) == 0:
                count_0 += 1
            if int(signal) == 1:
                count_1 += 1
            if int(signal) == 2:
                count_2 += 1
    proportion_0 = count_0 / 5000
    proportion_1 = count_1 / 5000
    proportion_2 = count_2 / 5000
    proportions.append(proportion_0)
    proportions.append(proportion_1)
    proportions.append(proportion_2)
    print('0 proportion: ', proportion_0, '\n1 proportion: ', proportion_1, '\n2 proportion: ', proportion_2)

    plotting(longitude_0, latitude_0, 'b.', 0.2)
    plotting(longitude_1, latitude_1, 'g.', 0.2)
    plotting(longitude_2, latitude_2, 'r.', 0.2)
    square_correct = square_signals - square_incorrect
    ratio = square_correct / square_signals
    print("Total: ", square_signals)
    print("Correct: ", square_correct)
    print("Incorrect: ", square_incorrect)
    print("Ratio: ", ratio)
    return ratio, proportions


def deviation():
    ratio, props = estimate()
    euclid = ((props[0] - props[3]) / (props[0] + props[3])) ** 2 + \
             ((props[1] - props[4]) / (props[1] + props[4])) ** 2 + \
             ((props[2] - props[5]) / (props[2] + props[5])) ** 2 + \
             ((1 - ratio) / (1 + ratio)) ** 2
    return euclid


if __name__ == '__main__':
    estimate()
