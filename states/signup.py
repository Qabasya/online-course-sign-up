from aiogram.fsm.state import State, StatesGroup


class SignUpStates(StatesGroup):
    """
    Группа состояний для процесса записи на курс.

    Порядок состояний:
    1. waiting_for_class - ожидаем класс и школу
    2. waiting_for_name - ожидаем ФИО
    3. waiting_for_contact - ожидаем контакт (телефон)
    """

    # Шаг 1: Ждём информацию о классе и школе
    waiting_for_class = State()

    # Шаг 2: Ждём ФИО пользователя
    waiting_for_name = State()

    # Шаг 3: Ждём контактные данные (номер телефона)
    waiting_for_contact = State()

