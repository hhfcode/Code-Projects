from flask import render_template, request, Blueprint, flash, redirect, url_for
from flasksite.models import Post, emailsos, db
from flask_login import login_required
from flasksite.main.forms import EmailForm
from flasksite.main.utils import send_SoS_message

main = Blueprint('main', __name__)




@main.route("/")
@main.route("/index")
@main.route("/home")
def index():
    return render_template('index2.html')


@main.route("/Share")
def share():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('share.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/adminteam")
def adminTeam():
    return render_template('adminteam.html', title='Contact Admin Team')

@main.route("/runaway")
def runaway():
    return render_template('runaway.html', title='SOS! Runaway Bike!')

@main.route("/sosmessage")
def sosmessage():
    return render_template('sosmessage.html', title='SOS!')


@main.route("/testsos", methods=['GET', 'POST'])
@login_required
def testsos():
    form = EmailForm()
    if form.validate_on_submit():
        email = emailsos(email=form.email.data)
        db.session.add(email)
        db.session.commit()
        send_SoS_message(email)
        flash('An email has been sent with the preloaded SoS Message.', 'info')
        return redirect(url_for('main.sosmessage'))
    return render_template('testsos.html', form=form)

@main.route("/development")
def development():
    return render_template('Development.html')

