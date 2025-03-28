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
    select 
        -- job_posting.id,
        job_posting.title, 
        job_posting.company_name, 
        job_posting.location, 
        job_posting.num_applicants, 
      job_posting.`description`, 
        job_posting.seniority_level, 
        job_posting.employment_type, 
        job_posting.job_function, 
      job_posting.industries,
      company_detail.number_of_employees,
      company_detail.industry as industry_of_company,
      company_detail.size as size_of_company,
      company_detail.followers as followers_of_company
    from RD.job_posting
    left join RD.company_detail
    on job_posting.cid = company_detail.cid
    where job_posting.location != "" 
        and job_posting.num_applicants != "" 
        and job_posting.`description` != "" 
        and job_posting.seniority_level != "" 
        and job_posting.employment_type != "" 
        and job_posting.job_function != "" 
        and job_posting.industries != ""
    limit 100
    ;
    '''

    query2 = '''
    select 
        experience.title,
        experience.company,
        experience.`description`,
        experience.start_date,
        experience.end_date,
        experience.change_job,
        profile_info.headline as headline_of_applicant,
        profile_info.location as locatio_of_applicant,
        profile_info.summary as summary_of_applicant
    from RD.experience
    left join RD.profile_info
    on experience.public_id = profile_info.public_id
    limit 100
    ;
    '''
    export_to_csv.mysql_to_csv(query=query1, file_path="./file_csv_limit/job_posting.csv")
    export_to_csv.mysql_to_csv(query=query2, file_path="./file_csv_limit/experience.csv")
