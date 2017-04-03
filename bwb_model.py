import sqlite3
import csv
from shutil import copyfile
import datetime

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

DATABASE_FILE_NAME = "bwb_database_file.db"
DEFAULT_DAYS_BEFORE_NOTIFICATION = 4
NO_NOTIFICATION = -1
SQLITE_FALSE = 0
SQLITE_TRUE = 1
TIME_NOT_SET = -1


def get_schema_version(i_db_conn):
    t_cursor = i_db_conn.execute("PRAGMA user_version")
    return t_cursor.fetchone()[0]


def set_schema_version(i_db_conn, i_version_it):
    i_db_conn.execute("PRAGMA user_version={:d}".format(i_version_it))


# Auto-increment is not needed in our case: https://www.sqlite.org/autoinc.html
def initial_schema_and_setup(i_db_conn):
    i_db_conn.execute(
        "CREATE TABLE " + DbSchemaM.PracticesTable.name + "("
        + DbSchemaM.PracticesTable.Cols.id + " INTEGER PRIMARY KEY" + ", "
        + DbSchemaM.PracticesTable.Cols.title + " TEXT" + " NOT NULL" + ", "
        + DbSchemaM.PracticesTable.Cols.description + " TEXT" + ", "
        + DbSchemaM.PracticesTable.Cols.user_text + " TEXT DEFAULT ''" + ", "
        + DbSchemaM.PracticesTable.Cols.question + " TEXT DEFAULT ''" + ", "
        + DbSchemaM.PracticesTable.Cols.time_of_day + " INTEGER DEFAULT " + str(TIME_NOT_SET)
        + ")"
    )
    i_db_conn.execute(
        "CREATE TABLE " + DbSchemaM.DiaryTable.name + "("
        + DbSchemaM.DiaryTable.Cols.id + " INTEGER PRIMARY KEY" + ", "
        + DbSchemaM.DiaryTable.Cols.date_added + " INTEGER" + ", "
        + DbSchemaM.DiaryTable.Cols.diary_text + " TEXT" + ", "
        + DbSchemaM.DiaryTable.Cols.practices_ref
            + " INTEGER REFERENCES " + DbSchemaM.PracticesTable.name
            + "(" + DbSchemaM.PracticesTable.Cols.id + ")"
            + " NOT NULL"
        + ")"
    )

    # Adding observances
    observances_lt = [
        ("Meditation", "longer description here", "Did I practice meditation today?"),
        ("Tai Chi or mindful movements", "", "Did I practice Tai Chi or did I do mindful movements?"),
        ("Dharma talk", "", "Did I listen to a Dharma talk?")
    ]
    i_db_conn.executemany(
        "INSERT INTO " + DbSchemaM.PracticesTable.name + " ("
        + DbSchemaM.PracticesTable.Cols.title + ", "
        + DbSchemaM.PracticesTable.Cols.description + ", "
        + DbSchemaM.PracticesTable.Cols.question
        + ")"
        + " VALUES (?, ?, ?)", observances_lt
    )


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
    class PracticesTable:
        name = "practices"

        class Cols:
            id = "id"  # key
            title = "title"
            description = "description"
            user_text = "user_text"

            archived = "archived"
            time_of_day = "time_of_day"  # can be changed in schedule?
            situation = "situation"
            question = "question"

            days_before_notification = "days_before_notification"

            # diary references this table
            # wisdom may reference this table in the future

    class DiaryTable:
        name = "diary"

        class Cols:
            id = "id"  # key
            date_added = "date_added"
            diary_text = "diary_text"
            practices_ref = "practices_ref"

            breathing = "breathing"
            enjoyment = "enjoyment"
            intention = "intention"
            hindrances = "hindrances"
            #state_of_mind


