from utils import ValidationError


class Template(object):

    @staticmethod  # rename that one
    def _hasConsecutive(pattern, n=3):
        return all([len(set(pattern[i:i+n])) != 1
                    for i in range(0, len(pattern) - (n-1))])

    @staticmethod
    def _is_derivation(word1, word2):
        """Checks whether word1 could have been derived from word2.

        Attributes:
            word1 (str): the target word (e.g. alligator)
            word2 (str): the template (e.g. a__ig_tor)
        """
        if len(word1) != len(word2):
            False
        else:
            return all([True if word1[i] == word2[i] or
                        word2[i] == '_' else False
                        for i in range(len(word1))])

    def validate(self):
        raise NotImplementedError


class BinaryTemplate(Template):
    def __init__(self, pattern, consecutive=3):
        self.pattern = pattern
        self.consecutive = consecutive
        self.validate()

    def derivation(self, word, masked):
        return self._is_derivation(word, self.mask(masked))

    def mask(self, word):
        """Returns a template given a binary filter.

        Attributes:
            word (str):
        """
        return ''.join([word[i] if self.pattern[i] else '_'
                        for i in range(len(word))])

    def validate(self):
        """ Performs some routine checks on the input."""
        if sum(self.pattern) <= (len(self.pattern) / 2):
            raise ValidationError('More empty spaces than actual letters')
        if not self._hasConsecutive(self.pattern, self.consecutive):
            raise ValidationError('Large n-grams found')

if __name__ == '__main__':
    bt = BinaryTemplate((1, 1, 0, 0, 1, 0, 1, 0, ))
    bt.derivation('abcdefgh', 'abcdefgh')  # True
    bt.derivation('abcdefgh', 'abgdefgh')  # Also true
