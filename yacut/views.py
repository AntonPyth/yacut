from flask import flash, redirect, render_template, url_for

from . import app, db
from .forms import LinkForm
from .models import URLMap
from .utils import (get_short_id_list,
                    get_unique_short_id, validate_custom_id)


@app.route('/', methods=['GET', 'POST'])
def generate_short_link_view():
    """Представление для генерации короткой ссылки."""
    form = LinkForm()
    if form.validate_on_submit():
        short_id = form.custom_id.data
        if short_id == '' or short_id is None:
            short_id = get_unique_short_id()
        else:
            if not validate_custom_id(short_id):
                flash('Указано недопустимое имя для короткой ссылки')
                return render_template('get_link.html', form=form)
            short_id_list = get_short_id_list()
            if short_id in short_id_list:
                flash('Предложенный вариант короткой ссылки уже существует.')
                return render_template('get_link.html', form=form)
        link = URLMap(
            original=form.original_link.data,
            short=short_id
        )
        db.session.add(link)
        db.session.commit()
        short_link = url_for(
            'redirect_to_original_link_view',
            short_id=link.short, _external=True
        )
        return render_template(
            'get_link.html', form=form, short_link=short_link
        )
    return render_template('get_link.html', form=form)


@app.route('/<short_id>', methods=['GET', 'POST'])
def redirect_to_original_link_view(short_id):
    """Принимает короткую ссылку и перенаправляет на оригинальную страницу."""
    original_link = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(original_link.original)
