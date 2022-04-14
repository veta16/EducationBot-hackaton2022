# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import typing

import logging

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import markdown

from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from bot_messages import MESSAGES
from keyboards import menu, generate_inline_courses_buttons, courses_callback, generate_current_course_inline, \
  generate_manipulate_button_course, generate_materials_buttons, materials_callback, generate_inline_my_courses_buttons, \
  generate_go_back_buttons, generate_answers_buttons, answers_callback

from model import user, course, material

class reg(StatesGroup):
  answer = State()
  course_id = State()
  material_id = State()


with open("bot_key", "r") as file:
  bot_token = file.read()

logging.basicConfig(level=logging.INFO)

bot = Bot(bot_token, parse_mode=types.ParseMode.MARKDOWN_V2)
dp = Dispatcher(bot, storage=MemoryStorage())

dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
  await bot.send_message(message.from_user.id, user.add_new_user(message.from_user.id, message.from_user.username))


@dp.message_handler(commands=['restart'])
async def process_restart_command(message: types.Message):
  user.remove_user(message.from_user.id)

  await bot.send_message(message.from_user.id, MESSAGES['restart'])


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
  await bot.send_message(message.from_user.id, MESSAGES['help'])


@dp.message_handler(commands=['menu'])
async def process_menu_command(message: types.Message):
  await bot.send_message(message.from_user.id, MESSAGES['menu'], reply_markup=menu)


@dp.message_handler(commands=['all_courses'])
async def process_all_courses_command(message: types.Message):
  await bot.send_message(message.from_user.id, MESSAGES['select_course'],
                         reply_markup=generate_inline_courses_buttons())


@dp.message_handler(commands=['my_courses'])
async def process_my_courses_command(message: types.Message):
  await bot.send_message(message.from_user.id, MESSAGES['select_course'],
                         reply_markup=generate_inline_my_courses_buttons(str(message.from_user.id)))


@dp.callback_query_handler(courses_callback.filter(action='go_to_course'))
async def process_select_course_command(callback_query: types.callback_query, callback_data: typing.Dict[str, str]):
  await bot.send_message(callback_query.from_user.id, MESSAGES['current_course_select'] +
                         course.find_course(course_id=callback_data['id'])['name'],
                         reply_markup=generate_current_course_inline(callback_data['id']))


@dp.callback_query_handler(courses_callback.filter(action='add_course'))
async def process_add_course_command(callback_query: types.callback_query, callback_data: typing.Dict[str, str]):
  course.subscribe_course(callback_query.from_user.id, callback_data['id'])

  await bot.send_message(callback_query.from_user.id,
                         MESSAGES['course_selected'] +
                         course.find_course(course_id=callback_data['id'])['name'],
                         reply_markup=generate_manipulate_button_course(callback_data['id']))


@dp.callback_query_handler(courses_callback.filter(action='my_course_progress'))
async def process_add_course_command(callback_query: types.callback_query, callback_data: typing.Dict[str, str]):
  progress = user.find_user_qeury(callback_query.from_user.id).child('courses').child(callback_data['id']).get()[
    'progress']

  progress_list = course.find_course_query(callback_data['id']).child('progress').get().values()
  one_item = 100 / len(progress_list)

  progress_image = 0
  while progress > (1 + progress_image) * one_item:
    progress_image = progress_image + 1

  await bot.send_message(callback_query.from_user.id,
                         markdown.pre(list(progress_list)[progress_image]),
                         reply_markup=generate_manipulate_button_course(callback_data['id']))


@dp.callback_query_handler(courses_callback.filter(action='my_course_materials'))
async def process_generate_materials_buttons(callback_query: types.callback_query,
                                             callback_data: typing.Dict[str, str]):
  await bot.send_message(callback_query.from_user.id,
                         MESSAGES['select_material'],
                         reply_markup=generate_materials_buttons(callback_query.from_user.id, callback_data['id']))


@dp.callback_query_handler(materials_callback.filter(action='go_to_material'))
async def process_go_to_materials_buttons(callback_query: types.callback_query, callback_data: typing.Dict[str, str]):
  user.update_progress(callback_query.from_user.id, callback_data['course_id'], callback_data['material_id'])

  current_material = course.get_material(callback_data['course_id'], callback_data['material_id']).get()
  await bot.send_message(callback_query.from_user.id,
                         current_material['description'],
                         reply_markup=generate_materials_buttons(callback_query.from_user.id,
                                                                 callback_data['course_id']))


