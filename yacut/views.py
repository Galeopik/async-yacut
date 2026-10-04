from flask import abort, flash, redirect, render_template

from . import app
from .constants import ERROR_404, REDIRECT_ENDPOINT
from .error_handler import InvalidAPIUsageError
from .forms import FileForm, URLForm
from .models import URLMap
from .ya_disc import async_upload_files_to_ya_disc


@app.route('/<short>', endpoint=REDIRECT_ENDPOINT)
def redirect_to_url(short):
    url_map = URLMap.get(short)
    if url_map is None:
        abort(ERROR_404)
    return redirect(url_map.original)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)

    try:
        return render_template(
            'index.html',
            form=form,
            short_link=URLMap.create(
                original=form.original_link.data,
                short=form.custom_id.data,
                validate_short=False,
                validate_original=False
            ).get_short_link())
    except (ValueError, RuntimeError) as error:
        flash(str(error))
        return render_template('index.html', form=form)


@app.route('/files', methods=['GET', 'POST'])
async def files_view():
    form = FileForm()
    if not form.validate_on_submit():
        return render_template('files.html', form=form)
    files = form.files.data
    try:
        urls = await async_upload_files_to_ya_disc(files)
    except Exception as error:
        flash(f'Не удалось загрузить файлы {error}')
        return render_template('files.html', form=form)

    try:
        return render_template(
            'files.html', form=form,
            files_and_links=[
                {
                    'filename': file.filename,
                    'short_link': URLMap.create(
                        original=url,
                        commit=index == len(urls) - 1
                    ).get_short_link()
                } for index, (file, url) in enumerate(zip(files, urls))])
    except (ValueError, RuntimeError) as error:
        raise InvalidAPIUsageError(str(error))
