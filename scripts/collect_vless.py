#!/usr/bin/env python3
"""
Derulo-VPN: VLESS Config Collector
Собирает VLESS конфиги из разных источников и объединяет их
"""

import requests
import os
from datetime import datetime
from pathlib import Path

# Источники конфигов
SOURCES = {
    'igareck_black': 'https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/BLACK_VLESS_RUS.txt',
    'igareck_black_mobile': 'https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/BLACK_VLESS_RUS_mobile.txt',
    'epodonios': 'https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/All_Configs_Sub.txt',
    'kort0881': 'https://raw.githubusercontent.com/kort0881/vpn-vless-configs-russia/main/mermeroo_only_new_for_mirror.txt',
}

# Папка для сохранения
OUTPUT_DIR = Path('configs')
OUTPUT_DIR.mkdir(exist_ok=True)

def download_config(source_name, url):
    """Скачивает конфиг из источника"""
    try:
        print(f"⬇️  Downloading from {source_name}...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        configs = response.text.strip().split('\n')
        configs = [c.strip() for c in configs if c.strip()]
        
        print(f"   ✅ Got {len(configs)} configs from {source_name}")
        return set(configs)
    except Exception as e:
        print(f"   ❌ Error downloading from {source_name}: {e}")
        return set()

def main():
    print("🚀 Starting Derulo-VPN VLESS Config Collection")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print()
    
    all_configs = set()
    
    # Скачиваем конфиги из всех источников
    for source_name, url in SOURCES.items():
        configs = download_config(source_name, url)
        all_configs.update(configs)
    
    print()
    print(f"📊 Total unique configs: {len(all_configs)}")
    
    # Сохраняем в файлы
    if all_configs:
        # Главный файл
        output_file = OUTPUT_DIR / 'vless-all.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sorted(all_configs)))
        
        print(f"💾 Saved to {output_file}")
        
        # Base64 версия
        import base64
        base64_configs = '\n'.join([
            base64.b64encode(config.encode()).decode()
            for config in sorted(all_configs)
        ])
        
        base64_file = OUTPUT_DIR / 'vless-all-base64.txt'
        with open(base64_file, 'w', encoding='utf-8') as f:
            f.write(base64_configs)
        
        print(f"💾 Saved base64 to {base64_file}")
        
        # Статистика
        stats_file = OUTPUT_DIR / 'stats.txt'
        with open(stats_file, 'w', encoding='utf-8') as f:
            f.write(f"""Derulo-VPN VLESS Config Collection Statistics
=====================================
Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
Total Configs: {len(all_configs)}

Sources:
""")
            for source_name in SOURCES.keys():
                f.write(f"  - {source_name}\n")
        
        print(f"📈 Saved stats to {stats_file}")
        print()
        print("✅ Collection completed successfully!")
    else:
        print("❌ No configs collected!")
        exit(1)

if __name__ == '__main__':
    main()
