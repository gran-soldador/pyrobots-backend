from engine import Game


def test_invalid_codes():
    # Is not code
    r1 = (1, "A", """
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Maecenas semper arcu in metus dignissim consectetur.
Nam consequat vulputate ullamcorper.
    """)
    # Wrong class name
    r2 = (2, "MyRobot", """
class NotMyRobot(Robot):
    def initialize(self):
        pass
    def respond(self):
        pass
    """)
    # Doesn't subclass Robot
    r3 = (3, "MyObj", """
class MyObj():
    def initialize(self):
        pass
    def respond(self):
        pass
    """)
    # Good Robot
    r4 = (4, "MyGoodRobot", """
class MyGoodRobot(Robot):
    def initialize(self):
        pass
    def respond(self):
        pass
    """)
    gut = Game([r1, r2, r3, r4], 100)
    assert len(gut.alive) == 1
    assert gut.alive[0]._status.name == r4[1]


def test_moving_robots():
    r = (1, "R", """
class R(Robot):
    def initialize(self):
        pass
    def respond(self):
        self.drive(0,1)
    """)
    rounds = 5
    gut = Game([r, r], rounds)
    result = gut.simulation()
    assert result["maxrounds"] == result["rounds_played"] == rounds
    assert len(result["robots"][0]["statuses"]) == result["rounds_played"] + 1
    statuses = result["robots"][0]["statuses"]
    for prev, curr in zip(statuses, statuses[1:]):
        assert curr["x"] > prev["x"] and curr["y"] == curr["y"]


def test_early_finish():
    r1 = (1, "ISurvive", """
class ISurvive(Robot):
    def initialize(self):
        pass
    def respond(self):
        pass
    """)
    r2 = (2, "IDieAt3", """
class IDieAt3(Robot):
    def initialize(self):
        self.a = 1

    def respond(self):
        if self.a == 3: raise Exception("Robot B was baddd")
        self.a += 1
""")
    rounds = 100
    gut = Game([r1, r2], rounds)
    result = gut.simulation()
    assert result["rounds_played"] == 3
    assert result["robots"][1]["name"] == r2[1]
    assert len(result["robots"][1]["statuses"]) == result["rounds_played"] + 1
    statuses = result["robots"][1]["statuses"]
    for status in statuses[:-1]:
        assert status["damage"] == 0
    assert statuses[-1]["damage"] == 100


def test_crashing_robots():
    def r(n):
        return (n, "IGoToCenter", """
class IGoToCenter(Robot):
    def initialize(self):
        pass
    def respond(self):
        x,y=self.get_position()
        if x < 500:
            if y < 500: #lower left
                self.drive(45+0,50)
            else: #upper left
                self.drive(45+270, 50)
        else:
            if y < 500: #lower right
                self.drive(45+90, 50)
            else: #upper right
                self.drive(45+180, 50)
    """)
    gut = Game([r(1), r(2), r(3), r(4)], 100000)
    result = gut.simulation()

    assert result["rounds_played"] < 10000  # Robots should die VERY quickly
    count = sum(1 for robot in result["robots"]
                if robot["statuses"][-1]["damage"] >= 100)
    assert count >= 3
