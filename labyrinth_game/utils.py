# labyrinth_game/utils.py
import math

from constants import ROOMS


def pseudo_random(seed, modulo):
    """Псевдослучайный генератор на основе синуса"""
    x = math.sin(seed * 12.9898) * 43758.5453
    fractional_part = x - math.floor(x)
    result = fractional_part * modulo
    return int(result)


def trigger_trap(game_state):
    """Активация ловушки"""
    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state['player_inventory']

    if inventory:
        # Выбираем случайный предмет для потери
        item_index = pseudo_random(game_state['steps_taken'], len(inventory))
        lost_item = inventory.pop(item_index)
        print(f"Из-за тряски вы теряете: {lost_item}")
    else:
        # Если инвентарь пуст - проверяем получение урона
        damage_chance = pseudo_random(game_state['steps_taken'], 10)
        if damage_chance < 3:
            print("Ловушка наносит вам смертельный урон! Игра окончена.")
            game_state['game_over'] = True
        else:
            print("Вам удалось увернуться от ловушки!")


def random_event(game_state):
    """Случайные события при перемещении"""
    # Проверяем, произойдет ли событие (10% вероятность)
    event_chance = pseudo_random(game_state['steps_taken'], 10)

    if event_chance == 0:
        # Выбираем тип события
        event_type = pseudo_random(game_state['steps_taken'] + 1, 3)
        current_room = game_state['current_room']
        room_data = ROOMS[current_room]

        if event_type == 0:
            # Находка
            print("\nНа полу вы замечаете блестящую монетку!")
            if 'coin' not in room_data['items']:
                room_data['items'].append('coin')

        elif event_type == 1:
            # Испуг
            print("\nВы слышите странный шорох из темноты...")
            if 'sword' in game_state['player_inventory']:
                print("Вы достаете меч, и шорох мгновенно прекращается.")
            else:
                print("Шорох становится громче... Вам становится не по себе.")

        elif event_type == 2:
            # Ловушка
            trap_conditions = (
                current_room == 'trap_room' and
                'torch' not in game_state['player_inventory']
            )
            if trap_conditions:
                print("\nВ темноте вы не заметили ловушку!")
                trigger_trap(game_state)


def describe_current_room(game_state):
    """Описание текущей комнаты"""
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]

    print(f"\n== {current_room.upper()} ==")
    print(room_data['description'])

    # Вывод предметов
    if room_data['items']:
        print("Заметные предметы:", ", ".join(room_data['items']))

    # Вывод выходов
    if room_data['exits']:
        exits_list = [
            f"{direction} -> {room}"
            for direction, room in room_data['exits'].items()
        ]
        exits_str = ", ".join(exits_list)
        print("Выходы:", exits_str)

    # Информация о загадке
    if room_data['puzzle']:
        print("Кажется, здесь есть загадка (используйте команду solve).")


def solve_puzzle(game_state):
    """Решение загадки в текущей комнате с альтернативными ответами"""
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]

    if not room_data['puzzle']:
        print("Загадок здесь нет.")
        return

    question, answer = room_data['puzzle']
    print(f"\n{question}")

    user_answer = input("Ваш ответ: ").strip().lower()

    # Создаем список альтернативных ответов
    alternative_answers = [answer.lower()]

    # Добавляем альтернативные варианты для числовых ответов
    if answer == '10':
        alternative_answers.extend(['десять', '10'])
    elif answer == 'шаг шаг шаг':
        alternative_answers.extend(['шагшагшаг', 'step step step'])
    elif answer == 'резонанс':
        alternative_answers.extend(['resonance'])

    if user_answer in alternative_answers:
        print("Верно! Загадка решена!")
        # Убираем загадку из комнаты
        room_data['puzzle'] = None

        # Награда в зависимости от комнаты
        if current_room == 'hall':
            print("Вы получаете ключ от сокровищницы!")
            game_state['player_inventory'].append('treasure_key')
        elif current_room == 'trap_room':
            print("Ловушка деактивирована! Теперь вы можете безопасно перемещаться.")
        elif current_room == 'library':
            print("Вы нашли скрытый свиток с мудростью!")
            game_state['player_inventory'].append('wisdom_scroll')
    else:
        print("Неверно. Попробуйте снова.")
        # Особый случай для trap_room - активация ловушки при неверном ответе
        if current_room == 'trap_room':
            print("Неверный ответ активирует ловушку!")
            trigger_trap(game_state)


def attempt_open_treasure(game_state):
    """Попытка открыть сундук с сокровищами"""
    current_room = game_state['current_room']

    if current_room != 'treasure_room':
        print("Здесь нет сундука с сокровищами.")
        return

    room_data = ROOMS[current_room]

    # Проверка ключа
    if 'treasure_key' in game_state['player_inventory']:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        if 'treasure_chest' in room_data['items']:
            room_data['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return

    # Предложение ввести код
    print("Сундук заперт. У вас нет ключа. Ввести код? (да/нет)")
    choice = input("> ").strip().lower()

    if choice == 'да':
        if room_data['puzzle']:
            _, answer = room_data['puzzle']
            user_code = input("Введите код: ").strip()
            # Альтернативные варианты для кода
            code_correct = (
                user_code == answer or
                (answer == '10' and user_code.lower() == 'десять')
            )
            if code_correct:
                print("Замок щёлкает! Сундук открыт!")
                if 'treasure_chest' in room_data['items']:
                    room_data['items'].remove('treasure_chest')
                print("В сундуке сокровище! Вы победили!")
                game_state['game_over'] = True
            else:
                print("Неверный код. Замок не поддается.")
        else:
            print("Загадка уже решена, но код не подошел.")
    else:
        print("Вы отступаете от сундука.")


def show_help(commands):
    """Показать справку по командам с красивым форматированием"""
    print("\nДоступные команды:")
    for command, description in commands.items():
        print(f"  {command:<16} - {description}")