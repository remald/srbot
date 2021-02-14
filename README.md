This is an educational project, reproducing ESRGAN network training and running it in inference by a Telegram bot.
Made for Deep Learning School: https://www.dlschool.org/ as a final project for CNN networks in 2021, January.

The software is distributed under the Apache-V2 license, on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

# I. Neural Network

Neural network for picture super resolution  is ESRGAN.

You can see training pipeline in collab notebook, which is located in the notebook directory.

I trained it with 23 RRDBs and totally 350 convolutional layers.

I just propose a dataset filtering method, based on the picture gradient threshold. I empirically noticed, that this helps
to train a network to make a bit more detailed images, when it used on pictures, containing grass, sand or other 
fine textures.

# II. Bot

The bot is asynchronous, uses rabbitmq queue and can be scaled for many worker machines, connected by a network.

## Requirements:

ESRGAN is a large network and needs a lot of resources. 
You need at least 16 Gb of memory for the inference on 256*256 pictures.
You need a linux machine (The code was not tested on windows or other systems,
but you can try) with RubbitMQ and Python3.6+ installed.

## Running the bot on the example of Ubuntu 20.04:

### 1) Prepare Rabbit MQ
   
sudo apt update 
   
sudo apt install rabbitmq-server
   
systemctl start rabbitmq-server
   
Check if the server is running:

systemctl status rabbitmq-server

### 2) Clone the project

git clone https://bitbucket.org/remald/srbot/

cd srbot

### 3) Create config file:

touch config.json

Open it in your favorite editor and place there a telgram token and rabbutmq credentials:

{
  "token" : "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "mq_addr": "mquser:mqpassword@mqhost"
}

### 4) install python dependencies:

pip install -r requirements.txt

### 5) On the API server, run master:

python3 main.py
   
### 6) On the every worker machine, run workers:

python3 worker.py

# III. Credits

ESRGAN: Enhanced Super-Resolution Generative Adversarial Networks
Xintao Wang, Ke Yu, Shixiang Wu, Jinjin Gu, Yihao Liu, Chao Dong, Chen Change Loy, Yu Qiao, Xiaoou Tang

https://github.com/xinntao/ESRGAN
https://arxiv.org/abs/1809.00219
