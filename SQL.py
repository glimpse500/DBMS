import Table,DBMS

class instruction():
    class decoder():
        def __init__(self,words):
            self.__words = words
            self.__len = len(self.__words)
            self.__ins = {}
            self.__ins['SELECT'] = ''
            self.__ins['FROM'] = ''
            self.__ins['WHERE'] = ''
            self.__ins['GROUP'] = ''
            self.__ins['HAVING'] = ''
            self.__wp = 0
            self.__count = 0
            self.__parse()
            pass
        def get(self,ins):
            return self.__ins[ins]
        def hasGroup(self):
            if len(self.__ins['GROUP']) > 0:
                return True
            else:
                return False
        def __parse(self):
            Type = ['SELECT','FROM','WHERE','GROUP','HAVING',None]
            self.__check(Type[0],Type[1])
            self.__check(Type[1],Type[2])
            self.__check(Type[2],Type[3])
            if self.__hasData():
                self.__check(Type[3],Type[4])
                self.__check(Type[4],Type[5]) 
        def __check(self,cType,nType,):
            if self.__now_point() == cType:
                if (cType == 'GROUP' ):
                    self.__wp +=1
                    if (self.__now_point() != 'BY'):
                        print('Grammar error (except BY at ) ',self.__wp, 'st word')
                while (self.__hasData()):
                    self.__wp +=1
                    if (self.__hasData() ):
                        p = self.__now_point() + ' '

                        if '(' in p:
                            self.__count+=1
                        if ')' in p :
                            self.__count-=1
                        if (self.__count > 0 ):
                            self.__ins[cType] += self.__now_point() + ' '
                        elif (self.__count == 0 and  self.__now_point() != nType):
                            self.__ins[cType] += self.__now_point() + ' '
                        else:
                            break
                    else:
                        break
            else:
                print('Grammar error at ',self.__wp+1, '(st) word')
                print('find (', self.__now_point() ,') expect "SELECT" ')
        def __hasData(self):
            if self.__wp < self.__len :
                return True
            else:
                return False
        def __now_point(self):
            if self.__hasData():
                return self.__words[self.__wp]
            else:
                return None
    def __init__(self):
        self.__origin = ''
        self.__count = 0
        self.__hasdata = False
        self.nest = None
        self.__SELECT = ''
        self.__FROM = ''
        self.__WHERE = ''
        self.__GROUPBY = ''
        self.__HAVING = ''
    def add(self,c):
        if (self.hasdata()):
            self.__origin +=c
        if (c == ')'):
            self.__count -=1
            if (self.__count == 0):
                self.__origin = self.__origin[0:len(self.__origin)-1]
                self.__decode()
        elif (c == '('):
            self.__hasdata = True
            self.__count +=1
        elif (c == ','):
            self.__origin += ' '
    def setData(self,d):
        self.__origin = d.strip()[1:len(d.strip())-1]
        self.__decode()
    def addFROM(self,f):
        self.__FROM += ', ' +f

    def hasGROUP(self):
        if len(self.__GROUPBY) > 0:
            return True
        else:
            return False
    def __decode(self):
        words = self.__origin.split()
        d = self.decoder(words)
        self.__SELECT = d.get('SELECT')
        self.__FROM = d.get('FROM')
        self.__WHERE = d.get('WHERE')
        if d.hasGroup():
            self.__GROUPBY = d.get('GROUP')
            self.__HAVING = d.get('HAVING')
        else:
            pass
        '''
        for w in words:
            if w == 'SELECT' or w == 'FROM' or w == 'WHERE':
                if (previous != 'WHERE'):
                    previous = w
                else:
                    self.__WHERE += w + ' '
            elif previous == 'SELECT':
                self.__SELECT += w + ' '
            elif previous == 'FROM':
                self.__FROM += w + ' '
            elif previous == 'WHERE':
                self.__WHERE += w + ' '
        '''

    def getCount(self):
        return self.__count
    def getSELECT(self):
        return self.__SELECT
    def getFROM(self):
        return self.__FROM
    def getWHERE(self):
        return self.__WHERE
    def getGROUPBY(self):
        return self.__GROUPBY
    def getHAVING(self):
        return self.__HAVING
    def hasdata(self):
        return self.__hasdata
    def __str__(self):
        return self.__origin
