import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from werkzeug.security import generate_password_hash, check_password_hash

# ---------- Простые функции для тестирования ----------
favorites = []

def add_favorite(ex_id):
    if ex_id not in favorites:
        favorites.append(ex_id)

def remove_favorite(ex_id):
    if ex_id in favorites:
        favorites.remove(ex_id)

def validate_exercise(name, difficulty):
    return name and len(name) > 0 and difficulty in ['easy', 'medium', 'hard']

def validate_workout(name, exercises):
    return name and len(name) > 0 and len(exercises) > 0

def total_sets(workout_exercises):
    return sum(ex.get('sets', 0) for ex in workout_exercises)

def calculate_volume(weight, reps, sets):
    return weight * reps * sets

# ---------- Тесты ----------
def test_add_favorite():
    global favorites
    favorites = []
    add_favorite(10)
    assert 10 in favorites
    print("✓ Тест 1: добавление в избранное")

def test_add_duplicate():
    global favorites
    favorites = []
    add_favorite(5)
    add_favorite(5)
    assert favorites.count(5) == 1
    print("✓ Тест 2: защита от дублирования")

def test_remove_favorite():
    global favorites
    favorites = [7]
    remove_favorite(7)
    assert 7 not in favorites
    print("✓ Тест 3: удаление из избранного")

def test_remove_nonexistent():
    global favorites
    favorites = []
    remove_favorite(99)
    assert favorites == []
    print("✓ Тест 4: удаление несуществующего")

def test_password_hashing():
    pwd = "student123"
    hashed = generate_password_hash(pwd)
    assert check_password_hash(hashed, pwd) == True
    assert check_password_hash(hashed, "wrong") == False
    print("✓ Тест 5: хеширование паролей")

def test_validate_exercise_valid():
    assert validate_exercise("Жим лёжа", "medium") == True
    print("✓ Тест 6: валидное упражнение")

def test_validate_exercise_invalid():
    assert validate_exercise("", "hard") == False
    assert validate_exercise("Присед", "ultra") == False
    print("✓ Тест 7: невалидное упражнение")

def test_validate_workout():
    exercises = [{"id": 1, "sets": 3}, {"id": 2, "sets": 4}]
    assert validate_workout("Моя тренировка", exercises) == True
    assert validate_workout("", exercises) == False
    assert validate_workout("Тренировка", []) == False
    print("✓ Тест 8: валидация тренировки")

def test_total_sets():
    exercises = [{"sets": 3}, {"sets": 4}, {"sets": 2}]
    assert total_sets(exercises) == 9
    print("✓ Тест 9: подсчёт общего количества подходов")

def test_calculate_volume():
    # Объём = вес × повторения × подходы
    assert calculate_volume(weight=50, reps=10, sets=3) == 1500
    assert calculate_volume(0, 10, 3) == 0
    print("✓ Тест 10: расчёт тренировочного объёма")

if __name__ == "__main__":
    tests = [
        test_add_favorite,
        test_add_duplicate,
        test_remove_favorite,
        test_remove_nonexistent,
        test_password_hashing,
        test_validate_exercise_valid,
        test_validate_exercise_invalid,
        test_validate_workout,
        test_total_sets,
        test_calculate_volume
    ]
    passed = failed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except AssertionError as e:
            print(f"✗ {t.__name__} провален: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {t.__name__} ошибка: {e}")
            failed += 1
    print(f"\nИтог: {passed} пройдено, {failed} провалено из {len(tests)}")