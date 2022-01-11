from mainJobBatch.taskManage.dao.errorFileCreateDao import ErrorFileCreateDao

class ErrorFileCreateDaoImple(ErrorFileCreateDao):
    def getJobNum(self, cur, result_file_num):
        select_user_job_num = ("""
        SELECT
          JOB_QUE_DATA.job_num
        FROM
          scrapingSystem_jobquedata AS JOB_QUE_DATA
        WHERE
          JOB_QUE_DATA.result_file_num = '""" + result_file_num + """'
        """)

        try:
            cur.execute(select_user_job_num)
            rows = cur.fetchall()
            return rows[0][0]
        except:
            raise