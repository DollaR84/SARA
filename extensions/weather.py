"""
Extension for assistant of weather functions.

Created on 25.04.2017

@author: Ruslan Dolovanyuk

"""

import json
import logging
import urllib.request

from datetime import datetime


def if_exists(ptr, config):
    """Check exists table in database."""
    return (ptr.bd.if_exists(config.name_bd, 'datetime') and
            ptr.bd.if_exists(config.name_bd, 'txt_data') and
            ptr.bd.if_exists(config.name_bd, 'simple_data'))


def setup(ptr, config):
    """Create tables in database."""
    log = logging.getLogger()
    log.info('setup Sara: create weather tables in database...')

    script = (
              "DROP TABLE IF EXISTS datetime",
              '''CREATE TABLE datetime (
                    id INTEGER PRIMARY KEY NOT NULL,
                    strtime TEXT NOT NULL) WITHOUT ROWID
              ''',
    )
    ptr.bd.put_other_bd(config.name_bd, script)

    script = (
              "DROP TABLE IF EXISTS txt_data",
              '''CREATE TABLE txt_data (
                    id INTEGER PRIMARY KEY NOT NULL,
                    data TEXT NOT NULL) WITHOUT ROWID
              ''',
    )
    ptr.bd.put_other_bd(config.name_bd, script)

    script = (
              "DROP TABLE IF EXISTS simple_data",
              '''CREATE TABLE simple_data (
                    id INTEGER PRIMARY KEY NOT NULL,
                    data TEXT NOT NULL) WITHOUT ROWID
              ''',
    )
    ptr.bd.put_other_bd(config.name_bd, script)


def check(ptr, config, text, arg, lang):
    """Check need actions for use."""
    if 'weather_today' == text:
        get_today(ptr, config, arg, lang)
    elif 'pop_today' == text:
        get_today(ptr, config, 'pop', lang)
    elif 'wind_today' == text:
        get_today(ptr, config, 'wind', lang)
    elif 'humidity_today' == text:
        get_today(ptr, config, 'humidity', lang)
    elif 'weather_tomorrow' == text:
        get_tomorrow(ptr, config, arg, lang)
    elif 'pop_tomorrow' == text:
        get_tomorrow(ptr, config, 'pop', lang)
    elif 'wind_tomorrow' == text:
        get_tomorrow(ptr, config, 'wind', lang)
    elif 'humidity_tomorrow' == text:
        get_tomorrow(ptr, config, 'humidity', lang)
    elif (('weather_monday' == text) or
          ('weather_tuesday' == text) or
          ('weather_wednesday' == text) or
          ('weather_thursday' == text) or
          ('weather_friday' == text) or
          ('weather_saturday' == text) or
          ('weather_sunday' == text) or
          ('pop_day' == text) or
          ('wind_day' == text) or
          ('humidity_day' == text)):
        get_day(ptr, config, text, arg, lang)


def get_today(ptr, config, arg, lang):
    """Get weater on today."""
    log = logging.getLogger()
    log.info('get weather on today...')

    weather = __get(ptr, config, 'today', None, lang)
    if weather is None:
        return
    if 'pop' == arg:
        __speak_pop(ptr, config, weather)
    elif 'wind' == arg:
        __speak_wind(ptr, config, weather)
    elif 'humidity' == arg:
        __speak_humidity(ptr, config, weather)
    else:
        weather = __get(ptr, config, 'today', arg, lang)
        if arg is None:
            __speak_simple(ptr, config, weather)
        else:
            __speak_txt(ptr, config, weather)


def get_tomorrow(ptr, config, arg, lang):
    """Get weater on tomorrow."""
    log = logging.getLogger()
    log.info('get weather on tomorrow...')

    weather = __get(ptr, config, 'tomorrow', None, lang)
    if weather is None:
        return
    if 'pop' == arg:
        __speak_pop(ptr, config, weather)
    elif 'wind' == arg:
        __speak_wind(ptr, config, weather)
    elif 'humidity' == arg:
        __speak_humidity(ptr, config, weather)
    else:
        weather = __get(ptr, config, 'tomorrow', arg, lang)
        if arg is None:
            __speak_simple(ptr, config, weather)
        else:
            __speak_txt(ptr, config, weather)


