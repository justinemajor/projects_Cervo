from PyQt5.QtWidgets import QWidget, QFileDialog
import os
import copy

# adapt code to test right here please

data = {1: [3, 4, 5]}
waves = [0, 1, 2]
folderPath = ""
fileName = ""
autoindexing = False

def select_save_folder(self):
    folderPath = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
    if folderPath != "":
        le_folderPath.setText(folderPath)


def toggle_autoindexing(self):
    pass


def save_capture_csv(self, *args, **kwargs):
    if data is None:
        pass

    elif data is not None:
        key, spectrum = data.items()[0]
        fileName = le_fileName.text()
        if fileName == "":
            fileName = f"spectrum_{direction}"

        if folderPath == "":
            pass

        else:
            fixedData = copy.deepcopy(spectrum)
            path = os.path.join(folderPath, f"{fileName}_{key}")
            with open(path + ".csv", "w+") as f:
                for i, x in enumerate(waves):
                    f.write(f"{x},{fixedData[i]}\n")
                f.close()