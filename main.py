import pandas as pd
import approximate_accuracy
import warnings
from sklearn.ensemble import RandomForestClassifier

warnings.filterwarnings("ignore")
pd.options.mode.chained_assignment = None


def best_params(dataset, answers, target, trees, depths):
    min_deviations = {"items": []}
    max_deviation = 0
    max_deviation_index = 0
    for tree in range(1, trees):
        for depth in range(1, depths):
            model = RandomForestClassifier(n_estimators=tree, max_depth=depth, random_state=17)
            model.fit(X=dataset, y=answers)
            predictions = model.predict(target)
            deviation = approximate_accuracy.deviation(predictions)
            if len(min_deviations["items"]) < 10:
                min_deviations["items"].append({"trees": tree, "depth": depth, "deviation": deviation})
            else:
                for index, item in enumerate(min_deviations["items"]):
                    if item["deviation"] > max_deviation:
                        max_deviation = item["deviation"]
                        max_deviation_index = index
            if max_deviation > deviation:
                min_deviations["items"][max_deviation_index] = {"trees": tree, "depth": depth, "deviation": deviation}
        print(min_deviations)
    min_deviations["items"].sort(key=lambda x: x["deviation"])
    return min_deviations


def main():
    dataset = pd.read_csv("transport_data.csv")
    dataset = dataset[dataset.label != '-']
    dataset.trans_ts = pd.to_datetime(dataset.trans_ts, unit='s')
    dataset['week_day'] = dataset.trans_ts.dt.dayofweek
    dataset['hour'] = dataset.trans_ts.dt.hour
    dataset['minute'] = dataset.trans_ts.dt.minute
    dataset['second'] = dataset.trans_ts.dt.second
    dataset = dataset.drop(['request_ts', 'trans_ts'], axis=1)
    training_dataset = dataset[dataset.label != '?'].drop('label', axis=1)
    answers = dataset[dataset.label != '?']['label']
    target_dataset = dataset[dataset.label == '?'].drop('label', axis=1)
    training_dataset.index = range(len(training_dataset))
    answers.index = range(len(answers))
    target_dataset.index = range(len(target_dataset))

    # model = RandomForestClassifier(n_estimators=536, max_depth=201, random_state=17)
    # model.fit(X=training_dataset, y=answers)
    # predictions = model.predict(target_dataset)

    params = best_params(training_dataset, answers, target_dataset, 100, 100)

    model = RandomForestClassifier(n_estimators=params["items"][0]["trees"],
                                   max_depth=params["items"][0]["depth"], random_state=17)
    model.fit(X=training_dataset, y=answers)
    predictions = model.predict(target_dataset)
    with open('transport_output.txt', 'w') as f:
        for prediction in predictions:
            f.write(prediction + "\n")
    print('Deviation: ', approximate_accuracy.deviation())


if __name__ == '__main__':
    main()
