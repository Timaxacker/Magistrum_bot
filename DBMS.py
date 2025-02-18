import sqlite3
from sqlite3 import Error
import pandas as pd



def create_connection(path):
    connection = None

    try:
        connection = sqlite3.connect(path, check_same_thread=False)
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()

    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_query_values(connection, query, values):    
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()


def add_information_in_table(connection, info):
    add_information_in_table_query = """
    INSERT INTO
        
    VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    
    execute_query_values(connection, add_information_in_table_query, info)



delete = "DELETE FROM teachers"



create_lessons_table = """
CREATE TABLE IF NOT EXISTS lessons (
  id INTEGER PRIMARY KEY,
  day_of_week_num INTEGER,
  day_of_week_txt TEXT,
  time_begin INTEGER,
  time_end INTEGER,
  teacher_id INTEGER,
  area_id INTEGER,
  lesson_id INTEGER,
  
  FOREIGN KEY (teacher_id) REFERENCES teachers(id),
  FOREIGN KEY (area_id) REFERENCES areas(id),
  FOREIGN KEY (lesson_id) REFERENCES lesson_types(id)
);
"""


create_lessons_week_table = """
CREATE TABLE IF NOT EXISTS lessons_week (
  id INTEGER PRIMARY KEY,
  day_of_week_num INTEGER,
  day_of_week_txt TEXT,
  time_begin INTEGER,
  time_end INTEGER,
  teacher_id INTEGER,
  area_id INTEGER,
  lesson_id INTEGER,
  
  FOREIGN KEY (teacher_id) REFERENCES teachers(id),
  FOREIGN KEY (area_id) REFERENCES areas(id),
  FOREIGN KEY (lesson_id) REFERENCES lesson_types(id)
);
"""


create_teachers_table = """
CREATE TABLE IF NOT EXISTS teachers (
  id INTEGER PRIMARY KEY,
  lastname TEXT,
  name TEXT,
  patronymic TEXT,
  tg_nick TEXT,
  teacher_state_id INTEGER,  
  
  FOREIGN KEY (teacher_state_id) REFERENCES state_teacher(id)
);
"""


create_areas_table = """
CREATE TABLE IF NOT EXISTS areas (
  id INTEGER PRIMARY KEY,
  title TEXT,
  adres TEXT,
  area_state_id INTEGER,  
  
  FOREIGN KEY (area_state_id) REFERENCES state_area(id)
);
"""


create_type_lesson_table = """
CREATE TABLE IF NOT EXISTS type_lesson (
  id INTEGER PRIMARY KEY,
  title TEXT
);
"""


create_state_teacher_table = """
CREATE TABLE IF NOT EXISTS state_teacher (
  id INTEGER PRIMARY KEY,
  state INTEGER
);
"""


create_state_area_table = """
CREATE TABLE IF NOT EXISTS state_area (
  id INTEGER PRIMARY KEY,
  state INTEGER
);
"""


create_comments_table = """
CREATE TABLE IF NOT EXISTS comments (
  id INTEGER PRIMARY KEY,
  date INTEGER,
  lesson_id INTEGER,
  comment TEXT,
  teacher_id INTEGER,
  info TEXT,
  active INTEGER,

  FOREIGN KEY (lesson_id) REFERENCES lessons(id),
  FOREIGN KEY (teacher_id) REFERENCES teachers(id)
);
"""



addition_lessons = """
INSERT INTO
  lessons (id, day_of_week_num, day_of_week_txt, time_begin, time_end, teacher_id, area_id, lesson_id)
VALUES
  (0, 2, "Вторник", 1930, 2100, 1835294966, 0, 0)
"""


addition_lessons_week = """
INSERT INTO
  lessons_week (id, day_of_week_num, day_of_week_txt, time_begin, time_end, teacher_id, area_id, lesson_id)
VALUES
  (0, 2, "Вторник", 1930, 2100, 1835294966, 0, 0)
"""


addition_teachers = """
INSERT INTO
  teachers (id, lastname, name, patronymic, tg_nick, teacher_state_id)
