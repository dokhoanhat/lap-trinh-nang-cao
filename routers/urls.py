
from flask import request, redirect, url_for, render_template, make_response, Blueprint, session

from objects.books import BookManager, BorrowManager
from objects.users import AccountManager, LibrarianManager
from routers.core import requires_authentication, requires_librarian


main_page = Blueprint("main_page", __name__, template_folder="templates")

@main_page.route("/")
@requires_authentication
def index():
    if session.get("librarian_id"):
        return redirect(url_for("admin_page.admin_accounts"))
    return redirect(url_for("main_page.books"))


@main_page.route("/books", methods=["POST", "GET"])
@requires_authentication
def books():
    search = request.args.get("search")
    params = {
        "ordering": ["title"]
    }
    if search:
        params["search"] = search
        book_list = BookManager().search(**params)
    else:
        book_list = BookManager().filter(**params)
    context = {
        "books": book_list,
        "session": session
    }
    if search:
        context["search"] = search
    return render_template("books.html", **context)


@main_page.route("/borrows", methods=["POST", "GET"])
@requires_authentication
def borrows():
    search = request.args.get("search")
    params = {
        "ordering": ["-borrow_time"]
    }
    if not session.get("librarian_id"):
        params = {
            "account_id": session.get("user_id")
        }
    if search:
        params["search"] = search
        borrow_list = BorrowManager().search(**params)
    else:
        borrow_list = BorrowManager().filter(**params)
    context = {
        "borrow_list": borrow_list,
        "session": session
    }
    if search:
        context["search"] = search
    return render_template("borrows.html", **context)


@main_page.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        resp = redirect(url_for("main_page.index"))
        session["username"] = username
        session["password"] = password
        return resp
    return render_template("login.html")


@main_page.route("/logout", methods=["POST", "GET"])
def logout():
    if request.method == "POST":
        resp = redirect(url_for("main_page.index"))
        for item in ["user_id", "librarian_id", "username", "password"]:
            try:
                session.pop(item)
            except:
                continue
        return resp
    return render_template("logout.html")
