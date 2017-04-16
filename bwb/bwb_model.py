import csv
import datetime
import shutil
import sqlite3
import time
from typing import List

from bwb import bwb_global

#################
#
# Model
#
# This module contains everything related to the model for the application:
# * The db schema
# * The db connection
# * Data structure classes (each of which contains functions for reading and writing to the db):
#   * ObservanceM
#   * KarmaM
#   * DiaryM
# * Database creation and setup
# * Various functions (for backing up the db etc)
#
# Notes:
# * When inserting vales, it's best to use "VALUES (?, ?)" because then the sqlite3 module will take care of
#   escaping values for us
#
#################

#DATABASE_FILE_NAME = "bwb_database_file.db"
DATABASE_FILE_NAME = ":memory:"
DEFAULT_DAYS_BEFORE_NOTIFICATION = 4
NO_NOTIFICATION = -1
SQLITE_FALSE = 0
SQLITE_TRUE = 1
TIME_NOT_SET = -1
NO_REFERENCE = -1


def get_schema_version(i_db_conn):
    t_cursor = i_db_conn.execute("PRAGMA user_version")
    return t_cursor.fetchone()[0]


def set_schema_version(i_db_conn, i_version_it):
    i_db_conn.execute("PRAGMA user_version={:d}".format(i_version_it))


# Auto-increment is not needed in our case: https://www.sqlite.org/autoinc.html
def initial_schema_and_setup(i_db_conn):
    i_db_conn.execute(
        "CREATE TABLE " + DbSchemaM.JournalTable.name + "("
        + DbSchemaM.JournalTable.Cols.id + " INTEGER PRIMARY KEY, "
        + DbSchemaM.JournalTable.Cols.title + " TEXT NOT NULL"
        + ")"
    )
    i_db_conn.execute(
        "CREATE TABLE " + DbSchemaM.ReminderTable.name + "("
        + DbSchemaM.ReminderTable.Cols.id + " INTEGER PRIMARY KEY, "
        + DbSchemaM.ReminderTable.Cols.title + " TEXT NOT NULL, "
        + DbSchemaM.ReminderTable.Cols.description + " TEXT DEFAULT '', "
        + DbSchemaM.ReminderTable.Cols.archived + " INTEGER DEFAULT " + str(SQLITE_FALSE) + ", "
        + DbSchemaM.ReminderTable.Cols.journal_ref
        + " INTEGER REFERENCES " + DbSchemaM.JournalTable.name
        + "(" + DbSchemaM.JournalTable.Cols.id + ")"
        + " NOT NULL"
        + ")"
    )
    i_db_conn.execute(
        "CREATE TABLE " + DbSchemaM.DiaryTable.name + "("
        + DbSchemaM.DiaryTable.Cols.id + " INTEGER PRIMARY KEY, "
        + DbSchemaM.DiaryTable.Cols.date_added + " INTEGER, "
        + DbSchemaM.DiaryTable.Cols.diary_text + " TEXT, "
        + DbSchemaM.DiaryTable.Cols.journal_ref
        + " INTEGER REFERENCES " + DbSchemaM.JournalTable.name
        + "(" + DbSchemaM.JournalTable.Cols.id + ")"
        + " NOT NULL" + ", "
        + DbSchemaM.DiaryTable.Cols.reminder_ref
        + " INTEGER REFERENCES " + DbSchemaM.ReminderTable.name
        + "(" + DbSchemaM.ReminderTable.Cols.id + ")"
        + " DEFAULT " + str(NO_REFERENCE)
        + ")"
    )

    """
    journal_list = [
        ("Gratitude",),
        ("Practice",),
        ("Livelihood",),
        ("Study",),
    ]
    """

    journal_list = [
        ("Generosity, ",),
        ("Practice",),
        ("Livelihood",),
        ("Study",),
    ]
    i_db_conn.executemany(
        "INSERT INTO " + DbSchemaM.JournalTable.name + " ("
        + DbSchemaM.JournalTable.Cols.title
        + ")"
        + " VALUES (?)", journal_list
    )

    populate_db_with_test_data()


