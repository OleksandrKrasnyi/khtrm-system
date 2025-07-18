# Функциональность Нарядчика (Dispatcher)

## Обзор
Нарядчик - ключевая роль в системе управления транспортом. Отвечает за создание и управление нарядами, назначение водителей на маршруты, контроль выходов на линию.

## Основные таблицы БД

### 1. `zanaradka` - Основная таблица нарядов (182,494 записи)
**Описание**: Главная таблица для хранения всех нарядов
**Ключевые поля**:
- `marshrut` - номер маршрута
- `vipusk` - выпуск
- `smena` - смена
- `tabvoditel` - табельный номер водителя
- `fiovoditel` - ФИО водителя
- `tabconduktor` - табельный номер кондуктора
- `fioconduktor` - ФИО кондуктора
- `pe№` - номер подвижного состава
- `data_day` - дата наряда
- `tvih` - время выхода
- `tzah` - время захода
- `putlist№` - номер путевого листа
- `del` - флаг удаления (0 - активный, 1 - удален)

### 2. `sprmarshrut` - Справочник маршрутов (296 записей)
**Описание**: Информация о маршрутах и заправочных адресах
**Ключевые поля**:
- `Marshrut` - номер маршрута
- `Vipusk` - выпуск
- `ZaprAdr` - адрес заправки

### 3. `sprpersonal` - Справочник персонала (966 записей)
**Описание**: Информация о сотрудниках
**Ключевые поля**:
- `Tab№` - табельный номер
- `FIO` - ФИО сотрудника
- `Priznak` - признак должности (0 - водитель, 1 - кондуктор)
- `Blok` - блокировка (0 - активный, 1 - заблокирован)

### 4. `sprpe` - Справочник подвижного состава (218 записей)
**Описание**: Информация о транспортных средствах
**Ключевые поля**:
- `Pe` - номер ПС
- `kodPe` - код ПС
- `PeTemp` - государственный номер
- `Nkod` - тип ПС (1-6метр, 2-8метр, 4-Irisbus, 5-Solaris15, 6-Solaris18)
- `Blok` - блокировка (0 - активный, 1 - заблокирован)

## Функциональность для нарядчика

### 1. Просмотр активных нарядов
- Отображение нарядов на текущую дату
- Фильтрация по маршрутам, сменам
- Статус выполнения нарядов

### 2. Создание нового наряда
- Выбор маршрута из справочника
- Назначение водителя
- Назначение кондуктора (если требуется)
- Назначение подвижного состава
- Установка времени выхода/захода
- Генерация номера путевого листа

### 3. Редактирование существующих нарядов
- Изменение назначенного персонала
- Изменение времени
- Изменение подвижного состава
- Добавление примечаний

### 4. Управление ресурсами
- Просмотр свободных водителей
- Просмотр свободного подвижного состава
- Контроль загрузки маршрутов

## Приоритетные задачи разработки

### Этап 1: Основная таблица нарядов
1. **API endpoint** для получения нарядов на дату
2. **Компонент таблицы** для отображения нарядов
3. **Фильтрация** по дате, маршруту, смене

### Этап 2: Справочники
1. **API endpoints** для справочников (маршруты, персонал, ПС)
2. **Компоненты** для отображения справочников

### Этап 3: Создание/редактирование нарядов
1. **Форма создания** наряда
2. **Валидация** данных
3. **API endpoints** для CRUD операций

## Структура данных для фронтенда

```typescript
interface Assignment {
  id: number;
  route: number;
  routeRelease: number;
  shift: string;
  driverTabNumber: number;
  driverName: string;
  conductorTabNumber?: number;
  conductorName?: string;
  vehicleNumber: number;
  departureTime: string;
  arrivalTime: string;
  waybillNumber: string;
  date: string;
  status: 'active' | 'completed' | 'cancelled';
  notes?: string;
}

interface Route {
  id: number;
  number: number;
  release: number;
  fuelAddress: string;
}

interface Employee {
  tabNumber: number;
  fullName: string;
  position: 'driver' | 'conductor';
  isActive: boolean;
}

interface Vehicle {
  number: number;
  code: string;
  stateNumber: string;
  type: 'bus_6m' | 'bus_8m' | 'irisbus' | 'solaris_15' | 'solaris_18';
  isActive: boolean;
}
```

## Пример SQL запросов

### Получение нарядов на дату:
```sql
SELECT 
    z.key as id,
    z.marshrut as route,
    z.vipusk as routeRelease,
    z.smena as shift,
    z.tabvoditel as driverTabNumber,
    z.fiovoditel as driverName,
    z.tabconduktor as conductorTabNumber,
    z.fioconduktor as conductorName,
    z.`pe№` as vehicleNumber,
    z.tvih as departureTime,
    z.tzah as arrivalTime,
    z.`putlist№` as waybillNumber,
    z.data_day as date,
    z.Soobhenie as notes
FROM zanaradka z
WHERE z.data_day = '2025-01-15' 
  AND z.del = 0
ORDER BY z.marshrut, z.vipusk, z.smena;
```

### Получение свободных водителей:
```sql
SELECT 
    sp.`Tab№` as tabNumber,
    sp.FIO as fullName
FROM sprpersonal sp
WHERE sp.Priznak = 0 
  AND sp.Blok = 0
  AND sp.`Tab№` NOT IN (
    SELECT z.tabvoditel 
    FROM zanaradka z 
    WHERE z.data_day = '2025-01-15' 
      AND z.del = 0
  );
```

### Получение свободного подвижного состава:
```sql
SELECT 
    pe.Pe as number,
    pe.kodPe as code,
    pe.PeTemp as stateNumber,
    pe.Nkod as typeCode
FROM sprpe pe
WHERE pe.Blok = 0
  AND pe.Pe NOT IN (
    SELECT z.`pe№` 
    FROM zanaradka z 
    WHERE z.data_day = '2025-01-15' 
      AND z.del = 0
  );
``` 