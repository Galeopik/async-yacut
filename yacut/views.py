from flask import abort, flash, redirect, render_template

from . import app
from .constants import ERROR_404
from .forms import FileForm, URLForm
from .models import URLMap
from .ya_disc import async_upload_files_to_ya_disc


@app.route('/<short>', endpoint='redirect_to_original')
def redirect_to_url(short):
    url_map = URLMap.get_url_map_by_short(short)
    if url_map is None:
        abort(ERROR_404)
    return redirect(url_map.original)


def create_short_link(original, short=None):
    link = URLMap.create(original=original, short=short)
    if link is None:
        raise RuntimeError('Не удалось создать короткую ссылку')
    return link.get_short_link()


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    if not form.validate_on_submit():
        flash('Указано недопустимое имя для короткой ссылки')
        return render_template('index.html', form=form)

    url_map = URLMap.create(
        original=form.original_link.data,
        short=form.custom_id.data
    )
    if url_map is None:
        flash('Предложенный вариант короткой ссылки уже существует.')
        return render_template('index.html', form=form)
    short_link = url_map.get_short_link()
    return render_template('index.html', form=form, short_link=short_link)


@app.route('/files', methods=['GET', 'POST'])
async def files_view():
    form = FileForm()
    if not form.validate_on_submit():
        return render_template('files.html', form=form)
    files = form.files.data
    try:
        urls = await async_upload_files_to_ya_disc(files)
    except Exception:
        flash('Не удалось загрузить файлы')
        return render_template('files.html', form=form)

    try:
        files_and_links = [
            {
                'filename': file.filename,
                'short_link': create_short_link(url)
            } for file, url in zip(files, urls)]
    except Exception:
        flash('Не удалось создать короткие ссылки.')
        return render_template('files.html', form=form)
    return render_template('files.html', form=form,
                           files_and_links=files_and_links)