VALUES
  (1835294966, "Лазарев", "Тимофей", "Максимович", "@Timahacker", 1),
  (0, "х", "Таня", "х", "@maidi17", 1),
  (1, "х", "Тимур", "х", "@ohetb", 1),
  (2, "х", "Саша", "х", "@myshshish", 1),
  (3, "Линда", "Мария", "х", "@Maria_Linda_1", 1),
  (4, "Ларина", "Анастасия", "х", "@new_nst", 1),
  (5, "Лазарева", "Кристина", "х", "@x", 1),
  (6, "Поедайлова", "Кристина", "х", "@Krisssstusha", 1),
  (7, "Логовинская", "Маша", "х", "@itxbazilio", 1),
  (8, "Козлов", "Артем", "х", "@tema_kaif", 1),
  (9, "Тузова", "Света", "х", "@murrrks_03", 1),
  (10, "Гуноев", "Адам", "х", "@m0untain_j3w", 1),
  (11, "Мельник", "Анастасия", "х", "@sssvvvoobboodda", 1),
  (12, "Шушкина", "Мария", "х", "@Fpdp2", 1),
  (13, "Супрунова", "Даша", "х", "@daria_ss13", 1),
  (14, "Неизвестная", "Катя", "х", "@neikatya", 1),
  (15, "Каверин", "Ваня", "х", "@Tangusik", 1),
  (16, "Пименов", "Дмитрий", "х", "@pimenovdm0125", 1),
  (17, "Ишина", "Надежда", "х", "@NadiIshi", 1),
  (18, "х", "Мирослав", "х", "@x", 1),
  (19, "х", "Вова", "х", "@vladimirzausaev", 1),
  (20, "Тихомирова", "Катя", "х", "@Kate_Starrr", 1),
  (21, "Абишова", "Алина", "х", "@x", 1),
  (22, "х", "Слава", "х", "@Vagoretka", 1),
  (981758737, "Белобров", "Тима", "Павлович", "@Durshl4k", 1),
  (23, "х", "Яна", "х", "@x", 1),
  (24, "х", "Андрей", "х", "@andreybagrow", 1),
  (25, "х", "Илья", "х", "@x", 1),
  (26, "Круглов", "Тимофей", "х", "@x", 1)
"""


addition_areas = """
INSERT INTO
  areas (id, title, adres, area_state_id)
VALUES
  (0, "Магиструм", "Композиторов 12", 1),
  (1, "Умка", "Парашютная 52", 1),
  (2, "Инфинитив Шуваловский", "х", 1),
  (3, "SunSchool Республиканская", "Республиканская 35", 1),
  (4, "Хасанская", "х", 1),
  (5, "Солдата Корзуна 4 (ветеранов)", "х", 1),
  (6, "CLS  детский сад Ветеранов", "х", 1),
  (7, "Кудрово", "Столичная 4/1", 1),
  (8, "Инфинитив Смоленская", "х", 1),
  (9, "Янино", "х", 1),
  (10, "Богатырский, 60", "Богатырский 60", 1),
  (11, "Комендантский, 8 к. 1 (коменданский)", "Комендантский 8к1", 1),
  (12, "SunSchool Дыбенко", "Дыбенко 8к3", 1),
  (13, "КидСтори", "Дыбенко 8к2", 1),
  (14, "Кудрово, Областная, д.9 к.", "х", 1),
  (15, "Кудрово, Строительный 4", "х", 1),
  (16, "Российский 14 (большевиков)", "х", 1),
  (17, "Косыгина, 33 (проспект большевиков)", "х", 1),
  (18, "К. Чуковского 3/1 (гражданка)", "х", 1),
  (19, "Инфинитив Гражданская", "х", 1),
  (20, "Всеволожск", "х", 1),
  (21, "Вяхтелево", "х", 1),
  (22, "Взмах", "х", 1),
  (23, "Взмах Школа 9.09", "х", 1),
  (24, "Светлановский 70 (гражданка)", "х", 1),
  (25, "Фея Суздальский", "х", 1),
  (26, "Ступпеньки", "х", 1),
  (27, "Бухарестская 80 (международная)", "х", 1),
  (28, "Пулковская 1/2 (звездная)", "х", 1),
  (29, "Тярлево", "х", 1),
  (30, "Нова", "х", 1),
  (31, "Nova Лесная", "х", 1),
  (32, "Взмах Школа", "х", 1),
  (33, "Инфинитив Веденеева", "х", 1),
  (34, "Пимка Онлайн", "х", 1),
  (35, "Детская Академия Наук", "х", 1),
  (36, "Школа А. Невского", "х", 1),
  (37, "Воронцовский", "х", 1),
  (38, "Ручьевский", "х", 1),
  (39, "Песочное", "х", 1),
  (40, "ЛФ Константиновский", "х", 1),
  (41, "Капитанская ул., 4", "Капитанская 4", 1),
  (42, "Санскул Приморсская", "х", 1),
  (43, "Сертолово, Тихвинская, д. 8 к. 3", "х", 1),
  (44, "LF Кременчугская", "х", 1),
  (45, "SunОбвод", "х", 1),
  (46, "Sun Респ", "х", 1),
  (47, "Умка Лидии Зверевой 9 к1", "х", 1),
  (48, "Песочка (скиду и веду)", "х", 1),5
  (49, "Северный 4 Эрудит", "х", 1),
  (50, "SunПарад", "х", 1)
