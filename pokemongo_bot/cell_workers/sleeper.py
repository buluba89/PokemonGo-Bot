from datetime import datetime, timedelta
from time import sleep
from random import random, uniform
from pokemongo_bot import logger
from pokemongo_bot.cell_workers.base_task import BaseTask
from pokemongo_bot.human_behaviour import jitter


class Sleeper(BaseTask):
    LOG_INTERVAL_SECONDS = 600

    def initialize(self):
        self._process_config()
        self._calc_next_sleep()
        logger.log('Sleeper initialized, next sleep at {}'.format(str(self._next_sleep)), color='red')

    def work(self):
        if datetime.now() >= self._next_sleep:
            self._sleep()
            self._calc_next_sleep()
            self.bot.login()

    def _process_config(self):
        self.time = datetime.strptime(self.config.get('time', '01:00'), '%H:%M')
        #Using datetime for easier stripping
        duration = datetime.strptime(self.config.get('duration', '07:00'), '%H:%M')
        self.duration = timedelta(hours=duration.hour, minutes=duration.minute).total_seconds()
        self.time_random_ratio = self.config.get('time_random_ratio', 0.1)
        self.duration_random_ratio = self.config.get('duration_random_ratio', 0.5)

    def _calc_next_sleep(self):
        now = datetime.now()
        self._next_sleep = now.replace(hour=self.time.hour, minute=self.time.minute)

        #Add a random offset
        max_offset = timedelta(days=1).total_seconds()
        offset_seconds = uniform(-max_offset, max_offset)
        self._next_sleep = self._next_sleep + timedelta(seconds=offset_seconds)

        #If sleep time is passed add one day
        if self._next_sleep <= now:
            self._next_sleep = self._next_sleep + timedelta(days=1)
        #
        self._next_sleep_duration = jitter(self.duration, self.duration_random_ratio)

    def _sleep(self):
        sleep_to_go = self._next_sleep_duration
        while sleep_to_go > 0:
            logger.log('It\'s time for sleep. Sleeping for {} seconds'.format(sleep_to_go))
            if sleep_to_go < self.LOG_INTERVAL_SECONDS:
                sleep(sleep_to_go)
                sleep_to_go = 0
            else:
                sleep(self.LOG_INTERVAL_SECONDS)
                sleep_to_go -= self.LOG_INTERVAL_SECONDS
