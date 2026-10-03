from aiohttp import ClientError
from flask import abort, flash, redirect, render_template
from sqlalchemy.exc import IntegrityError

from . import app, db
from .constants import ERROR_404, REDIRECT_ENDPOINT
from .error_handler import InvalidAPIUsageError
from .forms import FileForm, URLForm
from .models import URLMap
from .ya_disc import async_upload_files_to_ya_disc


@app.route('/<short>', endpoint=REDIRECT_ENDPOINT)
def redirect_to_url(short):
    url_map = URLMap.get_url_map_by_short(short)
    if url_map is None:
        abort(ERROR_404)
    return redirect(url_map.original)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    if not form.validate_on_submit():
        flash('Указано недопустимое имя для короткой ссылки')
        return render_template('index.html', form=form)

    try:
        short_link = URLMap.create(
            original=form.original_link.data,
            short=form.custom_id.data,
            validate_short=False,
            validate_original=False
        ).get_short_link()
        db.session.commit()
    except InvalidAPIUsageError as error:
        db.session.rollback()
        flash(error.message)
        return render_template('index.html', form=form)
    except IntegrityError as error:
        flash(f'Предложенный вариант короткой ссылки уже существует {error}')
        return render_template('index.html', form=form)
    return render_template('index.html', form=form, short_link=short_link)


@app.route('/files', methods=['GET', 'POST'])
async def files_view():
    form = FileForm()
    if not form.validate_on_submit():
        return render_template('files.html', form=form)
    files = form.files.data
    try:
        urls = await async_upload_files_to_ya_disc(files)
    except ClientError as error:
        flash(f'Не удалось загрузить файлы {error}')
        return render_template('files.html', form=form)

    try:
        files_and_links = [
            {
                'filename': file.filename,
                'short_link': URLMap.create(
                    original=url,
                    short=None
                ).get_short_link()
            } for file, url in zip(files, urls)]
        db.session.commit()
    except IntegrityError as error:
        flash(f'Не удалось создать короткие ссылки {error}')
        return render_template('files.html', form=form)
    return render_template('files.html', form=form,
                           files_and_links=files_and_links)
