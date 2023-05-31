import datetime
import random
from datetime import date
import pandas as pd
import numpy as np
import copy
import math

file = open("Code\schedule\Datesheet.txt", "w")
file_stu = open("Code\schedule\Datesheet.txt", "w")



class ExamSlot:
    def __init__(self, code, crs_name, day, time, room, teacher, stu_list, srNo):
        self.course_code = code
        self.course_name = crs_name
        self.time = time
        self.day = day
        self.classroom = room
        self.invigilator = teacher
        self.students = stu_list
        self.serial = srNo
        self.date = (date.today() + datetime.timedelta(days=srNo)).strftime("%d/%m/%Y")

    def get_students(self):
        return self.students

    def get_teacher(self):
        return self.invigilator

    def set_teacher(self, teacher):
        self.invigilator = teacher

    def get_course(self):
        return self.course_code

    def get_serial(self):
        return self.serial

    def show_student(self):
        for student in self.students:
            if type(student) != int:
                print(f'{str(self.day) :{" "}<{12}} {str(self.date) :{" "}<{15}}  {str(self.time) :{" "}<{15}}  '
                      f'{str(student) :{" "}<{50}}  {str(self.course_code) :{" "}<{8}}  {str(self.course_name) :{" "}<{50}}'
                      f'  {str(self.classroom) :{" "}<{8}}')

    def show(self):
        print(f'{str(self.serial) :{" "}<{3}}  {str(self.day) :{" "}<{12}} {str(self.date) :{" "}<{15}}  '
              f'{str(self.course_code) :{" "}<{8}}  {str(self.course_name) :{" "}<{50}}  {str(self.time) :{" "}<{15}}'
              f'  {str(self.classroom) :{" "}<{8}}  {str(self.invigilator) :{" "}<{20}}')

    def get_student_txt(self):
        for student in self.students:
            if type(student) != int:
                file_stu.write(f'{str(self.day) :{" "}<{12}} {str(self.date) :{" "}<{15}}  {str(self.time) :{" "}<{15}}  '
                      f'{str(student) :{" "}<{20}}  {str(self.course_code) :{" "}<{8}}  {str(self.course_name) :{" "}<{30}}'
                      f'  {str(self.classroom) :{" "}<{8}}\n')

    def get_string(self):
        file.write(f'{str(self.serial) :{" "}<{2}}  {str(self.day) :{" "}<{9}} {str(self.date) :{" "}<{10}}  '
                   f'{str(self.course_code) :{" "}<{8}}  {str(self.course_name) :{" "}<{30}} '
                   f' {str(self.time) :{" "}<{15}}'
                   f'  {str(self.classroom) :{" "}<{8}}  {str(self.invigilator) :{" "}<{20}}\n')


def print_dict(dictionary: dict):
    print()
    for key, value in dictionary.items():
        print(f"{key}: {value}")
    print()


def clean_fake_enroll(fake_enroll: dict):
    course = list()
    for key, value in fake_enroll.items():
        if len(value) == 0:
            course.append(key)
    for key in course:
        fake_enroll.pop(key)
    course.clear()
    for key, value in fake_enroll.items():
        if type(value[0]) is not int:
            value.insert(0, len(value))
        if type(value[0]) is int and len(value) == 1:
            course.append(key)
    for key in course:
        fake_enroll.pop(key)
    course.clear()


def intersection(list_1, list_2):
    score = 0
    for value in list_1:
        if value in list_2:
            score += 1
    return score


def print_fake_enroll(arg):
    print(f"PRINTING FAKE")
    for key, value in arg.items():
        print(f"{key}: {value}")
    print()


def is_mg_course(dictionary: dict):
    for key in dictionary.keys():
        if key.startswith("MG"):
            return key
    return False


