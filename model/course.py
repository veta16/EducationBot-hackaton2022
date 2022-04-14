from model.firebase import ref_course, ref_user

import model.user


def get_all_courses():
  return ref_course.order_by_child('name').get()


def find_course_query(course_id):
  return ref_course.child(course_id)


def find_course(course_id):
  return find_course_query(course_id).get()


def find_my_course(user_id, course_id):
  return model.user.find_user_qeury(user_id).child('courses').child(course_id)


def subscribe_course(user_id, course_id):
  if find_my_course(user_id, course_id).get() == None:
    model.user.find_user_qeury(user_id).child('courses').child(course_id).set({"progress": 0})


def my_courses(user_id):
  all_my_courses = model.user.find_user_qeury(user_id).child('courses').get()

  my_course = {}
  if all_my_courses != None:
    for key, course in get_all_courses().items():
      if key in all_my_courses.keys():
        my_course[key] = course

  return my_course

def get_material(course_id, material_id):
  return find_course_query(course_id).child('materials').child(material_id)