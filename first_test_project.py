import unittest
from agent import Agent

class TestEvolution(unittest.TestCase):
    def test_agent_initialization(self):
        bot = Agent(x=400, y=550)
        self.assertEqual(bot.x, 400)
        self.assertEqual(bot.y, 550)
        self.assertTrue(bot.is_alive)

if __name__ == "__main__":
    unittest.main()