#!/bin/bash

# Script para executar o Organizador Financeiro Bot
# Uso: ./run_bot.sh

echo "🏦 Iniciando Organizador Financeiro Bot..."

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado. Instale Python 3.11+ primeiro."
    exit 1
fi

# Verificar se o arquivo .env existe
if [ ! -f ".env" ]; then
    echo "❌ Arquivo .env não encontrado!"
    echo "Crie o arquivo .env com:"
    echo "TELEGRAM_BOT_TOKEN=seu_token_aqui"
    echo "GOOGLE_FORM_URL=https://forms.gle/j5M7oFGN2YxwDCY4A"
    exit 1
fi

# Verificar se as dependências estão instaladas
echo "📦 Verificando dependências..."
pip3 install -r requirements.txt --quiet

# Verificar configuração dos campos
echo "⚙️ Verificando configuração dos campos..."
python3 -c "
from manual_form_config import get_field_mapping
mapping = get_field_mapping()
if all(field_id.startswith('entry.123') for field_id in mapping.values()):
    print('⚠️  AVISO: IDs dos campos não foram configurados!')
    print('Execute: python3 manual_form_config.py para ver instruções')
    print('O bot funcionará em modo de demonstração.')
else:
    print('✅ Configuração dos campos OK')
"

echo ""
echo "🚀 Iniciando bot..."
echo "Pressione Ctrl+C para parar"
echo ""

# Executar o bot
python3 bot.py

