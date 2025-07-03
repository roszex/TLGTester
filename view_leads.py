#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime

def view_leads():
    """Просмотр всех сохраненных лидов"""
    leads_file = "leads.json"
    
    if not os.path.exists(leads_file):
        print("❌ Файл leads.json не найден")
        return
    
    try:
        with open(leads_file, 'r', encoding='utf-8') as f:
            leads = json.load(f)
        
        if not leads:
            print("📭 Лидов пока нет")
            return
        
        print(f"📊 Всего лидов: {len(leads)}\n")
        print("=" * 50)
        
        for i, lead in enumerate(leads, 1):
            print(f"🎯 ЛИД #{i}")
            print(f"👤 Пользователь: {lead.get('first_name', '')} {lead.get('last_name', '')}")
            print(f"🔗 Username: @{lead.get('username', 'Нет')}")
            print(f"🆔 User ID: {lead.get('user_id', 'Нет')}")
            print(f"⏰ Время: {lead.get('timestamp', 'Нет')}")
            
            form_data = lead.get('form_data', {})
            if form_data:
                print("📋 Данные формы:")
                if form_data.get('age'):
                    print(f"  • Возраст: {form_data['age']} лет")
                if form_data.get('occupation'):
                    print(f"  • Деятельность: {form_data['occupation']}")
                if form_data.get('income'):
                    print(f"  • Доход: {form_data['income']}")
                if form_data.get('motivation'):
                    print(f"  • Мотивация: {form_data['motivation']}")
                if form_data.get('teamwork'):
                    print(f"  • Командная работа: {form_data['teamwork']}")
            else:
                print("📋 Данные формы: НЕ ЗАПОЛНЕНЫ")
            
            print("-" * 30)
    
    except Exception as e:
        print(f"❌ Ошибка при чтении файла: {e}")

def export_leads_to_csv():
    """Экспорт лидов в CSV файл"""
    leads_file = "leads.json"
    
    if not os.path.exists(leads_file):
        print("❌ Файл leads.json не найден")
        return
    
    try:
        with open(leads_file, 'r', encoding='utf-8') as f:
            leads = json.load(f)
        
        if not leads:
            print("📭 Лидов для экспорта нет")
            return
        
        csv_file = "leads_export.csv"
        with open(csv_file, 'w', encoding='utf-8') as f:
            # Заголовки
            f.write("Номер,Имя,Фамилия,Username,User ID,Время,Возраст,Деятельность,Доход,Мотивация,Командная работа\n")
            
            # Данные
            for i, lead in enumerate(leads, 1):
                form_data = lead.get('form_data', {})
                row = [
                    str(i),
                    lead.get('first_name', ''),
                    lead.get('last_name', ''),
                    lead.get('username', ''),
                    lead.get('user_id', ''),
                    lead.get('timestamp', ''),
                    form_data.get('age', ''),
                    form_data.get('occupation', '').replace(',', ';'),
                    form_data.get('income', ''),
                    form_data.get('motivation', '').replace(',', ';'),
                    form_data.get('teamwork', '').replace(',', ';')
                ]
                f.write(','.join(f'"{item}"' for item in row) + '\n')
        
        print(f"✅ Лиды экспортированы в {csv_file}")
    
    except Exception as e:
        print(f"❌ Ошибка при экспорте: {e}")

if __name__ == "__main__":
    print("🔍 ПРОСМОТР ЛИДОВ")
    print("1. Показать все лиды")
    print("2. Экспорт в CSV")
    print("3. Выход")
    
    choice = input("\nВыберите действие (1-3): ").strip()
    
    if choice == "1":
        view_leads()
    elif choice == "2":
        export_leads_to_csv()
    elif choice == "3":
        print("👋 До свидания!")
    else:
        print("❌ Неверный выбор") 