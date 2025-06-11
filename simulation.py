import math

def apply_gravity(bodies, G=1000):
    for i, body_i in enumerate(bodies):
        for j, body_j in enumerate(bodies):
            if i == j:
                continue
            dx = body_j.position.x - body_i.position.x
            dy = body_j.position.y - body_i.position.y
            dist_sq = dx * dx + dy * dy
            if dist_sq == 0:
                continue
            dist = math.sqrt(dist_sq)
            force_mag = G * body_i.mass * body_j.mass / dist_sq
            force_x = force_mag * dx / dist
            force_y = force_mag * dy / dist
            body_i.body.apply_force_at_local_point((force_x, force_y), (0, 0))
