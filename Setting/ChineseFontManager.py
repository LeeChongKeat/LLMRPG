import os
import pygame

class ChineseFontManager:
    """中文字体管理器 - 修复中文显示"""
    def __init__(self):
        self.font = self.create_chinese_font(22)
        self.small_font = self.create_chinese_font(18)
        self.tiny_font = self.create_chinese_font(14)
    
    def create_chinese_font(self, size=22):
        """创建支持中文的字体 - 修复中文乱码"""
        try:
            # Windows系统中文字体
            if os.name == 'nt':
                chinese_fonts = [
                    'msyh.ttc',      # 微软雅黑
                    'simhei.ttf',    # 黑体
                    'simsun.ttc',    # 宋体
                      'SimSun',
                            'SimHei',
                    'Microsoft YaHei',
                ]
                for font_name in chinese_fonts:
                    try:
                        font_path = pygame.font.match_font(font_name.lower())
                        if font_path:
                            print(f"使用中文字体 (Windows 系统匹配): {font_name}")
                            return pygame.font.Font(font_path, size)
                    except Exception as e:
                        print(f"尝试加载 Windows 字体 {font_name} 失败: {e}")
                        continue
            
            # Linux/macOS系统中文字体路径
            chinese_font_paths = [
                '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',  # 文泉驿微米黑
                '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',   # DejaVu Sans
                '/System/Library/Fonts/PingFang.ttc',               # macOS苹方
                '/System/Library/Fonts/Helvetica.ttc',              # macOS Helvetica
                # 添加 Arial Unicode MS 常见路径
                '/usr/share/fonts/truetype/arphic/arialuni.ttf',
                '/System/Library/Fonts/Arial Unicode.ttf',
                'C:/Windows/Fonts/ARIALUNI.TTF'
            ]
            
            for font_path in chinese_font_paths:
                if os.path.exists(font_path):
                    try:
                        print(f"使用中文字体文件: {font_path}")
                        return pygame.font.Font(font_path, size)
                    except Exception as e:
                         print(f"尝试加载字体文件 {font_path} 失败: {e}")
                         continue
                        
        except Exception as e:
            print(f"字体加载过程中发生错误: {e}")
        
        # 如果都失败了，使用系统默认字体 (尝试支持中文的)
        try:
            print("尝试使用系统默认字体")
            # 优先尝试支持中文的系统字体
            return pygame.font.SysFont('microsoftyahei,simhei,arialunicode,arial', size)
        except Exception as e_sysfont:
            print(f"使用系统默认字体也失败了: {e_sysfont}")
            # 最终回退，使用默认字体（可能不支持中文）
            default_font = pygame.font.Font(None, size)
            print("回退到 pygame 默认字体 (可能不支持中文)")
            return default_font