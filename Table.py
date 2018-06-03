class table:
    def __init__(self,attributes,name = 'Default Table'):
        self.attributes = []
        for i in range(len(attributes)):
            self.attributes.insert(i,attributes[i])
        self.turples = []
        self.columns = []
        self.label = 'None'
        self.setName(name)
        for a in attributes:
            self.columns.insert(len(self.columns),[a])
    def setName(self,name):
        self.name = name
    def hasLabel(self):
        if self.label == 'None':
            return False
        else:
            return True
    def setLabel(self,label):
        self.label = label
        newA = []
        for a in self.attributes:
            newA.insert(len(newA),label+'.'+a)
            for t in self.turples:
                t[label+'.'+a] = t[a]
                del(t[a])
        
        for c in self.columns:
            c[0] = label +'.'+c[0]
        self.attributes = newA
    def getName(self):
        return self.name
    def getLabel(self):
        return self.label
    def getAttributes(self):
        return self.attributes
    def getAttributes2(self):
        newA = []
        for a in self.attributes:
            newA.insert(len(newA),self.getLabel()+'.'+a)
        return newA
    def insert(self,turple):
        if type(turple) == list:
            self.turples.insert(len(self.turples),{})
            current = self.turples[len(self.turples)-1] 
            i=0
            for attribute in self.attributes:
                current[attribute] = turple[i]
                i+=1
            i = 0
            for c in self.columns:
                c.insert(len(c),turple[i])
                i+=1
        elif type(turple) == dict:
            temp_turple = []
            for attribute in self.attributes:
                temp_turple.insert(len(temp_turple),turple[attribute])
            self.insert(temp_turple)
    def project(self,attributes,groupby = False):
        count = 0
        for a in attributes:
            if '(' in a and ')' in a:
                count+= 1
        if count != 0:
            conditions = []
            p = 0
            for a in attributes:
                if '(' in a and ')' in a:
                    conditions.insert(p,'')
                    for c in a:
                        if c == '(' or c == ')':
                            conditions[p] += ' '
                        else:
                            conditions[p] += c
                    p+=1
            if (groupby):

                groupby = groupby.split(',')
                return self.group(attributes,conditions,groupby)
            else:
                return self.group(attributes,conditions)
        else:
            projected_table = table(attributes)
            i=0
            temp_columns = []
            temp_turples = []
            for c in self.columns:
                if c[0] in attributes:
                    temp_columns.insert(i,c)
                    i+=1
            i = 0
            while (i < len(temp_columns[0])-1):
                temp_turples.insert(len(projected_table.turples),[])
                i+=1
            for c in temp_columns:
                j = 1 # first item is attribute
                for t in temp_turples: 
                    t.insert(len(t),c[j])
                    j+=1
            #remove repeated turples

            projected_turples = []
            for turple in temp_turples:
                if turple not in projected_turples:
                    projected_turples.insert(len(projected_turples),turple)         
            for turple in projected_turples:
                projected_table.insert(turple)
            projected_table.setName(self.getName())
            return projected_table;
    def select(self,condition):
        selected_table = table(self.attributes)
        decode = condition.split()
        key = decode[0]
        value = decode[2]
        if "'" not in value:
            value = int(value)
        if (decode[1] == '>'):
            for t in self.turples:
                if t[key] > value:
                    selected_table.insert(t)
        elif (decode[1] == '<'):
            for t in self.turples:
                if t[key] < value:
                    selected_table.insert(t)
        elif (decode[1] == '='):
            for t in self.turples:
                if t[key] == value:
                    selected_table.insert(t)
        elif (decode[1] == '<='):
            for t in self.turples:
                if t[key] <= value:
                    selected_table.insert(t)
        elif (decode[1] == '>='):
            for t in self.turples:
                if t[key] >= value:
                    selected_table.insert(t)
        selected_table.setName(self.getName())
        return selected_table
    def group(self,attributes,conditions,g_attribute = None):

        grouped_attributes = []
        grouped_turples = []
        for attribute in attributes:
            grouped_attributes.insert(len(grouped_attributes),attribute)
        grouped_table = table(grouped_attributes)
        if (g_attribute != None):
            grouped_attributes.insert(0,g_attribute)

        if (g_attribute != None):
            for turple in self.turples:
                dictionary = {}
                dictionary['__GROUP'] = {}
                for g in g_attribute:
                    g = g.strip()
                    dictionary['__GROUP'][g]  = turple[g]
                    dictionary[g] = turple[g]
                if dictionary not in grouped_turples:
                    grouped_turples.insert(len(grouped_turples),dictionary)
        else:
            grouped_turples.insert(0,{})
        i = 0
        for condition in conditions:
            decode = condition.split()
            function = decode[0]
            o_attribute = decode[1]
            for index in range(len(attributes)):
                if (o_attribute in attributes[index] and function in attributes[index]):
                    i = index
            if (g_attribute != None):
                for d in grouped_turples:
                    d[o_attribute+'*'] = []
                for turple_1 in self.turples:
                    temp_d = {}
                    for g in g_attribute:
                        g = g.strip()
                        temp_d[g] = turple_1[g]

                    for turple_2 in grouped_turples:
                        if temp_d == turple_2['__GROUP']:
                            if (o_attribute == '*'):
                                turple_2[o_attribute+'*'].insert(0,temp_d)
                            else:
                                turple_2[o_attribute+'*'].insert(0,turple_1[o_attribute])
                o_attribute = o_attribute + '*'
                for turple in grouped_turples:
                    turple[attributes[i]] = 0
                    if (function == 'COUNT'):
                        turple[attributes[i]] = len(turple[o_attribute])

                    elif (function == 'AVG'):
                        for value in turple[o_attribute]:
                            turple[attributes[i]] += value

                    elif (function == 'SUM'):
                        for value in turple[o_attribute]:
                            turple[attributes[i]] += value
                    elif (function == 'MAX'):
                        turple[attributes[i]] = None
                        for value in turple[o_attribute]:
                            if  turple[attributes[i]] == None or turple[attributes[i]] < value:
                                turple[attributes[i]] = value
                    elif (function == 'MIN'):
                        turple[attributes[i]] = None
                        for value in turple[o_attribute]:
                            if  turple[attributes[i]] == None or turple[attributes[i]] > value:
                                turple[attributes[i]] = value
                    del(turple[o_attribute])
            else:
                grouped_turples[0][o_attribute +'*'] = []
                grouped_turples[0][attributes[i]] = 0
                for turple in self.turples:
                    if (o_attribute == '*'):
                        grouped_turples[0][o_attribute+'*'].insert(0,'*')
                    else:
    
                        grouped_turples[0][o_attribute+'*'].insert(0,turple[o_attribute])
                o_attribute = o_attribute + '*'
                if (function == 'COUNT'):
                    grouped_turples[0][attributes[i]] = len(grouped_turples[0][o_attribute])
                elif (function == 'AVG'):
                    for value in grouped_turples[0][o_attribute]:
                        grouped_turples[0][attributes[i]] += value
                    grouped_turples[0][attributes[i]] /= len(grouped_turples[0][o_attribute])
                elif (function == 'SUM'):
                    for value in grouped_turples[0][o_attribute]:
                        grouped_turples[0][attributes[i]] += value
                elif (function == 'MAX'):
                    for value in grouped_turples[0][o_attribute]:
                        if grouped_turples[0][attributes[i]] < value:
                            grouped_turples[0][attributes[i]] = value
                elif (function == 'MIN'):
                    grouped_turples[0][attributes[i]] = None
                    for value in grouped_turples[0][o_attribute]:
                        if grouped_turples[0][attributes[i]] == None or grouped_turples[0][attributes[i]] > value:
    
                            grouped_turples[0][attributes[i]] = value
                del(grouped_turples[0][o_attribute])
        if (g_attribute != None):
            for turple in grouped_turples:
                del(turple['__GROUP'])
        for g in grouped_turples:
            grouped_table.insert(g)
        grouped_table
        return grouped_table
    def getResult(self):
        result = 'Table Name:\t' +  self.getName() + '\nAttribtes:\t'
        for attribute in self.attributes:
            result += attribute + ' '
        result += '\n'
        i = 0
        for turple in self.turples:
            i +=1
            result += 'Turples(' + str(i) +')=\t'
            for key in self.attributes:

                result += str(turple[key]) + ' '
            result += '\n'
        return result
    def __str__(self):
        return self.getResult()