"""


addition_type_lesson = """
INSERT INTO
  type_lesson (id, title)
VALUES
  (0, "Python"),
  (1, "Занятие")
"""


addition_state_teacher = """
INSERT INTO
  state_teacher (id, state)
VALUES
  (0, 0),
  (1, 1)
"""


addition_state_area = """
INSERT INTO
  state_area (id, state)
VALUES
  (0, 0),
  (1, 1)
"""


addition_comment =  """
INSERT INTO
  comments (id, date, lesson_id, comment, teacher_id, info, active)
VALUES
  (0, 06112024, 2, "Заболел", 1835294966, "Дети - цветы жизни!", 1)
"""



select_lessons_in_day = """
SELECT
  lessons.time_begin, lessons.time_end, teachers.tg_nick, areas.title, type_lesson.title
FROM 
  lessons 
INNER JOIN 
  teachers ON lessons.teacher_id = teachers.id
INNER JOIN 
  areas ON lessons.area_id = areas.id
INNER JOIN 
  type_lesson ON lessons.lesson_id = type_lesson.id
WHERE 
  lessons.day_of_week_num = 
"""


select_day_of_week_for_post = """
SELECT
  lessons.day_of_week_txt
FROM 
  lessons
WHERE 
  lessons.day_of_week_num = 
"""


select_lessons_for_change = """
SELECT
  lessons.id, lessons.time_begin, lessons.time_end, teachers.tg_nick, areas.title, type_lesson.title
FROM 
  lessons 
INNER JOIN 
  teachers ON lessons.teacher_id = teachers.id
INNER JOIN 
  areas ON lessons.area_id = areas.id
INNER JOIN 
  type_lesson ON lessons.lesson_id = type_lesson.id
WHERE 
  lessons.day_of_week_txt = 
"""


select_time_begin_for_change = """
SELECT
  time_begin
FROM 
  lessons 
WHERE 
  id = 
"""


select_time_end_for_change = """
SELECT
  time_end
FROM 
  lessons 
WHERE 
  id = 
"""


select_areas_for_change = """
SELECT
  id, title
FROM 
  areas 
"""


select_teachers_for_change = """
SELECT
  id, lastname, name
FROM 
  teachers 
"""



update_teacher_id0 = """
UPDATE 
  lessons
SET 
  teacher_id = """ 
update_teacher_id1 = """
WHERE 
  id = 
"""


update_time_begin0 = """
UPDATE 
  lessons
SET 
  time_begin = """ 
update_time_begin1 = """
WHERE 
  id = 
"""


update_time_end0 = """
UPDATE 
  lessons
SET 
  time_end = """ 
update_time_end1 = """
WHERE 
  id = 
"""


update_area_id0 = """
UPDATE 
  lessons
SET 
  area_id = """ 
update_area_id1 = """
WHERE 
  id = 
"""



def add_lesson_week_in_table(connection, info):
  add_lesson_in_table_query = """
  INSERT INTO
    lessons_week (id, day_of_week_num, day_of_week_txt, time_begin, time_end, teacher_id, area_id, lesson_id)
  VALUES
    (?, ?, ?, ?, ?, ?, ?, ?);
  """
    
  execute_query_values(connection, add_lesson_in_table_query, info)