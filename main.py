class Package:
    def __init__(self, weight: float, pickup: tuple, delivery: tuple):
        """
        weight: вага в кг
        pickup: координати звідки забрати (X, Y)
        delivery: координати куди доставити (X, Y)
        """
        self.weight = weight
        self.pickup = pickup
        self.delivery = delivery
        self.status = "Очікує на складі"  # Статуси: Очікує / В дорозі / Доставлено

    def get_info(self) -> str:
        """Повертає інформацію про вантаж."""
        return f"Вантаж {self.weight}кг | Старт: {self.pickup} -> Фініш: {self.delivery} | Статус: {self.status}"


class Drone:
    def __init__(self, name: str, max_battery: int, max_capacity: float):
        self.name = name
        self.max_battery = max_battery
        self.battery = max_battery
        self.max_capacity = max_capacity
        self.x = 0
        self.y = 0
        self.payload = None  # Поточний вантаж на борту (за замовчуванням немає)

    def get_status(self) -> str:
        payload_info = self.payload.get_info() if self.payload else "Порожній"
        return (f"Дрон [{self.name}]: Позиція ({self.x}, {self.y}) | "
                f"Заряд: {self.battery}% | Вантаж: {s.payload_info if hasattr(self, 'payload_info') else payload_info}")

    def move(self, target_x: int, target_y: int):
        """Переміщення (код з Кроку 1)"""
        distance = abs(target_x - self.x) + abs(target_y - self.y)
        battery_cost = distance * 5
        
        if self.battery >= battery_cost:
            self.battery -= battery_cost
            self.x = target_x
            self.y = target_y
            return True
        else:
            print(f"❌ {self.name}: Недостатньо заряду для польоту в ({target_x}, {target_y})!")
            return False

    def pick_up_package(self, package: Package):
        """Логіка підбору вантажу дроном."""
        if self.payload is not None:
            print("❌ Помилка: Дрон вже завантажений!")
            return

        # Перевірка координат: чи знаходиться дрон там, де й вантаж
        if (self.x, self.y) != package.pickup:
            print(f"⚠ Дрон не в точці збору. Летимо до вантажу в {package.pickup}...")
            if not self.move(package.pickup[0], package.pickup[1]):
                return  # Якщо не долетів через батарею

        # Перевірка вантажопідйомності
        if package.weight > self.max_capacity:
            print(f"❌ {self.name} не може підняти {package.weight}кг! Максимум: {self.max_capacity}кг")
            return

        # Завантаження успішне
        self.payload = package
        package.status = "В дорозі"
        print(f"📦 Вантаж успішно завантажено на {self.name}!")


# --- Демонстрація роботи Кроку 2 ---
if __name__ == "__main__":
    # Створюємо дрон
    drone = Drone(name="Птах-01", max_battery=100, max_capacity=5.0)
    
    # Створюємо вантаж: вага 3 кг, забрати в (2, 2), доставити в (4, 5)
    cargo = Package(weight=3.0, pickup=(2, 2), delivery=(4, 5))
    
    print("--- Початковий стан системи ---")
    print(drone.get_status())
    print(cargo.get_info())
    
    print("\n--- Процес збору вантажу ---")
    drone.pick_up_package(cargo)
    
    print("\n--- Стан після завантаження ---")
    print(drone.get_status())
    print(cargo.get_info())
