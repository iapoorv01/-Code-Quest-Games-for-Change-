from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import random

class UnderwaterCleanup(ShowBase):
    def __init__(self):
        super().__init__()
        self.setBackgroundColor(0, 0.5, 0.7)  # Set background to a blue color

        # Load the underwater environment
        self.load_environment()

        # Add player character
        self.player = self.loader.loadModel("models/your_player_model")  # Replace with your model path
        self.player.setScale(0.1, 0.1, 0.1)
        self.player.setPos(0, 10, 0)
        self.player.reparentTo(self.render)

        # Add trash items to collect
        self.trash_items = []
        for _ in range(10):
            self.add_trash_item()

        # Add basic movement controls
        self.taskMgr.add(self.move_player, "move_player")

    def load_environment(self):
        # Load a basic underwater model (replace with your model)
        self.environ = self.loader.loadModel("models/your_underwater_model")
        self.environ.setScale(1, 1, 1)
        self.environ.setPos(0, 0, -1)
        self.environ.reparentTo(self.render)

    def add_trash_item(self):
        # Load a trash item model (replace with your model)
        trash = self.loader.loadModel("models/your_trash_model")  # Replace with your model path
        trash.setScale(0.05, 0.05, 0.05)
        trash.setPos(random.uniform(-10, 10), random.uniform(5, 20), random.uniform(-2, -5))
        trash.reparentTo(self.render)
        self.trash_items.append(trash)

    def move_player(self, task):
        # Basic movement controls
        if self.mouseWatcherNode.hasMouse():
            mpos = self.mouseWatcherNode.getMouse()
            x = mpos.getX() * 10
            y = mpos.getY() * 10
            self.player.setPos(x, 10, -2)  # Move player based on mouse position

        return Task.cont

if __name__ == "__main__":
    game = UnderwaterCleanup()
    game.run()