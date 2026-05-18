class Package:
    def __init__(self, weight: float, pickup: tuple, delivery: tuple):
        self.weight = weight
        self.pickup = pickup
        self.delivery = delivery
        self.status = "Очікує на складі"

    def get_info(self) -> str:
        return f"Вантаж {self.weight}кг | Старт: {self.pickup} -> Фініш: {self.delivery} | Status: {self.status}"


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
        if self.payload is None:
            print("❌ Помилка: На борту немає вантажу для доставки!")
            return

        target = self.payload.delivery
        print(f"🚀 {self.name} прямує до точки фінішу {target}...")
        
        if self.move(target[0], target[1]):
            self.payload.status = "Доставлено"
            print(f"🎉 Вантаж успішно доставлено в точку {target}!")
            self.payload = None
        else:
            print(f"🚨 Критична ситуація! {self.name} застряг на позиції ({self.x}, {self.y})!")


if __name__ == "__main__":
    print("=== Ласкаво просимо до UAV Logistics Simulator! ===")
    drone = Drone(name="Птах-01", max_battery=100, max_capacity=5.0)
    cargo = Package(weight=3.0, pickup=(2, 2), delivery=(4, 5))
    
    while True:
        print("\n" + "="*30)
        print("ДОСТУПНІ КОМАНДИ:")
        print("1. Перевірити статус системи")
        print("2. Відправити дрон забрати вантаж")
        print("3. Наказати дрону доставити вантаж")
        print("4. Зарядити дрон (на поточній позиції)")
        print("5. Створити новий вантаж")
        print("0. Вийти з симулятора")
        print("="*30)
        
        choice = input("Введіть номер команди: ").strip()
        
        if choice == "1":
            print("\n--- СТАТУС СИСТЕМИ ---")
            print(drone.get_status())
            if cargo:
                print(cargo.get_info())
            else:
                print("Нових вантажів на складі немає.")
                
        elif choice == "2":
            if not cargo:
                print("❌ Помилка: Спочатку створіть вантаж (Команда 5).")
            else:
                print("\n--- ЗБІР ВАНТАЖУ ---")
                drone.pick_up_package(cargo)
                
        elif choice == "3":
            print("\n--- ДОСТАВКА ВАНТАЖУ ---")
            drone.deliver_package()
            if drone.payload is None and cargo and cargo.status == "Доставлено":
                cargo = None 
                
        elif choice == "4":
            print("\n--- ЗАРЯДКА ---")
            drone.battery = drone.max_battery
            # БАГ ВИПРАВЛЕНО: Тепер тут чистий виклик координати об'єкта drone.y
            print(f"🔋 {drone.name} повністю заряджено на позиції ({drone.x}, {drone.y})!")
            
        elif choice == "5":
            print("\n--- СТВОРЕННЯ НОВОГО ВАНТАЖУ ---")
            try:
                w = float(input("Вага вантажу (кг): "))
                p_x = int(input("Точка збору X: "))
                p_y = int(input("Точка збору Y: "))
                d_x = int(input("Точка доставки X: "))
                d_y = int(input("Точка доставки Y: "))
                
                cargo = Package(weight=w, pickup=(p_x, p_y), delivery=(d_x, d_y))
                print("✅ Новий вантаж успішно зареєстровано в системі!")
            except ValueError:
                print("❌ Помилка: Вводьте лише числа!")
                
        elif choice == "0":
            print("\nДякуємо за використання симулятора. Роботу завершено!")
            break
        else:
            print("❌ Некоректний вибір. Спробуйте ще раз.")