def get_day(ptr, config, text, arg, lang):
    """Get weater on day."""
    log = logging.getLogger()
    log.info('get weather on day...')

    weather = None
    day = ''
    if 'weather_monday' == text:
        day = ptr.phrases.calendar.weekday[0]
    elif 'weather_tuesday' == text:
        day = ptr.phrases.calendar.weekday[1]
    elif 'weather_wednesday' == text:
        day = ptr.phrases.calendar.weekday[2]
    elif 'weather_thursday' == text:
        day = ptr.phrases.calendar.weekday[3]
    elif 'weather_friday' == text:
        day = ptr.phrases.calendar.weekday[4]
    elif 'weather_saturday' == text:
        day = ptr.phrases.calendar.weekday[5]
    elif 'weather_sunday' == text:
        day = ptr.phrases.calendar.weekday[6]

    if ((('pop_day' == text) or
         ('wind_day' == text) or
         ('humidity_day' == text))):
        day = ptr.phrases.calendar.weekday[arg]
        weather = __get(ptr, config, day, None, lang)
        if weather is not None:
            if 'pop_day' == text:
                __speak_pop(ptr, config, weather)
            elif 'wind_day' == text:
                __speak_wind(ptr, config, weather)
            elif 'humidity_day' == text:
                __speak_humidity(ptr, config, weather)
    else:
        weather = __get(ptr, config, day, arg, lang)
        if weather is not None:
            if arg is None:
                __speak_simple(ptr, config, weather)
            else:
                __speak_txt(ptr, config, weather)


def __speak_simple(ptr, config, weather):
    """Speak weather information from simple dictionary."""
    log = logging.getLogger()
    log.info('speak weather information from simple dictionary')

    metric = True if "true" == config.metric else False
    ptr.speech.speak(ptr.phrases.weather.weather % weather['date']['weekday'])
    ptr.speech.speak(weather['conditions'])
    low = high = units = None
    if metric:
        low = weather['low']['celsius']
        high = weather['high']['celsius']
        units = ptr.phrases.weather.celsius
    else:
        low = weather['low']['fahrenheit']
        high = weather['high']['fahrenheit']
        units = ptr.phrases.weather.fahrenheit
    ptr.speech.speak(ptr.phrases.weather.temperature % (low, high, units))
    ptr.speech.speak(ptr.phrases.weather.probability % weather['pop'])
    allday = None
    if weather['qpf_allday']['in'] >= weather['snow_allday']['in']:
        if metric:
            allday = weather['qpf_allday']['mm']
            units = ptr.phrases.weather.mm
        else:
            allday = weather['qpf_allday']['in']
            units = ptr.phrases.weather.inch
        ptr.speech.speak(ptr.phrases.weather.rain % (allday, units))
    else:
        if metric:
            allday = weather['snow_allday']['cm']
            units = ptr.phrases.weather.cm
        else:
            allday = weather['snow_allday']['in']
            units = ptr.phrases.weather.inch
        ptr.speech.speak(ptr.phrases.weather.snow % (allday, units))
    speed = None
    if metric:
        units = ptr.phrases.weather.kph
        speed = weather['avewind']['kph']
    else:
        units = ptr.phrases.weather.mph
        speed = weather['avewind']['mph']
    ptr.speech.speak(ptr.phrases.weather.avewind % (speed, units))
    ptr.speech.speak(ptr.phrases.weather.humidity % weather['avehumidity'])


def __speak_txt(ptr, config, weather):
    """Speak weather information from txt dictionary."""
    log = logging.getLogger()
    log.info('speak weather information from txt dictionary')

    metric = True if "true" == config.metric else False
    ptr.speech.speak(ptr.phrases.weather.weather % weather['title'])
    if metric:
        ptr.speech.speak(weather['fcttext_metric'])
    else:
        ptr.speech.speak(weather['fcttext'])


