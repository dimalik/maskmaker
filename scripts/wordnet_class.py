import collections

from nltk.corpus import wordnet as wn


class MySynset(object):
    def __init__(self, synset):
        self.synset = wn.synset(synset)

    def flatten(self, l):
        for el in l:
            if isinstance(el, collections.Iterable) and not isinstance(
                    el, basestring):
                for sub in self.flatten(el):
                    yield sub
            else:
                yield el

    @staticmethod
    def hyp(s):
        return s.hypernyms()

    def get_hypernyms(self):
        hyps = self.synset.tree(self.hyp)
        return list(set([x.name() for x in self.flatten(hyps)]))


def getWordNetClass(word, possibilities=None):
    if not possibilities:
        raise ValueError('Please provide a list of possibilities')
    try:
        ss = wn.synsets(word, pos=wn.NOUN)
    except:
        return False
    ll = [MySynset(synset.name()).get_hypernyms() for synset in ss]
    for l in ll:
        feats = [x.split('.')[0] for x in l]
        for p in possibilities:
            if p in feats:
                return p
    return False
