import getpass
import glob
import os
import os.path
import platform
import shutil
import threading
import time
import traceback
import PySimpleGUI as sg
import cv2
import logging
from logging.handlers import TimedRotatingFileHandler


class GUIManager:
    def __init__(self, window_title, maximize=True):
        self.window_title = window_title
        self.maximize = maximize
        sg.theme('Black')

        self.window_handler = None
        self.event = None
        self.values = None

        self.stop_checking = True
        self.brick_clicked = False
        self.complete_path = None

    def initialize_window(self, layout):
        # Window initialization
        try:
            self.window_handler = sg.Window(self.window_title, layout, location=(0, 0), finalize=True,
                                            element_justification='c')
            if self.maximize:
                self.window_handler.Maximize()
        except:
            logger.critical(f"Wystapil problem podczas tworzenia okna interfejsu brakarza (PySimpleGUI). Opis bledu:\n{traceback.format_exc()}")
            os._exit(1)
        self.handle_window()

    def handle_window(self):
        global path_to_directory_with_brick_shapes
        while True:
            try:
                self.event, self.values = self.window_handler.read()
                self.event = self.event.replace("\n", " ")
                if self.event == "-STOP-":
                    self.window_handler["-OK-"].update(visible=False)
                    self.window_handler["-UWAGA-"].update(visible=True)
                if self.event == "OK":
                    self.window_handler["-UWAGA-"].update(visible=False)
                    self.window_handler['-RODZAJ_PRODUKTU-'].update(visible=True)
                if self.event == "Claro1" or self.event == "Claro0":
                    self.event = "Claro"
                if self.event in ['Kostka brukowa','Pustaki','Daszki',"Gazony","Obrzeza","Stopnie","Palisady"]:
                    rodzaj_produktu = self.event
                    logger.info(f"Wybrano rodzaj produktu {rodzaj_produktu}")
                    self.window_handler[f'-RODZAJ_PRODUKTU-'].update(visible=False)
                    if rodzaj_produktu == "Kostka brukowa":
                        self.window_handler[f'-KSZTALT_KOSTKI-'].update(visible=True)
                    elif rodzaj_produktu == "Pustaki":
                        self.window_handler[f'-KSZTALT_PUSTAKOW-'].update(visible=True)
                    elif rodzaj_produktu == "Daszki":
                        self.window_handler[f'-KSZTALT_DASZKOW-'].update(visible=True)
                    elif rodzaj_produktu == "Gazony":
                        self.window_handler[f'-KSZTALT_GAZONOW-'].update(visible=True)
                    elif rodzaj_produktu == "Obrzeza":
                        self.window_handler[f'-KSZTALT_OBRZEZY-'].update(visible=True)
                    elif rodzaj_produktu == "Stopnie":
                        self.window_handler[f'-KSZTALT_STOPNI-'].update(visible=True)
                    elif rodzaj_produktu == "Palisady":
                        self.window_handler[f'-KSZTALT_PALISAD-'].update(visible=True)

                    rodzaj_produktu_formatted = str(rodzaj_produktu).lower().replace(" ", "_")
                    if platform.system()=="Linux":
                        rodzaj_produktu_path = path_to_directory_with_brick_shapes+rodzaj_produktu_formatted+"/"
                        if not os.path.exists(rodzaj_produktu_path):
                            os.system(f"sudo mkdir {rodzaj_produktu_path}")
                    else:
                        rodzaj_produktu_path = path_to_directory_with_brick_shapes+rodzaj_produktu_formatted
                        if not os.path.exists(rodzaj_produktu_path):
                            os.mkdir(rodzaj_produktu_path)

                elif self.event in ['Bruk prosty','Cegielka','Fantazja','Grand','Kostka integracyjna','Master','Master XL','Metro','Metro XL','Mosaic','Perfect','Podwojne T','Smart','Starobruk','Trend','Vjetra','Wena','Cube','Ecolinea','Ecosolid','Linea','Longer','Magnum','Multi','Plyta azurowa','Simple','Solid','Style','Unique style','Viva','Claro','Murowy structur','Slupkowy structur','Dwuspadowy structur','Plaski structur','Agaflor','Lucaflor','Patiflor','Palisadowe','Palisadowe XL','8x30x100',"8x25x100","6x20x100",'Palisada kwadratowa','Palisada okragla','Palisada splitowana','Stopien','Stopien splitowany']:
                    ksztalt_produktu = self.event
                    logger.info(f"Wybrano ksztalt produktu: {ksztalt_produktu}")
                    self.window_handler[f'-KSZTALT_KOSTKI-'].update(visible=False)
                    self.window_handler[f'-KSZTALT_PUSTAKOW-'].update(visible=False)
                    self.window_handler[f'-KSZTALT_DASZKOW-'].update(visible=False)
                    self.window_handler[f'-KSZTALT_GAZONOW-'].update(visible=False)
                    self.window_handler[f'-KSZTALT_OBRZEZY-'].update(visible=False)
                    self.window_handler[f'-KSZTALT_STOPNI-'].update(visible=False)
                    self.window_handler[f'-KSZTALT_PALISAD-'].update(visible=False)
                    self.window_handler["-KOLOR-"].update(visible=True)

                    ksztalt_produktu_formatted = str(ksztalt_produktu).lower().replace(" ", "_")
                    if platform.system() == "Linux":
                        ksztalt_produktu_path = path_to_directory_with_brick_shapes + rodzaj_produktu_formatted + "/" + ksztalt_produktu_formatted + "/"
                        if not os.path.exists(ksztalt_produktu_path):
                            os.system(f"sudo mkdir {ksztalt_produktu_path}")
                    else:
                        ksztalt_produktu_path = path_to_directory_with_brick_shapes + rodzaj_produktu_formatted + "\\" + ksztalt_produktu_formatted
                        if not os.path.exists(ksztalt_produktu_path):
                            os.mkdir(ksztalt_produktu_path)

                elif self.event in ["White", "Gray", "Bialy", "Piaskowy", "Antracytowy", "Steel", "Carbon", "Carbon natural", "Steel natural", "Concrete natural", "White natural", "Style white", "Style gray", "Style steel", "Style carbon", "Barwy jesieni", "Czerwony", "Corten", "Dark", "Diamond", "Gothic", "Light", "Muszlowy", "York", "Grafit", "Grafitowy", "Szary", "Bianco", "Popielaty", "Antracyt", "Antracyt melanz", "Piaskowy melanz", "Ambra", "Giallo", "Brazowy", "Mokka", "Bronzo", "Granito", "Nero", "Vero"]:
                    kolor_produktu = self.event
                    print(rodzaj_produktu,ksztalt_produktu,kolor_produktu)
                    self.window_handler["-KOLOR-"].update(visible=False)
                    self.window_handler["-OK-"].update(visible=True)
                    self.brick_clicked = True
                    self.window_handler.Element("-TEXT-RODZAJ-PRODUKTU-").update(f"{rodzaj_produktu}")
                    self.window_handler.Element("-TEXT-KSZTALT-PRODUKTU-").update(f"{ksztalt_produktu}")
                    self.window_handler.Element("-TEXT-KOLOR-PRODUKTU-").update(f"{kolor_produktu}")

                    kolor_produktu_formatted = str(kolor_produktu).lower().replace(" ", "_")
                    logger.info(f"Wybrano kolor produktu: {kolor_produktu}")
                    if platform.system() == "Linux":
                        kolor_produktu_path = path_to_directory_with_brick_shapes + rodzaj_produktu_formatted + "/" + ksztalt_produktu_formatted + "/" + kolor_produktu_formatted+"/"
                        self.complete_path = kolor_produktu_path
                        if not os.path.exists(kolor_produktu_path):
                            os.system(f"sudo mkdir {kolor_produktu_path}")
                    else:
                        kolor_produktu_path = path_to_directory_with_brick_shapes + rodzaj_produktu_formatted + "\\" + ksztalt_produktu_formatted + "\\" + kolor_produktu_formatted
                        self.complete_path = kolor_produktu_path
                        if not os.path.exists(kolor_produktu_path):
                            os.mkdir(kolor_produktu_path)
                    logger.info(f"Pelna sciezka do folderu: {self.complete_path}")
                    self.stop_checking = False

                elif self.event == "Zmień produkt":
                    logger.info("Kliknieto przycisk 'Zmien produkt'")
                    self.stop_checking = True
                    self.window_handler["-OK-"].update(visible=False)
                    self.window_handler["-RODZAJ_PRODUKTU-"].update(visible=True)

            except:
                logger.critical(f"Wystapil nieznany dotad problem w interfejsie brakarza. Opis bledu:\n{traceback.format_exc()}")
                continue



