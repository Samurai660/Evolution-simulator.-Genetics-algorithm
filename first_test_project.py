import unittest 
from agent import Agent
from wavemethod import find_wave_way

class TestEvolution(unittest.TestCase):
    def test_agent_initialization(self):
        bot = Agent(start_x=400, start_y=550)
        self.assertEqual(bot.x, 400)
        self.assertEqual(bot.y, 550)
        self.assertTrue(bot.is_alive)

if __name__ == "__main__":
    unittest.main()