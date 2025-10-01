"""
Pytest configuration file for GalaxyWizard tests.
Initializes pygame and OpenGL context before running tests.
"""

import os
import sys

# Set environment variables before any pygame/OpenGL imports
# This MUST happen before pygame is imported
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

# Initialize pygame immediately before any test imports
import pygame
pygame.init()

# Create a minimal OpenGL-compatible display
# This is required for PyOpenGL to initialize properly
try:
    pygame.display.set_mode((640, 480), pygame.OPENGL | pygame.DOUBLEBUF | pygame.HIDDEN)
    print("✓ Pygame display initialized with OpenGL")
except pygame.error as e:
    print(f"Warning: OpenGL display failed ({e}), trying fallback...")
    # Fallback to minimal display if OpenGL fails
    try:
        pygame.display.set_mode((1, 1))
        print("✓ Pygame display initialized (fallback mode)")
    except pygame.error as e2:
        print(f"Error: Could not initialize pygame display: {e2}")

# Now it's safe to import pytest
import pytest

@pytest.fixture(scope="session", autouse=True)
def pygame_cleanup():
    """Cleanup pygame after all tests complete."""
    yield
    pygame.quit()
