import re

import pandas as pd
from bs4 import BeautifulSoup

from process_csv_file.processing_company_detail import ProcessingCompanyDetail


class ProcessingJobPosting:
    def __init__(self, file_path="../file_csv/job_posting.csv"):
        self.file_path = file_path
        self.keywords_contain = {
            "must", "valid", "diploma", "degree", "oriented", "specialty", "require", "able",
            "experience", "skill", "expertise", "background", "exposure", "knowledge", "practice",
            "proficiency", "professional", "track record", "familiarity", "ability", "competency",
            "mastery", "fluency"
            }
        self.keywords_not_contain = {
            "your", "we", "our", "disability", "unable",
            "without prior experience", "training", "your particular skill",

        }
        self.df = pd.read_csv(file_path)  # Đọc file CSV
        self.process_num_applicants()  # Xử lý num_applicants
        self.add_column_is_no_experience()
        self.add_column_is_freelance()
        self.process_job_descriptions()  # Xử lý description

    def process_num_applicants(self):
        """Chuẩn hóa dữ liệu cột num_applicants"""

        def transform_value(value):
            if isinstance(value, str):
                if "Over 200 applicants" in value:
                    return ">200"
                elif "Be among the first 25 applicants" in value:
                    return "<25"
            return "25-200"  # Giữ nguyên nếu không phù hợp

        self.df['num_applicants'] = self.df['num_applicants'].apply(transform_value)

    def extract_relevant_sentences(self, html):
        """Trích xuất các câu có chứa từ khóa và nối lại"""
        if not isinstance(html, str):
            return None

        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text("\n")  # Lấy toàn bộ nội dung văn bản từ HTML
        sentences = self.split_into_sentences(text)  # Tách thành từng câu
        relevant_sentences = [
            sentence for sentence in sentences
            if self.contains_keyword(sentence) and self.not_contains_keyword(sentence)
        ]
        return ". ".join(relevant_sentences) if relevant_sentences else None

    def split_into_sentences(self, text):
        """Tách nội dung thành danh sách các câu"""
        return re.split(r'[?.\n!]', text.strip())

    def contains_keyword(self, text):
        """Kiểm tra xem câu có chứa từ khóa không"""
        return any(keyword in text.lower() for keyword in self.keywords_contain)

    def not_contains_keyword(self, text):
        """Kiểm tra xem câu có ko chứa từ khóa không"""
        return not any(keyword in text.lower() for keyword in self.keywords_not_contain)

    def process_job_descriptions(self):
        """Áp dụng xử lý cho cột 'description'"""
        self.df['description'] = self.df['description'].apply(self.extract_relevant_sentences)
        self.df.rename(columns={'description': 'experiences_and_skills'}, inplace=True)

    def add_column_is_no_experience(self):
        """Thêm cột is_no_experience kiểm tra xem có chứa 'no experience' trong description không"""
        self.df['is_no_experience'] = self.df['description'].apply(self.check_no_experience)

    def check_no_experience(self, value):
        dict_no_experience = {"no prior experience", "no experience"}
        if isinstance(value, str):
            return 1 if any(keyword in value.lower() for keyword in dict_no_experience) else 0
        return ""  # Nếu không có giá trị, để trống

    def add_column_is_freelance(self):
        """Thêm cột is_freelance kiểm tra xem có chứa 'freelance' trong description không"""

        self.df['is_freelance'] = self.df['description'].apply(self.check_freelance)

    def check_freelance(self, value):
        if isinstance(value, str):
            return 1 if "freelance" in value.lower() else 0
        return ""  # Nếu không có giá trị, để trống


    def get_columns(self):
        """Lấy danh sách các trường trong file CSV"""
        return list(self.df.columns)

    def get_total_records(self):
        """Lấy tổng số bản ghi"""
        return len(self.df)

    def get_csv_info(self):
        """Lấy mô tả dữ liệu hiện tại"""
        return self.df.info()

    def save_csv(self, output_file="../file_csv/job_posting_processed.csv"):
        """Lưu file đã xử lý"""
        self.df.to_csv(output_file, index=False)
        print("-------ProcessingJobPosting-------")
        print(f"File đã được lưu tại: {output_file} sau khi xử lý job_posting")


# ---- Cách sử dụng ----
if __name__ == "__main__":
    file_path_input = "../file_csv_limit/job_posting.csv"
    file_path_output = "../file_csv_after_processed/job_posting.csv"

    process_company_detail = ProcessingCompanyDetail(file_path_input)
    process_company_detail.save_csv(output_file=file_path_output)

    processor_job_posting = ProcessingJobPosting(file_path=file_path_output)

    print("Danh sách các trường:", processor_job_posting.get_columns())
    print("Tổng số bản ghi:", processor_job_posting.get_total_records())
    print(processor_job_posting.get_csv_info())

    # Lưu file sau khi xử lý
    processor_job_posting.save_csv(output_file=file_path_output)

