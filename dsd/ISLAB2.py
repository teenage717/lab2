import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier
from collections import deque

# Параметры игры
TOTAL_RESOURCES = 20  # Общее количество ресурсов (например, кусочков пиццы)
NUM_ROUNDS = 100      # Количество раундов
MEMORY_SIZE = 50      # Размер памяти для обучения нейросети

# Функция для случайного выбора
def random_strategy():
    return random.randint(0, TOTAL_RESOURCES // 2)  # Игрок берёт случайное количество ресурсов

# Функция для нейросетевой стратегии
class NeuralNetworkStrategy:
    def __init__(self):
        self.model = MLPClassifier(hidden_layer_sizes=(10,), max_iter=1000, random_state=42)
        self.memory = deque(maxlen=MEMORY_SIZE)  # Память для хранения истории игры
        self.is_trained = False  # Флаг для проверки, была ли модель обучена

    def choose_action(self, state):
        if len(self.memory) < MEMORY_SIZE // 2 or not self.is_trained:  # Если памяти мало или модель не обучена, выбираем случайное действие
            return random.randint(0, TOTAL_RESOURCES // 2)

        # Преобразуем состояние в формат для нейросети
        X = np.array([state])
        prediction = self.model.predict(X)
        return int(prediction[0])

    def remember(self, state, action, reward, next_state):
        self.memory.append((state, action, reward, next_state))

    def train(self):
        if len(self.memory) < MEMORY_SIZE:  # Обучаемся только при достаточном количестве данных
            return

        # Подготовка данных для обучения
        batch = list(self.memory)
        states = np.array([x[0] for x in batch])
        actions = np.array([x[1] for x in batch])
        rewards = np.array([x[2] for x in batch])
        next_states = np.array([x[3] for x in batch])

        # Обучаем модель
        self.model.fit(states, actions)
        self.is_trained = True  # Устанавливаем флаг, что модель обучена

# Функция для игры
def play_game():
    nn_strategy = NeuralNetworkStrategy()
    random_score = 0
    nn_score = 0
    random_scores = []
    nn_scores = []

    for round in range(NUM_ROUNDS):
        # Состояние: сколько ресурсов осталось
        remaining_resources = TOTAL_RESOURCES
        state = [remaining_resources]

        # Выбор действий игроков
        random_action = random_strategy()
        nn_action = nn_strategy.choose_action(state)

        # Проверка, чтобы сумма действий не превышала доступные ресурсы
        total_taken = random_action + nn_action
        if total_taken > remaining_resources:
            # Если ресурсов недостаточно, делим поровну
            random_action = remaining_resources // 2
            nn_action = remaining_resources // 2

        # Начисление очков
        random_score += random_action
        nn_score += nn_action

        # Обновление состояния
        remaining_resources -= (random_action + nn_action)
        next_state = [remaining_resources]

        # Нейросеть запоминает результат
        reward = nn_action  # Награда — это количество ресурсов, которые она взяла
        nn_strategy.remember(state, nn_action, reward, next_state)

        # Сохранение очков для графика
        random_scores.append(random_score)
        nn_scores.append(nn_score)

        # Обучение нейросети по итогам раунда
        nn_strategy.train()

        # Вывод результатов раунда
        print(f"Раунд {round + 1}:")
        print(f"  Random взял {random_action}, Нейросеть взяла {nn_action}")
        print(f"  Очки: Random = {random_score}, Нейросеть = {nn_score}")
        print()

    # Итоговые результаты
    print("Игра завершена!")
    print(f"Итоговые очки: Random = {random_score}, Нейросеть = {nn_score}")
    if nn_score > random_score:
        print("Нейросеть победила!")
    elif nn_score < random_score:
        print("Random победил!")
    else:
        print("Ничья!")

    # Построение графика
    plt.plot(random_scores, label='Random')
    plt.plot(nn_scores, label='Neural Network')
    plt.xlabel('Раунды')
    plt.ylabel('Очки')
    plt.title('Результаты игры')
    plt.legend()
    plt.show()

# Запуск игры
if __name__ == "__main__":
    play_game()
