from flask import render_template
from app import app, db


@app.errorhandler(403)
def permission_denied(error):
    return render_template('noperm.html'), 403


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500