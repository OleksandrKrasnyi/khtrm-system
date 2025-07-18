# Извлечение кода из MS Access системы

## Цель
Получить SQL запросы, VBA код, структуры форм и отчетов из существующей MS Access системы для портирования в новую web-систему.

## Методы извлечения

### 1. Экспорт через Object Browser
```
1. Открыть MS Access базу данных
2. Нажать Alt + F11 (VBA Editor)  
3. View → Object Browser (F2)
4. Просмотреть все модули, формы, отчеты
5. Скопировать код в текстовые файлы
```

### 2. Документирование объектов
```
1. Database Tools → Database Documenter
2. Выбрать объекты для документирования:
   - Tables (таблицы)
   - Queries (запросы) 
   - Forms (формы)
   - Reports (отчеты)
   - Macros (макросы)
   - Modules (модули)
3. Экспорт в Word/PDF документ
```

### 3. Экспорт SQL запросов
```
1. Queries в Navigation Pane
2. Design View для каждого запроса
3. SQL View → скопировать SQL код
4. Сохранить в отдельные .sql файлы
```

### 4. Экспорт VBA кода
```
1. Alt + F11 → VBA Editor
2. Для каждого модуля/формы:
   - Правой кнопкой → Export File
   - Сохранить как .bas/.cls/.frm файлы
```

### 5. Структура форм и элементов управления
```
1. Design View для каждой формы
2. Property Sheet (F4) для элементов
3. Документировать:
   - Control Source (источник данных)
   - Row Source (источник строк)
   - Event Procedures (процедуры событий)
   - Validation Rules (правила валидации)
```

## Приоритетные объекты для извлечения

### Формы нарядчика:
- [ ] Главная форма с таблицей нарядов
- [ ] Форма создания/редактирования наряда  
- [ ] Формы справочников (маршруты, персонал, ПС)
- [ ] Формы фильтрации и поиска

### Запросы:
- [ ] Получение нарядов на дату
- [ ] Получение свободных водителей
- [ ] Получение свободного транспорта
- [ ] Статистические запросы

### VBA модули:
- [ ] Модули валидации данных
- [ ] Модули бизнес-логики
- [ ] Модули генерации путевых листов
- [ ] Модули импорта/экспорта

## Структура для сохранения

```
extracted_code/
├── sql_queries/
│   ├── assignments/
│   ├── employees/
│   ├── vehicles/
│   └── routes/
├── vba_modules/
│   ├── validation/
│   ├── business_logic/
│   └── utilities/
├── forms/
│   ├── dispatcher/
│   ├── timekeeper/
│   └── common/
└── reports/
    ├── assignments/
    └── statistics/
```

## Полезные команды для быстрого извлечения

### Список всех объектов БД:
```vba
Sub ListAllObjects()
    Dim obj As AccessObject
    Debug.Print "=== TABLES ==="
    For Each obj In CurrentData.AllTables
        Debug.Print obj.Name
    Next
    
    Debug.Print "=== QUERIES ==="
    For Each obj In CurrentData.AllQueries
        Debug.Print obj.Name
    Next
    
    Debug.Print "=== FORMS ==="
    For Each obj In CurrentProject.AllForms
        Debug.Print obj.Name
    Next
End Sub
```

### Экспорт SQL всех запросов:
```vba
Sub ExportAllQuerySQL()
    Dim qdf As QueryDef
    Dim fileName As String
    
    For Each qdf In CurrentDb.QueryDefs
        fileName = "C:\temp\queries\" & qdf.Name & ".sql"
        Open fileName For Output As #1
        Print #1, qdf.SQL
        Close #1
    Next qdf
End Sub
```

## Что искать в коде

### 1. Ключевые таблицы и связи
- Названия полей
- Типы данных  
- Связи между таблицами
- Индексы и ключи

### 2. Бизнес-логика
- Правила валидации
- Автоматические вычисления
- Ограничения данных
- Workflow процессы

### 3. UI логика
- Способы фильтрации
- Сортировка по умолчанию
- Форматирование данных
- Обработка событий

### 4. Интеграции
- Подключения к внешним БД
- Импорт/экспорт данных
- Интеграция с другими системами 