# My Inventory App

A Django app for inventory management, designed as a reusable Python package that can be installed via pip.

## Setup & Installation

### Install via GitHub
To install the package directly from GitHub, run:
```bash
pip install git+https://github.com/KAZTorant/kazza_inventory.git@v1.0.0
```


## How to Use

1. **Add the App to Django Settings:**
   Add `'inventory'` to your `INSTALLED_APPS` in `settings.py`:
   ```python
   INSTALLED_APPS = [
       ...
       'inventory',
   ]
   ```

2. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Start Your Django Server:**
   ```bash
   python manage.py runserver
   ```

## What This Package Does

- **Inventory Tracking:** Manage inventory items with additions and removals.
- **Django Admin Integration:** Includes a custom admin panel for inventory management.
- **Reusable Django App:** Can be integrated into any Django project via pip.
- **Supports Add/Remove Functionality:** Tracks stock adjustments and provides a reason-based history.

## License

This project is licensed under the [MIT License](LICENSE).
