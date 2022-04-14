start_message = 'Привет, добро пожаловать в бот дополнительного образования города Москвы\.\n' \
                'Можешь написать /help чтобы узнать больше о боте\.\n' \
                'Или же /menu чтобы отобразить навигационное меню\.'

help_message = 'Данный бот разработан для "Хакатон2022" \n' \
               'start \- Зарегестрироваться и начать обучение\.\n' \
               'restart \- Удалить аккаунт\.\n' \
               'help \- Отобразить информацию и команды\.\n' \
               'menu \- Отобразить меню\.\n' \
               'all\_courses \- Отобразить все курсы\.\n' \
               'my\_courses \- Отобразить ваши курсы\.'

menu_message = 'Выберите нужный пункт\.'

user_exist_message = 'Вы уже зарегистрированы\.\n' \
                     'Вы можете сбросить прогресс /restart'

select_course_message = 'Выберите курс:'

current_course_select_message = 'Выбирите действие с курсом '

restart_message = 'Ваши данные сброшены\.\n' \
                  'Если хотите возобновить обучение /start'

course_selected_message = 'Курс выбран: '

select_material_message = 'Выбирите материал:'

homework_message = '\nВведите ответ на вопрос ниже, чтобы выйти из материала без ответа нажмите \"Вернуться к материалам\.\"'

course_removed_message = 'Курс удален'

MESSAGES = {
  'start': start_message,
  'help': help_message,
  'menu': menu_message,
  'user_exist': user_exist_message,
  'select_course': select_course_message,
  'restart': restart_message,
  'current_course_select': current_course_select_message,
  'course_selected': course_selected_message,
  'select_material': select_material_message,
  'homework': homework_message,
  'course_removed': course_removed_message,
}
