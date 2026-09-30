import string
from random import choices

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import FileForm, URLForm
from .models import URLMap
from .ya_disc import async_upload_files_to_ya_disc


def get_unique_short_id():
    while True:
        short_code = ''.join(choices(
            string.ascii_letters + string.digits, k=6
        ))
        if not URLMap.query.filter_by(short=short_code).first():
            break
    return short_code


@app.route('/<short_code>')
def redirect_to_original(short_code):
    url = URLMap.query.filter_by(short=short_code).first()
    if url is None:
        abort(404)
    return redirect(url.original)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    if form.validate_on_submit():
        if not form.custom_id.data:
            short_code = get_unique_short_id()
        else:
            short_code = form.custom_id.data
        if (
            URLMap.query.filter_by(short=form.custom_id.data).first()
            or short_code == 'files'
        ):
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
        url = URLMap(
            original=form.original_link.data,
            short=short_code
        )
        short_link = url_for(
            'redirect_to_original',
            short_code=short_code,
            _external=True
        )
        db.session.add(url)
        db.session.commit()
        return render_template('index.html', form=form, short_link=short_link)
    return render_template('index.html', form=form)


@app.route('/files', methods=['GET', 'POST'])
async def files_view():
    form = FileForm()
    if form.validate_on_submit():
        files = form.files.data
        files_and_links = []
        urls = await async_upload_files_to_ya_disc(form.files.data)
        for file, url in zip(files, urls):
            short_code = get_unique_short_id()
            link = URLMap(
                original=url,
                short=short_code
            )
            db.session.add(link)
            db.session.commit()
            short_link = url_for(
                'redirect_to_original',
                short_code=short_code,
                _external=True
            )
            files_and_links.append({
                'filename': file.filename,
                'short_link': short_link
            })
        return render_template('files.html', form=form, short_link=short_link,
                               files_and_links=files_and_links)
    return render_template('files.html', form=form)
