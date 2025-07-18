#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para inspecionar o Google Forms e obter os IDs dos campos
Este script deve ser executado uma vez para configurar a integração
"""

import requests
import re
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import os
from dotenv import load_dotenv

def extract_form_fields(form_url: str) -> dict:
    """
    Extrai os IDs dos campos do Google Forms
    
    Args:
        form_url: URL do formulário
        
    Returns:
        dict: Mapeamento dos campos e seus IDs
    """
    try:
        print(f"Inspecionando formulário: {form_url}")
        
        # Fazer requisição para obter o HTML
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(form_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        html_content = response.text
        
        # Usar BeautifulSoup para parsing mais preciso
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Procurar por campos de entrada
        fields = {}
        field_counter = 0
        
        # Procurar por padrões entry.XXXXXXXXX
        entry_pattern = r'entry\.(\d+)'
        matches = re.findall(entry_pattern, html_content)
        
        # Remover duplicatas mantendo ordem
        unique_entries = []
        seen = set()
        for match in matches:
            if match not in seen:
                unique_entries.append(match)
                seen.add(match)
        
        print(f"Encontrados {len(unique_entries)} campos únicos")
        
        # Mapear campos baseado na ordem esperada do formulário
        field_names = ['tipo_lancamento', 'valor', 'categoria', 'descricao', 'data']
        
        for i, entry_id in enumerate(unique_entries[:len(field_names)]):
            if i < len(field_names):
                fields[field_names[i]] = f'entry.{entry_id}'
                print(f"Campo '{field_names[i]}': entry.{entry_id}")
        
        # Tentar encontrar informações adicionais sobre os campos
        print("\n--- Análise detalhada ---")
        
        # Procurar por elementos de input e select
        inputs = soup.find_all(['input', 'select', 'textarea'])
        for inp in inputs:
            name = inp.get('name', '')
            if name.startswith('entry.'):
                data_params = inp.get('data-params', '')
                aria_label = inp.get('aria-label', '')
                print(f"Campo {name}: {aria_label or 'sem label'}")
        
        return fields
        
    except Exception as e:
        print(f"Erro ao inspecionar formulário: {e}")
        return {}

def update_integration_file(fields: dict):
    """Atualiza o arquivo de integração com os IDs dos campos"""
    try:
        # Ler arquivo atual
        with open('google_forms_integration.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Criar novo mapeamento
        new_mapping = "        self.field_mapping = {\n"
        for field_name, entry_id in fields.items():
            new_mapping += f"            '{field_name}': '{entry_id}',\n"
        new_mapping += "        }"
        
        # Substituir o mapeamento antigo
        import re
        pattern = r'self\.field_mapping = \{[^}]+\}'
        new_content = re.sub(pattern, new_mapping.strip(), content, flags=re.DOTALL)
        
        # Salvar arquivo atualizado
        with open('google_forms_integration.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("Arquivo de integração atualizado com sucesso!")
        
    except Exception as e:
        print(f"Erro ao atualizar arquivo de integração: {e}")

def main():
    """Função principal"""
    load_dotenv()
    FORM_URL = os.getenv("GOOGLE_FORM_URL")
    
    print("=== Inspetor de Campos do Google Forms ===\n")
    
    form_url = FORM_URL
    
    # Extrair campos
    fields = extract_form_fields(form_url)
    
    if fields:
        print(f"\n=== Campos encontrados ===")
        for field_name, entry_id in fields.items():
            print(f"{field_name}: {entry_id}")
        
        # Salvar em arquivo JSON para referência
        with open("form_fields.json", "w", encoding="utf-8") as f:
            json.dump(fields, f, indent=2, ensure_ascii=False)
        
        print(f"\nCampos salvos em \'form_fields.json\'")
        
        # Atualizar arquivo de integração
        update_integration_file(fields)
        
    else:
        print("Nenhum campo encontrado. Verifique a URL do formulário.")

if __name__ == '__main__':
    main()

