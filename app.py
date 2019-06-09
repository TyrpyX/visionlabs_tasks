import os

from flask import Flask, request
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

app.config['SAVE_FOLDER'] = './save'
app.config['ALLOWED_EXTENSION'] = ['jpg', 'jpeg', 'png']


@app.route('/images', methods=['POST'])
def image_getter() -> str:
    '''
    Simple endpoint: no type or size checking, just get files and save them
    :raises: BadRequest
    :return:
    '''
    os.makedirs(app.config['SAVE_FOLDER'], exist_ok=True)
    if 'file' not in request.files:
        raise BadRequest('No files provided')
    for image in request.files.getlist("file"):
        image.save(os.path.join(app.config['SAVE_FOLDER'], image.filename))
    return 'ok'


if __name__ == '__main__':
    app.run()
