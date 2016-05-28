import pandas as pd

from scripts import MaskMaker


def main():
    insight_words = pd.read_csv('data/words.csv',
                                header=None)[0].tolist()
    mm = MaskMaker('/usr/share/dict/british-english')
    df = [mm.markFromWordNet(word, ('living_thing', 'artifact',))
          for word in insight_words]
    return [x for x in df if not isinstance(x, bool)]

if __name__ == '__main__':
    df = main()
    df.to_csv('words.csv')
