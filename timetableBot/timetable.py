import datetime

import psycopg2 as psycopg2

conn = psycopg2.connect(database="timetable_db",
                        user="postgres",
                        password="31415926",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()


def get_timetable(message):
    week = datetime.datetime.now().isocalendar()[1]
    if week % 2 == 0:
        week = 0
    else:
        week = 1

    if message.text == 'Расписание на текущую неделю':
        cursor.execute("SELECT day, time, subject FROM timetable WHERE is_even='2' or is_even=%s;", (str(week)))
        return list(cursor.fetchall())
    if message.text == 'Расписание на следующую неделю':
        cursor.execute("SELECT day, time, subject FROM timetable WHERE not is_even=%s;", (str(week)))
        return list(cursor.fetchall())
    cursor.execute("SELECT day, time, subject FROM timetable WHERE (is_even='2' or is_even=%s) and day=%s;", ((str(week)), str(message.text)))
    return list(cursor.fetchall())


def make_answer(timetable):
    if timetable:
        answer = ''
        for subject in timetable:
            if not subject[0] in answer:
                answer += f'{subject[0]}\n'
            answer += f'{subject[1]} {subject[2]}\n'
        return answer
    return 'В этот день пар нет'
