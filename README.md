# PC-organisation-bot


A lightweight Python tool that automatically organizes files in your desktop/folders based on their extensions. It monitors the filesystem for new or moved files and moves them to predefined directories, keeping your workspace clean.

## Features
- **Real-time monitoring**: Uses `watchdog` to detect file changes immediately.
- **Customizable**: Configure your own rules via a `config.json` file.
- **Automated**: Categorizes files by extension (e.g., .txt, .pdf, .py).
- **Safe**: Excludes system/temporary files to prevent loops.

## Setup
1. Clone the repository.
2. Create your virtual environment: `python -m venv venv`.
3. Install dependencies: `pip install -r requirements.txt`.
4. Copy `config.json_example` to `config.json` and update your folder paths.
5. Run the bot: `python main.py`.

## License
MIT