class ExamScheduler:
    def __init__(self):
        # self.courses = pd.read_csv('./test_dataset/courses.csv', header=None)
        self.courses = pd.read_csv('Code\\actual_dataset\\courses.csv', header=None)
        self.courses = np.array(self.courses)
        # self.rooms = pd.read_csv('./test_dataset/rooms.csv', header=None)
        self.rooms = pd.read_csv('Code\\actual_dataset\\rooms.csv', header=None)
        self.rooms = np.array(self.rooms)
        # self.student_courses = pd.read_csv('./test_dataset/studentCourse.csv')
        self.student_courses = pd.read_csv('Code\\actual_dataset\\studentCourses.csv')
        # self.students = pd.read_csv('./test_dataset/studentNames.csv', header=None)
        self.students = pd.read_csv('Code\\actual_dataset\\studentNames.csv', header=None)
        self.students = np.array(self.students)
        # self.teachers = pd.read_csv('./test_dataset/teachers.csv', header=None)
        self.teachers = pd.read_csv('Code\\actual_dataset\\teachers.csv', header=None)
        self.teachers = np.array(self.teachers)
        self.teachers = list(self.teachers)
        self.enroll = dict()
        self.SOLUTION_DAYS = 10
        self.course_size = len(self.courses)
        self.room_size = len(self.rooms)
        self.teacher_size = len(self.teachers)
        self.solution = np.zeros([self.room_size * 2, self.SOLUTION_DAYS], dtype=ExamSlot)
        self.room_strength = self.rooms[0][1]
        self.course_rooms = dict()
        self.solution_list = list()
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.time = ["09:00 AM", "02:00 PM"]

    def make_enrollment(self):
        for loc in range(len(self.courses)):
            self.enroll.update({self.courses[loc][0]: []})

        for pos in range(len(self.student_courses)):
            student = self.student_courses.loc[pos]['Student Name']
            course = self.student_courses.loc[pos]['Course Code']
            self.enroll[course].append(student)
        for key, value in self.enroll.items():
            value.insert(0, len(value))
        self.enroll = sorted(self.enroll.items(), key=lambda x: x[1][0], reverse=True)
        self.enroll = dict(self.enroll)

        print_dict(self.enroll)

    def sort_enrollment(self):
        for key, value in self.enroll.items():
            value[0] = len(value) - 1
        self.enroll = sorted(self.enroll.items(), key=lambda x: x[1][0], reverse=True)
        self.enroll = dict(self.enroll)
        # for key, value in self.enroll.items():
        #     print(f"{key}: {value}")

    def prune_enroll_all(self, student_list):
        for key, value in self.enroll.items():
            for student in student_list:
                if student in value:
                    value.remove(student)
        courses = list()
        for key, value in self.enroll.items():
            courses.append(key)
        for key in courses:
            self.enroll.pop(key)

    def prune_enroll_course(self, student_list, course):
        new_list = self.enroll[course]
        for student in student_list:
            if student in new_list:
                new_list.remove(student)
        self.enroll.update({course: new_list})
        courses = list()
        for key, value in self.enroll.items():
            if len(value) == 0:
                courses.append(key)
        for key in courses:
            self.enroll.pop(key)

    def occupied_students(self, day):
        students = set()
        for room in range(self.room_size * 2):
            if self.solution[room][day] != 0:
                list_student = self.solution[room][day].get_students()
                for each in list_student:
                    students.add(each)
        students = list(students)
        return students

    def set_course_rooms(self):
        for key, value in self.enroll.items():
            rooms = math.ceil(len(value) / self.room_strength)
            self.course_rooms.update({key: rooms})
        # print_dict(self.course_rooms)
    #
    # def random_solution(self):
    #     self.set_course_rooms()
    #     for room in range(self.room_size):
    #         for time in range(2):
    #             for day in range(self.SOLUTION_DAYS):
    #                 if len(self.course_rooms) > 0:
    #                     if self.solution[room + (self.room_size * time)][day] == 0:
    #                         key, value = self.course_rooms.popitem()
    #                         for assign in range(value):
    #                             if self.solution[room + (self.room_size * time) + assign][day] == 0:
    #                                 self.solution[room + (self.room_size * time) + assign][day] = key
    #     self.print_solution()
    #     score = 100
    #     minimum = 100
    #     while score != 0:
    #         self.print_solution()
    #         score, min_clash, max_clash = self.fitness_clash()
    #         self.random_clash_change(min_clash, max_clash)
    #         self.fitness_clash()
    #         if score < minimum:
    #             minimum = score
    #         print(f"Minimum: {minimum}")
    #
    #     # add annealing function
    #     # add teachers
    #     # assign time and students#
    #
    # def random_clash_change(self, min_day, max_day):
    #     course_set = set()
    #     for room in range(2 * self.SOLUTION_DAYS):
    #         if self.solution[room][max_day] != 0:
    #             course_set.add(self.solution[room][max_day])
    #     course_set = list(course_set)
    #     if len(course_set) > 0:
    #         print(f"{course_set[0]}, column: {max_day}")
    #         for room in range(2 * self.SOLUTION_DAYS):
    #             if self.solution[room][max_day] == course_set[0]:
    #                 self.solution[room][max_day] = 0
    #         itr = 0
    #         index = 0
    #         while itr < math.ceil(len(self.enroll[course_set[0]]) / 28) and index < 20:
    #             if self.solution[index][min_day] == 0:
    #                 self.solution[index][min_day] = course_set[0]
    #                 itr += 1
    #             index += 1
    #
    # def fitness_clash(self):
    #     course_set = list()
    #     score = 0
    #     col_score = 0
    #     max_clash = [0, 0]
    #     min_clash = [1000, 0]
    #     for day in range(self.SOLUTION_DAYS):
    #         for room in range(2 * self.room_size):
    #             if self.solution[room][day] != 0:
    #                 course_set.append(self.solution[room][day])
    #         course_set = set(course_set)
    #         course_set = list(course_set)
    #         for i in range(len(course_set) - 1):
    #             for j in range(i + 1, len(course_set)):
    #                 col_score += intersection(self.enroll[course_set[i]], self.enroll[course_set[j]])
    #         if col_score > max_clash[0]:
    #             max_clash[0] = col_score
    #             max_clash[1] = day
    #         if col_score < min_clash[0]:
    #             min_clash[0] = col_score
    #             min_clash[1] = day
    #         score += col_score
    #         col_score = 0
    #         course_set.clear()
    #
    #     print(f"Score is: {score}")
    #     print(f"max clash: {max_clash[1], max_clash[0]}, min clash: {min_clash[1], min_clash[0]}")
    #
    #     return score, min_clash[1], max_clash[1]

    def make_solution(self):
        for room in range(self.room_size):
            for time in range(2):
                for day in range(self.SOLUTION_DAYS):
                    fake_enroll = copy.deepcopy(self.enroll)
                    current = self.occupied_students(day)

                    for key, value in fake_enroll.items():
                        for student in current:
                            if student in value:
                                value.remove(student)

                    clean_fake_enroll(fake_enroll)

                    for key, value in fake_enroll.items():
                        if len(value) > 0:
                            value[0] = len(value) - 1
                    fake_enroll = sorted(fake_enroll.items(), key=lambda x: x[1][0], reverse=True)
                    fake_enroll = dict(fake_enroll)

                    if self.get_remaining_count() == 0:
                        return 0
                    if len(list(fake_enroll.keys())) > 0:
                        if is_mg_course(fake_enroll):
                            course = is_mg_course(fake_enroll)
                        else:
                            course = list(fake_enroll.keys())[random.randint(0, len(list(fake_enroll.keys())) - 1)]
                        crs_stu = list()
                        for stu in fake_enroll[course]:
                            if len(crs_stu) < 28:
                                crs_stu.append(stu)
                        times = self.time[time]
                        days = self.days.pop(0)
                        # self.teachers[day % self.teacher_size]
                        crs_name = self.get_course_name(course)
                        new_exam = ExamSlot(course, crs_name, str(days), str(times), "ROOM # " + str(room + 1), "ME",
                                            crs_stu, day + 1)
                        # print(f"{room}, {time}, {day}")
                        self.days.append(days)
                        self.solution_list.append(new_exam)
                        self.solution[room + (self.room_size * time)][day] = copy.deepcopy(new_exam)
                        self.prune_enroll_course(crs_stu, course)
                    self.sort_enrollment()

    def get_course_name(self, course):
        for crs in range(len(self.courses)):
            if self.courses[crs][0] == course:
                return self.courses[crs][1]
        return False

    def random_assign_teacher(self):
        for j in range(len(self.solution[0])):
            for i in range(len(self.solution)):
                rand = random.randint(0, self.teacher_size - 1)
                if self.solution[i][j] != 0:
                    self.solution[i][j].set_teacher(self.teachers[rand][0])
            print()

    def fitness_anneal(self):
        value = 1
        teacher_list = list()
        score = 0
        for j in range(len(self.solution[0])):
            for i in range(len(self.solution)):
                if self.solution[i][j] != 0:
                    if self.solution[i][j].get_serial() == value:
                        teacher_list.append(self.solution[i][j].get_teacher())
                    else:
                        score += len(teacher_list) - len(set(teacher_list))
                        teacher_list.clear()
                        teacher_list.append(self.solution[i][j])
                        value = self.solution[i][j].get_serial()
        score += len(teacher_list) - len(set(teacher_list))
        return score

    def start_annealing(self):
        self.make_enrollment()
        self.make_solution()
        self.random_assign_teacher()
        score = self.fitness_anneal()

        while score != 0:
            self.random_assign_teacher()
            score = self.fitness_anneal()

        self.print_solution()
        self.make_txt()
        self.show_student_txt()

    def print_enroll(self):
        print(f"PRINTING")
        for key, value in self.enroll.items():
            print(f"{key}: {value}")
        print()

    def get_remaining_count(self):
        count = 0
        for key, value in self.enroll.items():
            count += (value[0])
        return count

    def print_solution(self):
        for i in range(len(self.solution)):
            for j in range(len(self.solution[0])):
                if self.solution[i][j] != 0:
                    print(self.solution[i][j].get_course(), end="           ")
                else:
                    print(self.solution[i][j], end="            ")
            print()

        for j in range(len(self.solution[0])):
            for i in range(len(self.solution)):
                if self.solution[i][j] != 0:
                    self.solution[i][j].show()
            print()

        # for exam in self.solution_list:
        #     print(exam.get_serial())

    def make_txt(self):
        for j in range(len(self.solution[0])):
            for i in range(len(self.solution)):
                if self.solution[i][j] != 0:
                    self.solution[i][j].get_string()
        file.close()

    def show_student_txt(self):
        for j in range(len(self.solution[0])):
            for i in range(len(self.solution)):
                if self.solution[i][j] != 0:
                    self.solution[i][j].show_student()
        file.close()
        for j in range(len(self.solution[0])):
            for i in range(len(self.solution)):
                if self.solution[i][j] != 0:
                    self.solution[i][j].get_student_txt()
        file_stu.close()

    def new_room_solution(self):
        # get all the students giving exam the same day
        # make a temp enroll and remove all those from the thingy
        # now sort the temp enroll and schedule exams#

        # start
        # see all the teachers and students giving exam that day
        # remove them from the fake enroll and sort and schedule an exam
        # get list of the students you scheduled an exam for
        # and remove them from the true enroll
        # remove a course whose count drops to zero
        # do it until all count is zero #
        pass


