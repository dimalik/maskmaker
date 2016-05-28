import pandas as pd

from scripts import MaskMaker


def main(wordlist, dictionary, mark):
    words = pd.read_csv(wordlist, header=None)[0].tolist()
    mm = MaskMaker(dictionary)
    df = [mm.markFromWordNet(word, mark) for word in words]
    df = [x for x in df if not isinstance(x, bool)]
    return pd.concat(df)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--wordlist',
                        help='List of words you want the masks for',
                        type=str)
    parser.add_argument(
        '-d', '--dictionary',
        help='List of dictionary words -this will be used to pull \
potential words',
        type=str,
        default='/usr/share/dict/british-english')
    parser.add_argument('-o', '--outfile', help='Output path', type=str,
                        default='out.csv')
    parser.add_argument('-m', '--mark', nargs='*',
                        help='Mark these classes from wordnet',
                        type=str)

    args = parser.parse_args()
    df = main(args.wordlist,
              args.dictionary,
              args.mark)
    df.to_csv(args.outfile)
