from __future__ import annotations

import math
import random
from abc import ABC, abstractmethod
from dataclasses import dataclass

import pyxel


class Context:
    def __init__(self, state: State) -> None:
        self._state = state

    def transition_to(self, next_state: State) -> None:
        self._state = next_state


class State(ABC):
    @abstractmethod
    def update(self, context: Context) -> None: ...

    @abstractmethod
    def draw(self) -> None: ...


class GameState(State):
    def __init__(self) -> None:
        self._score: int = 10
        self._cur_enemy: Circle = Circle.random()

    def update(self, context: Context) -> None:
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            cursor = Circle(pyxel.mouse_x, pyxel.mouse_y, 2)
            if cursor.overlaps(self._cur_enemy):
                self._score += 10
                self._cur_enemy = Circle.random()
            else:
                self._score -= 15

        if self._score < 0:
            context.transition_to(GameOverState())

    def draw(self) -> None:
        pyxel.cls(10)

        if self._cur_enemy and self._cur_enemy.c:
            pyxel.circ(
                self._cur_enemy.x,
                self._cur_enemy.y,
                self._cur_enemy.r,
                self._cur_enemy.c,
            )
        pyxel.circ(pyxel.mouse_x, pyxel.mouse_y, 2, 11)

        score_txt = f"SCORE: {self._score:>4}"
        pyxel.text(5, 4, score_txt, 1)
        pyxel.text(4, 4, score_txt, 7)


class GameOverState(State):
    def __init__(self) -> None:
        self._cnt_click = 3
        pyxel.cls(0)

    def update(self, context: Context) -> None:
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self._cnt_click -= 1
            if not self._cnt_click:
                context.transition_to(GameState())

    def draw(self) -> None:
        pyxel.text(
            random.choice(range(0, 320)),
            random.choice(range(0, 240)),
            "GAME OVER",
            random.choice(range(1, 10)),
        )


@dataclass
class Circle:
    x: int
    y: int
    r: int
    c: int | None = None

    @staticmethod
    def random() -> Circle:
        return Circle(
            random.choice(range(1, 320)),
            random.choice(range(1, 240)),
            random.choice(range(5, 16)),
            random.choice(range(1, 10)),
        )

    def overlaps(self, other: Circle) -> bool:
        return math.hypot(other.x - self.x, other.y - self.y) < (self.r + other.r)


class App(Context):
    def __init__(self) -> None:
        self._state = GameState()
        pyxel.init(320, 240)

    def run(self) -> None:
        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self._state.update(self)

    def draw(self) -> None:
        self._state.draw()


App().run()
