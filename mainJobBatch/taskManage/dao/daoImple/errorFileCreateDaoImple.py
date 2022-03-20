from mainJobBatch.taskManage.dao.errorFileCreateDao import ErrorFileCreateDao

class ErrorFileCreateDaoImple(ErrorFileCreateDao):
    def getJobNum(self, cur, result_file_num):
        select_user_job_num = ("""
        SELECT
          JOB_QUE_DATA.job_num
        FROM
          scrapingSystem_jobquedata AS JOB_QUE_DATA
        WHERE
          JOB_QUE_DATA.result_file_num = '""" + str(result_file_num) + """'
        """)

        try:
            cur.execute(select_user_job_num)
            rows = cur.fetchall()
            return rows[0][0]
        except:
            raise

    def jadgeQueStock(self, cur, result_file_num):
        select_user_job_num = ("""
        SELECT
          JOB_QUE_DATA.job_num
        FROM
          scrapingSystem_jobquedata AS JOB_QUE_DATA
        WHERE
          JOB_QUE_DATA.user_id = '""" + result_file_num + """'
        ORDER BY JOB_QUE_DATA.job_num ASC""")

        try:
            cur.execute(select_user_job_num)
            cur.fetchall()
            if cur.rowcount == 0:
                return True
            else:
                return False
        except:
            raise