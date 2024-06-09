from PyQt6.QtWidgets import QFileDialog, QMainWindow, QApplication, QMessageBox
from ui.main_window import Ui_MainWindow
from algorithms.main import HUIGeneticAlgorithm as HUIGA
import sys
import os
import time
import psutil


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.file_input = ""
        self.ui.pushButtonSelectFile.clicked.connect(self.choose_file)
        self.ui.pushButtonRun.clicked.connect(self.run)
        self.ui.lineEditFileOutput.setText("output.txt")


    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose file", "", "Text files (*.txt)")
        if file_path:
            self.file_input = file_path
            file_name = os.path.basename(file_path)
            self.ui.lineEditFileInput.setText(file_name)
    
    def is_valid_value(self):
        generation = self.get_generations()
        pop_size = self.get_population_size()
        input_file = self.ui.lineEditFileInput.text()
        crossover_probability = self.get_crossover_probability()
        mutation_probability = self.get_mutation_probability()
        if generation and pop_size and mutation_probability and input_file and crossover_probability:
            return True
        
        return False
    
    def get_generations(self):
        return int(self.ui.lineEditGenerations.text())
    
    def get_population_size(self):
        return int(self.ui.lineEditPopulationSize.text())
    
    def get_crossover_probability(self):
        return float(self.ui.lineEditCrossoverProbability.text())
    
    def get_mutation_probability(self):
        return float(self.ui.lineEditMutationProbability.text())
    
    def get_input_file(self):
        return self.file_input
    
    def get_min_utility(self):
        return float(self.ui.lineEditFileMinUtility.text())
    
    def get_output_file(self):
        return self.ui.lineEditFileOutput.text()
    
    def show_error_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()
    
    def run(self):
        if not self.is_valid_value():
            self.show_error_message("One or more input values are invalid. Please check and try again.")
        else:
            start_time = time.time()
            process_start = psutil.Process()
            memory_start_info = process_start.memory_info()
            cur_memory_start = memory_start_info.rss / 1024 / 1024

            # clear prev result
            self.ui.textBrowserResult.setText("")
            self.ui.progressBarProcess.setValue(0)

            data_path = self.get_input_file()
            min_utility = self.get_min_utility()
            pop_size = self.get_population_size()
            generations = self.get_generations()
            crossover_probability = self.get_crossover_probability() or 0.8
            mutation_probability = self.get_mutation_probability() or 0.1
            hui_ga = HUIGA(
                dataset_path=data_path,
                min_utility=min_utility, 
                population_size=pop_size,
                generations=generations,
                mutation_probability=mutation_probability,
                crossover_probability=crossover_probability
            )
            output_file = self.get_output_file()
            hui_ga.run_algorithm(output_file)
            with open(output_file, "r") as file:
                result_content = file.read()
            self.ui.progressBarProcess.setValue(100)

            total_time = time.time() - start_time
            process_end = psutil.Process()
            memory_end_info = process_end.memory_info()
            cur_memory_end = memory_end_info.rss / 1024 / 1024
            max_memory = cur_memory_end - cur_memory_start
            content = f"> High-utility itemsets count: {len(hui_ga.hui_sets)} (HUIs)\n"
            content += f"> Total time: ~ {total_time:.3f} (s)\n"
            content += f"> Max memory (mb) ~ {max_memory:.3f} (mb)\n\n"
            content += "> HUIs detail:\n"

            self.ui.textBrowserResult.setText(content + result_content)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec())
