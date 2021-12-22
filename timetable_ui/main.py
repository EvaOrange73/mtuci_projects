import sys

import psycopg2
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton, QMessageBox)

from stylesheet import style


class Subject:
    def __init__(self, r):
        self.subject_id = r[0]
        self.week = r[1]
        self.day = r[2]
        self.subject = r[3]
        self.time = r[4]
        self.num = r[5]
        self.subject_num = r[6]


def read_susject(table, row_num, subject_id, day, num, subject_num):
    print(subject_id,
                    table.item(row_num, 2).text(),
                    day,
                    table.item(row_num, 1).text(),
                    table.item(row_num, 0).text(),
                    num,
                    subject_num)
    return Subject([subject_id,
                    table.item(row_num, 2).text(),
                    day,
                    table.item(row_num, 1).text(),
                    table.item(row_num, 0).text(),
                    num,
                    subject_num])


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self._connect_to_db()

        self.setWindowTitle("Расписание")

        self.vbox = QVBoxLayout(self)

        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)

        self._create_shedule_tab()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="timetable_db",
                                     user="postgres",
                                     password="31415926",
                                     host="localhost",
                                     port="5432")

        self.cursor = self.conn.cursor()

    def _create_shedule_tab(self):
        self.shedule_tab = QWidget()
        self.tabs.addTab(self.shedule_tab, "Расписание на неделю")
        self.svbox = QVBoxLayout()
        self.shbox1 = QVBoxLayout()
        self.shbox2 = QHBoxLayout()
        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.table_1 = QTableWidget()
        self.table_2 = QTableWidget()
        self.table_3 = QTableWidget()
        self.table_4 = QTableWidget()
        self.table_5 = QTableWidget()

        days = {"Понедельник": self.table_1, "Вторник": self.table_2, "Среда": self.table_3,
                "Четверг": self.table_4, "Пятница": self.table_5}
        for day in days:
            self.monday_gbox = QGroupBox(day)
            self.shbox1.addWidget(self.monday_gbox)
            self._create_table(day, ["Время", "Предмет", "Неделя", "", ""], self._update_table, self.monday_gbox,
                               days[day])

        self.update_shedule_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_shedule_button)

        self.shedule_tab.setLayout(self.svbox)

        self.time_tab = QWidget()
        self.tabs.addTab(self.time_tab, "Расписание звонков")

        self.timebox = QVBoxLayout()
        self.time_table_box = QGroupBox()
        self.timebox.addWidget(self.time_table_box)
        self.timetable = QTableWidget()
        self._create_table("", ["Время", "", ""], self._update_time_table, self.time_table_box, self.timetable)

        # self.update_shedule_button.clicked.connect(
        #     lambda fun, days_=days, time_table=self.timetable: self._update_shedule(days, time_table))

        self.time_tab.setLayout(self.timebox)

        self.subject_tab = QWidget()
        self.tabs.addTab(self.subject_tab, "Список предметов")

        self.subjects_box1 = QVBoxLayout()
        self.subjects_box2 = QGroupBox()
        self.subjects_box1.addWidget(self.subjects_box2)
        self.subject_table = QTableWidget()
        self._create_table("", ["Предмет", "", ""], self._update_subject_table, self.subjects_box2, self.subject_table)

        self.update_shedule_button.clicked.connect(
            lambda fun, days_=days, time_table=self.timetable, s_table=self.subject_table: self._update_shedule(days, time_table, s_table))

        self.subject_tab.setLayout(self.subjects_box1)

    def _create_table(self, day, headers, update_table, box, table):
        table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)

        update_table(day, table)

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(table)
        box.setLayout(self.mvbox)

    def _update_table(self, day, table):
        self.cursor.execute(
            "SELECT  timetable.id, timetable.week, timetable.day, subjects.subject, literally_timetable.time, "
            "timetable.num, timetable.subject FROM timetable JOIN literally_timetable ON timetable.num = "
            "literally_timetable.id "
            "AND timetable.day=%s JOIN subjects ON timetable.subject = subjects.id ORDER BY timetable.num;",
            (day,))
        records = list(self.cursor.fetchall())

        table.setRowCount(len(records) + 1)
        max_num = 0
        max_subject_num = 0

        for i, r in enumerate(records):
            subject = Subject(r)
            if subject.num > max_num:
                max_num = subject.num
            if subject.subject_num > max_subject_num:
                max_subject_num = subject.subject_num

            self.joinButton = QPushButton("join")
            self.deleteButton = QPushButton("delete")
            table.setItem(i, 0,
                          QTableWidgetItem(subject.time))
            table.setItem(i, 1,
                          QTableWidgetItem(subject.subject))
            table.setItem(i, 2,
                          QTableWidgetItem(subject.week))
            table.setCellWidget(i, 3, self.joinButton)
            table.setCellWidget(i, 4, self.deleteButton)

            self.joinButton.clicked.connect(
                lambda fun,
                       row_num=i, subject_id=subject.subject_id, table=table, num=subject.num, subject_num=subject.subject_num:
                self._change_subject(row_num, subject_id, table, num, subject_num)
            )
            self.deleteButton.clicked.connect(
                lambda fun, subject_id=subject.subject_id:
                self._delete_subject(subject_id)
            )
        self.addButton = QPushButton("add")
        table.setItem(len(records), 0,
                      QTableWidgetItem(""))
        table.setItem(len(records), 1,
                      QTableWidgetItem(""))
        table.setItem(len(records), 2,
                      QTableWidgetItem(""))
        table.setCellWidget(len(records), 3, self.addButton)
        table.setItem(len(records), 4,
                      QTableWidgetItem(""))

        self.addButton.clicked.connect(
            lambda fun,
                   row_num=len(records), table=table, num=max_num, subject_num=max_subject_num:
            self._add_subject(row_num, table, day, num, subject_num)
        )

        table.resizeRowsToContents()

    def _update_time_table(self, _, table):
        self.cursor.execute(
            "SELECT time FROM literally_timetable ORDER BY id;")
        records = list(self.cursor.fetchall())

        table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            self.joinButton1 = QPushButton("join")
            self.deleteButton1 = QPushButton("delete")
            table.setItem(i, 0,
                          QTableWidgetItem(r[0]))
            table.setCellWidget(i, 1, self.joinButton1)
            table.setCellWidget(i, 2, self.deleteButton1)
            self.joinButton1.clicked.connect(
                lambda fun,
                       num=i, table_=table:
                self._change_time(num, table_)
            )
            self.deleteButton1.clicked.connect(
                lambda fun,
                       num=i, table_=table:
                self._delete_time(num + 1)
            )
        self.addButton = QPushButton("add")
        table.setItem(len(records), 0,
                      QTableWidgetItem(""))
        table.setCellWidget(len(records), 1, self.addButton)

        self.addButton.clicked.connect(
            lambda fun, row=len(records), table=table:
            self._add_time(row, table)
        )
        table.resizeRowsToContents()

    def _update_subject_table(self, _, table):
        self.cursor.execute(
            "SELECT subject FROM subjects ORDER BY id;")
        records = list(self.cursor.fetchall())

        table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            self.joinButton1 = QPushButton("join")
            self.deleteButton1 = QPushButton("delete")
            table.setItem(i, 0,
                          QTableWidgetItem(r[0]))
            table.setCellWidget(i, 1, self.joinButton1)
            table.setCellWidget(i, 2, self.deleteButton1)
            self.joinButton1.clicked.connect(
                lambda fun,
                       num=i, table_=table:
                self._change_subject_name(num, table_)
            )
            self.deleteButton1.clicked.connect(
                lambda fun,
                       num=i, table_=table:
                self._delete_subject_name(num + 1)
            )
        self.addButton = QPushButton("add")
        table.setItem(len(records), 0,
                      QTableWidgetItem(""))
        table.setCellWidget(len(records), 1, self.addButton)

        self.addButton.clicked.connect(
            lambda fun, row=len(records), table=table:
            self._add_subject_name(row, table)
        )
        table.resizeRowsToContents()

    def _change_subject(self, rowNum, id, table, num, subject_num):
        subject = read_susject(table, rowNum, id, "", num, subject_num)
        self.cursor.execute("SELECT id FROM literally_timetable WHERE time=%s;", (subject.time,))
        num = list(self.cursor.fetchall())
        self.cursor.execute("SELECT id FROM subjects WHERE subject=%s;", (subject.subject,))
        sub = list(self.cursor.fetchall())
        if num and sub:
            self.cursor.execute("UPDATE timetable SET num=%s, subject=%s, week=%s WHERE id=%s;",
                                (str(num[0][0]), str(sub[0][0]), subject.week, subject.subject_id))
        else:
            if not num:
                self.cursor.execute("UPDATE literally_timetable SET time=%s WHERE id=%s;",
                                    (subject.time, str(subject.num)))
                self.cursor.execute("UPDATE timetable SET num=%s, subject=%s, week=%s WHERE id=%s;",
                                (subject.num, str(sub[0][0]), subject.week, subject.subject_id))
            if not sub:
                print(str(num[0][0]), subject.subject)
                self.cursor.execute("UPDATE subjects SET subject=%s WHERE id=%s;",
                                    (subject.subject, str(subject.num)))
                self.cursor.execute("UPDATE timetable SET num=%s, subject=%s, week=%s WHERE id=%s;",
                                (str(num[0][0]), subject.subject_num, subject.week, subject.subject_id))

        self.conn.commit()

    def _change_time(self, row, table):
        time = table.item(row, 0).text()
        self.cursor.execute(
            "UPDATE literally_timetable SET time=%s WHERE id=%s;", (time, row + 1))
        self.conn.commit()

    def _change_subject_name(self, row, table):
        time = table.item(row, 0).text()
        self.cursor.execute(
            "UPDATE subjects SET subject=%s WHERE id=%s;", (time, row + 1))
        self.conn.commit()

    def _add_subject(self, row, table, day, num, subject_num):
        subject = read_susject(table, row, 0, day, num, subject_num)
        self.cursor.execute("SELECT id FROM literally_timetable WHERE time=%s;", (subject.time,))
        num = list(self.cursor.fetchall())
        self.cursor.execute("SELECT id FROM subjects WHERE subject=%s;", (subject.subject,))
        subject_num = list(self.cursor.fetchall())

        print(num[0][0])
        if num or subject_num:
            self.cursor.execute(
                "insert into timetable (week, day, subject, num) values (%s, %s, %s, %s);",
                (subject.week, subject.day, subject_num[0][0], num[0][0])
            )
            self.conn.commit()

        else:
            QMessageBox.about(self, "Error", "Время или название пары некорректно")

    def _add_time(self, row, table):
        time = table.item(row, 0).text()
        self.cursor.execute(
            "INSERT INTO literally_timetable (time) VALUES (%s);", (time,))
        self.conn.commit()

    def _add_subject_name(self, row, table):
        time = table.item(row, 0).text()
        self.cursor.execute(
            "INSERT INTO subjects (subject) VALUES (%s);", (time,))
        self.conn.commit()

    def _delete_subject(self, subject_id):
        self.cursor.execute(
            "DELETE FROM timetable WHERE id=%s", (subject_id,)
        )
        self.conn.commit()

    def _delete_time(self, subject_id):
        self.cursor.execute(
            "DELETE FROM literally_timetable WHERE id=%s", (subject_id,)
        )
        self.conn.commit()

    def _delete_subject_name(self, subject_id):
        self.cursor.execute(
            "DELETE FROM subjects WHERE id=%s", (subject_id,)
        )
        self.conn.commit()

    def _update_shedule(self, days, time_table, subjects):
        for day in days:
            self._update_table(day, days[day])
        self._update_time_table("", time_table)
        self._update_subject_table("", subjects)


app = QApplication(sys.argv)
app.setStyleSheet(style)

win = MainWindow()
win.show()
sys.exit(app.exec_())
