# -*- coding: utf-8 -*-

from collections.abc import Iterable
import copy
from itertools import combinations


indexes = range(0, 9)
candidates = range(1, 10)
partial = [[jj for jj in range(ii * 3, (ii + 1) * 3)] for ii in range(0, 3)]

def make_key_matrix(R, C):
    if not isinstance(R, Iterable): R = [R]
    if not isinstance(C, Iterable): C = [C]
    return [(r, c) for r in R for c in C]

units = make_key_matrix(indexes, indexes)
bundles_row = [make_key_matrix(r, indexes) for r in indexes]
bundles_column = [make_key_matrix(indexes, c) for c in indexes]
bundles_block = [make_key_matrix(rs, rc) for rs in partial for rc in partial]
bundles = bundles_row + bundles_column + bundles_block

# For Test
problem_test_1 = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
problem_test_2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
problem_test_3 = '.....6....59.....82....8....45........3........6..3.54...325..6..................'
problem_test_4 = '438.962.5659.324.8271458693845219367713564829926873154194325786362987541587641932'
problem_test_5 = '438..6....59.32..82.14.8.9..45........3...8....68.3.54..43257.6362...5.......193.'

problem_test_9771 = '1....84...2..3......57....2..6.....5.7.....9.4.....1..3....45......8..2...96....7'
problem_test_8752 = '1...7.....4.....9.2...49.....84.62...6....4.34.35.8.....17.3.......8..1....1..6.5'

problem_test_bug = '239146587617852934584..7126726..8415345671892198425673461283759953714268872569341'


class Sudoku(object):
    def __init__(self, sudoku=None, *args, **kwargs):
        self.sudoku = sudoku
        self.args = args
        self.kwargs = kwargs

        if sudoku is None:
            self.problem = self.convert_to_problem(problem_test_bug)
        else:
            self.problem = self.convert_to_problem(sudoku)
        self.solutions = []

    def __repr__(self):
        sudoku = self.sudoku if self.sudoku is not None else ''
        args = f'{self.args}' if len(self.args) > 0 else ''
        kwargs = f'{self.kwargs}' if len(self.kwargs) > 0 else ''
        return  f'Sudoku({sudoku}, {args}, {kwargs})'

    def convert_to_problem(self, content):
        cs = list(map(str, candidates))
        chars = [c for c in content if c in cs or c in '0.']
        ints = list(map(lambda n: int(n) if n in cs else None, chars))
        assert len(ints) == 81
        return dict(zip(units, ints))

    def remove_value(self, ps, us, vs):
        """
        remove vs in peers of us without us itself
        ps: possible solution, dict, key: tuple (3, 5), value: list [1, 7, 9]
        us: units, keys of ps, tuple [(3, 5), (3, 8)]
        vs: values, list of value [1, 7, 9]
        """
        count_removal = 0
        # related bundle
        rbs = [b for b in bundles if all(u in b for u in us)]
        rbset = set(sum(rbs, [])) - set(us)
        for rbu in rbset:
            for v in vs:
                if v in ps[rbu]:
                    ps[rbu].remove(v)
                    count_removal += 1
        return count_removal

    def solve_main(self, ps):
        """
        ps: possible solution, dict, key: tuple (3, 5), value: list [1, 7, 9]
        """
        dps = copy.deepcopy(ps)
        while True:
            total_removal = 0
            us = [u for u in dps if len(dps[u]) == 1]
            for u in us:
                total_removal += self.remove_value(dps, [u], dps[u])
            for b in bundles:
                us = [u for u in b if len(dps[u]) >= 2]
                for ii in range(2, len(us)):
                    for cs in list(combinations(us, ii)):
                        vset = set(sum([dps[u] for u in cs], []))
                        if len(vset) == ii:
                            total_removal += self.remove_value(dps, cs, list(vset))

            if any([len(dps[u]) == 0 for u in dps]):
                return
            if total_removal == 0:
                if all([len(dps[u]) == 1 for u in dps]):
                    if self.solutions == [] or all(any(dps[u] != s[u] for u in s) for s in self.solutions):
                        solution = dict((u, dps[u][0]) for u in dps)
                        self.solutions.append(solution)
                else:
                    # list total candidates
                    ltc = sum((dps[u] for u in dps), [])
                    # count per candidate
                    cpc = [ltc.count(v) for v in candidates]
                    # minimum length of candidates
                    minlen = min(len(dps[u]) for u in dps if len(dps[u]) > 1)
                    # units of minimum length
                    minlenus = [u for u in dps if len(dps[u]) == minlen]
                    # maximum of summation of count per candidate in unit
                    maxsumu = max([(sum([cpc[v] for v in u]), u) for u in minlenus])
                    for v in dps[maxsumu[1]]:
                        dps[maxsumu[1]] = [v]
                        self.solve_main(dps)
                return

    def solve(self):
        import time
        time_start = time.perf_counter()
        self.get_sudoku_board(self.problem)
        ps = dict((u, [self.problem[u]] if self.problem[u] != None else list(candidates)) for u in self.problem)
        self.solve_main(ps)
        print(f'Number of solution: {len(self.solutions)}\n')
        for solution in self.solutions:
            print(f'{self.get_sudoku_board(solution)}')
        time_end = time.perf_counter()
        print(f'perf_counter(): {time_end - time_start}')

    def validate_ss_ps(self, ss, ps):
        pass

    def get_sudoku_board(self, sudoku):
        if any(isinstance(sudoku[(0, 0)], list) for r in indexes for c in indexes):
            length = max(len(sudoku[(r, c)]) for r in indexes for c in indexes)
            content = ''
            for r in indexes:
                for c in indexes:
                    content += ''.join(list(map(str, sudoku[(r, c)])))
                    content += ' ' * (length - len(sudoku[(r, c)]) + 1)
                    content += '| ' if c in [2, 5] else '\n' if c in [8] else ''
                if r in [2, 5]:
                    content += '-' * (3 * length + 3) + '+' + '-' * (3 * length + 4) + '+' + '-' * (3 * length + 3) + '\n'
        elif any(isinstance(sudoku[(r, c)], int) for r in indexes for c in indexes):
            content = ''
            for r in indexes:
                for c in indexes:
                    content += '{0} '.format(sudoku[(r, c)]) if sudoku[(r, c)] is not None else '  '
                    content += '| ' if c in [2, 5] else '\n' if c in [8] else ''
                if r in [2, 5]:
                    content += '------+-------+------\n'
        return content

if __name__ == '__main__':
    aa = Sudoku()
    aa.solve()
