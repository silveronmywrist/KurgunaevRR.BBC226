import random

class Player:
    def __init__(self):
        self.name = input("Введите имя игрока: ").strip()
        self.inventory = []
        self.health = 100
        self.coordinates = [0, 0]

    def move(self, direction):
        x, y = self.coordinates

        # Начало координат — левый верхний угол.
        if direction == "вверх":
            y -= 1
        elif direction == "вниз":
            y += 1
        elif direction == "влево":
            x -= 1
        elif direction == "вправо":
            x += 1
        else:
            print("Неверное направление.")
            return False

        if not (0 <= x < 10 and 0 <= y < 10):
            print("За границы лабиринта пройти нельзя.")
            return False

        self.coordinates = [x, y]
        return True


class Room:
    def __init__(self, name, room_type, coordinates, items=None):
        self.name = name
        self.type = room_type
        self.coordinates = coordinates
        self.items = list(items) if items is not None else []

def inventory_management(player, room):
    if not room.items:
        print("В комнате нет предметов.")
        return

    print(f"Предметы в комнате: {room.items}")

    while True:
        action = input(
            "Вы хотите взять предметы или уйти? (взять/уйти): "
        ).strip().lower()

        if action == "взять":
            player.inventory.extend(room.items)
            print(f"Вы взяли предметы: {room.items}")

            for item in room.items:
                if item == "Ключ":
                    healing = 15
                elif item == "Сокровище":
                    healing = 30
                else:
                    continue

                old_health = player.health
                player.health = min(100, player.health + healing)
                restored = player.health - old_health

                print(
                    f"{item} восстановил {restored} ХП. "
                    f"Теперь ваше здоровье: {player.health}"
                )

            room.items.clear()
            return

        elif action == "уйти":
            print("Вы решили уйти.")
            return

        else:
            print("Неверный ввод. Введите 'взять' или 'уйти'.")

def create_rooms():
    room_descriptions = [
        ("Комната с ключом", "ключ", ["Ключ"]),
        ("Комната с монстром", "монстр", ["Меч"]),
        ("Комната с сокровищем", "сокровище", ["Сокровище"]),
        ("Комната с порталом", "портал", []),
        ("Комната с ловушкой", "ловушка", []),
    ]

    available_coordinates = [
        (x, y)
        for x in range(10)
        for y in range(10)
        if (x, y) not in ((0, 0), (9, 9))
    ]

    random.shuffle(available_coordinates)
    rooms = {}

    for name, room_type, items in room_descriptions:
        count = random.randint(3, 6)

        for number in range(1, count + 1):
            coordinates = available_coordinates.pop()

            rooms[coordinates] = Room(
                name=f"{name} №{number}",
                room_type=room_type,
                coordinates=coordinates,
                items=items
            )
    return rooms

def interaction(player, room, rooms):
    while True:
        print(f'Вы вошли в комнату {room.name}')

        if room.type == 'сокровище':
            inventory_management(player, room)
            return

        elif room.type == "ключ":
            inventory_management(player, room)
            return

        elif room.type == "монстр":
            print("Монстр атакует! Вы вступили в бой.")
            player.health = max(0, player.health - 30)
            print(f"Вы потеряли 30 здоровья. Здоровье: {player.health}")

            if player.health > 0:
                print("Вы отбились от монстра.")
            return

        elif room.type == "ловушка":
            print("Вы попали в ловушку!")
            player.health = max(0, player.health - 10)
            print(f"Вы потеряли 10 здоровья. Здоровье: {player.health}")
            return

        elif room.type == "портал":
            action = input(
                "Использовать портал? (да/нет): "
            ).strip().lower()

            if action != "да":
                print("Вы остались в комнате.")
                return

            # Выбираем другую существующую комнату.
            destinations = [
                other_room
                for other_room in rooms.values()
                if other_room.coordinates != room.coordinates
            ]

            if not destinations:
                print("Нет комнат для перемещения.")
                return

            room = random.choice(destinations)
            player.coordinates = list(room.coordinates)

            print(f"Портал перенёс вас в точку {player.coordinates}.")
                  
        else:
            print("В этой комнате ничего не происходит.")
            return

print('Добро пожаловать в игру "Приключения в подземелье"!')

player1 = Player()
rooms = create_rooms()

print(f"Добро пожаловать, {player1.name}!")
print("Ваша задача: найти выход.")

while True:
    print(f"\nВаши координаты: {player1.coordinates}")

    command = input(
        "Введите направление, 'инвентарь' или 'выход': "
    ).strip().lower()

    if command == "выход":
        break

    if command == "инвентарь":
        # Вне входа в комнату доступен только просмотр.
        print(f"Ваш инвентарь: {player1.inventory}")
        continue

    if not player1.move(command):
        continue

    coordinates = tuple(player1.coordinates)

    if coordinates == (9, 9):
        print("Вы добрались до выхода! Победа!")
        break

    room = rooms.get(coordinates)

    if room is not None:
        interaction(player1, room, rooms)

        if player1.health <= 0:
            print("Вы погибли. Игра окончена.")
            break
    else:
        print("Вы находитесь в пустой клетке.")


