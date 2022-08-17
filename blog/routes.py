from flask import render_template, request
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm

@app.route("/")
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", all_posts=all_posts)

def create_edit_entry(entry_id = None):
    if entry_id == None:
        form = EntryForm()
        errors = None
        if request.method == 'POST':
            if form.validate_on_submit():               
                entry = Entry(
                    title=form.title.data,
                    body=form.body.data,
                    is_published=form.is_published.data
                    )
                db.session.add(entry)
                db.session.commit()
            else:
                errors = form.errors
    else:
        entry = Entry.query.filter_by(id=entry_id).first_or_404()
        form = EntryForm(obj=entry)
        errors = None
        if request.method == 'POST':
            if form.validate_on_submit():                      
                form.populate_obj(entry)
                db.session.commit()                 
            else:
                errors = form.errors
    return render_template("entry_form.html", form=form, errors=errors)

@app.route("/new-post/", methods=["GET", "POST"])
def call_function_create_entry():
    return create_edit_entry()

@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
def call_function_edit_entry(entry_id):
    return create_edit_entry(entry_id)