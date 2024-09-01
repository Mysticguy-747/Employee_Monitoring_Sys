from pynput import keyboard
import os

stop_file = 'stop_signal.txt'

def stop_listener():
    def on_press(key):
        try:
            if key == keyboard.KeyCode.from_char('k') and (
                keyboard.Controller().pressed[keyboard.Key.ctrl_l] or 
                keyboard.Controller().pressed[keyboard.Key.ctrl_r]
            ):
                with open(stop_file, 'w') as f:
                    f.write('Stop signal activated.')
                print(f"{stop_file} created. All scripts will stop.")
                return False  # Stop the listener
        except AttributeError:
            pass

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