@dp.callback_query_handler(materials_callback.filter(action='go_to_homework'))
async def process_go_to_materials_buttons(callback_query: types.callback_query, callback_data: typing.Dict[str, str]):
  await dp.get_current().current_state().update_data(course_id=callback_data['course_id'])
  await dp.get_current().current_state().update_data(material_id=callback_data['material_id'])
  await reg.answer.set()

  current_course = course.get_material(callback_data['course_id'], callback_data['material_id']).get()
  await bot.send_message(callback_query.from_user.id,
                         current_course['description'] + MESSAGES['homework'],
                         reply_markup=generate_go_back_buttons(callback_data['course_id']))


@dp.callback_query_handler(materials_callback.filter(action='go_to_test'))
async def process_go_to_next_question_buttons(callback_query: types.callback_query, callback_data: typing.Dict[str, str]):
  current_question_key = material.get_current_question(callback_query.from_user.id, callback_data['course_id'],
                                                       callback_data['material_id'])

  if current_question_key == None:
    is_true = True
    for key, value in material.get_material_questions(callback_query.from_user.id, callback_data['course_id'], callback_data['material_id']).get().items():
      if str(value) == 'false':
        is_true = False
        break

    user.update_progress(callback_query.from_user.id, callback_data['course_id'], callback_data['material_id'], is_true)
    await bot.send_message(callback_query.from_user.id,
                           MESSAGES['select_material'],
                           reply_markup=generate_materials_buttons(callback_query.from_user.id,
                                                                   callback_data['course_id']))
  else:
    current_question = course.get_material(callback_data['course_id'], callback_data['material_id']).child(
      'questions').child(current_question_key)

    answers = course.find_course_query(callback_data['course_id']).child('materials').child(
      callback_data['material_id']).child('questions').child(current_question_key).child('answers').get()

    answer_list = []

    num = 1
    for key, answer in answers.items():
      answer_list.append(str(num) + ' ' + answer['title'])
      num = num + 1

    await bot.send_message(callback_query.from_user.id,
                           current_question.get()['title'] + '\n' + '\n'.join(answer_list),
                           reply_markup=generate_answers_buttons(callback_data['course_id'],
                                                                 callback_data['material_id'], current_question_key))


@dp.callback_query_handler(answers_callback.filter(action='set_test_answer'))
async def process_go_to_materials_buttons(callback_query: types.callback_query, callback_data: typing.Dict[str, str]):
  material.set_question_answer(callback_query.from_user.id,
                               callback_data['course_id'],
                               callback_data['material_id'],
                               callback_data['question_id'],
                               callback_data['is_true'])

  await process_go_to_next_question_buttons(callback_query, callback_data)


@dp.callback_query_handler(courses_callback.filter(action='go_back_materials'), state="*")
async def process_go_back_materials_buttons(callback_query: types.callback_query, callback_data: typing.Dict[str, str]):
  await dp.current_state().finish()

  await bot.send_message(callback_query.from_user.id,
                         MESSAGES['select_material'],
                         reply_markup=generate_materials_buttons(callback_query.from_user.id, callback_data['id']))


@dp.message_handler(state=reg.answer)
async def process_set_answer_homework(message: types.Message):
  material_data = await dp.get_current().current_state().get_data()

  user.update_progress(message.from_user.id, material_data['course_id'], material_data['material_id'])
  course.find_my_course(message.from_user.id, material_data['course_id']).child('materials').child(
    material_data['material_id']).update({"answer": message['text']})

  await dp.current_state().finish()

  await bot.send_message(message.from_user.id,
                         MESSAGES['select_material'],
                         reply_markup=generate_materials_buttons(message.from_user.id, material_data['course_id']))


@dp.callback_query_handler(courses_callback.filter(action='remove_my_course'), state="*")
async def process_remove_course(callback_query: types.callback_query, callback_data: typing.Dict[str, str]):
  course.find_my_course(callback_query.from_user.id, callback_data['id']).set({})

  await bot.send_message(callback_query.from_user.id, MESSAGES['course_removed'], reply_markup=menu)

@dp.message_handler()
async def process_button_command(message: types.Message):
  if message.text == 'Все курсы 📚':
    await process_all_courses_command(message)
  if message.text == 'Мои курсы 📖':
    await process_my_courses_command(message)


# Press the green button in the gutter to run the script.
async def shutdown(dispatcher: Dispatcher):
  await dispatcher.storage.close()
  await dispatcher.storage.wait_closed()


if __name__ == '__main__':
  print('bot started!')
  executor.start_polling(dp, on_shutdown=shutdown)
