import pygame # pylint: disable=W0611

class HUD:
  METER_RADIUS = 10
  CHARGING_COLOR = (255, 127, 127)
  READY_COLOR = (127, 127, 255)
  HIGHLIGHT_PC_COLOR = (188, 254, 99)
  HIGHLIGHT_SKILL_COLOR = (0, 254, 0)
  COLUMN_SPACING = METER_RADIUS * 3
  SKILL_METER_SPACING = METER_RADIUS * 2
  ACTIVE_PC_BOX_WIDTH = METER_RADIUS * 1.5
  ACTIVE_SKILL_RADIUS = METER_RADIUS + 4

  def __init__(self, game):
    self.game = game
    self.screen_height = self.game.screen.get_height()
    pygame.font.init()
    self.font = pygame.font.SysFont('Comic Sans MS', 30)

  def draw(self):
    health = str(self.game.pcs[self.game.active_pc].health_points)
    health = self.font.render(health, False, (0, 0, 255))
    self.game.screen.blit(health, (10, 10))

    draw_y = self.screen_height

    draw_x = HUD.COLUMN_SPACING
    draw_y -= HUD.SKILL_METER_SPACING

    for i, pc in enumerate(self.game.pcs):
      draw_y = self.screen_height
      draw_y -= HUD.SKILL_METER_SPACING
      draw_x += HUD.COLUMN_SPACING

      if self.game.active_pc == i:
        pygame.draw.rect(self.game.screen,
                        HUD.HIGHLIGHT_PC_COLOR,
                        pygame.Rect(draw_x - (HUD.METER_RADIUS),
                        draw_y - (len(pc.skills) * HUD.SKILL_METER_SPACING * 2),
                        HUD.METER_RADIUS * 2,
                        len(pc.skills) * HUD.SKILL_METER_SPACING * 2))

      for j, skill in enumerate(pc.skills):
        draw_y -= HUD.SKILL_METER_SPACING

        if pc.active_skill == j:
          pygame.draw.circle(self.game.screen, HUD.HIGHLIGHT_SKILL_COLOR, (draw_x, draw_y), HUD.ACTIVE_SKILL_RADIUS)

        if skill.cooldown_countdown <= 0:
          pygame.draw.circle(self.game.screen, HUD.READY_COLOR, (draw_x, draw_y), HUD.METER_RADIUS)
        else:
          pygame.draw.circle(self.game.screen, HUD.CHARGING_COLOR, (draw_x, draw_y), HUD.METER_RADIUS)