class querier():
    def __init__(self):
        self.tables = []
        self.tables_copy = []
        self.attributes = []
        self.data = None
        self.result = None
        self.instruction = None
    def execute(self,instruction,data = None):
        self.instruction = instruction
        if data != None:
            self.data = data
        else:
            data = self.data
        self.__SELECT(instruction.getSELECT().split(','))
        
        for f in instruction.getFROM().split(','):
            if len(f.split()) == 2:
                newTable = data.getTable(f.split()[0].strip())
                if newTable != None:
                    self.__FROM(newTable)
                    if self.tables[0].hasLabel() == False:
                        self.tables[0].setLabel(f.split()[1].strip())
                else:
                    self.__FROM(data.getTable(f.split()[1].strip()))
            else:
                self.__FROM(data.getTable(f.strip()))
        self.result = self.__WHERE(instruction.getWHERE())
        return self.result
    def __copyTable(self):
        for t in self.tables:
            self.tables_copy.insert(0,t)
    def __reNew(self):
        self.tables = []
        for t in self.tables_copy:
            self.tables.insert(0,t)
    def __SELECT(self,attributes):
        for a in attributes:
            self.attributes.insert(len(self.attributes),a.strip())
    def __FROM(self,table):
        self.tables.insert(0,Table.copy(table))
    def __WHERE(self,conditions,inTable = None):
        OR_condition = self.__ORsplit(conditions)
        temp = ''
        result = None
        self.__copyTable()
        for o in OR_condition:
            AND_condition = self.__ANDsplit(o)
            temp_result = None
            self.__reNew()
            for c in AND_condition:
                inC = c.split()

                notIN = False
                if 'IN' in inC:
                    inData = ''
                   
                    for i in range(len(inC)):
                        if inC[i] == 'IN':
                            for j in range(i+1,len(inC)):
                                inData += ' ' + inC[j]
                            outDataI = i
                            break
                        elif inC[i] == 'NOT' and inC[i+1] == 'IN':
                            notIN = True
                            for j in range(i+2,len(inC)):
                                inData += ' ' + inC[j]
                            outDataI = i
                            break
                    outData = ''
                    for i in range(0,outDataI):
                        outData += inC[i]
                    outData = outData.strip('(').strip(')')

                    inData = inData.strip()
                    inst = instruction()
                    inst.setData(inData)

                    inst.addFROM( self.instruction.getFROM())
                    q = querier()
                    inTable = q.execute(inst,self.data)

                    c1 = outData.split(',')
                    c2 = inst.getSELECT().split(',')
                    self.tables.insert(0,inTable)
                    index1 = -1
                    index2 = -1
                    for j in range(len(c1)):
                        c1[j] = c1[j].strip()
                        c2[j] = c2[j].strip()
                        newC = c1[j] + ' = ' + c2[j]
                        index1 = -1
                        index2 = -1
                        for i in range(len(self.tables)):
                            if c1[j] in self.tables[i].getAttributes():
                                index1 = i
                            if c2[j] in self.tables[i].getAttributes():
                                index2 = i
                        temp_result = Table.join(self.tables[index1],self.tables[index2],newC)
                        if (notIN):
                            self.tables[index1] =  Table.minus(self.tables[index1],temp_result)
    
                        else:
                            self.tables[index1] = Table.copy(temp_result)
                        temp_result = self.tables[index1]
                        if index1 != index2:
                            del(self.tables[index2])
                else:
                    c = self.__normorize(c)
                    c_list = c.split()
                    index1 = -1
                    index2 = -1
                    for i in range(len(self.tables)):
                        if c_list[0] in self.tables[i].getAttributes():
                            index1 = i
                        if c_list[2] in self.tables[i].getAttributes():
                            index2 = i
                    
                    if index2 == -1:
                        self.tables[index1] =  self.tables[index1].select(c)
                        temp_result = Table.copy(self.tables[index1])
                    else:
                        self.tables[index1] = Table.join(self.tables[index1],self.tables[index2],c)
                        temp_result = Table.copy(self.tables[index1])
                        if index1 != index2:
                            del(self.tables[index2])
            result = Table.union(result,temp_result)
        if self.instruction.hasGROUP():
            result = result.project(self.attributes,self.instruction.getGROUPBY())
            c = self.__normorize(self.instruction.getHAVING())
            result = result.select(c)
            return result
        else:

            if len(self.attributes) == 1 and self.attributes[0].strip() == '*':
                return result
            print(result)
            return result.project(self.attributes)
    def __ORsplit(self,condition):
        condition = condition.strip()
        words = condition.split()
        count = 0
        temp = ''
        result = []
        for w in words:
            if (w == 'OR' and count == 0):
                result.insert(len(result),temp)
                temp = ''
            else:
                temp += w +' '
            if ('(' in w):
                count +=1
            if (')' in w):
                count -=1
        result.insert(len(result),temp)
        return result
    def __ANDsplit(self,condition):
        condition = condition.strip()

        words = condition.split()
        count = 0
        temp = ''
        result = []
        for w in words:
            if (w == 'AND' and count == 0):
                result.insert(len(result),temp)
                temp = ''
            else:
                temp += w +' '
            if ('(' in w):
                count +=1
            if (')' in w):
                count -=1
        result.insert(len(result),temp)
        return result
    def __normorize(self,origin):

        operator = ['>=','<=','!=','=','>','<']
        for o in operator:
            c = origin.split(o)
            if len(c) == 2:
                origin =  c[0].strip() + ' ' + o + ' '+c[1].strip()
                break;
        return origin
    def type_of_condition(condition):
        pass
        return 0
    
    def result():
        return self.table

