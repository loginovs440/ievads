import datetime

# Список из 15 учеников
students = ["Ученик1", "Ученик2", "Ученик3", "Ученик4", "Ученик5", 
            "Ученик6", "Ученик7", "Ученик8", "Ученик9", "Ученик10", 
            "Ученик11", "Ученик12", "Ученик13", "Ученик14", "Ученик15"]

# Список преподавателей
teachers = ["Преподаватель1", "Преподаватель2"]

# Группы учеников (группы могут быть из 2 или 4 человек)
student_groups = [
    ["Ученик1", "Ученик6"],
    ["Ученик2", "Ученик7"],
    ["Ученик3", "Ученик8"],
    ["Ученик4", "Ученик9"],
    ["Ученик12", "Ученик13", "Ученик14", "Ученик15"]  # Группа из 4 учеников
]

# Временные слоты
time_slots = ["09:00-10:00", "10:00-11:00", "11:00-12:00"]

# Дни недели
days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]

# Ввод расписания
def input_schedule():
    full_schedule = {}

    for day in days_of_week:
        print(f"\nВвод расписания на {day}:")
        day_schedule = {}

        # Вводим расписание для 5 групп (сначала по парам, потом по группам)
        for group_num, group in enumerate(student_groups, start=1):
            group_name = f"Группа {group_num}"
            print(f"\nВвод расписания для {group_name} (участники: {', '.join(group)}):")
            
            # Вводим временной слот для группы
            time_slot = input(f"Введите временной слот для {group_name} (например, 09:00-10:00): ")
            
            # Вводим преподавателя для группы
            teacher = input(f"Введите преподавателя для {group_name} (Преподаватель1 или Преподаватель2): ")
            
            # Добавляем данные в расписание на конкретный день
            day_schedule[group_name] = {
                "Ученики": group,
                "Преподаватель": teacher,
                "Время": time_slot,
                "День недели": day
            }
        
        full_schedule[day] = day_schedule
    
    return full_schedule

# Функция для добавления отсутствующих учеников на каждый день недели
def input_absent_students():
    absent_students = {}

    for day in days_of_week:
        print(f"\nВвод отсутствующих учеников на {day}:")
        num_absent = int(input(f"Сколько учеников отсутствует на {day}? "))
        
        for i in range(num_absent):
            student_name = input(f"Введите имя отсутствующего ученика {i+1}: ")
            if day not in absent_students:
                absent_students[day] = []
            absent_students[day].append(student_name)
    
    return absent_students

# Функция для добавления отсутствующих преподавателей на каждый день недели
def input_absent_teachers():
    absent_teachers = {}

    for day in days_of_week:
        print(f"\nВвод отсутствующих преподавателей на {day}:")
        num_absent = int(input(f"Сколько преподавателей отсутствует на {day}? "))
        
        for i in range(num_absent):
            teacher_name = input(f"Введите имя отсутствующего преподавателя {i+1}: ")
            if day not in absent_teachers:
                absent_teachers[day] = []
            absent_teachers[day].append(teacher_name)
    
    return absent_teachers

# Фильтрация учеников, которые отсутствуют в указанный день
def filter_absent_students(group, absent_students, day):
    return [student for student in group if student not in absent_students.get(day, [])]

# Проверка на отсутствие преподавателя
def is_teacher_absent(teacher, absent_teachers, day):
    return teacher in absent_teachers.get(day, [])

# Поиск следующей доступной группы или пары, если текущая недоступна
def find_next_available_group(group_num, absent_students, day):
    for i in range(group_num, len(student_groups)):
        available_students = filter_absent_students(student_groups[i], absent_students, day)
        if available_students:
            return available_students
    return None

# Проверка на занятость ученика в других группах
def is_student_busy(student, final_schedule, day, time_slot):
    if day in final_schedule:
        for group, details in final_schedule[day].items():
            if student in details["Ученики"] and details["Время"] == time_slot:
                return True
    return False

# Проверка на занятость преподавателя в других группах
def is_teacher_busy(teacher, final_schedule, day, time_slot):
    if day in final_schedule:
        for group, details in final_schedule[day].items():
            if details["Преподаватель"] == teacher and details["Время"] == time_slot:
                return True
    return False

# Основная функция для генерации расписания с учётом занятости учеников и преподавателей
def generate_schedule():
    # Вводим расписание на неделю
    full_schedule = input_schedule()
    
    # Вводим отсутствующих учеников на каждый день
    absent_students = input_absent_students()
    
    # Вводим отсутствующих преподавателей на каждый день
    absent_teachers = input_absent_teachers()
    
    # Создаём финальное расписание с учётом отсутствующих учеников и преподавателей
    final_schedule = {}

    for day in days_of_week:
        print(f"\nФинальное расписание на {day}:")
        final_schedule[day] = {}
        
        for group_num, (group_name, details) in enumerate(full_schedule[day].items(), start=1):
            available_students = filter_absent_students(details["Ученики"], absent_students, day)
            teacher = details["Преподаватель"]
            time_slot = details["Время"]
            
            # Проверяем, не занят ли преподаватель в это время
            if is_teacher_absent(teacher, absent_teachers, day) or is_teacher_busy(teacher, final_schedule, day, time_slot):
                print(f"{group_name}: Преподаватель {teacher} отсутствует или занят в это время. Пара отменена.")
                continue

            # Проверяем занятость каждого ученика и преподавателя
            all_available = True
            for student in available_students:
                if is_student_busy(student, final_schedule, day, time_slot):
                    print(f"{group_name}: Ученик {student} занят в это время в другой группе. Ищем другую группу.")
                    all_available = False
                    break

            if all_available:
                final_schedule[day][group_name] = {
                    "Ученики": available_students,
                    "Преподаватель": teacher,
                    "Время": time_slot
                }
            else:
                # Ищем следующую доступную группу
                next_group = find_next_available_group(group_num, absent_students, day)
                if next_group and not any(is_student_busy(student, final_schedule, day, time_slot) for student in next_group):
                    final_schedule[day][f"Группа {group_num} (Новая)"] = {
                        "Ученики": next_group,
                        "Преподаватель": teacher,
                        "Время": time_slot
                    }
                else:
                    print(f"{group_name}: Все возможные ученики недоступны или заняты. Пара отменена.")
    
    # Вывод расписания
    for day in days_of_week:
        print(f"\nРасписание на {day}:")
        for group, details in final_schedule[day].items():
            print(f"{group}: Ученики - {', '.join(details['Ученики'])}, Преподаватель - {details['Преподаватель']}, Время - {details['Время']}")

# Запуск программы
generate_schedule()
