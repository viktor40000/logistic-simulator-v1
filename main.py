class Package:
    def __init__(self, weight: float, pickup: tuple, delivery: tuple):
        self.weight = weight
        self.pickup = pickup
        self.delivery = delivery
        self.status = "Очікує на складі"

    def get_info(self) -> str:
        return f"Вантаж {self.weight}кг | Старт: {self.pickup} -> Фініш: {self.delivery} | Статус: {self.status}"


class Drone:
    def __init__(self, name: str, max_battery: int, max_capacity: float):
        self.name = name
        self.max_battery = max_battery
        self.battery = max_battery
        self.max_capacity = max_capacity
        self.x = 0
        self.y = 0
        self.payload = None

    def get_status(self) -> str:
        payload_info = self.payload.get_info() if self.payload else "Порожній"
        return (f"Дрон [{self.name}]: Позиція ({self.x}, {self.y}) | "
                f"Заряд: {self.battery}% | Вантаж: {payload_info}")

    def move(self, target_x: int, target_y: int):
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
        if self.payload is not None:
            print("❌ Помилка: Дрон вже завантажений!")
            return

        if (self.x, self.y) != package.pickup:
            print(f"⚠ Дрон не в точці збору. Летимо до вантажу в {package.pickup}...")
            if not self.move(package.pickup[0], package.pickup[1]):
                return

        if package.weight > self.max_capacity:
            print(f"❌ {self.name} не може підняти {package.weight}кг! Максимум: {self.max_capacity}кг")
            return

        self.payload = package
        package.status = "В дорозі"
        print(f"📦 Вантаж успішно завантажено на {self.name}!")

    def deliver_package(self):
        """Доставка вантажу в точку призначення."""
        if self.payload is None:
            print("❌ Помилка: На борту немає вантажу для доставки!")
            return

        target = self.payload.delivery
        print(f"🚀 {self.name} прямує до точки фінішу {target}...")
        
        # Намагаємося летіти до точки доставки
        if self.move(target[0], target[1]):
            # Якщо долетіли успішно
            self.payload.status = "Доставлено"
            print(f"  Вантаж успішно доставлено в точку {target}!")
            
            # Обнуляємо вантаж на борту (розвантаження)
            self.payload = None
        else:
            print(f"🚨 Критична ситуація! {self.name} застряг на позиції ({self.x}, {self.y}) з вантажем!")


# --- Демонстрація роботи Кроку 3 ---
if __name__ == "__main__":
    # Створюємо систему
    drone = Drone(name="Птах-01", max_battery=100, max_capacity=5.0)
    cargo = Package(weight=3.0, pickup=(1, 1), delivery=(4, 3))
    
    print("=== ЕТАП 1: Збір вантажу ===")
    drone.pick_up_package(cargo)
    print(drone.get_status())
    
    print("\n=== ЕТАП 2: Доставка ===")
    drone.deliver_package()
    
    print("\n=== ЕТАП 3: Фінальний статус ===")
    print(drone.get_status())
