# Program Runner
To create and manage shell scripts for specific programs. Allows the user to store multiple scripts in a central repository to allow ease of use with different version control softwares.


## Setup Instructions (MacOS/Linux)
1. Clone the repository
2. Get the default shell startup file
   - Run `echo $SHELL` in terminal
   - MacOS:
     - for `/bin/zsh` use `.zshrc`
     - for `/bin/bash` use `.profile`
   - Linux:
     - for `/bin/bash` use  `.bashrc`
4. Add an alias to the default shell startup file
   - Execute `echo "alias pr=python3 <path of main.py>" >> ~/<default shell startup file>` in terminal
     - Note: You can use any alias name instead of `pr`
6. Update the shell to use the new startup script
   - Execute `source ~/<default shell startup file>` in terminal
7. Run `pr --setup` to finish setup


## Setup Instructions (Windows)
1. Clone the repository
2. Create a new file `pr.bat` in any folder on the `%PATH%` variable
   - To view the current path folders, execute `echo %PATH%` in command prompt
     - Note: It might be better to make a new directory for certain aliases and add that to path
   - If you want to use a different alias, use `<alias>.bat` instead of `pr.bat`
3. Edit the `pr.bat` file to include the following lines
```
@echo off
echo.
python <path of main.py> %1
```
4. Run `pr --setup` to finish setup


## Usage Instructions
Ensure all instructions are run from the directory you would ideally want the script to be called from
#### Creating a new script:
- Creating a simple barebones script
  - `pr -n` or `pr --new`
- Creating a script from an existing script file
  - `pr -nf <file>` or `pr --new --file <file>`
#### Editing an existing script;
- Edit using vim
  - `pr -e` or `pr --edit`
- Edit by copying an existing script file
  - `pr -ef <file>` or `pr --edit --file <file>`
#### Deleting an existing script;
- `pr -d` or `pr --del`
#### Printing the current script:
- `pr -p` or `pr --print`
#### View the help menu;
- `pr -h` or `pr --help`
