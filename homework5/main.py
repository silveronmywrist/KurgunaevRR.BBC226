import re
import sqlite3
import sys
from contextlib import closing
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP, localcontext
from create_db import DB_PATH, create_database

from PyQt6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QComboBox,
    QDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

NUMBER_PATTERN = re.compile(r"[0-9]+(?:[.,][0-9]+)?")


def format_number(value):
    with localcontext() as context:
        context.prec = 50
        rounded = Decimal(value).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
    return f"{rounded:,.2f}".replace(",", " ").replace(".", ",")


class TripDatabase:
    def __init__(self, path):
        self.path = path

    def write(self, sql, parameters=()):
        with closing(sqlite3.connect(self.path)) as connection:
            with connection:
                cursor = connection.execute(sql, parameters)
                return cursor.rowcount

    def save(self, name, trip):
        self.write("""
            INSERT INTO trips (
                name, saved_at, distance, consumption, price, multiplier,
                people, total_distance, fuel, cost, per_person
            )
            VALUES (
                :name, :saved_at, :distance, :consumption, :price, :multiplier,
                :people, :total_distance, :fuel, :cost, :per_person
            )
        """, {**trip, "name": name, "saved_at": datetime.now().isoformat()})

    def read_all(self):
        with closing(sqlite3.connect(self.path)) as connection:
            connection.row_factory = sqlite3.Row
            return connection.execute("SELECT * FROM trips ORDER BY id DESC").fetchall()

    def delete(self, trip_id):
        return self.write("DELETE FROM trips WHERE id = ?", (trip_id,)) == 1


