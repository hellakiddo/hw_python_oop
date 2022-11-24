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
        LEN_STEP = 0.65
        M_IN_KM = 1000

        distance = self.action * LEN_STEP / M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        LEN_STEP = 0.65
        M_IN_KM = 1000

        speed = self.action * LEN_STEP / M_IN_KM / self.duration
        return speed

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
    LEN_STEP = 0.65
    M_IN_KM = 1000
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79
    MIN = 60

    def __init__(self, action, duration, weight):
        super().__init__(action, duration, weight)
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        calories = ((Running.CALORIES_MEAN_SPEED_MULTIPLIER
                     * self.action * Running.LEN_STEP / Running.M_IN_KM
                     / self.duration
                     + Running.CALORIES_MEAN_SPEED_SHIFT)
                    * self.weight / Running.M_IN_KM * Running.MIN)
        return calories

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_WEIGHT_SHIFT = 0.029
    LEN_STEP = 0.65
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC = 0.278
    CM_IN_M = 100
    MIN = 60

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        calories = (((SportsWalking.CALORIES_WEIGHT_MULTIPLIER
                      * self.weight + (SportsWalking.KMH_IN_MSEC
                                       ** 2 / self.height / SportsWalking.CM_IN_M)
                      * SportsWalking.CALORIES_SPEED_HEIGHT_MULTIPLIER
                      * self.weight) * self.duration * SportsWalking.MIN))

        return calories

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Swimming(Training):
    """Тренировка: плавание."""
    CF1 = 1.1
    CF2 = 2
    LEN_STEP = 1.38
    M_IN_KM = 1000

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        distance = self.action * Swimming.LEN_STEP / Swimming.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        M_IN_KM = 1000

        average_swim_speed = (self.lenght_pool * self.count_pool
                              / M_IN_KM / self.duration)
        return average_swim_speed

    def get_spent_calories(self) -> float:
        CF1 = 1.1
        CF2 = 2
        M_IN_KM = 1000

        calories = ((self.lenght_pool * self.count_pool
                     / M_IN_KM / self.duration + CF1) * CF2
                    * self.weight * self.duration)
        return calories

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    train_dict = {'SWM': Swimming,
                  'RUN': Running,
                  'WLK': SportsWalking
                  }

    train_type = train_dict[workout_type](*data)
    return train_type


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info().get_message()

    return print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
