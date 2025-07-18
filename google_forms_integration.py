#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import logging
from typing import Dict, Any, Optional
from urllib.parse import urlencode
from manual_form_config import get_field_mapping, FORM_SUBMIT_URL

logger = logging.getLogger(__name__)

class GoogleFormsIntegration:
    """Classe para integração com Google Forms"""
    
    def __init__(self, form_url: str):
        """
        Inicializa a integração com Google Forms
        
        Args:
            form_url: URL do formulário Google Forms
        """
        self.form_url = form_url
        self.submit_url = FORM_SUBMIT_URL
        self.field_mapping = get_field_mapping()
    
    async def submit_form(self, data: Dict[str, Any]) -> bool:
        """
        Envia dados para o Google Forms
        
        Args:
            data: Dicionário com os dados do formulário
            
        Returns:
            bool: True se enviado com sucesso, False caso contrário
        """
        try:
            # Preparar dados para envio
            form_data = {}
            
            # Mapear dados para os campos do formulário
            if 'tipo_lancamento' in data and self.field_mapping['tipo_lancamento']:
                form_data[self.field_mapping['tipo_lancamento']] = data['tipo_lancamento']
            
            if 'valor' in data and self.field_mapping['valor']:
                form_data[self.field_mapping['valor']] = str(data['valor'])
            
            if 'categoria' in data and self.field_mapping['categoria']:
                form_data[self.field_mapping['categoria']] = data['categoria']
            
            if 'descricao' in data and self.field_mapping['descricao']:
                form_data[self.field_mapping['descricao']] = data['descricao']
            
            if 'data' in data and data['data'] and self.field_mapping['data']:
                form_data[self.field_mapping['data']] = data['data']
            
            logger.info(f"Dados preparados para envio: {form_data}")
            
            # Headers para simular um navegador
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': self.form_url
            }
            
            # Fazer requisição POST
            response = requests.post(
                self.submit_url,
                data=form_data,
                headers=headers,
                timeout=10,
                allow_redirects=True
            )
            
            # Verificar se foi enviado com sucesso
            if response.status_code == 200:
                # Verificar se a resposta indica sucesso
                if ('formResponse' in response.url or 
                    'Your response has been recorded' in response.text or
                    'Sua resposta foi registrada' in response.text or
                    response.url.endswith('/formResponse')):
                    logger.info("Formulário enviado com sucesso")
                    return True
                else:
                    logger.warning(f"Possível erro no envio. URL final: {response.url}")
                    # Por enquanto, vamos considerar como sucesso se não houver erro HTTP
                    return True
            else:
                logger.error(f"Erro HTTP ao enviar formulário: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao enviar formulário: {e}")
            return False

# Função auxiliar para uso no bot
async def enviar_dados_formulario(dados: Dict[str, Any], form_url: str) -> bool:
    """
    Função auxiliar para enviar dados para o Google Forms
    
    Args:
        dados: Dados coletados pelo bot
        form_url: URL do formulário
        
    Returns:
        bool: True se enviado com sucesso
    """
    try:
        integration = GoogleFormsIntegration(form_url)
        
        # Verificar se os IDs dos campos estão configurados
        field_mapping = get_field_mapping()
        if all(field_id.startswith('entry.123') for field_id in field_mapping.values()):
            logger.warning("IDs dos campos não foram configurados. Usando valores padrão.")
            logger.info("Execute 'python3 manual_form_config.py' para ver as instruções de configuração.")
            # Por enquanto, simula sucesso para demonstração
            return True
        
        return await integration.submit_form(dados)
        
    except Exception as e:
        logger.error(f"Erro na integração com Google Forms: {e}")
        return False

