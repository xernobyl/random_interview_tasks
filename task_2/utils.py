import typing as T
from datetime import datetime


def date_string_to_timestamp(date: str) -> float:
    "Converts a date to a unix timestamp"

    return datetime.strptime(date, "%m/%d/%Y").timestamp()


def sort_multiple(main: list[float], *lists: list[T.Any]) -> None:
    "Implements a quick sort that sorts multiple lists according to the main list."

    def _sort_multiple_split(
        min: int, max: int, main: list[float], lists: tuple[list[T.Any]]
    ) -> int:
        i = min - 1
        t = main[max]

        for j in range(min, max):
            if main[j] <= t:
                i += 1
                tmp = main[i]
                main[i] = main[j]
                main[j] = tmp

                for l in lists:
                    tmp: T.Any = l[i]
                    l[i] = l[j]
                    l[j] = tmp

        tmp = main[i + 1]
        main[i + 1] = main[max]
        main[max] = tmp

        for l in lists:
            tmp: T.Any = l[i + 1]
            l[i + 1] = l[max]
            l[max] = tmp

        return i + 1

    def _sort_multiple_aux(
        min: int, max: int, main: list[float], lists: tuple[list[T.Any]]
    ) -> None:
        if min < max:
            p = _sort_multiple_split(min, max, main, lists)
            _sort_multiple_aux(min, p - 1, main, lists)
            _sort_multiple_aux(p + 1, max, main, lists)

    return _sort_multiple_aux(0, len(main) - 1, main, lists)
