@echo on
netstat -ano | findstr :3306
python main.py
