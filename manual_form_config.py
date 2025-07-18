#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuração manual dos campos do Google Forms
Como o formulário está protegido, os IDs dos campos devem ser configurados manualmente
"""

# Para obter os IDs dos campos, siga estes passos:
# 1. Abra o formulário no navegador
# 2. Clique com botão direito e selecione "Inspecionar elemento"
# 3. Procure pelos campos de entrada (input, select)
# 4. Encontre o atributo "name" que começa com "entry."
# 5. Substitua os valores abaixo pelos IDs reais

FORM_FIELD_IDS = {
    # IDs fornecidos pelo usuário
    'tipo_lancamento': 'entry.66743101',  # Mapeado para 'Tipo' na imagem
    'valor': 'entry.1144554732',            # Mapeado para 'Valor' na imagem
    'categoria': 'entry.1201304056',        # Mapeado para 'Cliente' na imagem (assumindo que 'Cliente' é a categoria)
    'descricao': 'entry.101816972',        # Mapeado para 'Descrição' na imagem
    'data': 'entry.385057229_day'              # Mapeado para 'Data (dia)' na imagem (usando apenas o dia para simplificar)
}

# URL do formulário para envio
FORM_SUBMIT_URL = "https://docs.google.com/forms/d/e/1FAIpQLScjT_Rs21zPy_8G_6WBml6ie3tNQihgJ8ccgm1F7-_hlN47QQ/formResponse"

def get_field_mapping():
    """Retorna o mapeamento dos campos"""
    return FORM_FIELD_IDS

def update_field_mapping(new_mapping):
    """Atualiza o mapeamento dos campos"""
    global FORM_FIELD_IDS
    FORM_FIELD_IDS.update(new_mapping)

# Instruções para configuração manual
CONFIGURATION_INSTRUCTIONS = """
=== INSTRUÇÕES PARA CONFIGURAÇÃO MANUAL ===

Para configurar os IDs dos campos do formulário:

1. Abra o formulário no navegador: https://docs.google.com/forms/d/e/1FAIpQLScjT_Rs21zPy_8G_6WBml6ie3tNQihgJ8ccgm1F7-_hlN47QQ/viewform?usp=header

2. Clique com botão direito na página e selecione "Inspecionar elemento" (F12)

3. Para cada campo do formulário, encontre o elemento HTML correspondente:
   - Tipo de Lançamento: procure por <input> ou <select> com name="entry.XXXXXXX"
   - Valor: procure por <input> com name="entry.XXXXXXX"
   - Categoria: procure por <select> com name="entry.XXXXXXX"
   - Descrição: procure por <textarea> ou <input> com name="entry.XXXXXXX"
   - Data: procure por <input> de data com name="entry.XXXXXXX"

4. Anote os números após "entry." para cada campo

5. Edite o arquivo 'manual_form_config.py' e substitua os valores em FORM_FIELD_IDS

6. Execute o bot novamente

Exemplo de como encontrar:
<input name="entry.1234567890" ...> → use "entry.1234567890"
"""

if __name__ == '__main__':
    print(CONFIGURATION_INSTRUCTIONS)


