# 🚀 Instruções de Deploy - Organizador Financeiro Bot

## Opções de Deploy

### 1. 🖥️ Servidor Local/VPS

#### Pré-requisitos
- Ubuntu 20.04+ ou similar
- Python 3.11+
- Acesso root/sudo

#### Passos

1. **Preparar o servidor**:
```bash
sudo apt update
sudo apt install python3 python3-pip git -y
```

2. **Clonar/enviar arquivos**:
```bash
# Opção 1: Se usando Git
git clone <seu-repositorio>

# Opção 2: Enviar arquivos via SCP
scp -r organizador_financeiro_bot/ user@servidor:/home/user/
```

3. **Configurar ambiente**:
```bash
cd organizador_financeiro_bot
pip3 install -r requirements.txt
```

4. **Configurar .env**:
```bash
nano .env
# Adicionar:
# TELEGRAM_BOT_TOKEN=seu_token_real
# GOOGLE_FORM_URL=https://forms.gle/j5M7oFGN2YxwDCY4A
```

5. **Configurar campos do formulário**:
```bash
python3 manual_form_config.py  # Ver instruções
nano manual_form_config.py     # Editar IDs dos campos
```

6. **Testar execução**:
```bash
./run_bot.sh
```

#### Executar como Serviço (systemd)

1. **Criar arquivo de serviço**:
```bash
sudo nano /etc/systemd/system/financeiro-bot.service
```

2. **Conteúdo do arquivo**:
```ini
[Unit]
Description=Organizador Financeiro Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/organizador_financeiro_bot
ExecStart=/usr/bin/python3 bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. **Ativar serviço**:
```bash
sudo systemctl daemon-reload
sudo systemctl enable financeiro-bot
sudo systemctl start financeiro-bot
sudo systemctl status financeiro-bot
```

### 2. 🐳 Docker

#### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
```

#### docker-compose.yml
```yaml
version: '3.8'
services:
  financeiro-bot:
    build: .
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - ./logs:/app/logs
```

#### Comandos
```bash
# Construir e executar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar
docker-compose down
```

### 3. ☁️ Cloud (Heroku)

#### Arquivos necessários

**Procfile**:
```
worker: python bot.py
```

**runtime.txt**:
```
python-3.11.0
```

#### Passos
```bash
# Instalar Heroku CLI
# Fazer login
heroku login

# Criar app
heroku create seu-financeiro-bot

# Configurar variáveis
heroku config:set TELEGRAM_BOT_TOKEN=seu_token
heroku config:set GOOGLE_FORM_URL=https://forms.gle/j5M7oFGN2YxwDCY4A

# Deploy
git add .
git commit -m "Deploy inicial"
git push heroku main

# Escalar worker
heroku ps:scale worker=1
```

### 4. 🌐 Railway

1. Conectar repositório no Railway
2. Configurar variáveis de ambiente
3. Deploy automático

### 5. 📱 Render

1. Conectar repositório no Render
2. Configurar como "Background Worker"
3. Adicionar variáveis de ambiente
4. Deploy automático

## ⚙️ Configuração de Produção

### Variáveis de Ambiente
```env
TELEGRAM_BOT_TOKEN=seu_token_real
GOOGLE_FORM_URL=https://forms.gle/j5M7oFGN2YxwDCY4A
LOG_LEVEL=INFO
ENVIRONMENT=production
```

### Logs
Para produção, considere:
- Rotação de logs
- Monitoramento de erros
- Alertas de falha

### Monitoramento
- Uptime monitoring
- Health checks
- Métricas de uso

### Backup
- Backup regular dos logs
- Backup da configuração
- Plano de recuperação

## 🔒 Segurança

### Boas Práticas
- Nunca commitar tokens no Git
- Usar HTTPS sempre que possível
- Manter dependências atualizadas
- Monitorar logs de segurança

### Firewall
```bash
# Permitir apenas SSH e saída
sudo ufw allow ssh
sudo ufw enable
```

## 📊 Monitoramento

### Logs do Sistema
```bash
# Ver logs do serviço
sudo journalctl -u financeiro-bot -f

# Ver logs do Docker
docker-compose logs -f
```

### Métricas Básicas
- Uptime do bot
- Número de mensagens processadas
- Taxa de erro de envio
- Tempo de resposta

## 🚨 Troubleshooting

### Bot não inicia
1. Verificar token do Telegram
2. Verificar conectividade de rede
3. Verificar logs de erro
4. Verificar dependências

### Erro de envio para formulário
1. Verificar IDs dos campos
2. Testar formulário manualmente
3. Verificar logs de requisição
4. Verificar conectividade

### Alta latência
1. Verificar recursos do servidor
2. Otimizar código se necessário
3. Considerar cache se aplicável

## 📈 Escalabilidade

Para alto volume:
- Usar Redis para cache
- Implementar rate limiting
- Considerar múltiplas instâncias
- Usar load balancer

## 🔄 Atualizações

### Processo de Atualização
1. Backup da configuração atual
2. Testar em ambiente de desenvolvimento
3. Deploy gradual
4. Monitorar após deploy
5. Rollback se necessário

### Versionamento
- Usar tags Git para versões
- Manter changelog
- Testar compatibilidade

---

**Escolha a opção de deploy que melhor se adequa às suas necessidades e recursos disponíveis.**

