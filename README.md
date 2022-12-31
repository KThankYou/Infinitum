# __Infinitum__

### _Preface_
This is a part of a project made for our first sem in college. The project we finally settled on was Infinitum. This python program was made purely in pygame and exists to act as a launcher/virtual machine for running pygame applications. 

### _Introduction_
When launched for the first time it will create an encrypted storage file. The encryption used is Vignere's cipher but its used on the hash of the password meaning the key for the cipher is 256 characters long, so it gives some level of protection. The virtual device is dynamically allocated to the physical drive.

While you can add in any file from your drive onto the virtual drive, currently (as of v.5.3), there is no GUI support for it.

After the first install you will need to relaunch the program again at which point you will be at the login window. Again it is possible to change all backgrounds/wallpapers but currently (as of v.5.3), there is no GUI support for it. These features will be added in v.7

After logging in you will be on the homescreen which was designed with inspiration from Windows. You can install compatible programs by using the Install button from the PopUp Menu which appears when you click on the power icon at the bottom left of the taskbar (see __Compatibility__ for further information). This will allow you to select the directory with the _infinstall.toml_ file. After a successful installation, an icon will appear on the desktop which when clicked will launch the program in a window inside the program. The behaviours of this window can be specified in the _infinstall.toml_ file (see __Compatibility__). You can drag, minimize, maximize, restore and close the app using the window frame. The icon in the taskbar also allows for minimizing and restoring.

## __Getting Started__

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
<br>

### __Prerequisites__

- Python 3.11.x (Tested only on 3.11)
- pygame
<br>

### __Installation__

Step-by-step instructions for setting up the project on your local machine.

1. Clone the repository to your local machine:

```bash
git clone https://github.com/KThankYou/Infinitum
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. __Running the Program__: to run the program, navigate to the directory containing the cloned repository and open run.py

## __Compatibility__

Infinitum is designed to be a platform for running Pygame applications. In order for a Pygame application to be compatible with Infinitum, it must include a `infinstall.toml` configuration file in its root directory. This file specifies the behaviors of the application when it is launched within Infinitum, such as the window size, title, and resizability.

To make a Pygame application compatible with Infinitum, create a `infinstall.toml` file in the root directory of the application and set the following variables:

- `target`: the name of the file containing the `Process` class which has  `draw()` generator and `handle_event()` method
- `width` and `height`: the window size in pixels
- `fullscreen`: a boolean value indicating whether the program should use the maximum resolution
- `borders`: a boolean value indicating whether the program should have window borders
- `name`: the name to be displayed on the icon and title bar
- `image`: the path to the image to be used as the icon
- `draggable`: a boolean value indicating whether the window should be draggable
- `resizeable`: a boolean value indicating whether the window should be resizable

Here is a sample:
```toml
# Infinitum Installer config(infinstall.toml):
#
# Any line starting with # is a comment
# 
# <> means placeholder and it must be replaced with appropriate values
# 
# The installer config must be in the uppermost level of the program directory
# Meaning the folder where the config is stored and everything inside it will be stored
# into the Infinitum.vc
#
# The Order of these variables does not matter but all must exist

# Name of the file with `Process` class which has 
# a generator draw() which yields a pygame.Surface and
# a method handle_event(event: pygame.event.Event, mouse_pos: Tuple[int, int], keys: pygame.key.ScancodeWrapper) to handle events
target = "<name of file>" 

# It must be integers in the form width x height, ex 1280x720
width = <width>
height = <height>

# Must be a boolean value. Indicates whether the program should use the max resolution or not. 
# If this is set to True, resolution, border, draggable and resizeable will be ignored.
fullscreen = <bool>

# Must be a boolean value. Indicates whether the program should have borders or not
# Borders are basically the frame of the window with the start, stop etc
borders = <bool>

# This name will be displayed on the Icon and the title bar of the window frame
name = "<name of app>"

# This is the image which will be used as the icon
image = "<path to image>"

# Must be a boolean value. Set if the window should be draggable or not.
# If set to True then a rect will be passed to process.handle_event(rect = pygame.Rect)
# whose x, y will be the topleft part of the window.
draggable = <bool>

# Must be a boolean value. Set if the window should be resizeable or not.
# If set to True then an will be passed to process.handle_event
# which has an event.type == pygame.VIDEORESIZE
resizeable = <bool>
```

Here is an example `infinstall.toml` file:

```toml
target = "main.py"
width = 640
height = 480
fullscreen = false
borders = true
name = "My Pygame App"
image = "icon.png"
draggable = true
resizeable = true
```

Here is an example of a Process class:
```python
class Process:
    def __init__(self, size: Tuple[int, int], working_dir: str, *args, **kwargs) -> None:
        raise NotImplementedError
    
    def draw(self) -> pygame.Surface:
        raise NotImplementedError

    def handle_event(self, event: pygame.event.Event, mouse_pos: Tuple[int, int],
        keys: pygame.key.ScancodeWrapper, rect: Optional[pygame.Rect], *args, **kwargs) -> None:
        raise NotImplementedError
```
In the `init` method, `size` refers to the resolution in wxh that your program will have. This uses the value specified in the `infinstall.toml` file. The `working_dir` is the path on the physical drive where the program has been currently extracted to for the purpose of execution. The file will be deleted once Infinitum is closed.

In the `handle_event` method, `rect` is provided only if your window is set to be draggable and not fullscreen.

### __Example__
The following programs were designed as part of the project:
Chess: https://github.com/KThankYou/Chess/tree/Infinitum-ver by [Gin](https://github.com/KThankYou/)

## __Built With__

- [Pygame](https://www.pygame.org/) - A set of Python modules designed for game development

## __License__

This project is released under the Unlicense - see the [LICENSE](LICENSE) file for details.