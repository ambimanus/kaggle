import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier


def read_and_clean(filename):
    df = pd.read_csv(filename, header=0)
    # Embarked: Fill NaN with most common value (here: 'S')
    embarked_fill = df['Embarked'].value_counts().index[0]
    df['Embarked'] = df['Embarked'].fillna(embarked_fill)
    # Embarked: Convert to numerical value
    df['Embarked'] = df['Embarked'].map({'C': 0, 'S': 1, 'Q': 2}).astype(int)
    # Same for Sex:
    df['Sex'] = df['Sex'].map({'female': 0, 'male': 1}).astype(int)
    # Age: Fill NaN with median age in each PClass with respect to Sex:
    # TODO: Include title information from Name as indicator for child/grown-up
    for sex in range(2):
        for pclass in range(1, 4):
            df.loc[(df['Age'].isnull()) &
                   (df['Sex'] == sex) &
                   (df['Pclass'] == pclass), 'Age'] = \
                df[(df['Sex'] == sex) &
                   (df['Pclass'] == pclass)]['Age'].dropna().median()
    # Similar for Fare, but also including Embarked:
    # TODO: Should also include binned age
    for sex in range(2):
        for pclass in range(1, 4):
            for embarked in range(3):
                df.loc[(df['Fare'].isnull()) &
                       (df['Sex'] == sex) &
                       (df['Pclass'] == pclass) &
                       (df['Embarked'] == embarked), 'Fare'] = \
                    df[(df['Sex'] == sex) &
                       (df['Pclass'] == pclass) &
                       (df['Embarked'] == embarked)]['Fare'].dropna().median()
    # TODO: Convert Age to categorical values
    # print df['Age'].value_counts(dropna=False)
    # print df['Age'].value_counts(bins=10, sort=False)
    # TODO: Create categorical 'Title' variable derived from Name
    # Drop non-numeric, non-categorical data
    df = df.drop(['Name', 'Ticket', 'Cabin'], axis=1)
    # Extract passenger ids
    ids = df['PassengerId'].values
    df = df.drop('PassengerId', axis=1)
    return df, ids


if __name__ == '__main__':
    # Training data
    df_train, _ = read_and_clean('train.csv')
    df_train.info()
    train = df_train.values
    forest = RandomForestClassifier(n_estimators=100)
    fit = forest.fit(train[:, 1:], train[:, 0])

    # Test data
    df_test, ids = read_and_clean('test.csv')
    df_test.info()

    # Prediction
    prediction = np.array(fit.predict(df_test.values), dtype=int)
    out = np.stack((np.array(ids, dtype=int), prediction), axis=-1)
    np.savetxt('prediction.csv', out, fmt='%d', delimiter=',',
               header='PassengerId,Survived', comments='')
