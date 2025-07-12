#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VideoForge Actions Module
Chứa tất cả các action classes cho các chức năng của VideoForge
"""

from .base_action import BaseAction
from .format_converter import VideoFormatConverter
from .compressor import VideoCompressor
from .speed_adjuster import VideoSpeedAdjuster
from .resolution_changer import VideoResolutionChanger
from .filter_applier import VideoFilterApplier
from .system_info import SystemInfoAction
from .api_service import APIServiceAction
from .folder_manager import FolderManagerAction
from .logo_remover import LogoRemoverAction

__all__ = [
    'BaseAction',
    'VideoFormatConverter',
    'VideoCompressor', 
    'VideoSpeedAdjuster',
    'VideoResolutionChanger',
    'VideoFilterApplier',
    'LogoRemoverAction',  
    'SystemInfoAction',
    'APIServiceAction',
    'FolderManagerAction'
]

# Version info
__version__ = '1.0.0'
__author__ = 'VideoForge Team'
__description__ = 'Action modules for VideoForge video processing'

# Action registry for dynamic loading
ACTION_REGISTRY = {
    'format_converter': VideoFormatConverter,
    'compressor': VideoCompressor,
    'speed_adjuster': VideoSpeedAdjuster,
    'resolution_changer': VideoResolutionChanger,
    'filter_applier': VideoFilterApplier,
    'system_info': SystemInfoAction,
    'logo_remover': LogoRemoverAction, 
    'api_service': APIServiceAction,
    'folder_manager': FolderManagerAction
}

def get_action(action_name):
    """
    Lấy action class theo tên
    
    Args:
        action_name (str): Tên của action
        
    Returns:
        class: Action class tương ứng hoặc None nếu không tìm thấy
    """
    return ACTION_REGISTRY.get(action_name)

def list_actions():
    """
    Lấy danh sách tất cả actions có sẵn
    
    Returns:
        list: Danh sách tên các actions
    """
    return list(ACTION_REGISTRY.keys())

def create_action(action_name):
    """
    Tạo instance của action
    
    Args:
        action_name (str): Tên của action
        
    Returns:
        BaseAction: Instance của action hoặc None nếu không tìm thấy
    """
    action_class = get_action(action_name)
    if action_class:
        return action_class()
    return None
