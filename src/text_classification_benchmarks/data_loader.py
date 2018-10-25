import numpy as np
import os
import pandas as pd
import spacy
from text_classification_benchmarks.fastai.util import fixup

nlp = spacy.load('en_core_web_sm')


def clean_data(data):
    df = data.copy()
    df = df.dropna()  # drop labels without an example utterance
    df[1] = df[1].apply(fixup)
    columns = ['label', 'utterance']
    df.columns = columns
    print('Length after cleaning data:', len(df))
    return df


def load_data():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    train_csv = current_dir + '/fastai/train.csv'
    val_csv = current_dir + '/fastai/val.csv'
    test_csv = current_dir + '/fastai/test.csv'
    classes_txt = current_dir + '/fastai/classes.txt'
    train_df = pd.read_csv(train_csv, header=None)
    val_df = pd.read_csv(val_csv, header=None)
    test_df = pd.read_csv(test_csv, header=None)
    classes = np.genfromtxt(classes_txt, dtype=str)
    print('Lengths Train: {}, Val: {}, Test: {}, Classes: {}'
          .format(len(train_df), len(val_df), len(test_df), len(classes)))
    return train_df, val_df, test_df, classes


def remove_classes_with_too_few_examples(data, min_examples=6):
    counts_by_label = data.groupby('label').utterance.count()
    excluded_labels = counts_by_label[counts_by_label < min_examples].index
    df = data[~data['label'].isin(excluded_labels)]
    print('Length after processing data:', len(df))
    return df


def tokenize(data):
    df = data.copy()
    df['tokens'] = df.utterance.apply(lambda x: [token.text for token in nlp(x)])
    df['length'] = df.tokens.apply(len)
    return df


def tokenize_text(text):
    return [token.text for token in nlp(text)]
