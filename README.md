# Overview


# Developing
> NOTE: This project uses Make to automate the python virtual environment workflow.
All Make commands run in a seperate venv instance that is closed when finished. 
This allows for the user to not have to start a venv everytime you want to test
or run the code.
## Install
```bash

# Clone the repo
git clone git@github.com:skyler-oakeson/multiagent_wealth_redistribution.git

# Initialize the project and install required packages in a python venv
make init
```

## Running
```bash
# Run the code
make run
```

## Testing
```bash
# Run tests
make test
```

## Linting
```bash
# Lint project
make lint
```

## Type Checking
```bash
# Type check project
make check
```

## Clean venv
```bash
# Remove venv
make clean
```
