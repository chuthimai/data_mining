import pandas as pd
import re


class ProcessingCompanyDetail:
    def __init__(self, file_path="../file_csv/job_posting.csv"):
        self.file_path = file_path
        self.df = pd.read_csv(file_path)
        self.process_size_of_company()
        self.process_followers_of_company()

    def process_size_of_company(self):
        """Chuyển đổi cột size_of_company thành các mức Micro, Small, Medium, Large, Super"""
        size_mapping = {
            "1": "Micro",
            "2-10": "Micro",
            "11-50": "Small",
            "51-200": "Medium",
            "201-500": "Large",
            "501-1000": "Large",
            "1001-5000": "Super",
            "5001-10000": "Super",
            "10001+": "Super"
        }
        self.df['size_of_company'] = self.df['size_of_company'].map(size_mapping)

    def process_followers_of_company(self):
        """Trích xuất số lượng followers từ chuỗi và chuyển thành số nguyên"""

        self.df['followers_of_company'] = self.df['followers_of_company'].apply(self._extract_followers)

    def _extract_followers(self, text):
        match = re.search(r"(\d{1,3}(?:,\d{3})*) followers", str(text))
        if match:
            return int(match.group(1).replace(",", ""))
        return None

    def save_csv(self, output_file="../file_csv/job_posting_processed.csv"):
        """Lưu file đã xử lý"""
        self.df.to_csv(output_file, index=False)
        print("-------ProcessingCompanyDetail-------")
        print(f"File đã được lưu tại: {output_file} sau khi xử lý company_detail")


