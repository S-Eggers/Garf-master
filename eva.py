import sqlite3

def evaluate(path_ori, path):
    # path_ori="Hosp_rules"
    # path="Hosp_rules_copy"
    # path_ori = "LETTER"
    # path = "LETTER_copy"\
    # print("Conduct an evaluation")
    # Connecting to the database
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    sql1 = "select * from \"" + path + "\" where \"Label\"='2' or \"Label\"='3'"    #where rownum < 3  #order by "Provider ID" desc
    # print(sql1)
    cursor.execute(sql1)
    data1 = cursor.fetchall()
    # print(data1)
    des = cursor.description
    att = []
    for item in des:
        att.append(item[0])
    print(att)
    t2 = len(data1[0]) - 1  # Length of data per row, -1 is to become index position


    #print("1")
    # print(data1)
    correct=0
    error=0
    len_update=len(data1)
    for row in data1:
        # print(row)
        for i in range(t2):  # t2
            if i == 0:
                sql_info = "\"" + att[i] + "\"='" + row[i] + "'"
            else:
                sql_info = sql_info + " and \"" + att[i] + "\"='" + row[i] + "'"
        # sql_info_ori=sql_info
        sql_info_label = sql_info + " and \"Label\"='2'"
        sql2 = "select * from \"" + path_ori + "\" where " + sql_info + ""  # where rownum < 3  #order by "Provider ID" desc
        # print(sql2)
        cursor.execute(sql2)
        data_ori = cursor.fetchall()
        # print(data_ori)
        if data_ori==[]:
            sql_update = "update \"" + path + "\" set \"Label\"='3'  where  " + sql_info + ""
            # print("Original：", sql_info)
            # print("Update Information：", sql_update)
            cursor.execute(sql_update)
            conn.commit()
            #print("The target result is missing, the original correct data is not the same as the repaired data")
            #print(sql2)
            error += 1
            continue
        x1=data_ori[0]
        x1=list(x1)[:-1]
        # print("Post-repair data",x1)

        sql3 = "select * from \"" + path + "\" where " + sql_info_label + ""  # where rownum < 3  #order by "Provider ID" desc
        # print(sql3)
        cursor.execute(sql3)
        data_new = cursor.fetchall()
        # print(data_new)
        x2 = data_new[0]
        x2 = list(x2)[:-1]
        # print("Post-repair data", x1)
        # print("Correct data  ",x2)
        if x1==x2:
            correct+=1
        else:
            print("Fix the bug, fix for", x1,"         The actual correct data is",x2)
            error+=1
    precision=1-error/(error+correct)

    # print(correct,error,len_update)
    # print("precision:",precision)


    sql4 = "select * from \"" + path + "\" where \"Label\"='2' or \"Label\"='1' or  \"Label\"='3'"
    # print(sql4)
    cursor.execute(sql4)
    data2 = cursor.fetchall()
    recall = correct / len(data2)

    print(len(data2),"Fixed",len_update,"of which the correct number is",correct,", The number of errors is",error)
    # print(correct, error, len_update)
    print("precision:", precision)
    print("recall:", recall)
    cursor.close()
    conn.close()
    f_measure = 2 * precision * recall / (precision + recall)
    print("f1:", f_measure)

    with open('data/save/log_evaluation.txt', 'a') as f:
        f.write("")
        f.write(str(len(data2)))
        f.write("Fixed")
        f.write(str(len_update))
        f.write("of which the correct number is")
        f.write(str(correct))
        f.write(", The number of errors is")
        f.write(str(error))
        f.write("precision:")
        f.write(str(precision))
        f.write("           recall:")
        f.write(str(recall))
        f.write("           f_measure:")
        f.write(str(f_measure))
        f.write("\n")

        f.close()


if __name__ == '__main__':

    flag = 2
    if flag == 1:
        path_ori = "Test"  # Hosp_rules
        path = "Test_copy"  #
    if flag == 2:
        path_ori = "Hosp_rules"  #
        path = "Hosp_rules_copy"
    if flag == 3:
        path_ori = "UIS"  #
        path = "UIS_copy"

    if flag == 4:
        path_ori = "Food"  #
        path = "Food_copy"

    evaluate(path_ori,path)
