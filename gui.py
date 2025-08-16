# gui.py — модуль, отвечающий за графический интерфейс на базе ttkbootstrap (tkinter)

# os — для работы с именами и путями файлов
import os
# стандартные модули tkinter для GUI и диалогов
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
# ttkbootstrap даёт современный стиль для tkinter
import ttkbootstrap as ttk
# импортируем AudioManager для обработки аудио
from audio_manager import AudioManager



class Audio_Editor:
    """
        GUI-приложение Audio_Editor:
        кнопки, диалоги и связь с AudioManager.
        """

    def __init__(self):
        """
        Инициализация окна, менеджера аудио и виджетов.
        """
        # создаём окно с темой 'superhero'
        self.root = ttk.Window(themename='superhero')
        # заголовок окна
        self.root.title("Audio Editor")
        # размер окна
        self.root.geometry("600x400")
        # экземпляр менеджера аудио
        self.manager = AudioManager()
        # создаём все кнопки и метки
        self._create_widgets()

    def _create_widgets(self):
        """
        Создаёт кнопки управления и метку для имени файла.
        """
        # фрейм для кнопок
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)

        # кнопка загрузки файла
        ttk.Button(btn_frame, text="Open", command=self.open_file).pack(side='left', padx=5)
        # кнопка воспроизведения
        ttk.Button(btn_frame, text="Play", command=self.play).pack(side='left', padx=5)
        # кнопка остановки
        ttk.Button(btn_frame, text="Stop", command=self.stop).pack(side='left', padx=5)
        # реверс звука
        ttk.Button(btn_frame, text="Reverse", command=self.reverse).pack(side='left', padx=5)
        # ускорение
        ttk.Button(btn_frame, text="Faster", command=lambda: self.change_speed(1.5)).pack(
            side='left', padx=5)
        # замедление
        ttk.Button(btn_frame, text="Slower", command=lambda: self.change_speed(0.75)).pack(
            side='left', padx=5)
        # громкость +5 дБ
        ttk.Button(btn_frame, text="Vol +5", command=lambda: self.change_volume(5)).pack(
            side='left', padx=5)
        # громкость -5 дБ
        ttk.Button(btn_frame, text="Vol -5", command=lambda: self.change_volume(-5)).pack(
            side='left', padx=5)
        # обрезка
        ttk.Button(btn_frame, text="Trim", command=self.trim).pack(side='left', padx=5)
        # сохранение
        ttk.Button(btn_frame, text="Save", command=self.save_file).pack(side='left', padx=5)

        # метка для отображения имени загруженного файла
        self.file_label = ttk.Label(self.root, text="No file loaded", bootstyle='info')
        self.file_label.pack(pady=10)

    def open_file(self):
        """
        Открывает диалог выбора аудиофайла и загружает его.
        """
        # диалог открытия файла с фильтрацией форматов
        file_path = filedialog.askopenfilename(
            title="Open Audio File",
            filetypes=[("Audio Files", "*.wav;*.mp3;*.flac;*.ogg")]
        )
        # если путь получен (не отмена)
        if file_path:
            try:
                # загружаем аудио в менеджер
                self.manager.load(file_path)
                # обновляем метку — показываем имя файла
                self.file_label.config(text=os.path.basename(file_path))
            except Exception as e:
                # показываем окно ошибки, если не удалось загрузить
                messagebox.showerror("Error", f"Cannot load file:\n{e}")

    def play(self):
        """
        Запускает воспроизведение загруженного аудио.
        """
        try:
            self.manager.play()
        except Exception:
            # предупреждение, если аудио не загружено
            messagebox.showwarning("Warning", "Load a file first.")

    def stop(self):
        """
        Останавливает воспроизведение.
        """
        self.manager.stop()

    def reverse(self):
        """
        Применяет эффект реверса к аудио.
        """
        self.manager.reverse()

    def change_speed(self, factor: float):
        """
        Меняет скорость воспроизведения на заданный множитель.
        :param factor: >1 замедляет, <1 ускоряет
        """
        self.manager.change_speed(factor)

    def change_volume(self, db: float):
        """
        Изменяет громкость на указанное количество дБ.
        :param db: положительное — громче, отрицательное — тише
        """
        self.manager.change_volume(db)

    def trim(self):
        """
        Обрезает аудио по введённым пользователем временным меткам.
        """
        # если аудио не загружено — предупреждаем и выходим
        if not self.manager.audio:
            messagebox.showwarning("Warning", "Load a file first.")
            return
        # запрашиваем начало в мс
        start = simpledialog.askinteger(
            "Trim Start", "Start (ms):",
            minvalue=0, maxvalue=len(self.manager.audio)
        )
        # запрашиваем конец в мс
        end = simpledialog.askinteger(
            "Trim End", "End (ms):",
            minvalue=0, maxvalue=len(self.manager.audio)
        )
        # проверяем корректность диапазона
        if start is not None and end is not None and start < end:
            self.manager.trim(start, end)
        else:
            # информируем о неверном диапазоне
            messagebox.showinfo("Info", "Invalid trim range.")

    def save_file(self):
        """
        Открывает диалог сохранения и сохраняет аудио.
        """
        # если аудио не загружено — предупреждаем
        if not self.manager.audio:
            messagebox.showwarning("Warning", "Load and process a file first.")
            return
        # диалог выбора места и имени файла
        export_path = filedialog.asksaveasfilename(
            title="Save Audio File",
            defaultextension=".wav",
            filetypes=[("WAV", "*.wav"),
                       ("MP3", "*.mp3"),
                       ("FLAC", "*.flac"),
                       ("OGG", "*.ogg")]
        )
        # если путь получен — сохраняем через менеджер
        if export_path:
            try:
                # определяем формат по расширению файла
                ext = os.path.splitext(export_path)[1][1:]
                self.manager.save(export_path, format=ext)
            except Exception as e:
                # показываем окно с ошибкой при сохранении
                messagebox.showerror("Error", f"Cannot save file:\n{e}")

    def run(self):
        """
        Запускает главный цикл GUI-приложения.
        """
        self.root.mainloop()

# точка входа: если этот скрипт запущен напрямую
if __name__ == "__main__":
    # создаём экземпляр приложения
    app = Audio_Editor()
    # запускаем GUI
    app.run()
