from setuptools import setup

setup(
    name='screensaver',
    options={
        'build_apps': {
            'gui_apps': {
                'screensaver': 'main.py',
            },

            # Set up output logging, important for GUI apps!
            'log_filename': 'output.log',
            'log_append': False,

            # Specify which files are included with the distribution
            'include_patterns': [
                'models/*',
            ],

            # Include the OpenGL renderer and OpenAL audio plug-in
            'plugins': [
                'pandagl',
                'p3openal_audio',
            ],
        }
    }
)