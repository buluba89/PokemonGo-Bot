from datetime import datetime, timedelta
from pokemongo_bot import logger
from pokemongo_bot.cell_workers.base_task import BaseTask
from pokemongo_bot.human_behaviour import sleep


class Sleeper(BaseTask):

    def initialize(self):
        self._process_config()
        self._calc_next_sleep()
        logger.log('Sleeper initialized, next sleep at {}'.format(str(self._next_sleep)), color='red')

    def work(self):
        if datetime.now() >= self._next_sleep:
            logger.log('It\'s time for sleep. Sleeping for  about {} seconds'.format(self._next_sleep_duration))
            sleep(self._next_sleep_duration, self.duration_random_ratio)

    def _process_config(self):
        self.time = datetime.strptime(self.config.get('time', '01:00'), '%H:%M')
        self.duration = datetime.strptime(self.config.get('duration', '07:00'), '%H:%M')
        self.time_random_ratio = self.config.get('time_random_ratio', 0.1)
        self.duration_random_ratio = self.config.get('duration_random_ratio', 0.5)

    def _calc_next_sleep(self):
        now = datetime.now()
        self._next_sleep = now.replace(hour=self.time.hour, minute=self.time.minute)
        #If sleep time is passed add one day
        if self._next_sleep <= now:
            self._next_sleep = self._next_sleep + timedelta(days=1)
        self._next_sleep_duration = timedelta(hours=self.duration.hour, minutes=self.duration.minute).total_seconds()


