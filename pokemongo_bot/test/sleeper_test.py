import unittest
from datetime import timedelta
from mock import patch
from pokemongo_bot.cell_workers.sleeper import Sleeper
from pokemongo_bot import PokemonGoBot


class SleeperTestCase(unittest.TestCase):
    config = {'time': '02:20',
              'duration': '07:05',
              'time_random_ratio': 0.1,
              'duration_random_ratio': 0.2
              }

    @patch('pokemongo_bot.PokemonGoBot')
    def test_config(self, bot):
        worker = Sleeper(bot, self.config)
        self.assertEqual(worker.duration.hour, 7)
        self.assertEqual(worker.duration.minute, 5)
        self.assertEqual(worker.time.hour, 2)
        self.assertEqual(worker.time.minute, 20)
        self.assertEqual(worker.time_random_ratio, 0.1)
        self.assertEqual(worker.duration_random_ratio, 0.2)

