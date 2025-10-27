#!/usr/bin/env python3

#def main():
#    print("Первая попытка запустить проект!")

#if __name__ == "__main__":
#    main()



# labyrinth_game/main.py
from constants import ROOMS, COMMANDS
from player_actions import move_player, take_item, show_inventory, use_item, get_input
from utils import describe_current_room, solve_puzzle, attempt_open_treasure, show_help

# Состояние игры
game_state = {
    'player_inventory': [],
    'current_room': 'entrance',
    'game_over': False,
    'steps_taken': 0
}

def process_command(game_state, command):
    """Обработка команд пользователя с поддержкой односложных команд движения"""
    parts = command.split()
    if not parts:
        return
    
    cmd = parts[0]
    arg = " ".join(parts[1:]) if len(parts) > 1 else ""
    
    # Обработка односложных команд движения
    if cmd in ['north', 'south', 'east', 'west']:
        move_player(game_state, cmd)
        return
    
    match cmd:
        case 'look':
            describe_current_room(game_state)
        
        case 'go' | 'move':
            if arg in ['north', 'south', 'east', 'west']:
                move_player(game_state, arg)
            else:
                print("Укажите направление: north, south, east, west")
        
        case 'take' | 'get':
            if arg:
                take_item(game_state, arg)
            else:
                print("Укажите предмет для взятия.")
        
        case 'use':
            if arg:
                use_item(game_state, arg)
            else:
                print("Укажите предмет для использования.")
        
        case 'inventory' | 'inv':
            show_inventory(game_state)
        
        case 'solve':
            # В treasure_room используем attempt_open_treasure вместо solve_puzzle
            if game_state['current_room'] == 'treasure_room':
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        
        case 'help':
            show_help(COMMANDS)
        
        case 'quit' | 'exit':
            print("Спасибо за игру!")
            game_state['game_over'] = True
        
        case _:
            print("Неизвестная команда. Введите 'help' для справки.")

def main():
    """Основная функция игры"""
    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)
    
    while not game_state['game_over']:
        command = get_input("\nЧто вы хотите сделать? ")
        process_command(game_state, command)
    
    print(f"\nИгра завершена. Вы сделали {game_state['steps_taken']} шагов.")

if __name__ == "__main__":
    main()