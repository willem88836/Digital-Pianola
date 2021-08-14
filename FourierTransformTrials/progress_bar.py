
import threading

class progress_bar: 
    __current_progress = 0

    def __init__(self, max_progress: int, bar_length: int) -> None:
        self.max_progress = max_progress
        self.bar_length = bar_length
        self.__current_progress = 0
        self.update_progress(0)

    def update_progress(self, i) -> None:
        self.__current_progress = i
        p = float(self.__current_progress) / self.max_progress
        length = int(p * self.bar_length)
        bar_fill = self.bar_length - length
        print(f'\rProgress: {self.__current_progress}/{self.max_progress} - {(p * 100):.2f}% [{length * "#"}{bar_fill * " "}]', end='')
        self.__current_progress += 1
