import re

import pandas as pd
import dateparser
from deep_translator import GoogleTranslator


class ProcessingExperience:
    def __init__(self, file_path="../file_csv/experience.csv"):
        self.file_name = file_path
        self.df = pd.read_csv(file_path)
        self.process_dates()
        self.translate_columns()
        self.merge_description_summary()

    def process_dates(self):
        if not {'start_date', 'end_date'}.issubset(self.df.columns):
            return

        """Chuẩn hóa ngày tháng và tính khoảng thời gian giữa start_date và end_date"""
        self.df['start_date'] = self.df['start_date'].apply(self.normalize_date)
        self.df['end_date'] = self.df['end_date'].apply(self.normalize_date)

        # Chuyển cột start_date và end_date sang dạng datetime
        self.df['start_date'] = pd.to_datetime(self.df['start_date'], errors='coerce')
        self.df['end_date'] = pd.to_datetime(self.df['end_date'], errors='coerce')

        # Tìm ngày lớn nhất
        max_end_date = self.df['end_date'].max()
        max_start_date = self.df['start_date'].max()
        max_date = max(max_start_date, max_end_date)

        # Điền giá trị thiếu trong end_date bằng max_date
        self.df['end_date'] = self.df['end_date'].fillna(max_date)

        # Tính khoảng thời gian (số ngày)
        self.df['duration_days'] = (self.df['end_date'] - self.df['start_date']).dt.days

    def normalize_date(self, date_str):
        """Chuẩn hóa ngày tháng từ nhiều định dạng khác nhau"""
        if pd.isna(date_str) or not isinstance(date_str, str) or date_str.strip() == "":
            return None  # Nếu trống thì bỏ qua

        # Nếu chỉ có năm -> thêm '-01-01'
        if date_str.isdigit() and len(date_str) == 4:
            return f"{date_str}-01-01"

        # Dùng dateparser để chuyển đổi định dạng ngày tháng từ các ngôn ngữ khác nhau
        parsed_date = dateparser.parse(date_str)

        if parsed_date:
            return parsed_date.strftime('%Y-%m-%d')  # Chuẩn hóa thành YYYY-MM-DD

        return None  # Nếu không thể parse

    def translate_columns(self):
        """Dịch nội dung các cột về tiếng Anh"""
        self.df['description'] = self.df['description'].apply(self.translate_text)
        self.df['summary_of_applicant'] = self.df['summary_of_applicant'].apply(self.translate_text)
        self.df['title'] = self.df['title'].apply(self.translate_text)
        self.df['title'] = self.df['title'].apply(self.clean_text)

    def translate_text(self, text):
        """Dịch văn bản sang tiếng Anh nếu không phải"""
        if pd.isna(text) or not isinstance(text, str) or text.strip() == "":
            return text  # Bỏ qua nếu trống

        try:
            translated_text = GoogleTranslator(source='auto', target='en').translate(text)
            return translated_text
        except Exception as e:
            print(f"Error translating text: {text} - {e}")
            return text  # Trả về nội dung gốc nếu lỗi

    def merge_description_summary(self):
        """Nối cột description và summary_of_applicant thành description"""
        self.df['description'] = self.df[
            ['description', 'summary_of_applicant']
        ].fillna('').agg(' '.join, axis=1).str.strip()
        self.df.drop(columns=['summary_of_applicant'], inplace=True)

    def clean_text(self, text):
        """Làm sạch văn bản, loại bỏ ký hiệu vô nghĩa & icon"""
        if pd.isna(text) or not isinstance(text, str):
            return text

        text = re.sub(r'\.Net', 'DOTNET_TEMP', text, flags=re.IGNORECASE)

        # Loại bỏ các ký hiệu không mong muốn
        text = re.sub(r'[?.,!@#$%^&*()_+=<>/|\\{}[\]~-]', ' ', text)

        # Loại bỏ ký tự icon & emoji (mã Unicode)
        text = re.sub(r'[\U00010000-\U0010FFFF]', '', text, flags=re.UNICODE)
        text = re.sub(r'\s+', ' ', text).strip()

        # Đổi lại `.Net`
        text = re.sub(r'DOTNET_TEMP', '.Net', text, flags=re.IGNORECASE)

        return text

    def get_columns(self):
        """Lấy danh sách các trường trong file CSV"""
        return list(self.df.columns)

    def get_total_records(self):
        """Lấy tổng số bản ghi"""
        return len(self.df)

    def get_csv_info(self):
        """Lấy mô tả dữ liệu hiện tại"""
        return self.df.info()

    def save_csv(self, output_file="../file_csv/experience.csv"):
        """Lưu file đã xử lý"""
        self.df.to_csv(output_file, index=False)
        print("-------ProcessingExperience-------")
        print(f"File đã được lưu tại: {output_file} sau khi xử lý experience")


if __name__ == '__main__':
    processor = ProcessingExperience(file_path="../file_csv_limit/experience.csv")
    print("Danh sách các trường:", processor.get_columns())
    print("Tổng số bản ghi:", processor.get_total_records())
    print(processor.get_csv_info())
    processor.save_csv(output_file="../file_csv_after_processed/experience.csv")
