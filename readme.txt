# Wind_Turbine_Model

1. Клонировать репозиторий с подмодулем openfast_toolbox
git clone --depth 1 --recurse-submodules -j8 https://github.com/tobaffoon/Turbine_Yaw_Modeling_NSU.git

2. Перейти в директорию openfast_toolbox
cd Turbine_Yaw_Modeling_NSU\project\openfast_toolbox

3. Установить подмодуль через pip
python -m pip install -e .

4. Запустить вычисления
cd ..\scripts
python main.py
