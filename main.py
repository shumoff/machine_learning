import pandas as pd
from sklearn.ensemble import RandomForestClassifier

pd.options.mode.chained_assignment = None


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

    model = RandomForestClassifier(n_estimators=536, max_depth=201)
    model.fit(X=training_dataset, y=answers)
    predictions = model.predict(target_dataset)

    with open('transport_output.txt', 'w') as f:
        for prediction in predictions:
            f.write(prediction + "\n")


if __name__ == '__main__':
    main()
