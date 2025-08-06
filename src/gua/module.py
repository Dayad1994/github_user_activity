from collections import defaultdict

from gua.typing import Event, GroupedEvents


def parse_events(events: GroupedEvents) -> None:
    """Sorting and grouping original event list."""
    sort_create_events(events)
    group_push_events(events)


def sort_create_events(events: GroupedEvents) -> None:
    """Сортировка событий CreateEvent.

    При создании репозитория генерируются два события или
    три, если задать ещё тег: создание репозитория и создание главной ветки.
    Бывает, что у этих событий одна временная метка. И в таком случае github
    возвращает эти события отсортировав по имени события.
    А для корректного отображения событий важен логический порядок:
    репозиторий, ветка, тег.
    
    Список событий перебирается группой по три подряд идущих события.
    Если в этой группе есть события CreateEvent с одинаковой временной меткой,
    то эта группа сортируется.
    """
    for index in range(2, len(events)):
        triple_e = events[index - 2:index + 1]

        # Фильтруем create events в тройке
        create_events = [
            (i, e) for i, e in enumerate(triple_e) if e['type'] == 'CreateEvent'
            ]

        if len(create_events) <= 1:
            continue

        # Группируем create_events по дате
        date_groups = defaultdict(list)
        for i, e in create_events:
            date_groups[e['created_at']].append((i, e))

        # Обрабатываем те группы, где 2 и более события с одинаковой датой
        triple_e_list = list(triple_e)

        for same_date_events in date_groups.values():
            if len(same_date_events) < 2:
                continue

            sorted_group = sorted(
                same_date_events,
                key=lambda pair: get_create_event_sort_key(pair[1]))

            # меняем местами в triple_e_list только в позициях этой группы
            for (pos, _), (_, sorted_event) in zip(
                same_date_events,
                sorted_group,
                strict=False
                ):
                triple_e_list[pos] = sorted_event

        # Записываем обратно в исходный список
        events[index - 2:index + 1] = triple_e_list


def get_create_event_sort_key(event: Event) -> tuple[str, int]:
    """Get key for sorting create events in triple."""
    type_weights = {
    'tag': 0,
    'branch': 1,
    'repository': 2,
    '': 3
    }

    event_date = event['created_at']
    event_ref_type = event['payload'].get('ref_type', '')
    return event_date, type_weights[event_ref_type]


def group_push_events(events: GroupedEvents) -> None:
    """Group same repository's push events.
    
    Изменяет список событий тем,
    что подряд идущие push события в один репозиторий заменяются кортежем,
    где первый элемент это одно из событий,
    второй - количество этих событий.
    
    Original events: [event, event, ...]
    Changed events: [event, (push_event, push_event_count), event, ...]
    """
    pushevent_repo_name: str | None = None
    pushevent: Event | None = None
    same_event_count: int = 0
    new_events: GroupedEvents = []
    
    for index in range(len(events)):
        event = events[index]
        if event['type'] == 'PushEvent':
            if pushevent_repo_name == event['repo']['name']:
                same_event_count += 1
            else:
                if same_event_count:
                    new_events.append((pushevent, same_event_count))
                same_event_count = 1
                pushevent_repo_name = event['repo']['name']
                pushevent = event
        else:
            if same_event_count:
                    new_events.append((pushevent, same_event_count))
            same_event_count = 0
            pushevent_repo_name = None
            new_events.append(event)
    if same_event_count:
        new_events.append((pushevent, same_event_count))

    # Change events to new items
    events.clear()
    events.extend(new_events)
