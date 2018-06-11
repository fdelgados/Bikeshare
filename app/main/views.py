from math import ceil
from flask import request, render_template, redirect, url_for
from . import main
from .. import utils as ut
from ..bikeshare import Bikeshare, EmptyDataFrameException


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city_code = request.form['city']
        month_number = int(request.form['month'])
        day_number = int(request.form['day'])

        return redirect(
            url_for('.stats',
                    city_code=city_code,
                    month_number=month_number,
                    day_number=day_number
                    )
        )

    return render_template('index.html',
                           cities=ut.cities(),
                           days_of_week=ut.days_of_week(),
                           months=ut.months())


@main.route('/stats/<city_code>/<int:month_number>/<int:day_number>')
def stats(city_code, month_number, day_number):
    try:
        bikeshare = Bikeshare(ut.city_name(city_code),
                              ut.month_name(month_number),
                              ut.day_name(day_number))

        time_stats = bikeshare.time_stats()
        stations_stats = bikeshare.station_stats()
        trip_duration_stats = bikeshare.trip_duration_stats()
        user_stats = bikeshare.user_stats()
        operation_time = bikeshare.operation_time

        return render_template('results.html',
                               cities=ut.cities(),
                               days_of_week=ut.days_of_week(),
                               months=ut.months(),
                               selected_city=city_code,
                               selected_month=month_number,
                               selected_day=day_number,
                               time_stats=time_stats,
                               station_stats=stations_stats,
                               trip_duration_stats=trip_duration_stats,
                               user_stats=user_stats,
                               operation_time=operation_time)

    except ValueError as e:
        return render_error(e, city_code, month_number, day_number)

    except EmptyDataFrameException:
        return render_no_data(city_code, month_number, day_number)


@main.route('/raw-data/<city_code>/<int:month_number>/<int:day_number>/<int:page>')
@main.route('/raw-data/<city_code>/<int:month_number>/<int:day_number>/')
def raw_data(city_code, month_number, day_number, page=1):
    try:
        bikeshare = Bikeshare(ut.city_name(city_code),
                              ut.month_name(month_number),
                              ut.day_name(day_number))

        start = (page - 1) * Bikeshare.SLICE_SIZE
        columns, rows = bikeshare.raw_data(start)
        total_pages = ceil(bikeshare.num_results() / Bikeshare.SLICE_SIZE)

        return render_template('raw_data.html',
                               city_name=ut.cities()[city_code],
                               day_name=ut.days_of_week()[day_number],
                               month_name=ut.months()[month_number],
                               city_code=city_code,
                               day_number=day_number,
                               month_number=month_number,
                               columns=columns,
                               rows=rows,
                               total_pages=total_pages,
                               page=page)

    except ValueError as e:
        return render_error(e, city_code, month_number, day_number)
    except EmptyDataFrameException:
        return render_no_data(city_code, month_number, day_number)


def render_no_data(city_code, month_number, day_number):
    return render_template('nodata.html',
                           cities=ut.cities(),
                           days_of_week=ut.days_of_week(),
                           months=ut.months(),
                           selected_city=city_code,
                           selected_month=month_number,
                           selected_day=day_number)


def render_error(error, city_code, month_number, day_number):
    return render_template('error.html',
                           error=error,
                           cities=ut.cities(),
                           days_of_week=ut.days_of_week(),
                           months=ut.months(),
                           selected_city=city_code,
                           selected_month=month_number,
                           selected_day=day_number)
