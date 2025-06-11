from objects import SpaceBody
from interface import ControlPanel
from simulation import apply_gravity
import settings
import pygame
import pymunk
import tkinter.messagebox as messagebox

def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Space model - Simulation")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0, 0)

    bodies = []

    paused = False

    def add_body(x, y, mass=100, radius=15):
        body = SpaceBody(space, x, y, mass, radius)
        bodies.append(body)

    control_panel = ControlPanel(add_body)

    running = True
    while running and control_panel.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                control_panel.running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                if event.button == 1:
                    for body in bodies:
                        dx = body.position.x - mouse_x
                        dy = body.position.y - mouse_y
                        dist_sq = dx * dx + dy * dy
                        if dist_sq <= (body.radius) ** 2:
                            info = (
                                f"Position: ({body.position.x:.2f}, {body.position.y:.2f})\n"
                                f"Speed: ({body.velocity.x:.2f}, {body.velocity.y:.2f})\n"
                                f"Weight: {body.mass:.2f}\n"
                                f"Radius: {body.radius:.2f}"
                            )
                            messagebox.showinfo("Body info", info)
                            break
                elif event.button == 3:
                    for body in bodies:
                        dx = body.position.x - mouse_x
                        dy = body.position.y - mouse_y
                        dist_sq = dx * dx + dy * dy
                        if dist_sq <= (body.radius) ** 2:
                            answer = messagebox.askyesno("Delete body", "Delete this body?")
                            if answer:
                                space.remove(body.body, body.shape)
                                bodies.remove(body)
                            break

        screen.fill(settings.BACKGROUND_COLOR)

        if not paused:
            apply_gravity(bodies, G=control_panel.G)
            space.step(1 / 60.0)

        for body in bodies:
            pos = body.position
            radius = body.radius
            pygame.draw.circle(screen, settings.BODY_COLOR, pos, radius)
            vel_end = (pos[0] + body.velocity.x, pos[1] + body.velocity.y)
            pygame.draw.line(screen, settings.VELOCITY_COLOR, pos, vel_end, 2)

        pygame.display.flip()
        clock.tick(60)

        control_panel.update()

    pygame.quit()

if __name__ == "__main__":
    main()
