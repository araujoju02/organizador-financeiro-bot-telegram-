#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
import json
from datetime import datetime
from typing import Dict, Any
from dotenv import load_dotenv

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Token do bot
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GOOGLE_FORM_URL = os.getenv('GOOGLE_FORM_URL')

# Estados da conversa
TIPO_LANCAMENTO, VALOR, CATEGORIA, DESCRICAO, DATA = range(5)

# Dados do formulário
TIPOS_LANCAMENTO = [
    'Entrada', 'Empréstimo', 'Despesa Débito', 
    'Despesa Crédito', 'Despesa Pix', 'Saldo'
]

CATEGORIAS = [
    'Restaurante', 'Supermercado', 'Farmácia', 'Posto de Gasolina',
    'Carro', 'Faculdades', 'Dentista', 'Luz', 'Gás', 'Mercado Livre',
    'IPVA', 'Mariluce - Mãe', 'Nubank Giulia', 'Nubank Beatriz',
    'Inter Juliana', 'Inter Giulia', 'Mercado Pago', 'Itau',
    'Animais', 'Imprevisto', 'Salário', 'Vale', 'Outros Ganhos', 'Transporte'
]

# Armazenamento temporário de dados do usuário
user_data_storage = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /start - Apresenta o bot"""
    welcome_message = """
🏦 *Organizador Financeiro Bot*

Olá! Eu sou seu assistente financeiro pessoal. 
Posso ajudá-lo a registrar suas transações financeiras de forma rápida e organizada.

*Comandos disponíveis:*
• /novo - Registrar nova transação
• /ajuda - Ver todos os comandos
• /cancelar - Cancelar operação atual

