from event_types import Event


def parse_events(events: list[Event]):
    sort_create_events(events)
    group_push_events(events)


def sort_create_events(events: list[Event]) -> None:
    '''Сортировка событий CreateEvent.

    При создании репозитория генерируются два события или три, если задать ещё тег:
    создание репозитория и создание главной ветки. Бывает, что у этих событий одна временная метка.
    И в таком случае github возвращает эти события отсортировав по имени события.
    А для корректного отображения событий важен логический порядок: репозиторий, ветка, тег.
    
    Список событий перебирается группой по три подряд идущих события. Если в этой группе есть события
    CreateEvent с одинаковой временной веткой, то эта группа сортируется.
    '''

    for index in range(2, len(events)):
        triple_e = events[index - 2:index + 1]

        triple_e_types = [e['type'] for e in triple_e]
        triple_e_dates = [e['created_at'] for e in triple_e]

        if triple_e_types.count('CreateEvent') <= 1:
            continue

        if len(set(triple_e_dates)) == 3:
            continue

        triple_e.sort(key=_get_create_event_sort_key)
        events[index - 2:index + 1] = triple_e


def _get_create_event_sort_key(event: Event) -> tuple[str, int]:
    '''Get key for sorting create events in triple.'''
    
    type_weights = {
    'tag': 0,
    'branch': 1,
    'repository': 2,
    '': 3
    }

    event_date = event['created_at']
    event_ref_type = event['payload'].get('ref_type', '')
    return event_date, type_weights[event_ref_type]


def group_push_events(events: list[Event]) -> None:
    '''Group same repository's push events.
    
    Изменяет список событий тем, что подряд идущие push события в один репозиторий заменяются кортежем,
    где первый элемент это одно из событий, второй - количество этих событий.
    
    Original events: [event, event, ...]
    Changed events: [event, (push_event, push_event_count), event, ...]
    '''

    pushevent_repo_name: str = None
    pushevent: Event
    same_event_count: int = 0
    new_events: list[Event | tuple[Event, int]] = []
    
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
    
    # Change events to new items
    events.clear()
    events.extend(new_events)