class ImageManager:
    def __init__(self, diff_threshold=0.70, print_result=True):
        self.diff_threshold = diff_threshold
        self.print_result = print_result

    def compare_images(self, image1, image2):
        diff_threshold = self.diff_threshold
        image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        hist1 = cv2.calcHist([image1], [0], None, [256], [0, 256])
        image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        hist2 = cv2.calcHist([image2], [0], None, [256], [0, 256])
        diff = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        if self.print_result:
            logger.info(f"Podobienstwo zdjec: {diff}")
            print(f"[!] Podobienstwo zdjec: {diff}")
        if diff < diff_threshold:
            return False
        else:
            return True

    def get_images(self):
        global latest_image, one_before_latest_image, folder_found
        while not folder_found:
            try:
                latest_directory = max(glob.glob(path_to_directories_with_brick_image_dates), key=os.path.getctime)
                if not os.path.exists(gui_window.complete_path):
                    try:
                        os.system(f"sudo mkdir {gui_window.complete_path}")
                        logger.info(f"Utworzono folder z kolorem produktu: {gui_window.complete_path}")
                        print("[+] Utworzono folder z kolorem produktu")
                    except:
                        print(traceback.print_exc())
                        logger.error(
                            f"Wystapil problem podczas proby utworzenia folderu z kolorem produktu: {gui_window.complete_path}. Opis bledu:\n{traceback.format_exc()}")
                        os._exit(1)
                folder_found = True
            except:
                print(traceback.print_exc())
                logger.error(f"Nie mozna bylo znalezc podanego folderu: '{path_to_directories_with_brick_image_dates}' Opis bledu:\n{traceback.format_exc()}")
                print(f"[-] Nie mozna bylo znalezc podanego folderu: '{path_to_directories_with_brick_image_dates}'")
                time.sleep(2)
        folder_found = False
        path_to_images = latest_directory + "/*"
        if platform.system() == "Linux":
            try:
                print("[~] Proba usuniecia pliku 'Thumbs.db'...")
                os.system(f"sudo rm {latest_directory}/Thumbs.db")
            except:
                print("[-] Wystapil problem podczas usuwania pliku 'Thumbs.db'")
                logger.error(f"Wystapil problem podczas usuwania pliku 'Thumbs.db'. Opis bledu:\n{traceback.format_exc()}")
        try:
            all_images = glob.glob(path_to_images)
            sorted_files = sorted(all_images, key=os.path.getctime)
            latest_image = sorted_files[-1]
            one_before_latest_image = sorted_files[-2]
            # latest_image = cv2.imread(
            #     latest_image)  # Tu wczytuj na biezaco najświezsze zdjecia aktualnie jadacej kostki, tu musi byc ta funkcja wyciagajaca najswiezsze elementy z folderu
            # latest_image = latest_image[65:300, 150:500]
        except ValueError as e:
            latest_image = None
            one_before_latest_image = None
            print(traceback.print_exc())
            print(f"[-] Brak plikow w folderze: '{latest_directory}'. Opis bledu: {e}")
            logger.error(f"Brak plikow w folderze: '{latest_directory}'. Opis bledu: {e}")
            time.sleep(2)
        except IndexError as e:
            latest_image = None
            one_before_latest_image = None
            print(traceback.print_exc())
            print(f"[-] Brak wystarczajacej ilosci plikow w folderze: '{latest_directory}'. Opis bledu: {e}")
            logger.error(f"Brak wystarczajacej ilosci plikow w folderze: '{latest_directory}'. Opis bledu: {e}")
            time.sleep(2)
        except:
            print(traceback.print_exc())
            logger.error(f"Wystapil inny problem podczas pobierania plikow ostatnich zdjec z folderu. Opis bledu:\n{traceback.format_exc()}")
            # os._exit(1)
        return latest_image, one_before_latest_image


