# 🏦 Organizador Financeiro Bot para Telegram

Um bot automatizado para Telegram que facilita o registro de transações financeiras, integrando diretamente com Google Forms para armazenamento dos dados.

## 📋 Funcionalidades

- ✅ Interface conversacional intuitiva no Telegram
- ✅ Coleta estruturada de dados financeiros
- ✅ Validação de dados em tempo real
- ✅ Integração com Google Forms
- ✅ Confirmação antes do envio
- ✅ Suporte a diferentes tipos de transações
- ✅ Categorização automática

## 🚀 Como Usar

### 1. Comandos Disponíveis

- `/start` - Iniciar o bot e ver boas-vindas
- `/novo` - Registrar nova transação financeira
- `/ajuda` - Ver ajuda e instruções
- `/cancelar` - Cancelar operação atual

### 2. Processo de Registro

1. Digite `/novo` para iniciar
2. Selecione o **tipo de lançamento**:
   - Entrada
   - Empréstimo
   - Despesa Débito
   - Despesa Crédito
   - Despesa Pix
   - Saldo

3. Digite o **valor** em reais (ex: 150.50)

4. Selecione a **categoria**:
   - Restaurante, Supermercado, Farmácia
   - Posto de Gasolina, Carro, Faculdades
   - Dentista, Luz, Gás, Mercado Livre
   - IPVA, Contas bancárias (Nubank, Inter, Itau)
   - Animais, Imprevisto, Salário, Vale
   - Outros Ganhos, Transporte

5. Digite uma **descrição** ou observação

6. Digite a **data** (DD/MM/AAAA) ou "hoje"

7. **Confirme** os dados antes do envio

## ⚙️ Configuração

### Pré-requisitos

- Python 3.11+
- Token do bot do Telegram
- Acesso ao Google Forms

### Instalação

1. **Clone ou baixe os arquivos do projeto**

2. **Instale as dependências**:
```bash
pip3 install -r requirements.txt
```

3. **Configure o arquivo `.env`**:
```env
TELEGRAM_BOT_TOKEN=seu_token_aqui
GOOGLE_FORM_URL=https://forms.gle/j5M7oFGN2YxwDCY4A
```

4. **Configure os IDs dos campos do formulário** (ver seção abaixo)

5. **Execute o bot**:
```bash
python3 bot.py
```

### Configuração dos Campos do Google Forms

⚠️ **IMPORTANTE**: Para que a integração funcione, você precisa configurar os IDs dos campos do formulário.

#### Método Manual (Recomendado)

1. Abra o formulário no navegador
2. Clique com botão direito → "Inspecionar elemento" (F12)
3. Para cada campo, encontre o elemento HTML e anote o valor do atributo `name`
4. Edite o arquivo `manual_form_config.py` e substitua os valores:

```python
FORM_FIELD_IDS = {
    'tipo_lancamento': 'entry.1234567890',  # Substitua pelo ID real
    'valor': 'entry.0987654321',            # Substitua pelo ID real
    'categoria': 'entry.1122334455',        # Substitua pelo ID real
    'descricao': 'entry.5544332211',        # Substitua pelo ID real
    'data': 'entry.9988776655'              # Substitua pelo ID real
}
```

#### Como Encontrar os IDs

1. **Tipo de Lançamento**: Procure por `<input>` ou `<select>` com `name="entry.XXXXXXX"`
2. **Valor**: Procure por `<input type="text">` com `name="entry.XXXXXXX"`
3. **Categoria**: Procure por `<select>` com `name="entry.XXXXXXX"`
4. **Descrição**: Procure por `<textarea>` com `name="entry.XXXXXXX"`
5. **Data**: Procure por `<input>` de data com `name="entry.XXXXXXX"`

## 📁 Estrutura do Projeto

```
organizador_financeiro_bot/
├── bot.py                      # Código principal do bot
├── google_forms_integration.py # Integração com Google Forms
├── manual_form_config.py       # Configuração dos campos
├── form_field_inspector.py     # Utilitário para inspeção
├── requirements.txt            # Dependências
├── .env                        # Configurações (criar)
└── README.md                   # Esta documentação
```

## 🔧 Arquivos Principais

### `bot.py`
Código principal do bot com:
- Handlers de comandos
- Fluxo conversacional
- Validação de dados
- Interface com usuário

### `google_forms_integration.py`
Módulo de integração que:
- Envia dados para Google Forms
- Mapeia campos do formulário
- Trata erros de envio

### `manual_form_config.py`
Configuração dos campos:
- IDs dos campos do formulário
- URL de envio
- Instruções de configuração

## 🚀 Execução

### Modo Desenvolvimento
```bash
python3 bot.py
```

### Modo Produção
Para executar em produção, considere usar:
- **systemd** para gerenciar o serviço
- **Docker** para containerização
- **PM2** para gerenciamento de processos

## 📊 Dados Coletados

O bot coleta e envia os seguintes dados:

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| Tipo de Lançamento | Seleção | ✅ | Entrada, Empréstimo, Despesas, etc. |
| Valor | Numérico | ✅ | Valor em reais (R$) |
| Categoria | Seleção | ✅ | Categoria da transação |
| Descrição | Texto | ✅ | Observações sobre a transação |
| Data | Data | ❌ | Data da transação (padrão: hoje) |

## 🔒 Segurança

- Token do bot mantido em arquivo `.env`
- Validação de dados de entrada
- Headers de segurança nas requisições
- Logs de auditoria

## 🐛 Solução de Problemas

### Bot não responde
- Verifique se o token está correto no `.env`
- Confirme que o bot está executando
- Verifique logs de erro

### Erro ao enviar formulário
- Confirme se os IDs dos campos estão corretos
- Verifique se o formulário está público
- Analise os logs para detalhes do erro

### Campos não mapeados
- Execute `python3 manual_form_config.py` para ver instruções
- Inspecione o formulário manualmente
- Atualize os IDs em `manual_form_config.py`

## 📝 Logs

O bot gera logs detalhados incluindo:
- Início e parada do bot
- Dados recebidos dos usuários
- Tentativas de envio ao formulário
- Erros e exceções

## 🤝 Contribuição

Para contribuir com o projeto:
1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Implemente as mudanças
4. Teste thoroughly
5. Envie um pull request

## 📄 Licença

Este projeto é fornecido como está, para uso pessoal e educacional.

## 📞 Suporte

Para suporte:
1. Verifique a documentação
2. Analise os logs de erro
3. Consulte a seção de solução de problemas
4. Entre em contato com o desenvolvedor

---

**Desenvolvido com ❤️ para facilitar o controle financeiro pessoal**

