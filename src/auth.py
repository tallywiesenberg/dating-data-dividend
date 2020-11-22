from flask import Blueprint

auth_bp = Blueprint(
    'auth_bp',
    __name__,
    template_folder='templates'
    static_folder='static'
)

@app.route('/register', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.username.data
        flash(f'Hi {user}!')
        return redirect('/')
    return render_template('login.html', title='Sign In', form=form)