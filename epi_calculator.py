import math

HISTORY_FILE = "epi_history.txt"


class EpiMetricsCalculator:
    def __init__(self):
        self.history = self.load_history()

    def load_history(self):
        data = []
        try:
            with open(HISTORY_FILE, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        data.append(line)
        except FileNotFoundError:
            pass
        return data

    def save_history(self):
        with open(HISTORY_FILE, "w") as f:
            for item in self.history:
                f.write(item + "\n")

    def get_number(self, message):
        while True:
            value = input(message)
            try:
                return float(value)
            except ValueError:
                print("Enter a valid number.")

    # ---- Epidemiological Metrics ----

    def attack_rate(self):
        cases = self.get_number("Enter number of new cases: ")
        population = self.get_number("Enter population at risk: ")
        try:
            result = (cases / population) * 100
            return result
        except ZeroDivisionError:
            print("Population cannot be zero.")
            return None

    def cfr(self):
        deaths = self.get_number("Enter number of deaths: ")
        cases = self.get_number("Enter number of confirmed cases: ")
        try:
            result = (deaths / cases) * 100
            return result
        except ZeroDivisionError:
            print("Cases cannot be zero.")
            return None

    def incidence_rate(self):
        cases = self.get_number("Enter number of new cases: ")
        population = self.get_number("Enter total population: ")
        multiplier = self.get_number("Enter multiplier (e.g., 1000 or 100000): ")
        try:
            result = (cases / population) * multiplier
            return result
        except ZeroDivisionError:
            print("Population cannot be zero.")
            return None

    def prevalence(self):
        existing_cases = self.get_number("Enter total existing cases: ")
        population = self.get_number("Enter total population: ")
        try:
            result = (existing_cases / population) * 100
            return result
        except ZeroDivisionError:
            print("Population cannot be zero.")
            return None

    def doubling_time(self):
        growth_rate = self.get_number("Enter exponential growth rate (e.g., 0.2): ")
        try:
            result = math.log(2) / growth_rate
            return result
        except ZeroDivisionError:
            print("Growth rate cannot be zero.")
            return None

    def record_result(self, metric_name, result):
        if result is not None:
            record = f"{metric_name}: {round(result, 2)}"
            print("Result:", round(result, 2))
            self.history.append(record)

    def show_history(self):
        if not self.history:
            print("No calculations yet.")
            return
        print("\nCalculation History:")
        for item in self.history:
            print(item)


def main():
    calc = EpiMetricsCalculator()

    while True:
        print("\nEpidemiology Metrics Calculator")
        print("1. Attack Rate")
        print("2. Case Fatality Rate (CFR)")
        print("3. Incidence Rate")
        print("4. Prevalence")
        print("5. Doubling Time")
        print("6. Show History")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            result = calc.attack_rate()
            calc.record_result("Attack Rate (%)", result)

        elif choice == "2":
            result = calc.cfr()
            calc.record_result("CFR (%)", result)

        elif choice == "3":
            result = calc.incidence_rate()
            calc.record_result("Incidence Rate", result)

        elif choice == "4":
            result = calc.prevalence()
            calc.record_result("Prevalence (%)", result)

        elif choice == "5":
            result = calc.doubling_time()
            calc.record_result("Doubling Time (days)", result)

        elif choice == "6":
            calc.show_history()

        elif choice == "7":
            calc.save_history()
            print("History saved. Goodbye.")
            break

        else:
            print("Invalid choice. Try again.")


main()