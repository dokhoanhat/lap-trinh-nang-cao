from functools import wraps

from flask import request, redirect, url_for, session

from objects.users import AccountManager, LibrarianManager


def requires_authentication(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        username = session.get("username")
        password = session.get("password")
        user_id = session.get("user_id")
        if not user_id:
            user = AccountManager().authenticate(username, password)
            if not user:
                return redirect(url_for("main_page.login"))
            session["user_id"] = user.id
        librarian_id = session.get("librarian_id")
        if not librarian_id:
            librarian = LibrarianManager().authenticate(username, password)
            if librarian:
                session["librarian_id"] = librarian.id
        return f(*args, **kwargs)
    return wrapped


def requires_librarian(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        username = session.get("username")
        password = session.get("password")
        librarian_id = session.get("librarian_id")
        if not librarian_id:
            librarian = LibrarianManager().authenticate(username, password)
            if not librarian:
                return redirect(url_for("main_page.login"))
            session["librarian_id"] = librarian.id
        return f(*args, **kwargs)
    return wrapped
