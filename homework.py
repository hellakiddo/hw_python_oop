class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type, duration,
                 distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')

    def show_training_info(self):
        pass


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * Training.LEN_STEP / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return ((self.action * Training.LEN_STEP)
                / Training.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((Running.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.action * Running.LEN_STEP / Running.M_IN_KM
                 / self.duration
                 + Running.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / Running.M_IN_KM
                * self.duration * Training.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_WEIGHT_SHIFT = 0.029
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    GET_KMH_IN_SEC = round(Training.M_IN_KM / 60 / 60, 3)
    KMH_IN_MSEC = 0.278
    CM_IN_M = 100
    EXPONENTIATION = 2

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return (((SportsWalking.CALORIES_WEIGHT_MULTIPLIER
                  * self.weight + ((SportsWalking.KMH_IN_MSEC
                                    * self.get_mean_speed())
                                   ** self.EXPONENTIATION
                                   / (self.height / SportsWalking.CM_IN_M))
                  * SportsWalking.CALORIES_SPEED_HEIGHT_MULTIPLIER
                  * self.weight) * self.duration * Training.MIN_IN_H))


class Swimming(Training):
    """Тренировка: плавание."""

    COEFFICIENT1 = 1.1
    COEFFICIENT2 = 2
    LEN_STEP = 1.38

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * Swimming.LEN_STEP / Swimming.M_IN_KM

    def get_mean_speed(self) -> float:
        return (self.lenght_pool * self.count_pool
                / Training.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.lenght_pool * self.count_pool
                 / Training.M_IN_KM / self.duration + self.COEFFICIENT1)
                * self.COEFFICIENT2
                * self.weight * self.duration)


TYPES_OF_TRAINING = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking
}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    if workout_type not in TYPES_OF_TRAINING.keys():
        print('Unknown type of training')
    else:
        return TYPES_OF_TRAINING[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    return print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
