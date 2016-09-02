import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt


if __name__ == '__main__':
    df = pd.read_csv('train.csv', header=0)
    # Drop non-numeric, non-categorical data
    df = df.drop(['Name', 'Ticket', 'Cabin'], axis=1)
    # Embarked: Fill NaN with most common value (here: 'S')
    embarked_fill = df['Embarked'].value_counts().index[0]
    df['Embarked'] = df['Embarked'].fillna(embarked_fill)
    # Embarked: Convert to numerical value
    df['Embarked'] = df['Embarked'].map({'C': 0, 'S': 1, 'Q': 2}).astype(int)
    # Same for Sex:
    df['Sex'] = df['Sex'].map({'female': 0, 'male': 1}).astype(int)
    # Age: Fill NaN with median age in each PClass with respect to Sex:
    for sex in range(2):
        for pclass in range(1, 4):
            df.loc[(df['Age'].isnull()) &
                   (df['Sex'] == sex) &
                   (df['Pclass'] == pclass), 'Age'] = \
                df[(df['Sex'] == sex) &
                   (df['Pclass'] == pclass)]['Age'].dropna().median()

    # print df['Age'].value_counts(dropna=False)
    # print df['Age'].value_counts(bins=10, sort=False)
    # df.info()

    # train_data = df.values
    # print train_data
