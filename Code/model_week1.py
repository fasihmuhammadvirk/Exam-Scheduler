import datetime
import random
from datetime import date
import pandas as pd
import numpy as np
import math
import copy

file = open("Code\schedule\Datesheet.txt", "w")
file_stu = open("Code\schedule\SeatingPlan.txt", "w")


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
                pass
                # #print(f'{str(self.day) :{" "}<{12}} {str(self.date) :{" "}<{15}}  {str(self.time) :{" "}<{15}}  '
                #       f'{str(student) :{" "}<{50}}  {str(self.course_code) :{" "}<{8}}  {str(self.course_name) :{" "}<{50}}'
                #       f'  {str(self.classroom) :{" "}<{8}}')

    def show(self):
        print(f'{str(self.serial) :{" "}<{3}}  {str(self.day) :{" "}<{12}} {str(self.date) :{" "}<{15}}  '
              f'{str(self.course_code) :{" "}<{8}}  {str(self.course_name) :{" "}<{50}}  {str(self.time) :{" "}<{15}}'
              f'  {str(self.classroom) :{" "}<{8}}  {str(self.invigilator) :{" "}<{20}}')

    def get_student_txt(self):
        for student in self.students:
            if type(student) != int:
                file_stu.write(
                    f'{str(self.day) :{" "}<{12}} {str(self.date) :{" "}<{15}}  {str(self.time) :{" "}<{15}}  '
                    f'{str(student) :{" "}<{45}}  {str(self.course_code) :{" "}<{8}}'
                    f'  {str(self.classroom) :{" "}<{8}}\n')
                # {str(self.course_name): {" "} < {30}}
        
    def get_string(self):
        file.write(f'{str(self.serial) :{" "}<{2}}  {str(self.day) :{" "}<{9}} {str(self.date) :{" "}<{10}}  '
                   f'{str(self.course_code) :{" "}<{8}}  {str(self.course_name) :{" "}<{50}} '
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
        

    def __init__(self, duration):
        # self.courses = pd.read_csv('./test_dataset/courses.csv', header=None)
        self.courses = pd.read_csv('Code/actual_dataset/courses.csv', header=None)
        self.courses = np.array(self.courses)
        # self.rooms = pd.read_csv('./test_dataset/rooms.csv', header=None)
        self.rooms = pd.read_csv('Code/actual_dataset/rooms.csv', header=None)
        self.rooms = np.array(self.rooms)
        # self.student_courses = pd.read_csv('./test_dataset/studentCourse.csv')
        self.student_courses = pd.read_csv('Code/actual_dataset/studentCourses.csv')
        # self.students = pd.read_csv('./test_dataset/studentNames.csv', header=None)
        self.students = pd.read_csv('Code/actual_dataset/studentNames.csv', header=None)
        self.students = np.array(self.students)
        # self.teachers = pd.read_csv('./test_dataset/teachers.csv', header=None)
        self.teachers = pd.read_csv('Code/actual_dataset/teachers.csv', header=None)
        self.teachers = np.array(self.teachers)
        self.teachers = list(self.teachers)
        self.enroll = dict()
        self.SOLUTION_DAYS = duration
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

        # print_dict(self.enroll)

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

    def make_solution(self):
        for room in range(self.room_size):
            for time in range(2):
                for day in range(self.SOLUTION_DAYS):
                    #print(f"Fitness Cost is: {self.solution_fitness() + self.fitness_anneal()}")
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

                    if self.solution_fitness() == 0:
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
                        new_exam = ExamSlot(course, crs_name, str(days), str(times), "ROOM " + '# '+ str(room + 1) + " ", "ME",
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
        return self.solution

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
        temp = 1000
        min_temp = 1
        cooling = 0.999

        self.make_enrollment()
        current_solution = self.make_solution()
        current_score = self.fitness_anneal()
        best_solution = current_solution
        best_score = current_score
        self.random_assign_teacher()
        #print(f"Fitness Cost is: {self.solution_fitness() + self.fitness_anneal()}")

        while temp > min_temp:

            if best_score == 0:
                #print(f"Solution Found")
                #print(f"The max conflicts in best solution are: {best_score}")
                break

            new_solution = self.random_assign_teacher()
            new_score = self.fitness_anneal()
            #print(f"Fitness Cost is: {self.solution_fitness() + self.fitness_anneal()}")

            if new_score < best_score:
                best_solution = copy.deepcopy(new_solution)
                best_score = new_score
                current_solution = copy.deepcopy(new_solution)
                current_score = new_score
            elif new_score < current_score:
                current_solution = copy.deepcopy(new_solution)
                current_score = new_score
            else:
                probability = math.pow(math.e, ((current_score - new_score) / temp))
                if probability > 0.3:
                    current_solution = new_solution.copy()
                    current_score = new_score
                else:
                    #print(f"Solution Found")
                    #print(f"The max conflicts in best solution are: {best_score}")
                    break

            temp *= cooling

        #self.print_solution()
        self.make_txt()
        self.show_student_txt()

    # def print_enroll(self):
    #     print(f"PRINTING")
    #     for key, value in self.enroll.items():
    #         print(f"{key}: {value}")
    #     print()

    def solution_fitness(self):
        count = 0
        for key, value in self.enroll.items():
            count += (value[0])
        return count

    # def print_solution(self):
    #     for i in range(len(self.solution)):
    #         for j in range(len(self.solution[0])):
    #             if self.solution[i][j] != 0:
    #                 print(self.solution[i][j].get_course(), end="           ")
    #             else:
    #                 print(self.solution[i][j], end="            ")
    #         print()

    #     for j in range(len(self.solution[0])):
    #         for i in range(len(self.solution)):
    #             if self.solution[i][j] != 0:
    #                 self.solution[i][j].show()
    #         print()

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


# def run():


# print("Press.")
# print("1. for 2 weeks schedule")
# print("2. for 3 weeks schedule")
# pass_duration = int(input("Enter: "))
# if pass_duration == 1:
#     pass_duration = 10
# elif pass_duration == 2:
#     pass_duration = 15
# else:
#     print("Invalid Input")

# # if pass_duration == 10 or pass_duration == 15:
def main():
    start = ExamScheduler(10)
    start.start_annealing()