"""
Example of db upgrade code:
def upgrade_1_2(i_db_conn):
    backup_db_file()
    i_db_conn.execute(
        "ALTER TABLE " + DbSchemaM.ObservancesTable.name + " ADD COLUMN "
        + DbSchemaM.ObservancesTable.Cols.user_text + " TEXT DEFAULT ''"
    )
"""

upgrade_steps = {
    1: initial_schema_and_setup,
}


class DbHelperM(object):
    __db_connection = None  # "Static"

    # def __init__(self):

    @staticmethod
    def get_db_connection():
        if DbHelperM.__db_connection is None:
            DbHelperM.__db_connection = sqlite3.connect(DATABASE_FILE_NAME)

            # Upgrading the database
            # Very good upgrade explanation:
            # http://stackoverflow.com/questions/19331550/database-change-with-software-update
            # More info here: https://www.sqlite.org/pragma.html#pragma_schema_version
            t_current_db_ver_it = get_schema_version(DbHelperM.__db_connection)
            t_target_db_ver_it = max(upgrade_steps)
            for upgrade_step_it in range(t_current_db_ver_it + 1, t_target_db_ver_it + 1):
                if upgrade_step_it in upgrade_steps:
                    upgrade_steps[upgrade_step_it](DbHelperM.__db_connection)
                    set_schema_version(DbHelperM.__db_connection, upgrade_step_it)
            DbHelperM.__db_connection.commit()

            # TODO: Where do we close the db connection? (Do we need to close it?)
            # http://stackoverflow.com/questions/3850261/doing-something-before-program-exit

        return DbHelperM.__db_connection


class DbSchemaM:
    class JournalTable:
        name = "journal"

        class Cols:
            id = "id"
            title = "title"

    class TagTable:
        name = "tag"

        class Cols:
            id = "id"
            name = "name"

    class ReminderTable:
        name = "reminder"

        class Cols:
            id = "id"  # key
            title = "title"
            archived = "archived"
            description = "description"
            journal_ref = "journal_ref"

    class DiaryTable:
        name = "diary"

        class Cols:
            id = "id"  # key
            date_added = "date_added"
            diary_text = "diary_text"
            reminder_ref = "reminder_ref"
            journal_ref = "journal_ref"


class JournalM:
    def __init__(self, i_id_it: int, i_title_sg: str) -> None:
        self.id_it = i_id_it
        self.title_sg = i_title_sg

    @staticmethod
    def get(i_id_it):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + DbSchemaM.JournalTable.name
            + " WHERE " + DbSchemaM.JournalTable.Cols.id + "=" + str(i_id_it)
        )
        journal_db_te = db_cursor_result.fetchone()
        db_connection.commit()

        return JournalM(*journal_db_te)

    @staticmethod
    def get_all():
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute("SELECT * FROM " + DbSchemaM.JournalTable.name)
        journal_db_te_list = db_cursor_result.fetchall()
        db_connection.commit()

        return [JournalM(*journal_db_te) for journal_db_te in journal_db_te_list]


