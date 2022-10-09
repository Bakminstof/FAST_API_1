from typing import Dict, List


def sort(data) -> List[Dict[str, str | int]]:
    items = [
        {
            'id': row[0].id,
            'name': row[0].name,
            'cooking_time': row[0].cooking_time,
            'views': row[0].views,
        } for row in data
    ]

    lst_val = 0
    start_index = None

    for i, item in enumerate(items):
        current_views = item.get('views')

        if current_views == lst_val:
            if i == len(items) - 1:
                _insertion_sort_(items, start_index, i + 1)

                start_index = None

            if not start_index:
                if i:
                    start_index = i - 1
                else:
                    start_index = i

        else:
            if start_index:
                _insertion_sort_(items, start_index, i + 1)

                start_index = None

        lst_val = current_views

    return items


def _insertion_sort_(items: List[Dict[str, str | int]], start: int, finish: int):
    to_sort_part = items[start:finish]

    for i_, el in enumerate(to_sort_part):
        cur = el.get('cooking_time')
        pos = i_

        while pos > 0 and to_sort_part[pos - 1].get('cooking_time') > cur:
            to_sort_part[pos] = to_sort_part[pos - 1]
            pos = pos - 1

        to_sort_part[pos] = el

    items[start:finish] = to_sort_part
