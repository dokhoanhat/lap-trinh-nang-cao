from functools import wraps

from flask import request, redirect, url_for, render_template, make_response, Blueprint, session

from objects.books import BookManager, BorrowManager
from objects.users import AccountManager, LibrarianManager
from routers.core import requires_librarian

admin_page = Blueprint("admin_page", __name__, template_folder="templates")


@admin_page.route("/accounts", methods=["POST", "GET"])
@requires_librarian
def admin_accounts():
    search = request.args.get("search")
    params = {
        "ordering": ["-created"]
    }
    if search:
        params["search"] = search
        accounts = AccountManager().search(**params)
    else:
        accounts = AccountManager().filter(**params)
    context = {
        "accounts": accounts,
        "session": session
    }
    if search:
        context["search"] = search
    return render_template("admin/accounts.html", **context)


@admin_page.route("/accounts/add", methods=["POST", "GET"])
@requires_librarian
def accounts_add():
    if request.method == "POST":
        username = request.form["username"]
        name = request.form["name"]
        password = request.form["password"]
        AccountManager().create(username=username, password=password, name=name)
        resp = redirect(url_for("admin_page.admin_accounts"))
        return resp
    return render_template("admin/add_account.html")


@admin_page.route("/accounts/<account_id>/edit", methods=["POST", "GET"])
@requires_librarian
def accounts_edit(account_id):
    account = AccountManager().get(account_id)
    if request.method == "POST":
        account.name = request.form["name"]
        account.password = request.form["password"]
        account.save()
        resp = redirect(url_for("admin_page.admin_accounts"))
        return resp
    return render_template("admin/edit_account.html", account=account)


@admin_page.route("/accounts/<account_id>/delete", methods=["POST", "GET"])
@requires_librarian
def accounts_delete(account_id):
    account = AccountManager().get(account_id)
    if request.method == "POST":
        account.delete()
        resp = redirect(url_for("admin_page.admin_accounts"))
        return resp
    return render_template("admin/delete_account.html", account=account)


@admin_page.route("/books/add", methods=["POST", "GET"])
@requires_librarian
def books_add():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        isbn = request.form["isbn"]
        publish_date = request.form["publish_date"]
        BookManager().create(title=title, author=author, isbn=isbn, publish_date=publish_date)
        resp = redirect(url_for("main_page.books"))
        return resp
    return render_template("admin/add_book.html")


@admin_page.route("/books/<book_id>/edit", methods=["POST", "GET"])
@requires_librarian
def books_edit(book_id):
    book = BookManager().get(book_id)
    if request.method == "POST":
        book.title = request.form["title"]
        book.author = request.form["author"]
        book.isbn = request.form["isbn"]
        book.publish_date = request.form["publish_date"]
        book.save()
        resp = redirect(url_for("main_page.books"))
        return resp
    return render_template("admin/edit_book.html", book=book)


@admin_page.route("/books/<book_id>/delete", methods=["POST", "GET"])
@requires_librarian
def books_delete(book_id):
    book = BookManager().get(book_id)
    if request.method == "POST":
        book.delete()
        resp = redirect(url_for("main_page.books"))
        return resp
    return render_template("admin/delete_book.html", book=book)


@admin_page.route("/borrows/add", methods=["POST", "GET"])
@requires_librarian
def borrows_add():
    if request.method == "POST":
        account_id = request.form["account_id"]
        book_id = request.form["book_id"]
        BorrowManager().create(account_id=account_id, book_id=book_id)
        resp = redirect(url_for("main_page.borrows"))
        return resp
    return render_template("admin/add_borrow.html")


@admin_page.route("/borrows/<borrow_id>/edit", methods=["POST", "GET"])
@requires_librarian
def borrows_edit(borrow_id):
    borrow = BorrowManager().get(borrow_id)
    if request.method == "POST":
        borrow.account_id = request.form["account_id"]
        borrow.book_id = request.form["book_id"]
        borrow.borrow_time = request.form["borrow_time"]
        borrow.return_time = request.form["return_time"]
        borrow.save()
        resp = redirect(url_for("main_page.borrows"))
        return resp
    return render_template("admin/edit_borrow.html", borrow=borrow)


@admin_page.route("/borrows/<borrow_id>/delete", methods=["POST", "GET"])
@requires_librarian
def borrows_delete(borrow_id):
    borrow = BorrowManager().get(borrow_id)
    if request.method == "POST":
        borrow.delete()
        resp = redirect(url_for("main_page.borrows"))
        return resp
    return render_template("admin/delete_borrow.html", borrow=borrow)