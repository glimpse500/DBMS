import Table
class DataSet:
    def __init__(self):
        self.__tables = []
    def getTables(self):
        return self.__tables
    def getTable(self,name):
        for t in self.__tables:
            if name == t.getName():
                return t
    def readData(self,name):
        f = open(name,'r')
        r = f.readline()
        while (r != ''):
            temp_list = r.split()
            if (temp_list[0] == 'CREATE'):
                attributes = f.readline().split()
                self.__tables.insert(len(self.__tables),Table.table(attributes,temp_list[1]))
            else:
                i = 0
                for value in temp_list:
                    if value[0] != "'":
                        temp_list[i] = int(temp_list[i])
                    '''
                    else:
                        temp_list[i] = value[1:len(value)-1]
                    '''
                    i+=1
                current_table = self.__tables[len(self.__tables)-1]
                current_table.insert(temp_list)
            r = f.readline()
