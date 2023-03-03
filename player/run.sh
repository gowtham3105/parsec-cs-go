# activate the virtual environment
source ./venv/bin/activate

# check if the virtual environment is activated
which python

# check if two arguments are passed
if [ $# -ne 2 ]; then
    echo "Invalid arguments"
    echo "Usage: ./run.sh --player <player_name>"
    exit 1
fi


echo "Running the player.."
# run the player
python main.py $1 $2
