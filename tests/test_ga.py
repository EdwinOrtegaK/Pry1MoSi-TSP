# tests/test_ga.py
from src.ga.operators import ox, pmx
from src.common.metrics import tour_length

def test_ox_pmx_preserve_permutation():
    p1 = list(range(20))
    p2 = list(range(19,-1,-1))
    c1 = ox(p1, p2)
    c2 = pmx(p1, p2)
    assert sorted(c1) == list(range(20))
    assert sorted(c2) == list(range(20))
    assert len(set(c1)) == 20
    assert len(set(c2)) == 20

def test_tour_length_wraps_cycle():
    coords = [(0,0), (1,0), (1,1), (0,1)]  # cuadrado lado 1
    order = [0,1,2,3]
    # perímetro = 4
    assert abs(tour_length(order, coords) - 4.0) < 1e-6

def test_pmx_valid_permutation_and_differs():
    from src.ga.operators import pmx
    p1 = list(range(20))
    p2 = list(range(19, -1, -1))
    child = pmx(p1, p2)
    assert sorted(child) == sorted(p1)  # misma multiconjunto
    assert child != p1 and child != p2  # no calcado