def __speak_pop(ptr, config, weather):
    """Speak pop information."""
    log = logging.getLogger()
    log.info('speak pop information')

    metric = True if "true" == config.metric else False
    ptr.speech.speak(ptr.phrases.weather.weather_pop %
                     weather['date']['weekday'])
    ptr.speech.speak(ptr.phrases.weather.probability % weather['pop'])
    allday = day = night = units = None
    if weather['qpf_allday']['in'] >= weather['snow_allday']['in']:
        if metric:
            allday = weather['qpf_allday']['mm']
            day = weather['qpf_day']['mm']
            night = weather['qpf_night']['mm']
            units = ptr.phrases.weather.mm
        else:
            allday = weather['qpf_allday']['in']
            day = weather['qpf_day']['in']
            night = weather['qpf_night']['in']
            units = ptr.phrases.weather.inch
        ptr.speech.speak(ptr.phrases.weather.rain % (allday, units))
        ptr.speech.speak(ptr.phrases.weather.daynight %
                         (day, units, night, units))
    else:
        if metric:
            allday = weather['snow_allday']['cm']
            day = weather['snow_day']['cm']
            night = weather['snow_night']['cm']
            units = ptr.phrases.weather.cm
        else:
            allday = weather['snow_allday']['in']
            day = weather['snow_day']['in']
            night = weather['snow_night']['in']
            units = ptr.phrases.weather.inch
        ptr.speech.speak(ptr.phrases.weather.snow % (allday, units))
        ptr.speech.speak(ptr.phrases.weather.daynight %
                         (day, units, night, units))


def __speak_wind(ptr, config, weather):
    """Speak wind information."""
    log = logging.getLogger()
    log.info('speak wind information')

    metric = True if "true" == config.metric else False
    ptr.speech.speak(ptr.phrases.weather.weather_wind %
                     weather['date']['weekday'])
    speed = units = None
    if metric:
        units = ptr.phrases.weather.kph
        speed = weather['avewind']['kph']
    else:
        units = ptr.phrases.weather.mph
        speed = weather['avewind']['mph']
    ptr.speech.speak(ptr.phrases.weather.avewind % (speed, units))
    ptr.speech.speak(ptr.phrases.weather.dirwind %
                     (weather['avewind']['dir'],
                      weather['avewind']['degrees']))
    if metric:
        speed = weather['maxwind']['kph']
    else:
        speed = weather['maxwind']['mph']
    ptr.speech.speak(ptr.phrases.weather.maxwind % (speed, units))
    ptr.speech.speak(ptr.phrases.weather.dirwind %
                     (weather['maxwind']['dir'],
                      weather['maxwind']['degrees']))


def __speak_humidity(ptr, config, weather):
    """Speak humidity information."""
    log = logging.getLogger()
    log.info('speak humidity information')

    ptr.speech.speak(ptr.phrases.weather.weather_humidity %
                     weather['date']['weekday'])
    ptr.speech.speak(ptr.phrases.weather.humidity % weather['avehumidity'])
    ptr.speech.speak(ptr.phrases.weather.minmax %
                     (weather['minhumidity'],
                      weather['maxhumidity']))


def __get(ptr, config, day, arg, lang):
    """Get day and period of weather."""
    log = logging.getLogger()
    log.info('get day and period of weather')
    weather = __get_data(ptr, config, lang)
    if weather.get('simple', None) is None:
        return None

    if 'today' == day:
        if 'day' == arg:
            return weather['txt'][0]
        elif 'night' == arg:
            return weather['txt'][1]
        else:
            return weather['simple'][0]
    elif 'tomorrow' == day:
        if 'day' == arg:
            return weather['txt'][2]
        elif 'night' == arg:
            return weather['txt'][3]
        else:
            return weather['simple'][1]

    if arg is None:
        for data in weather['simple']:
            if day == data['date']['weekday']:
                return data
        ptr.speech.speak(ptr.phrases.weather.failure % day)
        return None
    else:
        night = False
        for data in weather['txt']:
            if day == data['title']:
                if 'day' == arg:
                    return data
                elif 'night' == arg:
                    night = True
                elif night:
                    return data
        ptr.speech.speak(ptr.phrases.weather.failure % day)
        return None


