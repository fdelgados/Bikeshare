from . import main
from .. import formatter as fmt


@main.app_template_filter('int_formatter')
def int_formatter_filter(number):
    return fmt.int_formatter(number)


@main.app_template_filter('float_formatter')
def float_formatter_filter(number):
    return fmt.float_formatter(number)


@main.app_template_filter('seconds_formatter')
def seconds_formatter_filter(seconds):
    return fmt.seconds_formatter(seconds)
