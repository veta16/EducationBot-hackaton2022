from model import course, user


def get_material_questions(user_id, course_id, material_id):
  return course.find_my_course(user_id, course_id).child('materials').child(material_id).child('questions')

def get_current_question(user_id, course_id, material_id):
  answered_questions = get_material_questions(user_id, course_id, material_id).get()

  all_material_questions = course.find_course_query(course_id).child('materials').child(material_id).child('questions')

  not_answered_question = None
  for key, value in all_material_questions.get().items():
    if answered_questions != None:
      if key not in answered_questions.keys():
        not_answered_question = key
        break
    else:
      not_answered_question = key
      break

  return not_answered_question


def set_question_answer(user_id, course_id, material_id, question_id, is_true):
  get_material_questions(user_id, course_id, material_id).child(question_id).set(is_true)