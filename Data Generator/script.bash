sudo yum update -y
sudo yum install python3.12
sudo yum install unzip
python3.12 --version
python3.12 -m ensurepip --upgrade
python3.12 -m pip install --upgrade pip
mkdir MCTS
unzip quantum-chess-bot-player-main.zip
mv quantum-chess-bot-player-main/ MCTS/
mv MCTS/quantum-chess-bot-player-main/Data\ Generator/* MCTS/
mv MCTS/quantum-chess-bot-player-main/ MCTS/quantum-chess-bot-player/
python3.12 -m pip install -r MCTS/quantum-chess-bot-player/requirements.txt
cd MCTS