class ReminderM:
    def __init__(self, i_id_it: int, i_title_sg: str, i_description_sg: str,
            i_archived_it: int, i_journal_ref_it: int) -> None:
        self.id = i_id_it
        self.title = i_title_sg
        self.description_sg = i_description_sg
        self.archived_it = i_archived_it
        self.journal_ref_it = i_journal_ref_it

    @staticmethod
    def add(i_title_sg, i_journal_ref_it):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "INSERT INTO " + DbSchemaM.ReminderTable.name + "("
            + DbSchemaM.ReminderTable.Cols.title + ", "
            + DbSchemaM.ReminderTable.Cols.journal_ref
            + ") VALUES (?, ?)",
            (i_title_sg, i_journal_ref_it)
        )
        db_connection.commit()

    @staticmethod
    def get(i_id_it):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + DbSchemaM.ReminderTable.name
            + " WHERE " + DbSchemaM.ReminderTable.Cols.id + "=" + str(i_id_it)
        )
        reminder_db_te = db_cursor_result.fetchone()
        db_connection.commit()

        return ReminderM(*reminder_db_te)

    @staticmethod
    def get_all() -> List:
        ret_reminder_list = []
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        orderby_sg = DbSchemaM.ReminderTable.Cols.id
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + DbSchemaM.ReminderTable.name
            + " ORDER BY " + orderby_sg + " ASC"
        )
        reminder_db_te_list = db_cursor_result.fetchall()
        for reminder_db_te in reminder_db_te_list:
            ret_reminder_list.append(ReminderM(*reminder_db_te))
        db_connection.commit()
        return ret_reminder_list

    @staticmethod
    def get_all_for_journal(i_journal_id_it: int) -> List:
        ret_reminder_list = []
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        orderby_sg = DbSchemaM.ReminderTable.Cols.id
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + DbSchemaM.ReminderTable.name
            + " WHERE " + DbSchemaM.ReminderTable.Cols.journal_ref + " = ?"
            + " ORDER BY " + orderby_sg + " ASC",
            (i_journal_id_it,)
        )
        reminder_db_te_list = db_cursor_result.fetchall()
        for reminder_db_te in reminder_db_te_list:
            ret_reminder_list.append(ReminderM(*reminder_db_te))
        db_connection.commit()
        return ret_reminder_list

    @staticmethod
    def update_description(i_id_it: int, i_new_description_sg: str) -> None:
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + DbSchemaM.ReminderTable.name
            + " SET " + DbSchemaM.ReminderTable.Cols.description + " = ?"
            + " WHERE " + DbSchemaM.ReminderTable.Cols.id + " = ?",
            (i_new_description_sg, i_id_it)
        )
        db_connection.commit()


class DiaryM:
    def __init__(self, i_id, i_date_added_it, i_diary_text="", i_journal_ref_it=-1, i_practice_ref_it=-1):
        self.id = i_id
        self.date_added_it = i_date_added_it
        self.diary_text = i_diary_text
        self.practice_ref_it = i_practice_ref_it
        self.journal_ref_it = i_journal_ref_it

    @staticmethod
    def add(i_date_added_it, i_diary_text, i_journal_ref_it):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "INSERT INTO " + DbSchemaM.DiaryTable.name + "("
            + DbSchemaM.DiaryTable.Cols.date_added + ", "
            + DbSchemaM.DiaryTable.Cols.diary_text + ", "
            + DbSchemaM.DiaryTable.Cols.journal_ref
            + ") VALUES (?, ?, ?)",
            (i_date_added_it, i_diary_text, i_journal_ref_it)
        )
        db_connection.commit()

        # t_diary_id = db_cursor.lastrowid

    @staticmethod
    def update_note(i_id_it, i_new_text_sg):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + DbSchemaM.DiaryTable.name
            + " SET " + DbSchemaM.DiaryTable.Cols.diary_text + " = ?"
            + " WHERE " + DbSchemaM.DiaryTable.Cols.id + " = ?",
            (i_new_text_sg, str(i_id_it))
        )
        db_connection.commit()

    @staticmethod
    def update_date(i_id_it, i_new_time_it):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + DbSchemaM.DiaryTable.name
            + " SET " + DbSchemaM.DiaryTable.Cols.date_added + " = ?"
            + " WHERE " + DbSchemaM.DiaryTable.Cols.id + " = ?",
            (str(i_new_time_it), str(i_id_it))
        )
        db_connection.commit()

    @staticmethod
    def remove(i_id_it):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "DELETE FROM " + DbSchemaM.DiaryTable.name
            + " WHERE " + DbSchemaM.DiaryTable.Cols.id + "=" + str(i_id_it)
        )
        db_connection.commit()

    @staticmethod
    def get(i_id_it):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + DbSchemaM.DiaryTable.name + " WHERE "
            + DbSchemaM.DiaryTable.Cols.id + "=" + str(i_id_it)
        )
        diary_db_te = db_cursor_result.fetchone()
        db_connection.commit()

        return DiaryM(*diary_db_te)

    @staticmethod
    def get_all(i_reverse_bl = False):  # -TODO: Change to for just one month
        t_direction_sg = "ASC"
        if i_reverse_bl:
            t_direction_sg = "DESC"
        ret_diary_list = []
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + DbSchemaM.DiaryTable.name
            + " ORDER BY " + DbSchemaM.DiaryTable.Cols.date_added + " " + t_direction_sg
        )
        diary_db_te_list = db_cursor_result.fetchall()
        for diary_db_te in diary_db_te_list:
            ret_diary_list.append(DiaryM(*diary_db_te))
        db_connection.commit()
        return ret_diary_list

    @staticmethod
    def get_all_for_journal_and_month(i_journal_id_it, i_start_of_month_as_unix_time_it,
            i_number_of_days_in_month_it, i_reverse_bl=True):
        ret_diary_list = []
        t_direction_sg = "DESC"
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + DbSchemaM.DiaryTable.name
            + " WHERE " + DbSchemaM.DiaryTable.Cols.date_added + ">=" + str(i_start_of_month_as_unix_time_it)
            + " AND " + DbSchemaM.DiaryTable.Cols.date_added + "<"
            + str(i_start_of_month_as_unix_time_it + 24 * 3600 * i_number_of_days_in_month_it)
            + " AND " + DbSchemaM.DiaryTable.Cols.journal_ref + "=" + str(i_journal_id_it)
            + " ORDER BY " + DbSchemaM.DiaryTable.Cols.date_added + " " + t_direction_sg
        )
        diary_db_te_list = db_cursor_result.fetchall()
        for diary_db_te in diary_db_te_list:
            ret_diary_list.append(DiaryM(*diary_db_te))
        db_connection.commit()

        if i_reverse_bl:
            ret_diary_list.reverse()
        return ret_diary_list

    @staticmethod
    def get_all_for_active_day(i_reverse_bl=True):
        start_of_day_datetime = datetime.datetime(
            year=bwb_global.active_date_qdate.year(),
            month=bwb_global.active_date_qdate.month(),
            day=bwb_global.active_date_qdate.day()
        )
        start_of_day_unixtime_it = int(start_of_day_datetime.timestamp())

        ret_diary_list = []
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + DbSchemaM.DiaryTable.name
            + " WHERE " + DbSchemaM.DiaryTable.Cols.date_added + ">=" + str(start_of_day_unixtime_it)
            + " AND " + DbSchemaM.DiaryTable.Cols.date_added + "<" + str(start_of_day_unixtime_it + 24 * 3600)
        )
        diary_db_te_list = db_cursor_result.fetchall()
        for diary_db_te in diary_db_te_list:
            ret_diary_list.append(DiaryM(*diary_db_te))
        db_connection.commit()

        if i_reverse_bl:
            ret_diary_list.reverse()
        return ret_diary_list