def equal(turple1,turple2):
    if (len(turple1) == len(turple2)):
        for item1 in turple1:
            if (item1 not in turple2):
                return False
        for item2 in turple2:
            if (item2 not in turple1):
                return False
        return True
    else:
        return False
def intersection(table1,table2):
    intersection_table = table(table1.attributes)
    for item1 in table1.turples:
        if item1 in table2.turples:
            intersection_table.insert(item1)
    return intersection_table

def minus(table1,table2):
    minus_table = table(table1.getAttributes())
    intersection_table = intersection(table1,table2)
    for item in table1.turples:
        if item not in intersection_table.turples:
            minus_table.insert(item)
    return minus_table
def union(table1,table2):
    if table1 == None:
        return copy(table2)
    if table2 == None:
        return copy(table1)
    minus_table1 = minus(table1,table2)
    minus_table2 = minus(table2,table1)
    intersection_table = intersection(table1,table2)
    combine_minus = plus(minus_table1,minus_table2)
    union_table = plus(intersection_table,combine_minus)
    
    return union_table
def join(table1,table2,condition):
    condition_list = condition.split()
    joined_attributes = []
    joined_table = None
    if condition_list[1] == '=':
        key1 = condition_list[0].strip()
        key2 = condition_list[2].strip()
        for attribute in table1.attributes:
            joined_attributes.insert(len(joined_attributes),attribute)
        for attribute in table2.attributes:
            if attribute not in joined_attributes:
                joined_attributes.insert(len(joined_attributes),attribute)
        joined_attributes.remove(key2)
        
        joined_table = table(joined_attributes)
        if table1 == table2:
            for turple1 in table1.turples:
                if turple1[key1] == turple1[key2]:
                    joined_table.insert(__createTurple(joined_attributes,turple1,turple1))
        else:
            for turple1 in table1.turples:
                for turple2 in table2.turples:
                    if turple1[key1] == turple2[key2]:
                        joined_table.insert(__createTurple(joined_attributes,turple1,turple2))
                                        
    return joined_table

    
def __createTurple(attributes,turple1,turple2):
    dictionary = {} 
    for key in turple1:
        dictionary[key] = turple1[key]
    for key in turple2:
        if key not in dictionary:
            dictionary[key] = turple2[key]
    newTurple = []
    for attribute in attributes:
        newTurple.insert(len(newTurple),dictionary[attribute])
    return newTurple

def copy(table1):
    copy_table = table(table1.attributes)
    for item1 in table1.turples:
        copy_table.insert(item1)
    return copy_table
def plus(table1,table2):
    plus_table = copy(table1)
    for item2 in table2.turples:
        plus_table.insert(item2)
    return plus_table
