from typing import List, Tuple


def square(x):
    return x**2


def square_neg(x):
    return -1*((x-1)**2)+1


def validate_inp(inp: str):
    try:
        x = float(inp)
    except ValueError:
        return False
    if x < 0 or x > 10:
        return False
    return x


def corpus_scores(scores: List[float], corp_ids: List[int]):
    corp_scores = []
    for c in sorted(set(corp_ids)):
        cscores = [scores[i] for i in range(len(scores)) if corp_ids[i] == c]
        corp_scores.append(sum(cscores) / len(cscores))
    return corp_scores


def store_scores_to_file(sents: List[Tuple[str, str]], scores: List[float], corp_ids: List[int]=None):
    if not corp_ids:
        corp_ids = [1]*len(sents)
    corp_scores = corpus_scores(scores, corp_ids)
    with open('eval.txt', 'w') as f:
        f.write('# Corpus scores\n')
        for i, corp_score in enumerate(corp_scores):
            f.write(f'{i+1} {corp_score:.3f}\n')
        f.write('# Paraphrase scores\n')
        for i in range(len(sents)):
            f.write(f'{corp_ids[i]} {scores[i]:.3f} {sents[i][0]} ||| {sents[i][1]}\n')


def eval_cmd(sents: List[Tuple[str, str]], sim_wfunc=None, div_wfunc=None) -> List[float]:
    scores = []
    n = len(sents)
    for i, spair in enumerate(sents):
        s1, s2 = spair
        print(f'Sentence pair {i}/{n}')
        print('1.', s1)
        print('2.', s2)
        sim = False
        while not sim:
            sim = validate_inp(input('Semantic similarity [0-10]: '))
        div = False
        while not div:
            div = validate_inp(input('Lexical divergence [0-10]: '))
        sim /= 10
        if sim_wfunc:
            sim = sim_wfunc(sim)
        div /= 10
        if div_wfunc:
            div = div_wfunc(div)
        scores.append(sim*div)
    return scores


if __name__ == '__main__':
    sents = [('asdf', 'asdd'), ('wert zui', 'zui wert'), ('hhhhh', 'hh, hhhh'), ('hallo', 'guten morgen'), ('aaa bb c', 'ab bb cc')]
    corp_ids = [1,2,1,2,3]
    scores = eval_cmd(sents, square, square_neg)
    store_scores_to_file(sents, scores, corp_ids)