if __name__ == "__main__":
    print("[+] Uruchomiono skrypt")

    # logger = logging.getLogger('brakarz_logger')
    if platform.system() == "Linux":
        logname = "/home/pi/aparat/logs/brakarz.log"
    else:
        logname = "brakarz.log"
    logger = logging.getLogger(logname)
    log_format = "[%(asctime)s - %(levelname)s] %(message)s"
    handler = TimedRotatingFileHandler(logname, when="midnight", interval=1, backupCount=7)
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    handler.suffix = "%Y%m%d"
    logger.addHandler(handler)
    logger.info("Uruchomiono skrypt")


    user = getpass.getuser()
    manager = ImageManager()
    gui_window = GUIManager("interfejs_brakarza")
    BUTTON_SIZE = (12, 5)
    BUTTON_SIZE_FOR_COLORS = (9,3)
    FONT_SIZE_FOR_COLORS = ("Helvetica", 19)
    FONT_SIZE = ("Helvetica", 17)
    latest_image = None
    one_before_latest_image = None
    folder_found = False

    if platform.system() == "Linux":
        path_to_directory_with_brick_shapes = "/home/pi/gui/kostki/"
        path_to_directories_with_brick_image_dates = "/home/pi/zdjecia_automatyczne/rozpoznawanie/kostki/*"
    else:
        path_to_directory_with_brick_shapes = f"C:\\Users\\{user}\\Desktop\\zdjecia_posegregowane\\"
        path_to_directories_with_brick_image_dates = f"C:\\Users\\{user}\\Desktop\\zdjecia_nowe\\"

    if platform.system() == "Linux" and os.environ.get('DISPLAY', '') == '':
        try:
            logger.warning("Nie mozna bylo znalezc wyswietlacza. Uzywam ':0.0'")
            print("[-] Nie mozna bylo znalezc wyswietlacza. Uzywam ':0.0'")
            os.environ.__setitem__('DISPLAY', ':0.0')
        except:
            logger.error(f"Problem ze znalezieniem wyswietlacza. Opis bledu:\n{traceback.format_exc()}")
            time.sleep(0.5)
            print(traceback.print_exc())
            # os._exit(1)

    def main():
        time.sleep(1)
        while True:
            try:
                if not gui_window.stop_checking:

                    try:
                        image1, image2 = manager.get_images()
                        logger.info(f"Pobrano zdjecia z odpowiednich folderow: \nImage1: '{image1}'\nImage2: '{image2}'")
                    except:
                        print(f"Wystapil problem podczas pobierania zdjec z odpowiednich folderow folderow. Opis bledu:\n{traceback.format_exc()}")
                        logger.error(f"Wystapil problem podczas pobierania zdjeć. Opis bledu:\n{traceback.format_exc()}")
                        time.sleep(2)
                        continue

                    try:
                        img1 = cv2.imread(image1)
                        img1_crop = img1[65:300, 150:500]
                        img2 = cv2.imread(image2)
                        img2_crop = img2[65:300, 150:500]
                    except:
                        print(f"Wystapil problem podczas wczytywania zdjec przez OpenCV. Opis bledu {traceback.format_exc()}")
                        logger.error(f"Wystapil problem podczas wczytywania zdjec przez OpenCV. Opis bledu:\n{traceback.format_exc()}")
                        time.sleep(2)
                        continue

                    try:
                        print(f"[~] Porownywanie zdjec:\nImage1: '{image1}'\nImage2: '{image2}')")
                        compare_result = manager.compare_images(img1_crop, img2_crop)
                    except:
                        print(f"Wystapil problem podczas porownywania zdjec. Opis bledu {traceback.format_exc()}")
                        logger.error(f"Wystapil problem podczas porownywania zdjec (histogramow zdjec). Opis bledu:\n{traceback.format_exc()}")
                        time.sleep(2)
                        continue

                    if compare_result == True:
                        gui_window.brick_clicked = False
                        print("[!] To ten sam produkt")
                        print(f"[~] Kopiuje zdjecie do folderu: {gui_window.complete_path}")
                        try:
                            if platform.system() == "Linux":
                                os.system(f"sudo cp {image1} {gui_window.complete_path}")
                            else:
                                shutil.copy(image1, gui_window.complete_path)
                            print("[+] Skopiowano")
                            logger.info(f"Skopiowano porownywane zdjecie (Image1) do odpowiedniego folderu: {gui_window.complete_path}")
                        except:
                            print(f"Wystapil problem podczas kopiowania zdjecia do odpowiedniego folderu. Opis bledu:\n{traceback.format_exc()}")
                            logger.error(f"Wystapil problem podczas kopiowania zdjecia (Image1) do odpowiedniego folderu: {gui_window.complete_path}. Opis bledu:\n{traceback.format_exc()}")
                            continue
                        # if not os.path.isfile(
                        #         latest_image):  # Jeśli zdjecie najświezszej kostki nie istnieje w folderze to skopiuj je (jeśli nie ma duplikatu nazw)
                        #     copyfile(latest_image, gui_window.complete_path)
                    else:
                        logger.warning("Wykryto inny produkt")
                        print("[!] To inny produkt")
                        print("[-] Nie kopiuje zdjecia")
                        gui_window.window_handler.write_event_value('-STOP-', 1)
                        logger.info("Oczekiwanie na klikniecie w graficznym interfejsie")
                        print("[~] Oczekiwanie na klikniecie w graficznym interfejsie")
                        while True:
                            time.sleep(0.5)
                            if gui_window.brick_clicked:
                                print("[+] Kliknieto w graficzny interfejs")
                                break
                        gui_window.brick_clicked = False
                    print("-------------------")
                time.sleep(1)
            except:
                print(f"[-] Wystapil inny nieznany dotad problem w watku 'main'. Opis bledu:\n{traceback.format_exc()}")
                logger.critical(f"Wystapil inny nieznany dotad problem w watku 'main'. Opis bledu:\n{traceback.format_exc()}")
                os._exit(1)


    main_thread = threading.Thread(target=main)
    main_thread.start()
    gui_window.initialize_window([[
            sg.Column([
                [sg.Text('1. Wybierz rodzaj aktualnego produktu:', font=("Helvetica", 25))],
                [sg.Button('Kostka\nbrukowa', size=BUTTON_SIZE, font=FONT_SIZE),
                 sg.Button('Pustaki', size=BUTTON_SIZE, font=FONT_SIZE),
                 sg.Button('Daszki', size=BUTTON_SIZE, font=FONT_SIZE),
                 sg.Button("Gazony", size=BUTTON_SIZE, font=FONT_SIZE),
                 sg.Button("Obrzeza", size=BUTTON_SIZE, font=FONT_SIZE),
                 sg.Button("Stopnie", size=BUTTON_SIZE, font=FONT_SIZE)],
                 [sg.Button("Palisady", size=BUTTON_SIZE, font=FONT_SIZE)]],
                key='-RODZAJ_PRODUKTU-', visible=True),
            sg.Column([
                [sg.Text('2. Wybierz kształt kostki:', font=("Helvetica", 25))],
                [sg.Button('Bruk\nprosty', size=BUTTON_SIZE, font=FONT_SIZE),
                 sg.Button('Cegielka', size=BUTTON_SIZE, font=FONT_SIZE),
                 sg.Button('Fantazja', size=BUTTON_SIZE, font=FONT_SIZE),
                 sg.Button('Grand', size=BUTTON_SIZE, font=FONT_SIZE),
                 sg.Button('Kostka\nintegracyjna', size=BUTTON_SIZE, font=FONT_SIZE),
                 sg.Button('Master', size=BUTTON_SIZE, font=FONT_SIZE)],
                [sg.Button('Master\nXL', size=BUTTON_SIZE, font=FONT_SIZE),
                 sg.Button('Metro', size=BUTTON_SIZE, font=FONT_SIZE),
                 sg.Button('Metro\nXL', size=BUTTON_SIZE, font=FONT_SIZE),
                 sg.Button('Mosaic', size=BUTTON_SIZE, font=FONT_SIZE),
                 sg.Button('Perfect', size=BUTTON_SIZE, font=FONT_SIZE),
                 sg.Button('Podwojne\nT', size=BUTTON_SIZE, font=FONT_SIZE)],
                [sg.Button('Smart', size=BUTTON_SIZE, font=FONT_SIZE),
                 sg.Button('Starobruk', size=BUTTON_SIZE, font=FONT_SIZE),
                 sg.Button('Trend', size=BUTTON_SIZE, font=FONT_SIZE),
                 sg.Button('Vjetra', size=BUTTON_SIZE, font=FONT_SIZE),
                 sg.Button('Wena', size=BUTTON_SIZE, font=FONT_SIZE)]],
                key='-KSZTALT_KOSTKI-',visible=False),
            sg.Column([
                [sg.Text('2. Wybierz kształt płyty:', font=("Helvetica", 25))],
                [sg.Button('Cube', size=BUTTON_SIZE, font=FONT_SIZE),
                 sg.Button('Ecolinea', size=BUTTON_SIZE, font=FONT_SIZE),
                 sg.Button('Ecosolid', size=BUTTON_SIZE, font=FONT_SIZE),
                 sg.Button('Linea', size=BUTTON_SIZE, font=FONT_SIZE),
                 sg.Button('Longer', size=BUTTON_SIZE, font=FONT_SIZE),
                 sg.Button('Magnum', size=BUTTON_SIZE, font=FONT_SIZE)],
                [sg.Button('Multi', size=BUTTON_SIZE, font=FONT_SIZE),
                 sg.Button('Plyta\nazurowa', size=BUTTON_SIZE, font=FONT_SIZE),
                 sg.Button('Simple', size=BUTTON_SIZE, font=FONT_SIZE),
                 sg.Button('Solid', size=BUTTON_SIZE, font=FONT_SIZE),
                 sg.Button('Style', size=BUTTON_SIZE, font=FONT_SIZE),
                 sg.Button('Unique\nstyle', size=BUTTON_SIZE, font=FONT_SIZE)],
                [sg.Button('Viva', size=BUTTON_SIZE, font=FONT_SIZE)]],
                key='-KSZTALT_PLYTY-', visible=False),
            sg.Column([
                [sg.Text('2. Wybierz kształt pustaka:', font=("Helvetica", 25))],
                [sg.Button('Claro', size=BUTTON_SIZE, key="Claro1", font=FONT_SIZE),
                 sg.Button('Murowy\nstructur', size=BUTTON_SIZE, font=FONT_SIZE),
                 sg.Button('Slupkowy\nstructur', size=BUTTON_SIZE, font=FONT_SIZE)]],
                key='-KSZTALT_PUSTAKOW-', visible=False),
        sg.Column([
            [sg.Text('2. Wybierz kształt daszka:', font=("Helvetica", 25))],
            [sg.Button('Claro', size=BUTTON_SIZE, key="Claro0", font=FONT_SIZE),
             sg.Button('Dwuspadowy\nstructur', size=BUTTON_SIZE, font=FONT_SIZE),
             sg.Button('Plaski\nstructur', size=BUTTON_SIZE, font=FONT_SIZE)]],
            key='-KSZTALT_DASZKOW-', visible=False),
        sg.Column([
            [sg.Text('2. Wybierz kształt gazona:', font=("Helvetica", 25))],
            [sg.Button('Agaflor', size=BUTTON_SIZE, font=FONT_SIZE),
             sg.Button('Lucaflor', size=BUTTON_SIZE, font=FONT_SIZE),
             sg.Button('Patiflor', size=BUTTON_SIZE, font=FONT_SIZE)]],
            key='-KSZTALT_GAZONOW-', visible=False),
        sg.Column([
            [sg.Text('2. Wybierz kształt obrzeża:', font=("Helvetica", 25))],
            [sg.Button('Palisadowe', size=BUTTON_SIZE, font=FONT_SIZE),
             sg.Button('Palisadowe\nXL', size=BUTTON_SIZE, font=FONT_SIZE),
             sg.Button('8x30x100', size=BUTTON_SIZE, font=FONT_SIZE),
             sg.Button("8x25x100", size=BUTTON_SIZE, font=FONT_SIZE),
             sg.Button("6x20x100", size=BUTTON_SIZE, font=FONT_SIZE)]],
            key='-KSZTALT_OBRZEZY-', visible=False),

        sg.Column([
            [sg.Text('2. Wybierz kształt palisady:', font=("Helvetica", 25))],
            [sg.Button('Palisada\nkwadratowa', size=BUTTON_SIZE, font=FONT_SIZE),
             sg.Button('Palisada\nokragla', size=BUTTON_SIZE, font=FONT_SIZE),
             sg.Button('Palisada\nsplitowana', size=BUTTON_SIZE, font=FONT_SIZE)]],
            key='-KSZTALT_PALISAD-', visible=False),

        sg.Column([
            [sg.Text('2. Wybierz kształt stopnia:', font=("Helvetica", 25))],
            [sg.Button('Stopien', size=BUTTON_SIZE, font=FONT_SIZE),
             sg.Button('Stopien\nsplitowany', size=BUTTON_SIZE, font=FONT_SIZE)]],
            key='-KSZTALT_STOPNI-', visible=False),

            sg.Column([
                [sg.Text('3. Wybierz kolor wskazanego produktu:', font=("Helvetica", 25))],
                [sg.Button('Ambra', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                 sg.Button('Antracyt', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                 sg.Button('Antracyt\nmelanz', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                 sg.Button('Antracytowy', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                 sg.Button('Barwy\njesieni', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                 sg.Button('Bianco', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                 sg.Button('Bialy', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS)],
                 [sg.Button('Bronzo', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                  sg.Button('Brazowy', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                  sg.Button('Carbon', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                  sg.Button('Carbon\nnatural', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                  sg.Button('Concrete\nnatural', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                  sg.Button('Corten', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                  sg.Button('Czerwony', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS)],
                 [sg.Button('Dark', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                  sg.Button('Diamond', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                  sg.Button('Giallo', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                  sg.Button('Gothic', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                  sg.Button('Grafit', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                  sg.Button('Grafitowy', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                  sg.Button('Granito', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS)],
                 [sg.Button('Gray', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                  sg.Button('Light', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                  sg.Button('Mokka', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                  sg.Button('Muszlowy', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                  sg.Button('Nero', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                  sg.Button('Piaskowy', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                  sg.Button('Piaskowy\nmelanz', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS)],
                 [sg.Button('Popielaty', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                  sg.Button('Steel', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                  sg.Button('Steel\nnatural', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                  sg.Button('Style\ncarbon', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                  sg.Button('Style\ngray', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                  sg.Button('Style\nsteel', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                  sg.Button('Style\nwhite', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS)],
                [sg.Button('Szary', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                 sg.Button('Vero', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                 sg.Button('White', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                 sg.Button('White\nnatural', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS),
                 sg.Button('York', size=BUTTON_SIZE_FOR_COLORS, font=FONT_SIZE_FOR_COLORS)]
            ],
                visible=False, key='-KOLOR-'),
            sg.Column([
                                        [sg.Text("WYKRYTO INNY PRODUKT", font=("Helvetica", 60), pad=(160, 100),text_color="red")],
                                        [sg.B("OK", size=(13, 5), font=("Helvetica", 30),button_color=('white', 'red'),pad=(450, 1))],
                                        [sg.T("",pad=(135,60)),sg.T("Brakarzu nacisnij OK i wybierz aktualny rodzaj kostki", font=("Helvetica", 20))],
                                        [sg.T("", font=("Helvetica", 100))]
                                    ],
                visible=False, key='-UWAGA-'),
            sg.Column([
                                        [sg.Text("SYSTEM ZDJĘĆ OK", font=("Helvetica", 80), pad=(140, 50),text_color="green")],
                                        [sg.T("", pad=(216, 1)), sg.Text("Rodzaj:", font=("Helvetica", 33)), sg.Text("brak_danych", key="-TEXT-RODZAJ-PRODUKTU-", font=("Helvetica", 33))],
                                        [sg.T("", pad=(216, 10)),sg.Text("Kształt:", font=("Helvetica", 33)),sg.Text("brak_danych",key="-TEXT-KSZTALT-PRODUKTU-", font=("Helvetica", 33))],
                                        [sg.T("", pad=(216, 10)),sg.Text("  Kolor:", font=("Helvetica", 33)),sg.Text("brak_danych",key="-TEXT-KOLOR-PRODUKTU-", font=("Helvetica", 33))],
                                        [sg.B("Zmień produkt", size=(15, 4), font=("Helvetica", 28), pad=(430, 40))],
                                        [sg.T("", font=("Helvetica", 100))]
                                    ],
                visible=False, key='-OK-')]])

