

def prepare_questions(world_list: list[str]) -> dict:
    payload = {}
    for pair in world_list:
        pair = pair.split(" = ")
        payload[pair[0]] = payload.get(pair[0], pair[1])
    return payload


if __name__=="__main__":
    print(prepare_questions(['Белый = White', 'Желтый = Yellow', 'Красный = Red', 'Синий = Blue']))