def export_all():
    csv_writer = csv.writer(open("exported.csv", "w"))
    for diary_item in DiaryM.get_all():
        time_datetime = datetime.date.fromtimestamp(diary_item.date_added_it)
        date_str = time_datetime.strftime("%Y-%m-%d")
        csv_writer.writerow((date_str, diary_item.diary_text))

def backup_db_file():
    date_sg = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    new_file_name_sg = DATABASE_FILE_NAME + "_" + date_sg
    shutil.copyfile(DATABASE_FILE_NAME, new_file_name_sg)
    return

def populate_db_with_test_data():

    # add(i_date_added_it, i_diary_text, i_journal_ref_it):

    delta_day_it = 24 * 60 * 60

    DiaryM.add(time.time(), "Dear Buddha, today i have been practicing meditation before meeting a friend of mine", 2)
    DiaryM.add(time.time(), "Dear Buddha, i'm grateful for being able to breathe!", 1)
    DiaryM.add(time.time() - delta_day_it, "Most difficult today was my negative thinking", 2)
    DiaryM.add(time.time() - 7 * delta_day_it, "Grateful for having a place to live, a roof over my head, food to eat, and people to care for", 1)
    DiaryM.add(time.time() - 7 * delta_day_it, "Grateful for the blue sky and the white clouds", 1)
    DiaryM.add(time.time() - 7 * delta_day_it, "Happy to be alive!", 1)

    ReminderM.add("Meditation", 1)
    ReminderM.add("Tai Chi or mindful movements", 2)
    ReminderM.add("Dharma talk", 1)


