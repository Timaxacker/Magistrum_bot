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



delete = "DROP TABLE lessons"


create_lessons_table = """
CREATE TABLE IF NOT EXISTS lessons (
  id INTEGER PRIMARY KEY,
  day_of_week INTEGER,
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
  lessons (id, day_of_week, time_begin, time_end, teacher_id, area_id, lesson_id)
VALUES
  (0, 1, 1200, 1330, 1835294966, 0, 0),
  (1, 1, 1400, 1500, 1835294966, 0, 1),
  (2, 3, 1815, 1945, 1835294966, 0, 0)
"""


addition_teachers = """
INSERT INTO
  teachers (id, lastname, name, patronymic, tg_nick, teacher_state_id)
VALUES
  (1835294966, "Лазарев", "Тимофей", "Максимович", "Timahacker", 1)
"""


addition_areas = """
INSERT INTO
  areas (id, title, adres, area_state_id)
VALUES
  (0, "Магиструм", "Композиторов 12", 1)
"""


addition_type_lesson = """
INSERT INTO
  type_lesson (id, title)
VALUES
  (0, "Python"),
  (1, "WeDo")
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