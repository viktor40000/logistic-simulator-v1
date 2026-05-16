class Drone:
    def __init__(self, name: str, max_battery: int, max_capacity: float):
        """Ініціалізація характеристик дрона."""
        self.name = name
        self.max_battery = max_battery
        self.battery = max_battery  # Поточний заряд (починаємо з 100%)
        self.max_capacity = max_capacity  # Максимальна вантажопідйомність (кг)
        
        # Початкові координати дрона на карті (X, Y)
        self.x = 0
        self.y = 0

    def get_status(self) -> str:
        """Повертає поточний стан дрона у вигляді тексту."""
        return (f"Дрон [{self.name}]: Позиція ({self.x}, {self.y}) | "
                f"Заряд: {self.battery}/{self.max_battery}% | "
                f"Вантажність: {self.max_capacity}кг")

    def move(self, target_x: int, target_y: int):
        """Переміщення дрона в нову точку та розрахунок витрати батареї."""
        # Рахуємо відстань за спрощеною формулою (Мангеттенська відстань)
        distance = abs(target_x - self.x) + abs(target_y - self.y)
        
        # Припустимо, 1 одиниця відстані коштує 5% заряду батареї
        battery_cost = distance * 5
        
        if self.battery >= battery_cost:
            self.battery -= battery_cost
            self.x = target_x
            self.y = target_y
            print(f" Успішний політ до ({target_x}, {target_y}). Витрачено {battery_cost}% заряду.")
        else:
            print(f" Помилка: Недостатньо заряду для польоту! Потрібно {battery_cost}%, є {self.battery}%.")


# --- Демонстрація роботи (симуляція) ---
if __name__ == "__main__":
    print("--- Створення автономного дрона ---")
    # Створюємо модель "Птаха" з батареєю 100% і вантажопідйомністю 5 кг
    my_drone = Drone(name="Птах-01", max_battery=100, max_capacity=5.0)
    print(my_drone.get_status())
    
    print("\n--- Команда: Летіти в точку (3, 4) ---")
    my_drone.move(target_x=3, target_y=4)
    print(my_drone.get_status())
    
    print("\n--- Команда: Летіти в далеку точку (10, 10) ---")
    my_drone.move(target_x=10, target_y=10)