def __get_data(ptr, config, lang):
    """Get data and set weather struct."""
    log = logging.getLogger()
    log.info('get data and set weather struct')
    weather = {}
    if '' == config.country:
        ptr.speech.speak(ptr.phrases.weather.country_empty)
        return weather
    if '' == config.city:
        ptr.speech.speak(ptr.phrases.weather.city_empty)
        return weather
    url = '''http://api.wunderground.com/api/%s/forecast/lang:%s/q/%s/%s.json
          ''' % (config.key, lang.upper(), config.country.upper(), config.city)

    if __need_update(ptr, config):
        log.info('get data weather from wunderground')
        try:
            http_data = urllib.request.urlopen(url)
        except:
            ptr.speech.speak(ptr.phrases.weather.net_error)
            return weather
        else:
            data = json.loads(http_data.read().decode('utf8'))
            http_data.close()

            txt = json.dumps(data['forecast']['txt_forecast']['forecastday'])
            weather['txt'] = json.loads(txt.replace('null', '0'))
            simple = json.dumps(data['forecast']['simpleforecast']['forecastday'])
            weather['simple'] = json.loads(simple.replace('null', '0'))
            __set_data(ptr, config, weather)
    else:
        bd_data = ptr.bd.get_other_bd(config.name_bd, 'SELECT * FROM txt_data')
        weather['txt'] = [json.loads(data[1]) for data in bd_data]
        bd_data = ptr.bd.get_other_bd(config.name_bd,
                                      'SELECT * FROM simple_data')
        weather['simple'] = [json.loads(data[1]) for data in bd_data]
    return weather


def __set_data(ptr, config, weather):
    """Save data weather data in cache database."""
    log = logging.getLogger()
    log.info('save data weather in cache database...')
    now = datetime.now()
    nowstr = datetime.strftime(now, '%d.%m.%Y %H:%M')

    if ptr.bd.get_other_bd(config.name_bd, 'SELECT * FROM datetime'):
        script = 'UPDATE datetime SET strtime="%s" WHERE id=1' % nowstr
        ptr.bd.put_other_bd(config.name_bd, script)
        script = []
        for data in weather['txt']:
            line = '''UPDATE txt_data SET data="%s" WHERE id=%d
                   ''' % (json.dumps(data).replace('"', '""'),
                          data['period']+1)
            script.append(line)
        ptr.bd.put_other_bd(config.name_bd, script)
        script.clear()
        for data in weather['simple']:
            line = '''UPDATE simple_data SET data="%s" WHERE id=%d
                   ''' % (json.dumps(data).replace('"', '""'), data['period'])
            script.append(line)
        ptr.bd.put_other_bd(config.name_bd, script)
    else:
        script = 'INSERT INTO datetime (id, strtime) VALUES (1, "%s")' % nowstr
        ptr.bd.put_other_bd(config.name_bd, script)
        script = []
        for data in weather['txt']:
            line = '''INSERT INTO txt_data (id, data) VALUES (%d, "%s")
                   ''' % (data['period']+1,
                          json.dumps(data).replace('"', '""'))
            script.append(line)
        ptr.bd.put_other_bd(config.name_bd, script)
        script.clear()
        for data in weather['simple']:
            line = '''INSERT INTO simple_data (id, data) VALUES (%d, "%s")
                   ''' % (data['period'], json.dumps(data).replace('"', '""'))
            script.append(line)
        ptr.bd.put_other_bd(config.name_bd, script)


def __need_update(ptr, config):
    """Check need update information in cache database."""
    log = logging.getLogger()
    log.info('check need update information in cache database')
    now = datetime.now()

    bd_data = ptr.bd.get_other_bd(config.name_bd, 'SELECT * FROM datetime')
    if bd_data:
        bd_time = datetime.strptime(bd_data[0][1], '%d.%m.%Y %H:%M')

        day = (now.date() == bd_time.date())
        delta = now - bd_time
        if (day or ((0 == delta.days) and (12 > (delta.seconds // 3600)))):
            return False
    return True
