from model.firebase import ref_user

from model import course

from bot_messages import MESSAGES

def find_user_qeury(user_id):
  return ref_user.child(str(user_id))


def find_user(user_id):
  return find_user_qeury(user_id).get()


def add_new_user(user_id, username):
  if find_user(user_id) == None:
    user_object = {
      "username": username,
    }
    ref_user.child(str(user_id)).set(user_object)

    return MESSAGES['start']
  else:
    return MESSAGES['user_exist']


def remove_user(user_id):
  ref_user.child(str(user_id)).set({})


def update_progress(user_id, course_id, material_id, is_passed=True):
  course.find_my_course(user_id, course_id).child('materials').child(material_id).update({"is_passed": is_passed})
  my_materials = course.find_my_course(user_id, course_id).child('materials').get()

  all_materials = course.find_course_query(course_id).child('materials').get().items()

  current_progress = len(my_materials)/len(all_materials) * 100

  course.find_my_course(user_id, course_id).update({'progress': current_progress})