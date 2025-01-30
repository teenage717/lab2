import random
from sklearn.neural_network import MLPClassifier
import numpy as np
import matplotlib.pyplot as plt

# Функция для стратегии случайного выбора
def stag_hunt_strategy():
    choice = random.choice(["Stag", "Hare"])
    return choice

# Функция для преобразования строк в числа
def encode_choice(choice):
    return 0 if choice == "Stag" else 1

# Функция для преобразования чисел в строки
def decode_choice(encoded_choice):
    return "Stag" if encoded_choice == 0 else "Hare"

# Функция для стратегии нейросети
def neural_network_strategy(history):
    if len(history) < 2:  # Нужно хотя бы два элемента для обучения
        return random.choice(["Stag", "Hare"])
    
    # Преобразуем историю в признаки и метки
    X = []
    y = []
    for i in range(1, len(history)):
        X.append([encode_choice(history[i-1][0]), encode_choice(history[i-1][1])])
        y.append(encode_choice(history[i][1]))
    
    X = np.array(X)
    y = np.array(y)
    
    # Обучаем модель
    model = MLPClassifier(hidden_layer_sizes=(10,), max_iter=1000)
    model.fit(X, y)
    
    # Предсказываем следующий выбор
    last_round = history[-1]
    prediction = model.predict([[encode_choice(last_round[0]), encode_choice(last_round[1])]])
    return decode_choice(prediction[0])

# Главная функция для тестирования стратегии
def main():
    num_rounds = 30
    history = []
    results = {
        "Both Stag": 0,  # Оба выбрали Stag
        "Both Hare": 0,  # Оба выбрали Hare
        "Player1 Stag, Player2 Hare": 0,  # Игрок 1 выбрал Stag, Игрок 2 выбрал Hare
        "Player1 Hare, Player2 Stag": 0,  # Игрок 1 выбрал Hare, Игрок 2 выбрал Stag
    }

    # Очки игроков
    player1_score = 0
    player2_score = 0

    for round in range(num_rounds):
        player1_choice = stag_hunt_strategy()
        
        # Игрок 2 использует нейросеть для выбора
        player2_choice = neural_network_strategy(history)

        print(f"Раунд {round + 1}: Игрок 1 выбрал {player1_choice}, Игрок 2 выбрал {player2_choice}")

        # Логика для начисления очков
        if player1_choice == "Stag" and player2_choice == "Stag":
            print("Оба игрока успешно охотятся на оленя и получают по 4 очка!")
            player1_score += 4
            player2_score += 4
            results["Both Stag"] += 1
        elif player1_choice == "Stag" and player2_choice == "Hare":
            print("Игрок 1 выбрал оленя, но Игрок 2 выбрал зайца. Игрок 2 получает 3 очка, Игрок 1 — 0.")
            player2_score += 3
            results["Player1 Stag, Player2 Hare"] += 1
        elif player1_choice == "Hare" and player2_choice == "Stag":
            print("Игрок 1 выбрал зайца, но Игрок 2 выбрал оленя. Игрок 1 получает 3 очка, Игрок 2 — 0.")
            player1_score += 3
            results["Player1 Hare, Player2 Stag"] += 1
        else:
            print("Оба игрока выбрали зайца и получают по 2 очка.")
            player1_score += 2
            player2_score += 2
            results["Both Hare"] += 1

        # Обновляем историю
        history.append((player1_choice, player2_choice))

    # Вывод статистики
    print("\nСтатистика за все раунды:")
    for key, value in results.items():
        print(f"{key}: {value} раз")

    # Вывод итоговых очков
    print(f"\nИтоговые очки:")
    print(f"Игрок 1: {player1_score} очков")
    print(f"Игрок 2: {player2_score} очков")

    # Построение графика
    labels = list(results.keys())
    values = list(results.values())

    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color=['blue', 'green', 'red', 'purple'])
    plt.title("Результаты игры 'Охота на оленя'")
    plt.xlabel("Тип исхода")
    plt.ylabel("Количество раз")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()