import os
import olefile

folder_path = 'C:\\Users\\남현승\\Desktop\\programing\\PythonWorkspace\\kumoh\\Kakao\\hwp_'  # Replace with the actual path to your folder

for filename in os.listdir(folder_path):
    if filename.endswith('.hwp'):
        hwp_path = os.path.join(folder_path, filename)
        output_txt_path = os.path.splitext(hwp_path)[0] + '.txt'

        with olefile.OleFileIO(hwp_path) as f:
            encoded_text = f.openstream('PrvText').read()

        try:
            decoded_text = encoded_text.decode('utf-16-le', errors='replace')  # Try little-endian first
        except UnicodeDecodeError:
            try:
                decoded_text = encoded_text.decode('utf-16-be', errors='replace')  # Try big-endian if little-endian fails
            except UnicodeDecodeError:
                print(f"Error decoding file: {hwp_path}")
                continue  # Skip to the next file if decoding fails with both endianness options

        with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(decoded_text)
