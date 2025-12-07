# utils.py

def render_text_centered(surface, text, font, color, center):
    """Render text centered at a given position on the surface."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=center)
    surface.blit(text_surface, text_rect)
    return text_rect