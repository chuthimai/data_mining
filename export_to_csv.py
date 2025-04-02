import pandas as pd
from mysql_connection import MySQLConnection


class ExportToCSV:
    def __init__(self):
        # Kết nối MySQL
        self._db = MySQLConnection(
            host="123.31.12.175",
            user="rd_user",
            password="rduser@123",
            database="RD"
        )

    def mysql_to_csv(self, query, file_path):
        connection = self._db.get_connection()
        df = pd.read_sql(query, connection)

        # Xuất ra file CSV
        df.to_csv(f"{file_path}", index=False)

        # Đóng kết nối
        self._db.close_connection()
        print(f"Xuất dữ liệu thành công: {file_path}")


if __name__ == '__main__':
    export_to_csv = ExportToCSV()
    query1 = '''
    SELECT 
        job_posting.id,
        job_posting.title, 
        job_posting.`description`, 
        job_posting.industries
    FROM RD.job_posting
    WHERE job_posting.`description` != "" 
        AND job_posting.industries != ""
    LIMIT 1000;
    '''

    query2 = '''
    SELECT 
        profile_info.id,
        GROUP_CONCAT(DISTINCT experience.title SEPARATOR '. ') AS title,
        GROUP_CONCAT(DISTINCT experience.company SEPARATOR '. ') AS company,
        GROUP_CONCAT(DISTINCT experience.`description` SEPARATOR '. ') AS `description`,
        GROUP_CONCAT(DISTINCT company_detail.industry SEPARATOR '. ') AS industry_of_company,
        GROUP_CONCAT(DISTINCT profile_info.summary SEPARATOR '. ') AS summary_of_applicant
    FROM RD.experience
    LEFT JOIN RD.profile_info
    ON experience.public_id = profile_info.public_id
    LEFT JOIN RD.company_detail 
    ON company_detail.cid = experience.company_id
    WHERE (experience.`description` != '')
       OR (profile_info.summary != '')
       AND (experience.title != '')
    GROUP BY profile_info.id
    LIMIT 1000;
    '''
    export_to_csv.mysql_to_csv(query=query1, file_path="./file_csv_limit/job_posting.csv")
    export_to_csv.mysql_to_csv(query=query2, file_path="./file_csv_limit/experience.csv")


