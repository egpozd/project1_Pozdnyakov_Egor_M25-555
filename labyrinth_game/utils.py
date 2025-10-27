# labyrinth_game/utils.py
from constants import ROOMS

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
        exits_str = ", ".join([f"{dir} -> {room}" for dir, room in room_data['exits'].items()])
        print("Выходы:", exits_str)
    
    # Информация о загадке
    if room_data['puzzle']:
        print("Кажется, здесь есть загадка (используйте команду solve).")

def solve_puzzle(game_state):
    """Решение загадки в текущей комнате"""
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]
    
    if not room_data['puzzle']:
        print("Загадок здесь нет.")
        return
    
    question, answer = room_data['puzzle']
    print(f"\n{question}")
    
    user_answer = input("Ваш ответ: ").strip().lower()
    
    if user_answer == answer.lower():
        print("Верно! Загадка решена!")
        # Убираем загадку из комнаты
        room_data['puzzle'] = None
        # Добавляем награду
        if current_room == 'hall':
            print("Вы получаете ключ от сокровищницы!")
            game_state['player_inventory'].append('treasure_key')
        elif current_room == 'trap_room':
            print("Ловушка деактивирована!")
        elif current_room == 'library':
            print("Вы нашли скрытый свиток с мудростью!")
    else:
        print("Неверно. Попробуйте снова.")

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
            if user_code == answer:
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

def show_help():
    """Показать справку по командам"""
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")