
# Simple Flask App

У цьому проєкті ми реалізували адресу 'api/v1/hello-world-{variant}' з HTTP статус кодом відповіді 200. Для цього ми використовували віртуальне середовище Python 3.9 та систему контролю залежностей requirements.txt.



## Вимоги

 - [Python 3.9](https://www.python.org/downloads/release/python-390/)
 - [virtualenv](https://virtualenv.pypa.io/en/latest/)

## Завантаження проєкту
Для того щоб завантажити даний проєкт на свій комп'ютер та потім ним скористатися, слід скористатися командою git clone.
```bash
  git clone git@github.com:AnastasiiaDunas/PP3.git
```
Нам потрібно створити віртуальне середовище за допомогою команди та активувати віртуальне середовище.
```bash
  python -m virtualenv venv
```
```bash
  venv\Scripts\activate
```
Після чого нам потрібно перейти до директорії проєкту в cmd чи PowerShell.
```bash
  cd ...\...\...\venv
```
Тепер ми можемо сміливо запускати наш проєкт.
```bash
  python script.py
```
## Приклад використання
Далі ми можемо просто перейти за наступною адресою:
```bash
  http://127.0.0.1:5000/api/v1/hello-world-10
```
![App Screenshot](https://snipboard.io/WMNOQe.jpg)
