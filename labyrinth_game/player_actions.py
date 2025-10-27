# labyrinth_game/player_actions.py
from constants import ROOMS

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
    """Перемещение игрока"""
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]
    
    if direction in room_data['exits']:
        new_room = room_data['exits'][direction]
        game_state['current_room'] = new_room
        game_state['steps_taken'] += 1
        print(f"Вы переместились в {new_room}.")
        
        # Импортируем здесь, чтобы избежать циклических импортов
        from utils import describe_current_room
        describe_current_room(game_state)
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
    else:
        print(f"Вы не знаете, как использовать {item_name}.")