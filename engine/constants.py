from math import radians

MAXX = 1000.0  # in meters
MAXY = 1000.0
HITBOX = 10
MAXSPEED = 10  # in meters/round at 100% speed
INERTIA = 0.1  # Percentage of past movement added to curr movement
MISSILE_SPEED = 40.0  # in meters/round
EPSILON = 0.0001  # |A-B|<EPSILON === A==B
EPS_ANG = radians(0.1)  # Epsilon, but for angles. Used for comparing drive dir
