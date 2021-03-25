import spacy
from stemming.porter2 import stem
import itertools
import math

def steming():
    # stem("casually")
    r1 = stem("beautiful")
    r2 = stem("beautifully")
    r3 = stem("beauty")
    r4 = stem("responsibly")
    r5 = stem("responsivity")

    print("beautiful的词干：", r1)
    print("beautifully的词干：", r2)
    print("beauty的词干：", r3)
    # print("casualty的词干：", r2)
    # print("casualty的词干：", r2)


def yuanxing(nlp):
    doc = "good better best bad worse worst"

    for token in nlp(doc):
        print(str(token) + " 的原型：" + str(token.lemma_))


def cixingbiaozhu(nlp):
    sentence = "Ashok killed the snake with a stick"
    for token in nlp(sentence):
        print(str(token) + " 的词性：" + str(token.pos_))


def NER(nlp):
    sentence = "Ram of Apple Inc. travelled to Sydney on 5th October 2017"
    for token in nlp(sentence):
        print(str(token) + "：" + str(token.ent_type_))


def lemma(nlp):
    doc = "worse worst greater"
    print("词形还原：")
    for token in nlp(doc):
        print(token, token.lemma_)


def test():
    raw=['[1,2]', '[3,4]', '[4,5]']
    print(list(itertools.chain(*map(eval, raw))))

    n_s = [(1, 2), (3, 1), (4, 1)]
    print(n_s[1])
    x = n_s[1][0]
    z = n_s[1][1]
    print(x, z)

    a = 3
    b = 2
    print(math.pow(a, b))


if __name__ == "__main__":
    print(">>>BEGIN...")
    nlp = spacy.load("en_core_web_sm")

    # cixingbiaozhu(nlp)
    # yuanxing(nlp)
    test()
    print("*" * 50)
    # test(nlp)

    print(">>>END...")

