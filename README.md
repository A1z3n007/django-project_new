# FinalProject — Django (Билеты + Маркетплейс)

Демо-учебный проект на Django с двумя приложениями:

- **`bilets/`** — покупка билетов (авиа/ЖД), поиск, фильтры, бронирование, отметка оплаты (учебный режим), загрузка изображений, «Мои брони».
- **`marketplace/`** — маркетплейс с каталогом, поиском/фильтрами, корзиной, учебным чекаутом, деталями заказа, экспортом в PDF, загрузкой изображений, «Мои заказы», сменой статусов (для staff).

> **Важно:** платежи в учебной версии **без реальных шлюзов** — статусы выставляются внутри приложения.

---

## 📦 Стек

- Python 3.12+
- Django 5.0
- SQLite (по умолчанию)
- ReportLab (PDF)
- HTML + CSS (кастом, без UI-фреймворков), немного JS (предпросмотр картинок)

---

## 🚀 Быстрый старт

```bash
# 1) Клонирование
git clone <URL-ВАШЕГО-РЕПО> finalproject
cd finalproject

# 2) Виртуальная среда (Windows CMD)
python -m venv .venv
.venv\Scripts\activate
# (PowerShell: .\.venv\Scripts\Activate.ps1 ; macOS/Linux: source .venv/bin/activate)

# 3) Зависимости
pip install -r requirements.txt

# 4) Миграции
python manage.py makemigrations
python manage.py migrate

# 5) Суперпользователь (опционально)
python manage.py createsuperuser

# 6) Демо-данные
python manage.py loaddata bilets_demo marketplace_demo
python manage.py loaddata bilets_more marketplace_more

# 7) Запуск
python manage.py runserver

---

## 🗺️ Основные URL

* Главная: /
* Аккаунт:
    Вход/выход: /accounts/login/, /accounts/logout/
    Регистрация: /signup/
    Профиль («Мой кабинет»): /profile/
* Билеты:
    Список/поиск: /bilets/
    Детали: /bilets/<id>/
    Бронирование: /bilets/<id>/book/
    Успех: /bilets/booking/<booking_id>/success/
    Отметить оплату (учебный): POST /bilets/booking/<booking_id>/mark_paid/
    Добавить билет (staff): /bilets/manage/ticket/add/
* Маркетплейс:
    Каталог/поиск: /marketplace/
    Детали товара: /marketplace/product/<id>/
    Корзина: /marketplace/cart/
    Удалить из корзины: /marketplace/cart/remove/<id>/
    Оформить заказ (учебный): /marketplace/checkout/
    Заказ: /marketplace/order/<id>/
    Смена статуса (staff): /marketplace/order/<id>/status/<paid|shipped|done|cancelled>/
    Добавить товар (staff): /marketplace/manage/product/add/

---

## ✨ Фичи
Общее
* Два независимых UI (у каждого приложения свой base-шаблон и собственные цвета).
* Единый базовый CSS с «прочной» версткой карточек (обрезка длинных заголовков, адаптив).
* Пагинация без ошибок (чистое формирование querystring на стороне view).
bilets/
* Фильтры: тип транспорта, города, дата «с/по», цена «от/до», быстрый поиск.
* Бронирование с формой пассажира.
* Учебная «оплата» — кнопка «Отметить как оплачено».
* Загрузка изображения билета (+ предпросмотр на форме).
* «Мои брони» в кабинете (фильтр по статусу оплаты + пагинация).
marketplace/
* Категории, поиск по названию/описанию, фильтры по цене.
* Корзина на сессиях, учебный чекаут (сразу paid).
* Детальная страница заказа + экспорт в PDF.
* Загрузка изображений товаров (+ предпросмотр).
* «Мои заказы» в кабинете (фильтр по статусу + пагинация).
* Смена статуса заказа (только staff).

---

finalproject/
├─ finalproject/            # settings/urls/wsgi
├─ main/                    # home, signup, profile
├─ bilets/                  # приложение билетов
│  ├─ templates/bilets/     # UI билетов
│  ├─ fixtures/             # bilets_demo.json, bilets_more.json
│  └─ ...
├─ marketplace/             # приложение маркетплейса
│  ├─ templates/marketplace/
│  ├─ fixtures/             # marketplace_demo.json, marketplace_more.json
│  └─ ...
├─ templates/               # base.html и др.
├─ static/
│  ├─ css/                  # styles.css, bilets.css, marketplace.css
│  └─ js/                   # preview.js (предпросмотр изображений)
├─ media/                   # загружаемые файлы (создастся автоматически)
├─ db.sqlite3               # БД (после миграций)
└─ requirements.txt

## 🖼️ Медиа и статика

MEDIA: MEDIA_ROOT = media/, MEDIA_URL = /media/ (подключено в urls.py при DEBUG=True).

Для загрузки изображений используйте формы:

Товар (staff): /marketplace/manage/product/add/

Билет (staff): /bilets/manage/ticket/add/

Предпросмотр на форме работает через static/js/preview.js.

---

## 🔐 Роли и доступ

* Гость: просмотр каталога/билетов, корзина, чекаут (заказ без пользователя), бронирование.

* Пользователь: «Мой кабинет», заказы/брони привязываются к аккаунту.

* Staff: добавление товаров/билетов, изменение статусов заказов, экспорт PDF.

Сделать пользователя staff:
    python manage.py createsuperuser
    # или в админке: /admin

---

## 🧪 Демоданные

Команды загрузки:
    python manage.py loaddata bilets_demo marketplace_demo
    python manage.py loaddata bilets_more marketplace_more

|Если получите конфликт PK: либо удалите db.sqlite3 и мигрируйте заново,
|либо отредактируйте pk в фикстурах, либо загружайте частично.

---

## 🛠️ Траблшутинг

* Internal Server Error с пагинацией — убедитесь, что обновили шаблоны и вьюхи, где формируется qs_no_page (мы убрали небезопасный фильтр cut).

* Статика/медиа не отдаются — проверьте DEBUG=True, пути STATICFILES_DIRS, MEDIA_URL/MEDIA_ROOT, и что в urls.py добавлено:

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

* ReportLab не ставится — обновите pip / установите компилятор, либо используйте готовые колёса (pip install reportlab в свежей версии Python обычно ок).

---

## 🧭 Roadmap / идеи для развития

- Экспорт брони билетов в PDF.
- Массовая загрузка товаров/билетов из CSV.
- Автодополнение поисковых полей (AJAX).
- Drag-n-drop загрузка изображений.
- Реальная оплата (Stripe/Paybox) + вебхуки (отключено в учебной версии).
- Тесты (pytest + factory_boy).

## 👤 Автор

Учебный проект совместно с наставником. Вопросы/идеи — PR и Issues приветствуются!