Para começar, digite /novo para registrar uma nova transação financeira.
    """
    
    await update.message.reply_text(
        welcome_message,
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /ajuda - Mostra ajuda"""
    help_text = """
🆘 *Ajuda - Organizador Financeiro*

*Comandos disponíveis:*

• `/start` - Iniciar o bot
• `/novo` - Registrar nova transação financeira
• `/ajuda` - Mostrar esta mensagem de ajuda
• `/cancelar` - Cancelar operação atual

*Como usar:*
1. Digite `/novo` para iniciar um novo registro
2. Siga as instruções passo a passo
3. Confirme os dados antes do envio

*Tipos de lançamento disponíveis:*
• Entrada • Empréstimo • Despesa Débito
• Despesa Crédito • Despesa Pix • Saldo

O bot irá guiá-lo através de cada etapa do processo!
    """
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def novo_lancamento(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Inicia o processo de novo lançamento"""
    user_id = update.effective_user.id
    user_data_storage[user_id] = {}
    
    # Criar teclado com tipos de lançamento
    keyboard = []
    for i in range(0, len(TIPOS_LANCAMENTO), 2):
        row = TIPOS_LANCAMENTO[i:i+2]
        keyboard.append(row)
    
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        "💰 *Novo Lançamento Financeiro*\n\n"
        "Vamos registrar sua transação passo a passo.\n\n"
        "**1/5** - Selecione o tipo de lançamento:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    
    return TIPO_LANCAMENTO

async def receber_tipo_lancamento(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Recebe o tipo de lançamento"""
    user_id = update.effective_user.id
    tipo = update.message.text
    
    if tipo not in TIPOS_LANCAMENTO:
        await update.message.reply_text(
            "❌ Tipo inválido. Por favor, selecione uma das opções do teclado."
        )
        return TIPO_LANCAMENTO
    
    user_data_storage[user_id]['tipo_lancamento'] = tipo
    
    await update.message.reply_text(
        f"✅ Tipo selecionado: *{tipo}*\n\n"
        "**2/5** - Digite o valor em reais (R$):\n"
        "Exemplo: 150.50 ou 1500",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode='Markdown'
    )
    
    return VALOR

async def receber_valor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Recebe o valor"""
    user_id = update.effective_user.id
    valor_texto = update.message.text.replace(',', '.')
    
    try:
        valor = float(valor_texto)
        if valor <= 0:
            raise ValueError("Valor deve ser positivo")
        
        user_data_storage[user_id]['valor'] = valor
        
        # Criar teclado com categorias (3 por linha)
        keyboard = []
        for i in range(0, len(CATEGORIAS), 3):
            row = CATEGORIAS[i:i+3]
            keyboard.append(row)
        
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        
        await update.message.reply_text(
            f"✅ Valor registrado: *R$ {valor:.2f}*\n\n"
            "**3/5** - Selecione a categoria:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        
        return CATEGORIA
        
    except ValueError:
        await update.message.reply_text(
            "❌ Valor inválido. Digite apenas números.\n"
            "Exemplo: 150.50 ou 1500"
        )
        return VALOR

async def receber_categoria(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Recebe a categoria"""
    user_id = update.effective_user.id
    categoria = update.message.text
    
    if categoria not in CATEGORIAS:
        await update.message.reply_text(
            "❌ Categoria inválida. Por favor, selecione uma das opções do teclado."
        )
        return CATEGORIA
    
    user_data_storage[user_id]['categoria'] = categoria
    
    await update.message.reply_text(
        f"✅ Categoria selecionada: *{categoria}*\n\n"
        "**4/5** - Digite uma descrição ou observação:",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode='Markdown'
    )
    
    return DESCRICAO

async def receber_descricao(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Recebe a descrição"""
    user_id = update.effective_user.id
    descricao = update.message.text
    
    user_data_storage[user_id]['descricao'] = descricao
    
    await update.message.reply_text(
        f"✅ Descrição registrada: *{descricao}*\n\n"
        "**5/5** - Digite a data do lançamento ou envie 'hoje' para usar a data atual:\n"
        "Formato: DD/MM/AAAA ou 'hoje'",
        parse_mode='Markdown'
    )
    
    return DATA

async def receber_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Recebe a data e finaliza o registro"""
    user_id = update.effective_user.id
    data_texto = update.message.text.lower()
    
    if data_texto == 'hoje':
        data = datetime.now().strftime('%d/%m/%Y')
    else:
        try:
            # Validar formato da data
            datetime.strptime(data_texto, '%d/%m/%Y')
            data = data_texto
        except ValueError:
            await update.message.reply_text(
                "❌ Data inválida. Use o formato DD/MM/AAAA ou digite 'hoje'.\n"
                "Exemplo: 15/07/2025"
            )
            return DATA
    
    user_data_storage[user_id]['data'] = data
    
    # Mostrar resumo e pedir confirmação
    dados = user_data_storage[user_id]
    resumo = f"""
📋 *Resumo da Transação*

• **Tipo:** {dados['tipo_lancamento']}
• **Valor:** R$ {dados['valor']:.2f}
• **Categoria:** {dados['categoria']}
• **Descrição:** {dados['descricao']}
• **Data:** {dados['data']}

Confirma o envio desta transação?
    """
    
    keyboard = [
        [InlineKeyboardButton("✅ Confirmar", callback_data="confirmar")],
        [InlineKeyboardButton("❌ Cancelar", callback_data="cancelar")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        resumo,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    
    return ConversationHandler.END

async def confirmar_envio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Confirma e processa o envio"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if query.data == "confirmar":
        if user_id in user_data_storage:
            dados = user_data_storage[user_id]
            
            # Aqui seria feita a integração com o Google Forms
            # Por enquanto, vamos simular o envio
            sucesso = await enviar_para_google_forms(dados)
            
            if sucesso:
                await query.edit_message_text(
                    "✅ *Transação registrada com sucesso!*\n\n"
                    "Seus dados foram enviados para o sistema financeiro.\n\n"
                    "Digite /novo para registrar outra transação.",
                    parse_mode='Markdown'
                )
            else:
                await query.edit_message_text(
                    "❌ *Erro ao registrar transação*\n\n"
                    "Houve um problema ao enviar os dados. Tente novamente.\n\n"
                    "Digite /novo para tentar novamente.",
                    parse_mode='Markdown'
                )
            
            # Limpar dados do usuário
            del user_data_storage[user_id]
        else:
            await query.edit_message_text("❌ Dados não encontrados. Inicie novamente com /novo")
    
    elif query.data == "cancelar":
        if user_id in user_data_storage:
            del user_data_storage[user_id]
        
        await query.edit_message_text(
            "❌ *Transação cancelada*\n\n"
            "Digite /novo para registrar uma nova transação.",
            parse_mode='Markdown'
        )

async def enviar_para_google_forms(dados: Dict[str, Any]) -> bool:
    """Envia dados para Google Forms"""
    from google_forms_integration import enviar_dados_formulario
    
    try:
        sucesso = await enviar_dados_formulario(dados, GOOGLE_FORM_URL)
        if sucesso:
            logger.info(f"Dados enviados com sucesso: {dados}")
        else:
            logger.error(f"Falha ao enviar dados: {dados}")
        return sucesso
    except Exception as e:
        logger.error(f"Erro ao enviar para Google Forms: {e}")
        return False

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancela a operação atual"""
    user_id = update.effective_user.id
    
    if user_id in user_data_storage:
        del user_data_storage[user_id]
    
    await update.message.reply_text(
        "❌ Operação cancelada.\n\n"
        "Digite /novo para registrar uma nova transação.",
        reply_markup=ReplyKeyboardRemove()
    )
    
    return ConversationHandler.END

def main() -> None:
    """Função principal"""
    if not TOKEN:
        logger.error("Token do Telegram não encontrado!")
        return
    
    # Criar aplicação
    application = Application.builder().token(TOKEN).build()
    
    # Configurar handlers de conversa
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('novo', novo_lancamento)],
        states={
            TIPO_LANCAMENTO: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_tipo_lancamento)],
            VALOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_valor)],
            CATEGORIA: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_categoria)],
            DESCRICAO: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_descricao)],
            DATA: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_data)],
        },
        fallbacks=[CommandHandler('cancelar', cancelar)],
    )
    
    # Adicionar handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ajuda", help_command))
    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(confirmar_envio))
    
    # Iniciar bot
    logger.info("Bot iniciado!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()

