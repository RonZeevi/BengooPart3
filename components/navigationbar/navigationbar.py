from flask import Blueprint, render_template, session, url_for, Response
from utilities.db.db_connector import *

# navigationbar blueprint definition
navigationbar = Blueprint(
    'navigationbar',
    __name__,
    static_folder='static',
    static_url_path='/navigationbar',
    template_folder='templates'
)

@navigationbar.route('/')
def index():
    user_profile_image = None
    if session and 'username' in session and session['username']:
        username = session['username']
        user_profile_image = get_user_profile_image(username)
    
    return render_template('navigationbar/templates/navigationbar.html', user_profile_image=user_profile_image)