class PracticesM:
    def __init__(self, i_id, i_title, i_description,
            i_user_text="", i_question="", i_time_of_day=TIME_NOT_SET):
        self.id = i_id
        self.title = i_title
        self.description = i_description
        self.user_text = i_user_text
        self.question = i_question
        self.time_of_day = i_time_of_day

    @staticmethod
    def add(i_practice_title_sg):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "INSERT INTO " + DbSchemaM.PracticesTable.name + "("
            + DbSchemaM.PracticesTable.Cols.title + ", "
            + DbSchemaM.PracticesTable.Cols.description
            + ") VALUES (?, ?)",
            (i_practice_title_sg, "no description set")
        )
        db_connection.commit()

    @staticmethod
    def get(i_id):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + DbSchemaM.PracticesTable.name
            + " WHERE " + DbSchemaM.PracticesTable.Cols.id + "=" + str(i_id)
        )
        practice_tuple_from_db = db_cursor_result.fetchone()
        db_connection.commit()

        return PracticesM(
            practice_tuple_from_db[0],
            practice_tuple_from_db[1],
            practice_tuple_from_db[2],
            practice_tuple_from_db[3],
            practice_tuple_from_db[4],
            practice_tuple_from_db[5]
        )

    @staticmethod
    def get_for_diary_id(i_diary_id):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + DbSchemaM.PracticesTable.name
            + " WHERE " + DbSchemaM.PracticesTable.Cols.id + "=" + str(i_diary_id)
        )
        t_obs_tuple = db_cursor_result.fetchone()
        db_connection.commit()

        ret_return = PracticesM(
            t_obs_tuple[0],
            t_obs_tuple[1],
            t_obs_tuple[2],
            t_obs_tuple[3],
            t_obs_tuple[4],
            t_obs_tuple[5]
        )

        return ret_return

    @staticmethod
    def get_all(i_orderby_timeofday_bl=False):
        ret_observance_lt = []
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        orderby_sg = DbSchemaM.PracticesTable.Cols.id
        if i_orderby_timeofday_bl:
            orderby_sg = DbSchemaM.PracticesTable.Cols.time_of_day
        db_cursor_result = db_cursor.execute("SELECT * FROM " + DbSchemaM.PracticesTable.name
            + " ORDER BY " + orderby_sg + " ASC")
        observances_from_db = db_cursor_result.fetchall()
        for tuple in observances_from_db:
            ret_observance_lt.append(
                PracticesM(
                    tuple[0],
                    tuple[1],
                    tuple[2],
                    tuple[3],
                    tuple[4],
                    tuple[5]
                )
            )
        db_connection.commit()
        return ret_observance_lt

    @staticmethod
    def update_custom_user_text(i_id, i_text):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + DbSchemaM.PracticesTable.name
            + " SET " + DbSchemaM.PracticesTable.Cols.user_text + " = ?"
            + " WHERE " + DbSchemaM.PracticesTable.Cols.id + " = ?",
            (i_text, i_id)
        )
        db_connection.commit()

    @staticmethod
    def update_question_text(i_id, i_text):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + DbSchemaM.PracticesTable.name
            + " SET " + DbSchemaM.PracticesTable.Cols.question + " = ?"
            + " WHERE " + DbSchemaM.PracticesTable.Cols.id + " = ?",
            (i_text, i_id)
        )
        db_connection.commit()

    @staticmethod
    def update_time_of_day(i_id, i_hour_it):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE " + DbSchemaM.PracticesTable.name
            + " SET " + DbSchemaM.PracticesTable.Cols.time_of_day + " = ?"
            + " WHERE " + DbSchemaM.PracticesTable.Cols.id + " = ?",
            (str(i_hour_it), i_id)
        )
        db_connection.commit()


class DiaryM:
    def __init__(self, i_id, i_date_added_it, i_diary_text="", i_practice_ref_it=-1):
        self.id = i_id
        self.date_added_it = i_date_added_it
        self.diary_text = i_diary_text
        self.practice_ref_it = i_practice_ref_it

    @staticmethod
    def add(i_date_added_it, i_diary_text, i_practice_ref_it):
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "INSERT INTO " + DbSchemaM.DiaryTable.name + "("
            + DbSchemaM.DiaryTable.Cols.date_added + ", "
            + DbSchemaM.DiaryTable.Cols.diary_text + ", "
            + DbSchemaM.DiaryTable.Cols.practices_ref
            + ") VALUES (?, ?, ?)",
            (i_date_added_it, i_diary_text, i_practice_ref_it)
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
        t_diary_tuple_from_db = db_cursor_result.fetchone()
        db_connection.commit()

        return DiaryM(
            t_diary_tuple_from_db[0],
            t_diary_tuple_from_db[1],
            t_diary_tuple_from_db[2],
            t_diary_tuple_from_db[3]
        )

    @staticmethod
    def get_all(i_reverse_bl = False):
        t_direction_sg = "ASC"
        if i_reverse_bl:
            t_direction_sg = "DESC"
        ret_diary_lt = []
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + DbSchemaM.DiaryTable.name
            + " ORDER BY " + DbSchemaM.DiaryTable.Cols.date_added + " " + t_direction_sg
        )
        t_diary_from_db = db_cursor_result.fetchall()
        for t_tuple in t_diary_from_db:
            ret_diary_lt.append(DiaryM(
                t_tuple[0],
                t_tuple[1],
                t_tuple[2],
                t_tuple[3]
            ))
        db_connection.commit()
        return ret_diary_lt

    @staticmethod
    def get_all_for_practice_and_day(i_practice_id, i_start_of_day_as_unix_time_it, i_reverse_bl=True):
        """
        :param i_practice_id:
        :param i_start_of_day_as_unix_time_it: It's very important that this is given as the start of the day
        :param i_reverse_bl:
        :return:
        """
        ret_diary_lt = []
        db_connection = DbHelperM.get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor_result = db_cursor.execute(
            "SELECT * FROM " + DbSchemaM.DiaryTable.name
            + " WHERE " + DbSchemaM.DiaryTable.Cols.date_added + ">=" + str(i_start_of_day_as_unix_time_it)
            + " AND " + DbSchemaM.DiaryTable.Cols.date_added + "<" + str(i_start_of_day_as_unix_time_it + 24 * 3600)
            + " AND " + DbSchemaM.DiaryTable.Cols.practices_ref + "=" + str(i_practice_id)
        )
        t_diary_from_db = db_cursor_result.fetchall()
        for t_tuple in t_diary_from_db:
            ret_diary_lt.append(DiaryM(
                t_tuple[0],
                t_tuple[1],
                t_tuple[2],
                t_tuple[3]
            ))
        db_connection.commit()

        if i_reverse_bl:
            ret_diary_lt.reverse()

        return ret_diary_lt


def export_all():
    pass


def backup_db_file():
    date_sg = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    new_file_name_sg = DATABASE_FILE_NAME + "_" + date_sg
    copyfile(DATABASE_FILE_NAME, new_file_name_sg)
    return
    """
    Alternative: Appending a number to the end of the file name
    i = 1
    while(True):
        if not os.path.isfile(new_file_name_sg):
            break
        i += 1
    """
