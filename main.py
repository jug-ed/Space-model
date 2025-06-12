from objects import SpaceBody
from interface import ControlPanel
from simulation import apply_gravity
from camera import Camera
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

    camera = Camera()

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
                if event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                    camera.zoom_in(settings.SCALE_STEP, settings.MIN_SCALE)
                elif event.key == pygame.K_MINUS:
                    camera.zoom_out(settings.SCALE_STEP, settings.MIN_SCALE)
                elif event.key == pygame.K_LEFT:
                    camera.move_left(settings.MOVE_STEP)
                elif event.key == pygame.K_RIGHT:
                    camera.move_right(settings.MOVE_STEP)
                elif event.key == pygame.K_UP:
                    camera.move_up(settings.MOVE_STEP)
                elif event.key == pygame.K_DOWN:
                    camera.move_down(settings.MOVE_STEP)
                elif event.key == pygame.K_SPACE:
                    paused = not paused
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                world_x = mouse_x / camera.scale - camera.offset_x
                world_y = mouse_y / camera.scale - camera.offset_y

                if event.button == 1:
                    for body in bodies:
                        dx = body.position.x - world_x
                        dy = body.position.y - world_y
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
                        dx = body.position.x - world_x
                        dy = body.position.y - world_y
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
            pos = camera.world_to_screen(body.position)
            radius = int(body.radius * camera.scale)
            pygame.draw.circle(screen, settings.BODY_COLOR, pos, radius)
            vel_end = (pos[0] + int(body.velocity.x * camera.scale), pos[1] + int(body.velocity.y * camera.scale))
            pygame.draw.line(screen, settings.VELOCITY_COLOR, pos, vel_end, 2)

        pygame.display.flip()
        clock.tick(60)

        control_panel.update()

    pygame.quit()

if __name__ == "__main__":
    main()