class HistoryDialog(QDialog):
    def __init__(self, database, parent):
        super().__init__(parent)
        self.database = database
        self.trips = database.read_all()
        self.selected_trip = None
        self.setWindowTitle("История поездок")
        self.resize(740, 340)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(
            ["Сохранено", "Название", "Расстояние", "Стоимость", "На человека"]
        )
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.verticalHeader().hide()
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        self.empty_label = QLabel("Сохранённых поездок пока нет.")
        self.load_button = QPushButton("Загрузить")
        self.delete_button = QPushButton("Удалить")
        close_button = QPushButton("Закрыть")

        buttons = QHBoxLayout()
        buttons.addWidget(self.load_button)
        buttons.addWidget(self.delete_button)
        buttons.addStretch()
        buttons.addWidget(close_button)

        layout = QVBoxLayout(self)
        layout.addWidget(self.empty_label)
        layout.addWidget(self.table)
        layout.addLayout(buttons)

        self.table.itemSelectionChanged.connect(self.update_buttons)
        self.table.cellDoubleClicked.connect(self.load_row)
        self.load_button.clicked.connect(self.load_selected)
        self.delete_button.clicked.connect(self.delete_selected)
        close_button.clicked.connect(self.reject)
        self.fill_table()

    def fill_table(self):
        self.table.clearSelection()
        self.table.setRowCount(len(self.trips))

        for row, trip in enumerate(self.trips):
            saved_at = datetime.fromisoformat(trip["saved_at"])
            values = (
                saved_at.strftime("%d.%m.%Y %H:%M"),
                trip["name"],
                f'{format_number(trip["total_distance"])} км',
                f'{format_number(trip["cost"])} ₽',
                f'{format_number(trip["per_person"])} ₽',
            )
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setToolTip(value)
                self.table.setItem(row, column, item)

        self.empty_label.setVisible(not self.trips)
        self.update_buttons()

    def update_buttons(self):
        has_selection = self.table.selectionModel().hasSelection()
        self.load_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)

    def load_selected(self):
        rows = self.table.selectionModel().selectedRows()
        if rows:
            self.load_row(rows[0].row())

    def load_row(self, row, _column=0):
        self.selected_trip = self.trips[row]
        self.accept()

    def delete_selected(self):
        rows = self.table.selectionModel().selectedRows()
        if not rows:
            return

        row = rows[0].row()
        trip = self.trips[row]
        answer = QMessageBox.question(
            self,
            "Удаление поездки",
            "Удалить выбранную поездку из истории?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return

        try:
            deleted = self.database.delete(trip["id"])
        except sqlite3.Error as error:
            QMessageBox.critical(self, "Ошибка удаления", str(error))
            return

        self.trips.pop(row)
        self.fill_table()
        if not deleted:
            QMessageBox.information(self, "История поездок", "Запись уже удалена.")


class TripCalculator(QMainWindow):
    def __init__(self, database):
        super().__init__()
        self.database = database
        self.setWindowTitle("Калькулятор поездки")
        self.setMinimumWidth(480)

        form = QFormLayout()
        self.fields = {}
        for key, label, example in (
            ("distance", "Расстояние в одну сторону, км", "250"),
            ("consumption", "Расход топлива, л/100 км", "7,5"),
            ("price", "Цена топлива, ₽/л", "60,50"),
        ):
            field = QLineEdit()
            field.setPlaceholderText(example)
            field.setMaxLength(12)
            form.addRow(label, field)
            self.fields[key] = field

        self.route = QComboBox()
        self.route.addItem("В одну сторону", 1)
        self.route.addItem("Туда и обратно", 2)
        form.addRow("Маршрут", self.route)

        self.people = QSpinBox()
        self.people.setRange(1, 100)
        form.addRow("Человек, включая водителя", self.people)

        calculate_button = QPushButton("Рассчитать")
        clear_button = QPushButton("Очистить")
        self.details_button = QPushButton("Подробнее")
        self.save_button = QPushButton("Сохранить поездку")
        history_button = QPushButton("История")

        calculate_buttons = QHBoxLayout()
        calculate_buttons.addWidget(calculate_button)
        calculate_buttons.addWidget(clear_button)
        calculate_buttons.addWidget(self.details_button)

        history_buttons = QHBoxLayout()
        history_buttons.addWidget(self.save_button)
        history_buttons.addWidget(history_button)

        self.error = QLabel()
        self.error.setStyleSheet("color: #c43b3b")
        self.error.setWordWrap(True)
        self.result = QLabel()
        self.result.setWordWrap(True)
        result_box = QGroupBox("Результат")
        QVBoxLayout(result_box).addWidget(self.result)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addLayout(form)
        layout.addLayout(calculate_buttons)
        layout.addWidget(self.error)
        layout.addWidget(result_box)
        layout.addLayout(history_buttons)
        self.setCentralWidget(central_widget)

        calculate_button.clicked.connect(self.calculate)
        clear_button.clicked.connect(self.clear_form)
        self.details_button.clicked.connect(self.show_details)
        self.save_button.clicked.connect(self.save_trip)
        history_button.clicked.connect(self.show_history)
        for field in self.fields.values():
            field.returnPressed.connect(self.calculate)
            field.textChanged.connect(self.reset_result)
        self.route.currentIndexChanged.connect(self.reset_result)
        self.people.valueChanged.connect(self.reset_result)

        self.reset_result()
        self.fields["distance"].setFocus()

    def calculate(self):
        self.reset_result()
        inputs = {}

        for key, field in self.fields.items():
            text = field.text().strip()
            if NUMBER_PATTERN.fullmatch(text):
                number = Decimal(text.replace(",", "."))
                if number > 0:
                    inputs[key] = number
                    continue

            labels = {
                "distance": "расстояние",
                "consumption": "расход топлива",
                "price": "цену топлива",
            }
            self.error.setText(f"Введи {labels[key]} числом больше нуля.")
            self.error.show()
            field.setFocus()
            field.selectAll()
            return

        multiplier = self.route.currentData()
        people = self.people.value()
        with localcontext() as context:
            context.prec = 50
            total_distance = inputs["distance"] * multiplier
            fuel = total_distance * inputs["consumption"] / 100
            cost = fuel * inputs["price"]
            per_person = cost / people

        # Записываем десятичные числа в SQLite строками, сохраняя их точность.
        self.trip = {
            **{key: format(value, "f") for key, value in inputs.items()},
            "multiplier": multiplier,
            "people": people,
            "total_distance": format(total_distance, "f"),
            "fuel": format(fuel, "f"),
            "cost": format(cost, "f"),
            "per_person": format(per_person, "f"),
        }
        self.result.setText(
            f"Общее расстояние — {format_number(total_distance)} км\n"
            f"Понадобится топлива — {format_number(fuel)} л\n"
            f"Стоимость поездки — {format_number(cost)} ₽\n"
            f"На человека — {format_number(per_person)} ₽"
        )
        self.details_button.setEnabled(True)
        self.save_button.setEnabled(True)

    def reset_result(self, *_):
        self.trip = None
        self.error.hide()
        self.result.setText("Заполни поля и нажми «Рассчитать» или Enter.")
        self.details_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.statusBar().clearMessage()

    def clear_form(self):
        for field in self.fields.values():
            field.clear()
        self.route.setCurrentIndex(0)
        self.people.setValue(1)
        self.reset_result()
        self.fields["distance"].setFocus()

    def show_details(self):
        trip = self.trip
        if trip is None:
            return

        distance = trip["distance"].replace(".", ",")
        consumption = trip["consumption"].replace(".", ",")
        price = trip["price"].replace(".", ",")
        total_distance = trip["total_distance"].replace(".", ",")
        QMessageBox.information(
            self,
            "Подробный расчёт",
            f'Расстояние = {distance} × {trip["multiplier"]} = {total_distance} км\n'
            f'Топливо = {total_distance} × {consumption} ÷ 100 '
            f'≈ {format_number(trip["fuel"])} л\n'
            f'Стоимость = объём топлива × {price} ₽/л '
            f'≈ {format_number(trip["cost"])} ₽\n'
            f'На человека = стоимость ÷ {trip["people"]} '
            f'≈ {format_number(trip["per_person"])} ₽',
        )

    def save_trip(self):
        if self.trip is None:
            return

        name = ""
        while True:
            name, confirmed = QInputDialog.getText(
                self, "Сохранить поездку", "Название поездки", text=name
            )
            if not confirmed:
                return
            name = name.strip()
            if 1 <= len(name) <= 80:
                break
            QMessageBox.warning(
                self, "Проверь название", "Введи название длиной от 1 до 80 символов."
            )

        try:
            self.database.save(name, self.trip)
        except sqlite3.Error as error:
            QMessageBox.critical(self, "Ошибка сохранения", str(error))
            return
        self.statusBar().showMessage("Поездка сохранена.", 4000)

    def show_history(self):
        try:
            dialog = HistoryDialog(self.database, self)
        except sqlite3.Error as error:
            QMessageBox.critical(self, "Ошибка чтения истории", str(error))
            return

        if dialog.exec() == QDialog.DialogCode.Accepted:
            trip = dialog.selected_trip
            for key, field in self.fields.items():
                field.setText(trip[key].replace(".", ","))
            self.route.setCurrentIndex(self.route.findData(trip["multiplier"]))
            self.people.setValue(trip["people"])
            self.calculate()


def main():
    app = QApplication(sys.argv)
    try:
        create_database()
    except sqlite3.Error as error:
        QMessageBox.critical(
            None, "Ошибка базы данных", f"Не удалось открыть {DB_PATH}.\n\n{error}"
        )
        return 1

    window = TripCalculator(TripDatabase(DB_PATH))
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
