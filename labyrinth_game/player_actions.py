# labyrinth_game/player_actions.py
from constants import ROOMS
from utils import random_event

def show_inventory(game_state):
    """Показать инвентарь игрока"""
    inventory = game_state['player_inventory']
    if inventory:
        print("\nВаш инвентарь:", ", ".join(inventory))
    else:
        print("\nВаш инвентарь пуст.")

def get_input(prompt="> "):
    """Безопасный ввод пользователя"""
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def move_player(game_state, direction):
    """Перемещение игрока с проверкой доступа к treasure_room"""
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]
    
    if direction in room_data['exits']:
        new_room = room_data['exits'][direction]
        
        # Особенная проверка для перехода в treasure_room
        if new_room == 'treasure_room':
            if 'rusty_key' in game_state['player_inventory']:
                print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.")
                game_state['current_room'] = new_room
                game_state['steps_taken'] += 1
            else:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
                return
        else:
            game_state['current_room'] = new_room
            game_state['steps_taken'] += 1
        
        print(f"Вы переместились в {new_room}.")
        
        # Импортируем здесь, чтобы избежать циклических импортов
        from utils import describe_current_room
        describe_current_room(game_state)
        
        # Вызываем случайное событие после перемещения
        random_event(game_state)
    else:
        print("Нельзя пойти в этом направлении.")

def take_item(game_state, item_name):
    """Взять предмет из комнаты"""
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]
    
    if item_name == 'treasure_chest':
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return
    
    if item_name in room_data['items']:
        room_data['items'].remove(item_name)
        game_state['player_inventory'].append(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state, item_name):
    """Использовать предмет из инвентаря"""
    if item_name not in game_state['player_inventory']:
        print("У вас нет такого предмета.")
        return
    
    if item_name == 'torch':
        print("Вы зажигаете факел. Стало светлее.")
    elif item_name == 'sword':
        print("Вы размахиваете мечом. Чувствуете себя увереннее.")
    elif item_name == 'bronze_box':
        if 'rusty_key' not in game_state['player_inventory']:
            print("Вы открываете бронзовую шкатулку. Внутри вы находите ржавый ключ!")
            game_state['player_inventory'].append('rusty_key')
        else:
            print("Шкатулка пуста.")
    elif item_name == 'coin':
        print("Вы подбрасываете монетку. Она блестит в свете факела.")
    elif item_name == 'wisdom_scroll':
        print("Вы читаете свиток: 'Мудрость - это понимание того, что ключ не всегда открывает то, что ожидаешь'")
    else:
        print(f"Вы не знаете, как использовать {item_name}.")