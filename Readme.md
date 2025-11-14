# Multi-Agent Simulation Framework for Safety Tests and identifying potential risks.

## Install Instructions
```shell
sudo apt update
sudo apt install -y python3-venv python3-pip

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

cat > .env << 'EOF'
OPENAI_API_KEY=your-open-ai-key
OPENAI_MODEL=gpt-4o-mini
EOF
```
**Make sure to fill the .env with your OpenAI Key**

