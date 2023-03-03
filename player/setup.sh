# if venv is present then delete it
if [ -d venv ]; then
  echo "-> Deleting the existing virtual environment.."
  rm -rf venv
fi

echo "-> Creating virtual environment.."
# create env
python3 -m venv venv

echo "-> Virtual environment created.."
echo "-> Activating virtual environment.."
# activate env
source ./venv/bin/activate

# check if the virtual environment is activated
which python

echo "-> Virtual environment activated.."
# check if requirements.txt is present
if [ ! -f requirements.txt ]; then
  echo "requirements.txt not found"
  exit 1
fi
echo "-> Installing requirements.."

# install the requirements
pip install -r requirements.txt

echo "-> Requirements installed.."
# deactivate env
deactivate

echo "-> Setup complete.. Run the player with ./run.sh"
