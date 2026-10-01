from flask import jsonify, render_template

from . import app, db
from .constants import ERROR_400, ERROR_404


class InvalidAPIUsageError(Exception):
    def __init__(self, message, status_code=ERROR_400):
        super().__init__()
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsageError)
def invalid_api_usage(error):
    db.session.rollback()
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(ERROR_404)
def page_not_found(error):
    db.session.rollback()
    return render_template('404.html'), ERROR_404
