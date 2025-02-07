import os
import shutil

def clean_desktop():
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    document_folder = os.path.join(desktop, "Document")
    media_folder = os.path.join(desktop, "Media")
    label_folder = os.path.join(desktop, "Label")
    
    folders = [document_folder, media_folder, label_folder]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
    
    document_types = (".pdf", ".doc", ".docx", ".txt", ".xlsx", ".pptx")
    media_types = (".jpg", ".png", ".mp4", ".mp3", ".avi", ".mov", "gif")
    label_types = (".zip", ".rar", ".7z", ".exe", ".lnk")
    
    for item in os.listdir(desktop):
        item_path = os.path.join(desktop, item)
        
        if os.path.isfile(item_path):
            if item.endswith(document_types):
                shutil.move(item_path, document_folder)
            elif item.endswith(media_types):
                shutil.move(item_path, media_folder)
            elif item.endswith(label_types):
                shutil.move(item_path, label_folder)

clean_desktop()
