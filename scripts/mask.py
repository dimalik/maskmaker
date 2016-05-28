import itertools

import pandas as pd

from cached_property import cached_property
import editdistance

from utils import ValidationError, Memoized
from templates import BinaryTemplate
from wordnet_class import getWordNetClass


class MaskMaker(object):
    """Create masked versions of words.

    This class defines a set of methods to create masked versions of
    words (using makeDerivs) to be used in psychology experiments.
    The methods take into account the possible words with which
    the target word could be confused with.

    For example, given _alligator_ as the target word the masks


    Attributes:
        wordlist (str): path to a dictionary (to be used for lookup)
    """

    def __init__(self, wordlist_path):
        self.wordlist_path = wordlist_path

    @cached_property
    def wordlist(self):
        """This is the internal dictionary of words."""
        return pd.read_csv(self.wordlist_path,
                           header=None,
                           keep_default_na=False)[0].tolist()

    @Memoized
    def getNWordlist(self, n):
        return [x for x in self.wordlist if len(x) == n]

    @Memoized
    def getMasks(self, wordlength=4, n=3):
        ans = []
        for x in itertools.product([0, 1], repeat=wordlength):
            try:
                ans.append(BinaryTemplate(x))
            except ValidationError:
                continue
        return ans

    def makeMasks(self, word):
        length = len(word)
        masked = self.getMasks(length)
        df = []

        for word1, mask in itertools.product(self.getNWordlist(length),
                                             masked):
            if mask.derivation(word1, word) and word1 != word:
                df.append(tuple([mask.mask(word), word1, word,
                                 editdistance.eval(word, word1)]))
        return pd.DataFrame(df)

    def markFromWordNet(self, word, keep_ss=False):
        try:
            df = self.makeMasks(word)
            df['word_net'] = [getWordNetClass(x, keep_ss) for x in df[1]]
            return df
        except KeyError:
            print 'No suggestions for %s' % word
            return False

if __name__ == '__main__':
    mm = MaskMaker('/usr/share/dict/british-english')
    mm.markFromWordNet('alligator', ('living_thing', 'artifact',))
