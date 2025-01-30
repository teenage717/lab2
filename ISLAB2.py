import random

def stag_hunt_strategy():
    choice = random.choice(["Stag", "Hare"])
    return choice

# Главная функция для тестирования стратегии
def main():
  
    num_rounds = 100

    for round in range(num_rounds):
       
        player1_choice = stag_hunt_strategy()
        player2_choice = stag_hunt_strategy()

        print(f"Раунд {round + 1}: Игрок 1 выбрал {player1_choice}, Игрок 2 выбрал {player2_choice}")

        # Логика для награды в зависимости от выборов игроков
        if player1_choice == "Stag" and player2_choice == "Stag":
            print("Оба игрока успешно охотятся на оленя и получают большую награду!")
        elif player1_choice == "Stag" and player2_choice == "Hare":
            print("Игрок 1 успешно охотится на оленя, но Игрок 2 охотится на зайца, поэтому охота неудачна.")
        elif player1_choice == "Hare" and player2_choice == "Stag":
            print("Игрок 1 охотится на зайца, но Игрок 2 успешно охотится на оленя, поэтому охота неудачна.")
        else:
            print("Оба игрока охотятся на зайца и получают меньшую награду.")

if __name__ == "__main__":
    main()