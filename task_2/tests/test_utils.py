from utils import sort_multiple


def test_sort_multiple():
    l0 = [0.0, 2.0, 1.0]
    l1 = ["a", "c", "b"]
    l2 = ["A", "C", "B"]

    sort_multiple(l0, l1, l2)

    assert l0 == [0, 1, 2]
    assert l1 == ["a", "b", "c"]
    assert l2 == ["A", "B", "C"]
