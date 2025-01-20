# conda create -n minicpm python=3.10 -y
# conda activate minicpm

# pip install -U packaging
# pip install -r requirements_o2.6.txt
# pip install flash_attn

# sudo amazon-linux-extras install epel -y
# sudo yum-config-manager --enable epel
# sudo yum install -y git-lfs

# sudo apt update
# sudo apt install -y git-lfs

# git lfs install
# git clone https://huggingface.co/openbmb/MiniCPM-o-2_6

python web_demos/minicpm-o_2.6/model_server.py --model MiniCPM-o-2_6

# curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
# export NVM_DIR="$HOME/.nvm"
# [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
# [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
# nvm install 20

# curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
# sudo apt install -y nodejs
# sudo npm install -g pnpm

# cd web_demos/minicpm-o_2.6/web_server
# # create ssl cert for https, https is required to request camera and microphone permissions.
# bash ./make_ssl_cert.sh  # output key.pem and cert.pem

# pnpm install  # install requirements
# pnpm run dev  # start server