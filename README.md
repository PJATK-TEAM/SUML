Hi, here are the steps to run the app
1. Clone the repository
2. Navigate to the project directory
3. Install conda if you haven't already
4. To create a conda environment with the required dependencies from file run:

    `conda env create -f environment.yml`
5. Activate the conda environment with:

    `conda activate bird-drone-classifier-env`

6. To start the app, run:

    `fastapi dev backend/main.py`

To export the current conda environment to a new file
when you make changes to the dependencies, run:

    conda env export > environment.yml
You should delete the prefix with the path at the end of the file,
or simply run:

    conda env export | grep -v "^prefix: " > environment.yml