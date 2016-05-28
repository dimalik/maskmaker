import pandas as pd

from scripts import MaskMaker


def main():
    insight_words = pd.read_csv('data/insight_words.csv',
                                header=None)[0].tolist()
    mm = MaskMaker('/usr/share/dict/british-english')
    df = pd.concat([mm.markFromWordNet(word, ('living_thing', 'artifact',))
                    for word in insight_words])
    return df

df = main()
print df
