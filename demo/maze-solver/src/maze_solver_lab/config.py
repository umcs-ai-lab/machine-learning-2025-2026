from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    rows: int = 31
    cols: int = 41
    cell_size: int = 20
    panel_height: int = 116
    frames_per_second: int = 60
    solver_steps_per_tick: int = 1
    random_seed: int | None = 7

    @property
    def window_width(self) -> int:
        return self.cols * self.cell_size

    @property
    def window_height(self) -> int:
        return self.rows * self.cell_size + self.panel_height
