#__author:  Administrator
#date:  2017/1/19

#url type : 0 = related , 1 absolute
'''(('can_fuck_him_to_death','弄死小虎逼'),
                       ('can_access_my_course','可以访问我的课程'),
                       ('can_access_customer_list','可以访问客户列表'),
                       ('can_access_customer_detail','可以访问客户详细'),
                       ('can_access_studyrecords','可以访问学习记录页面'),
                       ('can_access_homework_detail','可以访问作业详情页面'),
                       ('can_upload_homework','可以交作业'),
                       ('access_kingadmin_table_obj_detail','可以访问kingadmin每个表的对象'),
                       ('change_kingadmin_table_obj_detail','可以修改kingadmin每个表的对象'),
                       )


'''



perm_dic = {
     'crm.can_access_student_index':{
         'url':'stu_index',
         'url_type':0,
         'method':'GET',
         'args':[],
     },

     # 'crm.can_access_stu_detail': {
     #     'url_type':0,
     #     'url': 'stu_detail', #url name
     #     'method': 'GET',
     #     'args': []
     # },

    # '__crm.can_access_customer_detail':{
    #     'url_type':0,
    #     'url': 'table_obj_change',  # url name
    #     'method': 'GET',
    #     'args': []
    # },
    #
    #
    #
    #
    # 'crm.change_kingadmin_table_obj_detail': {
    #     'url_type': 0,
    #     'url': 'table_obj_change',  # url name
    #     'method': 'POST',
    #     'args': [],
    #     'hooks':['func1' and  'func2']
    #
    # },
}