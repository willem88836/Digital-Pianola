
def update_progress(progress, max_progress): 
    p = progress / max_progress * 100
    bar_length = 50
    bar = int(progress / max_progress * bar_length)
    bar_fill = bar_length - bar
    print(f'\rProgress: {progress}/{max_progress} - {p:.2f}% [{bar * "#"}{bar_fill * " "}]', end='')
        