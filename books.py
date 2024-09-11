from db import get_db_connection, close_db_connection


class Books:
    @staticmethod
    def borrow():
        """To take a book or other library material for a specified period, typically with the agreement that it will be returned by a set date."""

    @staticmethod
    def restore():
        """To give back a borrowed book or material to the library, ensuring it's no longer registered under the borrower’s name."""

    @staticmethod
    def search(title):
        """To look up books or resources in the library’s database or catalog by title, author, subject, or keyword to locate specific items."""
        con = get_db_connection()
        cur = con.cursor()
        cur.execute(
            "SELECT title, author, availability, return_date FROM books JOIN availability ON books.id = availability.book_id WHERE title LIKE ?",
            ("%" + title + "%",),
        )
        results = cur.fetchall()
        close_db_connection()

        if results:
            return results
        else:
            return None