print((date.today() + datetime.timedelta(days=1)).strftime("%d/%m/%Y"))
start = ExamScheduler()
start.start_annealing()

#
# def set_course_rooms(self):
#     for key, value in self.enroll.items():
#         rooms = math.ceil(len(value) / self.room_strength)
#         self.course_rooms.update({key: rooms})
#     # print_dict(self.course_rooms)
#
# def random_solution(self):
#     self.set_course_rooms()
#     for room in range(self.room_size):
#         for time in range(2):
#             for day in range(self.SOLUTION_DAYS):
#                 if len(self.course_rooms) > 0:
#                     if self.solution[room + (self.room_size * time)][day] == 0:
#                         key, value = self.course_rooms.popitem()
#                         for assign in range(value):
#                             if self.solution[room + (self.room_size * time) + assign][day] == 0:
#                                 self.solution[room + (self.room_size * time) + assign][day] = key
#     self.print_solution()
#     score = 100
#     minimum = 100
#     while score != 0:
#         self.print_solution()
#         score, min_clash, max_clash = self.fitness_clash()
#         self.random_clash_change(min_clash, max_clash)
#         self.fitness_clash()
#         if score < minimum:
#             minimum = score
#         print(f"Minimum: {minimum}")
#
#     # add annealing function
#     # add teachers
#     # assign time and students#
#
# def random_clash_change(self, min_day, max_day):
#     course_set = set()
#     for room in range(2 * self.SOLUTION_DAYS):
#         if self.solution[room][max_day] != 0:
#             course_set.add(self.solution[room][max_day])
#     course_set = list(course_set)
#     if len(course_set) > 0:
#         print(f"{course_set[0]}, column: {max_day}")
#         for room in range(2 * self.SOLUTION_DAYS):
#             if self.solution[room][max_day] == course_set[0]:
#                 self.solution[room][max_day] = 0
#         itr = 0
#         index = 0
#         while itr < math.ceil(len(self.enroll[course_set[0]]) / 28) and index < 20:
#             if self.solution[index][min_day] == 0:
#                 self.solution[index][min_day] = course_set[0]
#                 itr += 1
#             index += 1
#
# def fitness_clash(self):
#     course_set = list()
#     score = 0
#     col_score = 0
#     max_clash = [0, 0]
#     min_clash = [1000, 0]
#     for day in range(self.SOLUTION_DAYS):
#         for room in range(2 * self.room_size):
#             if self.solution[room][day] != 0:
#                 course_set.append(self.solution[room][day])
#         course_set = set(course_set)
#         course_set = list(course_set)
#         for i in range(len(course_set) - 1):
#             for j in range(i + 1, len(course_set)):
#                 col_score += intersection(self.enroll[course_set[i]], self.enroll[course_set[j]])
#         if col_score > max_clash[0]:
#             max_clash[0] = col_score
#             max_clash[1] = day
#         if col_score < min_clash[0]:
#             min_clash[0] = col_score
#             min_clash[1] = day
#         score += col_score
#         col_score = 0
#         course_set.clear()
#
#     print(f"Score is: {score}")
#     print(f"max clash: {max_clash[1], max_clash[0]}, min clash: {min_clash[1], min_clash[0]}")
#
#     return score, min_clash[1], max_clash[1]