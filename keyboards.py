from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
  InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.callback_data import CallbackData

from model import course

menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

my_course = KeyboardButton('Мои курсы 📖')
all_courses = KeyboardButton('Все курсы 📚')

menu.add(my_course)
menu.add(all_courses)

courses_callback = CallbackData('course', 'id', 'action')

def generate_inline_courses_buttons():
  inline_buttons = InlineKeyboardMarkup()

  for key, value in course.get_all_courses().items():
    inline_buttons.add(InlineKeyboardButton(value['name'],
                                            callback_data=courses_callback.new(id=key, action='go_to_course')))

  return inline_buttons


def generate_inline_my_courses_buttons(user_id):
  inline_buttons = InlineKeyboardMarkup()

  for key, value in course.my_courses(user_id).items():
    inline_buttons.add(InlineKeyboardButton(value['name'],
                                            callback_data=courses_callback.new(id=key, action='go_to_course')))

  return inline_buttons




def generate_current_course_inline(course_id):
  inline_buttons = InlineKeyboardMarkup()

  inline_buttons.add(InlineKeyboardButton('Начать курс',
                                          callback_data=courses_callback.new(id=course_id, action='add_course')))

  return inline_buttons


def generate_manipulate_button_course(course_id):
  inline_buttons = InlineKeyboardMarkup()

  inline_buttons.add(InlineKeyboardButton('Посмотреть текущий прогресс',
                                          callback_data=courses_callback.new(id=course_id,
                                                                             action='my_course_progress')))

  inline_buttons.add(InlineKeyboardButton('Отобразить материалы',
                                          callback_data=courses_callback.new(id=course_id,
                                                                             action='my_course_materials')))

  inline_buttons.add(InlineKeyboardButton('Удалить курс',
                                          callback_data=courses_callback.new(id=course_id,
                                                                             action='remove_my_course')))

  return inline_buttons


materials_callback = CallbackData('course', 'course_id', 'material_id', 'action')


def generate_go_back_buttons(course_id):
  inline_buttons = InlineKeyboardMarkup()

  inline_buttons.add(InlineKeyboardButton('Вернуться к материалам.',
                                          callback_data=courses_callback.new(id=course_id,
                                                                             action='go_back_materials')))
  return inline_buttons


def generate_materials_buttons(user_id, course_id):
  my_materials = course.find_my_course(user_id, course_id).child('materials')

  all_materials = course.find_course_query(course_id).child('materials').get().items()

  inline_buttons = InlineKeyboardMarkup()

  for key, material in all_materials:
    is_final = ''
    if my_materials.get() != None:
      if key in list(my_materials.get().keys()):
        if my_materials.child(key).get()['is_passed']:
          is_final = ' (пройдено)'
        else:
          is_final = ' (провалено)'


    if material['type'] == 1:
      inline_buttons.add(InlineKeyboardButton('Материал: ' + material['name'] + is_final,
                                              callback_data=materials_callback.new(course_id=course_id,
                                                                                   material_id=key,
                                                                                   action='go_to_material')))
    if material['type'] == 2:
      inline_buttons.add(InlineKeyboardButton('Домащнее задание: ' + material['name'] + is_final,
                                              callback_data=materials_callback.new(course_id=course_id,
                                                                                   material_id=key,
                                                                                   action='go_to_homework')))

    if material['type'] == 3:
      inline_buttons.add(InlineKeyboardButton('Тест: ' + material['name'] + is_final,
                                              callback_data=materials_callback.new(course_id=course_id,
                                                                                   material_id=key,
                                                                                   action='go_to_test')))

  inline_buttons.add(InlineKeyboardButton('Вернуться к курсу.',
                                          callback_data=courses_callback.new(id=course_id,
                                                                               action='add_course')))

  return inline_buttons


answers_callback = CallbackData('course', 'course_id', 'material_id', 'question_id', 'answer_id', 'is_true', 'action')


def generate_answers_buttons(course_id, material_id, question_id):
  answers = course.find_course_query(course_id).child('materials').child(material_id).child('questions').child(question_id).child('answers').get()

  inline_buttons = InlineKeyboardMarkup()

  num = 1
  for key, answer in answers.items():
    inline_buttons.add(InlineKeyboardButton(str(num),
                                            callback_data=answers_callback.new(course_id=course_id,
                                                                               material_id=material_id,
                                                                               question_id=question_id,
                                                                               answer_id=key,
                                                                               is_true=answer['is_current'],
                                                                               action='set_test_answer')))
    num = num + 1

  return inline_buttons

